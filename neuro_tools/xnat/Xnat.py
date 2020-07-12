# XNATYPY: https://xnat.readthedocs.io/en/latest/
import xnat as xnatpy
import os
import sys
import time
from .util import tmp_zip

# Main interface with XNAT
# methods created to simplify XNAT access
class Xnat:
    def __init__(self, server, user, password):
        self.server   = server
        self.user     = user
        self.password = password
        self.__prearc_session = None
        self.__connect()

    # Uses interface from xnatpy
    def __connect(self):
        self.session = xnatpy.connect(self.server, user=self.user, password=self.password)

    # Listing all projects
    def list_projects(self):
        projects = []
        for project in self.session.projects.values():
            projects.append( (project.id, project.name) )
        return projects

    # Function to import resources
    def import_resource( self, obj, subdir, files ):
        for file in files:
            filename = os.path.basename(file)
            uri = '{}/resources/{}/files/{}'.format(obj.uri, subdir, filename)
            self.session.put(uri, files={'file': open(file, 'rb')})
            
    def archive(self, retries = 5):
        time.sleep(2)
        try:
            if( retries > 0 ):
                self.__prearc_session.archive(overwrite='delete',trigger_pipelines=True)
        except xnatpy.exceptions.XNATResponseError:
            print('retrying...')
            self.archive(retries-1)
        except:
            pass

    # function to send a specific sequence to xnat
    def send_sequence(self, project, subject, sequence_dir, session = ''):
        zipfname = tmp_zip( sequence_dir )
        try:
            query = {
                'import-handler': 'DICOM-zip',
                'PROJECT_ID': project,
                'SUBJECT_ID': subject,
                'EXPT_LABEL': subject+'_'+session,
                'rename': 'true',
                'prevent_anon': 'true',
                'prevent_auto_commit': 'true',
                'SOURCE': 'uploader',
                'autoArchive': 'AutoArchive'
            }
            self.session.upload(uri='/data/services/import', file_=fh, query=query, content_type='application/zip', method='post')
        except:
            print("Unexpected error during XNAT import:")
            print(sys.exc_info())
        zipfname.close()

    # function to send a complete session to xnat
    def send_session(self, project, subject, session_dir, sequences = None, session = ''):
        if not sequences:
            sequences = os.listdir(session_dir)

        for (n, sequence) in enumerate(sequences):
            print("[{:02d}] Sending: {}".format(n+1, sequence))
            sequence_dir = os.path.join(session_dir, sequence)
            self.send_sequence( project, subject, sequence_dir, session=session)
            
        self.__prearc_session = self.session.prearchive.find(project=project, subject=subject, session=subject+'_'+session)[0]
        self.__prearc_session.rebuild()
        self.archive()
        self.__prearc_session = None

        print('Finished!')