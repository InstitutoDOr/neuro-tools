#!/usr/bin/python
import setup_test
import argparse
import sys
import os
import glob
import getpass
from neuro_tools.xnat import Xnat, util

def main():
    parser = argparse.ArgumentParser(description='XNAT sender')
    parser.add_argument('-project', help='Project ID', required=True)
    parser.add_argument('-subject', help='Subject ID', required=True)
    parser.add_argument('-input', help='Files to be sent', required=True)
    parser.add_argument('-destination', help='Destination in XNAT', required=True)
    parser.add_argument('-server', help='Server for XNAT connection', required=True)
    parser.add_argument('-username', help='Username for XNAT connection', required=True)
    parser.add_argument('-password', help='Password for XNAT connection', required=True)
    args = parser.parse_args()
    
    # Directory for each sequence
    files = sorted( glob.glob( '{}/**/{}*.log'.format( args.input, args.subject ) ) ) 
    zipfname = util.tmp_zip( files )
    print('PRESENTATION: ' + zipfname)

    files = sorted( glob.glob( '{}/ECG/{}_*.*'.format( args.input, args.subject ) ) ) 
    zipfname = util.tmp_zip( files )
    print('ECG: ' + zipfname)

    #xnat = Xnat(args.server, args.username, args.password)
    # Sending each sequence
    #xnat.send_sequence(args.project, args.subject, seq_dir)

# init
if __name__ == '__main__':
    main()
