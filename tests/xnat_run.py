#!/usr/bin/python
import setup_test
import argparse
import sys
import os
import getpass
from neuro_tools.xnat import Xnat

def main():
    parser = argparse.ArgumentParser(description='XNAT sender')
    parser.add_argument('-project', help='Project ID', required=True)
    parser.add_argument('-subject', help='Subject ID', required=True)
    parser.add_argument('-studydir', help='Study directory with all sequences', required=True)
    parser.add_argument('-sequences', nargs='+', help='List of sequences to be uploaded [if not defined, all sequences]')
    parser.add_argument('-server', help='Server for XNAT connection', required=True)
    parser.add_argument('-username', help='Username for XNAT connection', required=True)
    parser.add_argument('-password', help='Password for XNAT connection', required=True)
    args = parser.parse_args()

    xnat = Xnat(args.server, args.username, args.password)
    
    sequences = os.listdir(args.studydir) if not args.sequences else args.sequences
    for sequence in sequences:
        # Directory for each sequence
        seq_dir = os.path.join( args.studydir, sequence )
        print(seq_dir)
        # Sending each sequence
        xnat.send_sequence(args.project, args.subject, seq_dir)

# init
if __name__ == '__main__':
    main()
