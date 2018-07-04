import xnat

# function to send data to xnat
def send_to_xnat(ss, server, project, user, password):
    ss = [(k,v) for k,v in selectedss.options.items() if v in selectedss.value]
    xnat_session = xnat.connect(server, user=user, password=password)
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