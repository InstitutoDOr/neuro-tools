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

    # function to send data to xnat
    def send_to_xnat(self, project, subject, session_dir):
        for sequence in os.listdir(session_dir):
            f_sequence = os.path.join(session_dir, sequence)
            print(f_sequence)
            zipfname = tmp_zip( f_sequence )
            try:
                print("sending image:")
                print("SEQUENCE: " + sequence)
                self.session.services.import_( zipfname,\
                    overwrite='append',\
                    project=project,\
                    subject=subject,\
                    trigger_pipelines=False )
            except:
                print("Unexpected error during XNAT import:")
                print(sys.exc_info())
            os.remove( zipfname )
        print('Finished!')