# Author: Mustafa Yagcioglu
# Author email: yagciogluengieering@gmail.com
# Coding date:  jan 2021
'''
This file is written to measure the performance of the "duplicateFiles" script
for different directories and different classification methods.

'''

# Imports
import sys, os
import duplicateFiles

# Disable prints
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Enable prints
def enablePrint():
    sys.stdout = sys.__stdout__

'''
directory to analyze
IMPORTANT: Do not forget to set this path to your path before running
'''
#path = "C:\IS_BASVURUSU\CV_2020"
path = "C:\FRANSIZCA"

blockPrint() # added to block the prints in the called scripts
list = [[],[],[],[]] # List to store the execution times for different trials

for i in range(4): #i is for the preclassification method types
    for j in range(5):# j is the number of trials for each preclassification method
        enablePrint()
        print ("Execution Time : " , list)
        print('Processing... hash type is', i, 'cycle is', j)
        blockPrint()
        execution_time = duplicateFiles.main(path,i)
        list[i].append(execution_time)

enablePrint()

print ("Execution Time : " , list)
