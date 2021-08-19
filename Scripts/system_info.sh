#!/bin/ash

#Hostname
cat /etc/config/system | grep hostname


# Mocel and Architecture
cat /proc/cpuinfo | egrep 'system type|machine'



# OpenWrt Release
cat /etc/os-release | grep '_RELEASE'


# Luci Release
opkg list | grep 'luci - ' | egrep -v "rpcd|nginx"


# Kernel Version
uname -a


# local time
date



# uptime + load avg
uptime


# Memory Info
cat /proc/meminfo | grep Mem



#no. of connections
echo Active Connections: ; cat /proc/net/nf_conntrack | wc -l


#active dhcp leases
cat /tmp/dhcp.leases

# wlan stations
iwinfo

# station 1
echo connected devices wlan0: ; iwinfo wlan0 assoclist
echo connected devices wlan1: ; iwinfo wlan1 assoclist