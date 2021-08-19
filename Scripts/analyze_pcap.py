from scapy.all import *
from scipy import stats
import matplotlib.pyplot as plt
import random
import numpy as np
from collections import Counter

# Open pcap file
scapy_cap = rdpcap('dns_dump.pcap')

# select only DNS packages from 192.168.1.1 (openwrt router)
important_packages = []
for pkt in scapy_cap:
    if IP in pkt and pkt[IP].src == '192.168.1.1':
        try:
            if pkt.haslayer(DNS):
                important_packages.append(pkt)
        except:
            pass

# extract port and transaction ID
DNS_PORT = []
TRANS_ID = []
for pkt in important_packages:
    DNS_PORT.append(pkt.dport)
    TRANS_ID.append(pkt.getlayer(DNS).id)

dns_count = Counter(DNS_PORT)
trans_count = Counter(TRANS_ID)

# Printing results

print('Test results for DNS port randomization:\n')
print(f'\tNumber of samples: {len(DNS_PORT)}')
print(f'\tNumber of unique ports: {len(set(DNS_PORT))}')
print(f'\tRange: {min(DNS_PORT)} - {max(DNS_PORT)}')
print(f'\tStandard Deviation: {np.std(DNS_PORT)}')
print(f'\tMost common ports: {dns_count.most_common(15)}\n')

print('#'*100, '\n')
print('Test results for transaction ID randomization:\n')
print(f'\tNumber of samples: {len(TRANS_ID)}')
print(f'\tNumber of unique ports: {len(set(TRANS_ID))}')
print(f'\tRange: {min(TRANS_ID)} - {max(TRANS_ID)}')
print(f'\tStandard Deviation: {np.std(TRANS_ID)}')
print(f'\tMost common ports: {trans_count.most_common(15)}\n')


print(stats.kstest(DNS_PORT, random.sample(range(0, 65535), 1000)))
print(stats.kstest(TRANS_ID, random.sample(range(0, 65535), 1000)))

fig = plt.figure(figsize=(12, 8))
sub1 = fig.add_subplot(221)
sub1.hist(DNS_PORT)
sub1.set_xlabel('Ports')
sub1.set_ylabel('Occurances per bin')

sub2 = fig.add_subplot(222)
sub2.hist(TRANS_ID)
sub2.set_xlabel('Ports')
sub2.set_ylabel('Occurances per bin')

sub3 = fig.add_subplot(223)
sub3.scatter(range(0,len(DNS_PORT)), DNS_PORT)
sub3.set_xlabel('Ports')
sub3.set_ylabel('Queries')

sub4 = fig.add_subplot(224)
sub4.scatter(range(0,len(TRANS_ID)), TRANS_ID)
sub4.set_xlabel('Ports')
sub4.set_ylabel('Queries')

plt.show()