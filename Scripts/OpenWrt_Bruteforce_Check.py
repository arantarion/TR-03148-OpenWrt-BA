# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:34:27 2020

@author: Henry Weckermann (henry.weckermann@smail.inf.h-brs.de)

A script to visualize the behavior of OpenWrt when faced with multiple
wrong login attempts to the ssh server or the webserver. 
Uses linear regresion to fit a line in the response data of the server. 

Used in testing TR.D.11 of BSI TR-03148
"""

import sys
import time
import pprint
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy import stats

# Global parameters. Change these to your needs
USERNAME = "root"
PASSWORD = "imawrongpassword"
CORRECT_PW = "1234"

no_of_requests = 100

# Change this if you want to test ssh
IP = '192.168.1.1'
PORT = 22

# Change this if you want to test the webserver
URL = f"http://192.168.1.1/cgi-bin/luci/admin/status?luci_username={USERNAME}&luci_password={PASSWORD}"


def plot_results(xlabel_text, ylabel_text):
    # Define x values as the number of requests (so 1, 2, ..., x)
    x = range(1, no_of_requests+1)
    
    # Calculate the linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, times)
    
    # Define the matplotlib figure
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    # Define plots
    ax1.scatter(x, times)
    ax1.plot(x, intercept + slope*x, 'black', label='Regression line')
    
    # Define looks 
    plt.xlabel(xlabel_text)
    plt.ylabel(ylabel_text)
    plt.legend()
    plt.grid(True)
    
    plt.show()
    
    # -------------------------------------------------------------------------- #
    
    # Define results
    results = {'Mean' : np.round(np.mean(times),3),
               'Median' : np.round(np.median(times),3),
               'Regression coefficient' : str(np.round(r_value,5)) + f" (p = {np.round(p_value,3)})",
               'Standard error' : np.round(std_err, 3)
               }
    
    # Plot results in a nice way. You don't have to understand the print statement. It justs looks better
    myStr = pprint.pformat(results)
    print(myStr.translate(myStr.maketrans("'{},", "    ")))

def check_success_web():
    
    import re
    
    # Checking if the webserver still responds to a correct login attempt
    id_string = "Invalid username and/or password! Please try again."
    
    URL_new = URL.replace(PASSWORD, CORRECT_PW)
    r = requests.post(URL_new)
    sessionID, token = re.findall("[a-zA-Z0-9]{32}", r.text)
    
    if id_string not in r.text:
        print(f""""Successfully logged in with user {USERNAME}. Got Session-ID {sessionID} and token {token}.
               The IP does not seem to be blacklisted by the DUT.""")
    
    # -------------------------------------------------------------------------- #
    
    browser_open = input("Do you want to open the OpenWrt web-interface in your browser (y / n): ")
    if browser_open.lower() == "y":
        import webbrowser
        webbrowser.open_new(URL)

def check_success_ssh():
    # Final login to see if login is still possible
    print("\n\nThis should print the OpenWrt Banner if the ssh server did not block the IP\n")
    ssh.open_connection(IP, port=PORT)
    openwrt_banner_new = ssh.login(USERNAME, CORRECT_PW)
    print(openwrt_banner_new)


if sys.argv[1] == "web":
    
    import requests
    
    # -------------------------------------------------------------------------- #
    
    # Check if webserver is alive and connection is possible
    tmp = requests.post(URL.replace(PASSWORD, CORRECT_PW))
    if tmp.status_code == 200 and "Invalid username and/or password!" not in tmp.text:
        print(f"Status code {tmp.status_code} -> Webserver found and is accessable via password {CORRECT_PW}")
    else:
        print(f"Error. Please check the password and if the webserver is accessable at the specified URL -> {URL[:URL.find('?')]}")
        sys.exit(0)
    
    # -------------------------------------------------------------------------- #
    
    # Making the requests to the OpenWrt login page
    times = []
    for _ in tqdm(range(no_of_requests)):
        start = time.time()
        r = requests.post(URL)
        stop = time.time()
        if r.status_code == 403:
            times.append(stop - start)
        elif r.status_code == 200:
            print("This should not happen if you set a wrong password")
        else:
            print(f"Status Code: {r.status_code}. Please seek help.")
    
    assert len(times) == no_of_requests
    
    plot_results('Number of POST requests to the OpenWrt webserver', 'Time to complete the request (sec)')
    check_success_web()



elif sys.argv[1] == "ssh":
   
    from SSHLibrary import SSHLibrary
   
    ssh = SSHLibrary()

    # -------------------------------------------------------------------------- #
    
    # Sanity checks
    connection_status = ssh.open_connection(IP, port=PORT)
    
    if connection_status != 1:
        print("The SSH Server is not reachable. Please try something different")
        sys.exit(0)
    
    try:
        openwrt_banner = ssh.login(USERNAME, CORRECT_PW)
        if "built-in shell (ash)" not in openwrt_banner:
            print("Server is reachable but no login is possible. Is the password correct?")
            sys.exit(0)
    except:
        print("Server is reachable but no login is possible. Is the password correct?")
        sys.exit(0)
    
    
    # -------------------------------------------------------------------------- #
    
    # Testing
    times = []
    for _ in tqdm(range(no_of_requests)):
        failed = False
        start = time.time()
        try:
            ssh.open_connection(IP, port=PORT)
            ssh.login(USERNAME, PASSWORD)
        except:
            ssh.close_connection()
            failed = True    
        stop = time.time()
        
        if failed:
            times.append(stop-start)
        else:
            print("This should not happen.")
            sys.exit(0)
    
    # Checking if all login attempts have been made.
    assert len(times) == no_of_requests
    
    plot_results('Number of login attempts at the ssh server', 'Time to complete the request (sec)')
    check_success_ssh()
    
    
else:
    print("Please choose either 'web' or 'ssh'")
