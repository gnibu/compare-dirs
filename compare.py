import os
import hashlib
import os.path
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--other', help='list file that are only in this dir and not in reference', required=True)
parser.add_argument('--reference', help='list file from other that are not in this dir', required=True)
parser.add_argument('-o', help='output to a file', required=False)
#TODO add options --missing from reference and --duplicates
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
            if not os.path.islink(path):
                hashes[hash_bytestr_iter(file_as_blockiter(open(path, 'rb')), hashlib.sha256(), ashexstr=True)] = path
    return hashes

other = list_hash(args.other)
reference = list_hash(args.reference)

msg = '\nonly in ' + args.other + ' / not in ' + args.reference + '\n'

if(args.o):
    f = open(args.o,"w") 
    f.write(msg)

print(msg)
print('-----------------------')
for hash in list(set(other.keys()) - set(reference.keys())):
    print(other[hash])
    if(args.o):
        f.write(other[hash] + '\n')
f.close()

