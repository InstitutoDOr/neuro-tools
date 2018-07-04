'XNATYPY: https://xnat.readthedocs.io/en/latest/'
import xnat as xnatpy

class Xnat:

    def __init__(self, server, user, password):
        self.server   = server
        self.user     = user
        self.password = password
        self.__connect()

    'Uses interface from xnatpy'
    def __connect(self):
        self.session = xnatpy.connect(self.server, user=self.user, password=self.password)

    def list_projects(self):
        list = []
        for project in self.session.projects:
            print(dir(project))
            list.append(project)
        return list

    # function to send data to xnat
    def send_to_xnat(self, ss, project):
        ss = [(k,v) for k,v in selectedss.options.items() if v in selectedss.value]
        for (s,fp) in ss:
            subject = s.split("_")[0]
            print("PROJECT: " + project)
            print("SUBJECT: " + subject)

            for session in os.listdir(fp):
                sfp = os.path.join(fp,session)
                print(sfp)
                zipfname = '/tmp/xnat_' + datetime.datetime.now().strftime("%y%m%d%H%M%S")
                shutil.make_archive(zipfname, 'zip', sfp)
                try:
                    print("sending image:")
                    print("SESSION: " + session)
                    experiment = xnat_session.services.import_( zipfname + '.zip',\
                        overwrite='append',\
                        project=project,\
                        subject=subject,\
                        trigger_pipelines=False )
                except:
                    print("Unexpected error during xnat import:", sys.exc_info()[0])
                    print(sys.exc_info())
                os.remove(zipfname + ".zip")
        print("FINISHED")