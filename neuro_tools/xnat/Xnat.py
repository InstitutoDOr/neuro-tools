# XNATYPY: https://xnat.readthedocs.io/en/latest/
import xnat as xnatpy
import os, sys
from .util import tmp_zip

# Main interface with XNAT
# methods created to simplify XNAT access
class Xnat:
    def __init__(self, server, user, password):
        self.server   = server
        self.user     = user
        self.password = password
        self.__connect()

    # Uses interface from xnatpy
    def __connect(self):
        self.session = xnatpy.connect(self.server, user=self.user, password=self.password)

    # Listing all projects
    def list_projects(self):
        projects = []
        total_p = len( self.session.projects )
        for n_p in range(total_p):
            project = self.session.projects[n_p]
            projects.append( (project.id, project.name) )
        return projects

    # function to send a specific sequence to xnat
    def send_sequence(self, project, subject, sequence_dir):
        zipfname = tmp_zip( sequence_dir )
        try:
            self.session.services.import_( zipfname,\
                overwrite='none',\
                project=project,\
                subject=subject,\
                trigger_pipelines=False )
        except:
            print("Unexpected error during XNAT import:")
            print(sys.exc_info())
        os.remove( zipfname )

    # function to send a complete session to xnat
    def send_session(self, project, subject, session_dir):
        sequences = os.listdir(session_dir)
        for (n, sequence) in enumerate(sequences):
            print("[{:02d}] Sending: {}".format(n, sequence))
            sequence_dir = os.path.join(session_dir, sequence)
            self.send_sequence( project, subject, sequence_dir )
            
        print('Finished!')