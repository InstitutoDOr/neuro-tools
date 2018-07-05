import os, shutil, tempfile, bz2

# Function to manipulate bz files
def unbzip( filepath, dest=None ):
    newfile = filepath.rsplit('.', 1)[0]
    # If the results will be moved to other destination
    if dest:
        newfile = os.path.join(dest, os.path.basename(newfile))

    with open(newfile, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
        for data in iter(lambda : file.read(100 * 1024), b''):
            new_file.write(data)

# Function to create a temporary zip file
# Ignores subfolders
def tmp_zip( folder ):
    tmpdir = tempfile.mkdtemp()
    try:
        # Moving all files to temporary directory
        for subfile in os.listdir(folder):
            subfile = os.path.join(folder, subfile)
            if subfile.endswith('.bz'):
                unbzip(subfile, tmpdir)
            else:
                shutil.copyfile(subfile, tmpdir)

        # Creating temporary zip name
        fzip = tempfile.NamedTemporaryFile(prefix='xnat_')
        fzip.close()

        shutil.make_archive(fzip.name, 'zip', tmpdir)
    finally:
        shutil.rmtree(tmpdir)
    
    return fzip.name + '.zip'