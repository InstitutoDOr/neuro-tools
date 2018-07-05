import setup_test, sys, getpass
from neuro_tools.xnat import Xnat

username = raw_input('Username: ')
password = getpass.getpass('Password: ')
x = Xnat('http://xnat.idor.org', username, password)

project   = raw_input('Project: ')
subject   = raw_input('Subject: ')
sess_path = raw_input('Session: ')
x.send_to_xnat(project, subject, sess_path)