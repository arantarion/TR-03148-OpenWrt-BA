# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 12:50:08 2020

@author: Henry
Hashing all files in the current directory
"""


import glob
import hashlib
import os

os.chdir(os.getcwd())

filenames = glob.glob("*")

for filename in filenames:
    if os.path.isfile(filename):
        try:
            with open(filename, 'rb') as inputfile:
                data = inputfile.read()
                print(f"{filename}")
                print(f"MD5: \t{hashlib.md5(data).hexdigest()}")
                print(f"SHA256: {hashlib.sha256(data).hexdigest()}\n\n" + "-"*72 + "\n")
        except:
            print(f"Error in file {filename}")
            
os.system("pause")