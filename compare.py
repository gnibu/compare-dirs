import os
import hashlib

def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return (hasher.hexdigest() if ashexstr else hasher.digest())

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

def list_hash(folder):
    hashes = {}
    for root, dirs, files in os.walk(folder):
        print('indexing ' + root)
        for mfile in files:
            path = root+"/"+mfile
            hashes[hash_bytestr_iter(file_as_blockiter(open(path, 'rb')), hashlib.sha256(), ashexstr=True)] = path
    return hashes

a=list_hash('/Volumes/backup/sort/photos-sauron/2010')
b=list_hash('/Volumes/photos/2010')

print('only in a')
for hash in list(set(a.keys()) - set(b.keys())):
    print(a[hash])
