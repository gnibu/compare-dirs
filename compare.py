import os
import hashlib

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-a', help='list file that are only in this dir', required=True)
parser.add_argument('-b', help='folder to compare to', required=True)
parser.add_argument('-o', help='output to a file', required=True)
args = parser.parse_args()

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
    for root, dirs, files in os.walk(folder, followlinks=False):
        print('indexing ' + root)
        for mfile in files:
            path = root+"/"+mfile
            hashes[hash_bytestr_iter(file_as_blockiter(open(path, 'rb')), hashlib.sha256(), ashexstr=True)] = path
    return hashes

a=list_hash(args.a)
b=list_hash(args.b)

msg = '\nonly in ' + args.a + ' not in ' + args.b + '\n'

if(args.o):
    f = open(args.o,"w") 
    f.write(msg)

print(msg)
print('-----------------------')
for hash in list(set(a.keys()) - set(b.keys())):
    print(a[hash])
    if(args.o):
        f.write(a[hash] + '\n')
f.close()

