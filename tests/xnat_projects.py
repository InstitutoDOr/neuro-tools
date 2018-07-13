import setup_test, sys, getpass
from neuro_tools.xnat import Xnat

username = input('Username: ')
password = getpass.getpass('Password: ')
x = Xnat('http://xnat.idor.org', username, password)
print( x.list_projects() )