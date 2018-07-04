import setup_test, sys, getpass
from neuro_tools.xnat_sdk import Xnat

username = raw_input('Username: ')
password = getpass.getpass('Password: ')
x = Xnat('http://xnat.idor.org', username, password)
x.list_projects()