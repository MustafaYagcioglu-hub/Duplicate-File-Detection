Author: Mustafa Yagcioglu
Author email: yagciogluengieering@gmail.com
Coding date:  jan 2021

*******************************************************************************
Change Log

This is the first version

*******************************************************************************
General information

This code is written to classify the files in a given directory according to
their content.

*******************************************************************************
Install

The scripts are executed on windows 10 command prompt, with Python 3.9.1

*******************************************************************************
Problem Definition

A cross-platform command-line application that receives a directory as
parameter and outputs the groups of files in the directory that are duplicate
in terms of contents.

The application should:
• take into account that there might be a very large number of files in the
directory
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

*******************************************************************************
Solution Description

The first step is listing all the files in the directory. After that, each file
is analyzed to detect equality.

The brute-force method is, getting a hash key for the content of the files one
by one, and store the filename(with its path) in a hash table by using its
hash key as the key. Files with the same hash key are considered as same files.
This method is implemented in duplicateFiles.py script if it's called with
second parameter value 0;

duplicateFiles.py /path/to/dir/ 0

It takes too much time if we have many and big size files.
We may not need to read the contents of all the files if we simply consider
their sizes. If sizes are not the same, obviously files are not the same. The
algorithm is improved by considering the sizes of the files. Contents of the
files are read if the sizes of the files are same. This method is implemented
in duplicateFiles.py script if it's called with second parameter value 1;

duplicateFiles.py /path/to/dir/ 1

Instead of separating the files according to their size, we can also look first
n bytes of the file to distinguish them. This method is implemented in
duplicateFiles.py script if its called with second parameter value 2;

duplicateFiles.py /path/to/dir/ 2

Final, and the best solution according to execution times obtained from test.py,
is using both size and first bytes for pre-classification. This method is
implemented in duplicateFiles.py script if it's called with second parameter
value 3;

duplicateFiles.py /path/to/dir/ 3

This is also the default choice if the  second parameter is not given to the
script file.

*******************************************************************************
Experimental Results

By using test.py, all 4 methods are executed for the same path and the following
execution times are obtained:

[[15.179826498031616, 23.86618399620056, 20.875025749206543, 16.82053518295288, 14.789377450942993],
[0.027017593383789062, 0.02024054527282715, 0.01960468292236328, 0.014702320098876953, 0.016356706619262695],
[1.0355746746063232, 0.026567697525024414, 0.03464770317077637, 0.026821136474609375, 0.030803680419921875],
[0.010843992233276367, 0.01786971092224121, 0.015315055847167969, 0.019574403762817383, 0.009278535842895508]]

Classification results of all methods are the same, it is checked by manually.

Of course, the size of the files, the contents of the files, number of "same"
files in directory affect the results. The windows OS is not a real-time OS at
all and it also affects the uncertainty of the execution times. However, we can
obviously say that using the pre-classification methods dramatically decreases
the execution times from tens of seconds to tens of milliseconds.

Classifying according to sizes of the files is powerful than first n bytes
classification.

Using both size and first n bytes classification is the most powerful method.
Because of that, it is selected as the default configuration if the second
parameter is not given

*******************************************************************************
Files

duplicateFiles.py:
A python script to analyze the directory and prints the groups of file
    input : dirName, directory to analyze, if nothing entered, the current path
     is used
    input : hash_type, used hashing methods for classification
        0: Don't use file size and first 1024 bytes for pre-classifying
        1: Use only file size for pre-classifying
        2: Use only first 1024 bytes for pre-classifying
        3: Use both file size and first 1024 bytes for pre-classifying
    output : execution time (for performance analysis)

Example usage: duplicateFiles.py C:\AMD 3



test.py
A python script to analyze the performances of the classification methodologies

Example usage: test.py

Note: Do not forget to change directory variable in test.py file, it could be
parametric but I didn't want to make this file complex
*******************************************************************************
BUGS and IMPROVEMENTS

There are no known bugs

Engineering tests are completed. In these tests, all possible conditions are
tested. These conditions are:
Two files with the same size but different content.
Two files with the same first 1024 bytes but different content.
Two files with the same content.
Files with different sizes
Files with different first 1024 bytes

As future work, 1024 bytes choice may be considered. But since the test
results strictly depend on the file characteristics on the directory, any
optimization isn't implemented now. If the files in the related domain have a
characteristic, optimization may be done accordingly. Test infrastructure is
suitable and ready for such optimization.

Detailed verification and validation should be done by independent people

*******************************************************************************
