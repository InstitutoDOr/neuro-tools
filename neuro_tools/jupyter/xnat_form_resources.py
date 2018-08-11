import os
import glob
from ..xnat import Xnat, util
from ipywidgets import widgets, Layout, HBox

xnat = ''

def get_xnat():
    global xnat
    if isinstance(xnat, str):
        print('Connecting...')
        xnat = Xnat(xnatserver.value, login.value, password.value)   
    return xnat

# CALLBACKS
def update_ss(b):
    xnat = get_xnat()
    subjects = xnat.session.projects[prjid.value].subjects.values()
    ss = [(x.label, x.id) for x in subjects]
    # Sorting subjects
    selectedss.options = sorted(ss, reverse=True)
    print('Done!')

def on_send_clicked(b):
    xnat = get_xnat()
    prjdir = '/dados1/PROJETOS/PRJ1607_TEPT/03_PROCS/RAW_DATA'
    
    # Importing each subject
    ss_sel = [(k,v) for v,k in selectedss.options if k in selectedss.value]
    for (key,subjid) in ss_sel:
        print( "XNAT importing resources for {}".format(subjid) )
        # Creating connection and load experiment object
        item = xnat.session.projects[prjid.value].subjects[key].experiments[0]

        # Sending each PRESENTATION file
        logsfiles = sorted( glob.glob( '{}/**/{}*.log'.format( prjdir, subjid ) ) ) 
        xnat.import_resource(item, 'PRESENTATION', logsfiles)
        print('PRESENTATION imported.')

        # Sending each ECG file
        ecgfiles = sorted( glob.glob( '{}/ECG/{}_*.*'.format( prjdir, subjid ) ) ) 
        xnat.import_resource(item, 'ECG', ecgfiles)
        print('ECG imported.')

# widgets
xnatserver = widgets.Text(description="XNAT SERVER", tooltip='URL to XNAT', value='', width=200)
prjid = widgets.Text(
    description="PRJID",
    tooltip='Leave this empty when defining non-project dicom dir',
    value='PRJ1607_TEPT',
    width=200,
    layout=Layout(disabled='disabled')
)

subjbutton = widgets.Button(
    description='List subject matches',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='',
    icon='refresh',
    layout=Layout(width='30%'),
)
subjbutton.on_click(update_ss)

selectedss = widgets.SelectMultiple(
    options=[],
    value=[],
    #rows=10,
    description='Subjects to send',
    disabled=False,
    layout={'height': '200px'}
)
    
login    = widgets.Text(description="XNAT login", value='', width=200)
password = widgets.Password(description="PASSWORD", value='', width=200)

sendbutton = widgets.Button(
    description='Send to XNAT',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Sends selected subjects to xnat',
    icon='check',
    layout=Layout(width='30%')
)
    
sendbutton.on_click(on_send_clicked)

# display
def display_form():
    display(xnatserver)
    display(HBox([login, password]))
    display(subjbutton)
    display(selectedss)
    display(sendbutton)