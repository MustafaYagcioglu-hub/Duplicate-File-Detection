# Author: Mustafa Yagcioglu
# Author email: yagciogluengieering@gmail.com
# Coding date:  jan 2021

# Imports
from collections import defaultdict
import hashlib
import os
import sys
import time

'''
Problem Definition:
Write a cross-platform command-line application that receives a directory as parameter and outputs
the groups of files in the directory that are duplicate in terms of contents.
The application should:
• take into account that there might be a very large number of files in the directory
• optimise for execution time.

The application should be called e.g.:
$ ./lsdup /path/to/dir/
[group #1]
/path/to/dir/file1
/path/to/dir/file3
[group #2]
/path/to/dir/file2
/path/to/dir/file4
/path/to/dir/file5
...
[group #n]
/path/to/dir/filex
/path/to/dir/filey
'''

'''
Script usage:
The code is tested on Windows 10 command prompt, with Python 3.9.1.
It should work on any operating system with python 3 but not guaranteed.

Example usage:
duplicateFiles C:\IS_BASVURUSU 3
Parameters are described in main function

'''

def getListOfFiles(dirName):
    '''
    For the given path, create a list of all files in the directory and sub directories,
    returns the file list
    '''
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk
def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    '''
    This method calculates the hash keys for the files
    Method is generic to apply different hashing methodologies
    sha1 is used for this solution
    Method is parametric to calculate hash keys for only first 1024 bytes or whole file
    '''
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed


def main( dirName, hash_type):
    '''
        main method
        input : dirName, directory to analyze, if nothing entered, current path is used
        input : hash_type, used hashing methods for classification
            0: Don't use file size and first 1024 bytes for pre-classifying
            1: Use only file size for pre-classifying
            2: Use only first 1024 bytes for pre-classifying
            3: Use both file size and first 1024 bytes for pre-classifying
        output : execution time (for perfomance analysis)
    '''
    print("Classifing the files in directory : ",dirName)
    print("hash_type : ",hash_type)
    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)

    #Store the starting time for perfomance measurements
    start_time = time.time()

    hashes_by_size = defaultdict(list)  # dict of size_in_bytes: [full_path_to_file1, full_path_to_file2, ]
    hashes_1024 = defaultdict(list)  # dict of (hash1024, size_in_bytes): [full_path_to_file1, full_path_to_file2, ]
    hashes_full = defaultdict(list)   # dict of full_file_hash: full_path_to_file_string

    if hash_type == 0:
        '''
        Don't use file size and first 1024 bytes for pre-classifying
        '''
        for filename in listOfFiles:
            try:
                full_hash = get_hash(filename, first_chunk_only=False)
                hashes_full[full_hash].append(filename)
            except (OSError,):
                # not accessible (permissions, etc) - pass on
                continue

    elif hash_type == 1:
        '''
        Use only file size for pre-classifying
        '''

        for filename in listOfFiles:
            try:
                file_size = os.path.getsize(filename)
                hashes_by_size[file_size].append(filename)
            except (OSError,):
                # not accessible (permissions, etc) - pass on
                continue

        for __, files_list in hashes_by_size.items():

            # if there is only one entry for an index at the size hash table,
            # this file is already unique by its size, dont process anymore
            if len(files_list) < 2:
                continue    # this file is already unique by its first 1024 bytes, dont process anymore

            # if there are more than one entry for an index at the size hash table,
            # try to distinguish them by their whole file hash keys
            for filename in files_list:
                    try:
                        full_hash = get_hash(filename, first_chunk_only=False)
                        hashes_full[full_hash].append(filename)
                    except (OSError,):
                        # the file access might've changed till the exec point got here
                        continue

    elif hash_type == 2:
        '''
        Use only first 1024 bytes for pre-classifying
        '''
        for filename in listOfFiles:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
                hashes_1024[small_hash].append(filename)
            except (OSError,):
                # not accessible (permissions, etc) - pass on
                continue

        for __, files_list in hashes_1024.items():

            # if there is only one entry for an index at the short key hash table,
            # this file is already unique by its short hash key, dont process anymore
            if len(files_list) < 2:
                continue    # this file is already unique by its first 1024 bytes, dont process anymore

            # if there are more than one entry for an index at the small hash table,
            # try to distinguish them by their whole file hash keys
            for filename in files_list:
                    try:
                        full_hash = get_hash(filename, first_chunk_only=False)
                        hashes_full[full_hash].append(filename)
                    except (OSError,):
                        # the file access might've changed till the exec point got here
                        continue


    elif hash_type == 3:
        '''
        Use both file size and first 1024 bytes for pre-classifying
        '''
        for filename in listOfFiles:
            try:
                file_size = os.path.getsize(filename)
                hashes_by_size[file_size].append(filename)
            except (OSError,):
                # not accessible (permissions, etc) - pass on
                continue

        for size_in_bytes, files in hashes_by_size.items():

            # if there is only one entry for an index at the size hash table,
            # this file is already unique by its size, dont process anymore
            if len(files) < 2:
                continue

            # if there are more than one entry for an index at the size hash table,
            # try to distinguish them by their first 1024 bytes
            for filename in files:
                    try:
                        small_hash = get_hash(filename, first_chunk_only=True)
                        # use both the size and the hash on the first 1024 bytes as key
                        # to avoid collisions on same hashes in the first 1024 bytes
                        hashes_1024[(small_hash, size_in_bytes)].append(filename)
                    except (OSError,):
                        # the file access might've changed till the exec point got here
                        continue

        for __, files_list in hashes_1024.items():

            # if there is only one entry for an index at the short key hash table,
            # this file is already unique by its short hash key, dont process anymore
            if len(files_list) < 2:
                continue    # this file is already unique by its first 1024 bytes, dont process anymore

            # if there are more than one entry for an index at the small hash table,
            # try to distinguish them by their whole file hash keys
            for filename in files_list:
                    try:
                        full_hash = get_hash(filename, first_chunk_only=False)
                        hashes_full[full_hash].append(filename)
                    except (OSError,):
                        # the file access might've changed till the exec point got here
                        continue

    #Set end_time here because we dont want to add printing times for performance calculations
    end_time = time.time()

    '''
    Time to print the files as specified in the requirements
    There are 3 seperate lists, each contains different files
    hashes_by_size : contains the files that has unique size_in_bytes
    hashes_1024 : contains the files that has unique hashkey for first 1024 bytes
    hashes_full : contains the files that has unique hashkey for whole file
    Print them one by one
    '''
    index = 0 # index for group number
    for size_in_bytes, files in hashes_by_size.items():
        if len(files) < 2:
            index = index+1
            print ("group #", index)
            print (files)

    for __, files_list in hashes_1024.items():
        if len(files_list) < 2:
            index = index+1
            print ("group #", index)
            print (files_list)

    for files_list in hashes_full.items():
        index = index+1
        print ("group #", index)
        for item in files_list:
            print (item)

    # print and return execution time
    execution_time = end_time - start_time;
    print("Execution Time: " , execution_time)
    return execution_time

if __name__ == "__main__":
    if len(sys.argv) >1:
        dirName = sys.argv[1]
    else:
        dirName = "./" #If the path is not givin, use the current path

    if len(sys.argv) >2:
        hash_type = int(sys.argv[2])
    else:
        hash_type = 3
        #If the hash type is not given, Use both file size and first 1024 bytes
        # for pre-classifying
    print(hash_type)
    x= main(dirName, hash_type )
