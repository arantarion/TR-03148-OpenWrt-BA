# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:17:11 2020

@author: Henry Weckermann
"""

import re
import requests
from tqdm import tqdm
from collections import Counter
import matplotlib.pyplot as plt

USERNAME = "root"
PASSWORD = "1234"

no_of_requests = 100

# Change this if you want to test the webserver
URL = f"http://192.168.1.1/cgi-bin/luci/admin/status?luci_username={USERNAME}&luci_password={PASSWORD}"

# -------------------------------------------------------------------------- #

sessionID_list, token_list = [], []

for _ in tqdm(range(no_of_requests)):
    response = requests.post(URL)
    sessionID, token = re.findall("[a-zA-Z0-9]{32}", response.text)
    
    sessionID_list.append(sessionID)
    token_list.append(token)
    
cnt = Counter(token_list)

# -------------------------------------------------------------------------- #

# Define the matplotlib figure
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(111)

# Define plots
ax1.bar(cnt.keys(), cnt.values(), align='center', alpha=0.5)

# Define looks 
plt.xlabel('Token')
plt.ylabel('Occurrences')
plt.xticks(rotation=90, fontsize=8)
plt.yticks([1,2])
plt.grid(True)

plt.show()

# -------------------------------------------------------------------------- #

print(f"""
      \n\tNumber of requests: {len(token_list)}\n
      Number of unique tokens: {len(set(token_list))}
      Number of unique sessionIDs: {len(set(sessionID_list))}""")

