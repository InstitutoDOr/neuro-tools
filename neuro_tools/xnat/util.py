import os
import shutil
import bz2
import tempfile
from zipfile import ZipFile
from six import BytesIO

# Function to manipulate bz files
def unbzip(filepath, dest=None):
    newfile = filepath.rsplit('.', 1)[0]
    # If the results will be moved to other destination
    if dest:
        newfile = os.path.join(dest, os.path.basename(newfile))

    with open(newfile, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
        for data in iter(lambda: file.read(100 * 1024), b''):
            new_file.write(data)


# Function to create a temporary zip file
# data_in = folder if is a string or files if a list
# Ignores subfolders
def tmp_zip(data_in, prefix='xnat_', method='file'):
    # Creating temporary zip name
    if method == 'memory':
        fh = BytesIO()
    else:
        fh = tempfile.TemporaryFile('wb+')
        
    tmpdir = tempfile.mkdtemp()
    try:
        files = os.listdir(data_in) if isinstance(data_in, str) else data_in
        # Moving all files to temporary directory
        for subfile in files:
            # When data_in is a folder, it completes the path
            if isinstance(data_in, str):
                subfile = os.path.join(data_in, subfile)
            # Uncompressing bz files
            # TODO: Uncompress gz and zip
            if subfile.endswith('.bz'):
                unbzip(subfile, tmpdir)
            else:
                shutil.copy2(subfile, tmpdir)
        
        # Preparing output zip
        with ZipFile(fh, 'w') as zip_file:
            for dirpath, dirs, files in os.walk(tmpdir):
                for f in files:
                    fn = os.path.join(dirpath, f)
                    zip_file.write(fn)
        fh.seek(0)
    finally:
        shutil.rmtree(tmpdir)

    return fh
