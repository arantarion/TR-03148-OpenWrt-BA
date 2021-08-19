# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 19:00:16 2020

@author: Henry

OpenWrt configuration summary and analysis tool
"""

import glob, os, re

os.chdir("OpenWrtBackup")

ff = []
summary = []

for file in glob.glob(r'**\*', recursive=True):
    if re.match('opkg', file) or re.match('dropbear', file):
        continue
    else:
        if os.path.isfile(file):
            try:
                with open(file, "r") as f:
                    summary.append(f"File Location: {file}\n" + "\n" + f.read() + "\n" + "-"*80 + "\n")
            except:
                print(f"Error in file: {file}")


with open('your_file.txt', 'w') as f:
    for item in summary:
        f.write("%s\n" % item)
