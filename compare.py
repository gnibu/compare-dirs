import os

for root, dirs, files in os.walk('/Volumes/photos/2011'):
    for mfile in files:
        print(root+"/"+ mfile)