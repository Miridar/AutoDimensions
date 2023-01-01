# import required module
import os
from zipfile import ZipFile
import shutil

# assign directory
source_directory = 'Desktop\Models'
# Iterate over files in the source directory and recursively check subdirectories
for root, dirs, files in os.walk(source_directory):
    for filename in files:
        file_path = os.path.join(root, filename)
        # Check if the file is a .FCStd file
        if file_path.endswith('.FCStd'):
            # Open the zip file in read mode using a context manager
            with ZipFile(file_path, 'r') as zip_file:
                # Find a file with the name 'Document.xml' in the zip file
                if 'Document.xml' in zip_file.namelist():
                    # Extract the file to a temporary location
                    zip_file.extract('Document.xml', 'Desktop\Models\Temp')
            # Open the extracted file in read mode using a context manager
            with open('Desktop\Models\Temp\Document.xml', 'r', encoding='utf-8') as file:
                # Read the file
                data = file.read()
                #close the file
                file.close()
                # Check if the file contains the string '<Object name="Dimension'
                if '<Object name="Dimension' in data:
                    # Create the destination directories if they do not exist
                    if not os.path.exists('Desktop/AutoDimensions/baseddata/training'):
                        os.makedirs('Desktop/AutoDimensions/baseddata/training')
                    # If the file does not already exist, move it to a new directory
                    if not os.path.exists('Desktop/AutoDimensions/baseddata/training\{}.xml'.format(filename)):
                        os.rename(file.name, 'Desktop/AutoDimensions/baseddata/training\{}.xml'.format(filename))
                # delete the extracted file if it exists
                if os.path.exists('Desktop\Models\Temp\Document.xml'):
                    os.remove('Desktop\Models\Temp\Document.xml')
        # delete the file after processing
        os.remove(file_path)

# Iterate over the directories in the source directory and recursively check subdirectories
for root, dirs, files in os.walk(source_directory):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        # Delete the directory and its contents using shutil.rmtree
        shutil.rmtree(dir_path)

# print a message to the console to indicate that the script has finished
print('Finished')