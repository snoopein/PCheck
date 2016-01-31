#!/usr/bin/env python

# -==[ PCheck - V 1.0 ]==-
# -==[ Author : Snoopein ]==-
#
# Copyright 2016 Snoopein
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, socket, json, os
from datetime import datetime

#Port to scan
port = 0

#default range to scan
xStart = 1
xEnd = 255
yStart = 1
yEnd = 255

hosts = []
hostsN = 0
num = 0

HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
ENDLINE = "\033[0m"
INFO = "[+] "
ERROR = "[-] "
WARNING = "\033[93m"

def getArgs():
    global ip
    global port
    global xStart
    global xEnd
    global yStart
    global yEnd

    yRange = ''
    xRange = ''
    #less than tow arguments
    if len(sys.argv) < 2:
        print HEADER+WARNING+ERROR+ENDLINE+"There is no ip in the arguments"
        displayHelp()
    #the number of arguments is odd number
    elif len(sys.argv)%2 != 0:
        print HEADER+WARNING+ERROR+ENDLINE+"Error in arguments"
        displayHelp()
    #more than four arguments
    elif len(sys.argv) >= 4:
        if sys.argv[1] == "-x":
            xRange = sys.argv[2]
        elif sys.argv[1] == "-y":
            yRange = sys.argv[2]
        elif sys.argv[1] == "-p":
            port = int(sys.argv[2])
        # six arguments
        if len(sys.argv) >= 6 :
            if sys.argv[3] == "-x":
                xRange = sys.argv[4]
            elif sys.argv[3] == "-y":
                yRange = sys.argv[4]
            elif sys.argv[3] == "-p":
                port = int(sys.argv[4])
            #eight arguments
            if len(sys.argv) == 8:
                if sys.argv[5] == "-x":
                    xRange = sys.argv[6]
                elif sys.argv[5] == "-y":
                    yRange = sys.argv[6]
                elif sys.argv[5] == "-p":
                    port = int(sys.argv[6])
    elif len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        displayHelp()

    ip = sys.argv[(len(sys.argv))-1]

    if port == 0:
        print HEADER+WARNING+ERROR+ENDLINE+"Port is not specified"
        sys.exit()

    if len(xRange) > 2:
        xList = xRange.split('-')
        xStart = int(xList[0])
        xEnd = int(xList[1])
    if len(yRange) > 2:
        yList = yRange.split('-')
        yStart = int(yList[0])
        yEnd = int(yList[1])

def checkPort(ip):
    global hostsN
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    result = s.connect_ex((ip, port))
    if result == 0:
        print HEADER+GREEN+INFO+ENDLINE+"Host {}: \t\t Open".format(ip)
        hosts.append(ip)
	hostsN+=1
    else:
        print HEADER+BLUE+INFO+ENDLINE+"Host {}: \t\t Close".format(ip)
    s.close()

def saveList():
    data = {}
    data['hosts'] = hosts
    data['ip'] = ip
    data['port'] = port
    data['hosts_number'] = hostsN
    if "x" in ip:
        data['x_range'] = str(xStart)+","+str(xEnd)
        if "y" in ip:
            data['y'] = str(yStart)+","+str(yEnd)
    data['scanned_hosts_num'] = num
    data = json.dumps(data)
    path = "hosts"
    if os.path.isfile(path):
        for x in range(1,1000):
            if not os.path.isfile(path+str(x)):
                path = "hosts"+str(x)
                break
    sfile = open(path, "w")
    sfile.write(data)
    sfile.close()
    return os.getcwd()+"/"+path

def displayHelp():
    print ""
    print "Usage:"
    print "------"
    print ""
    print "python pcheck.py [Options] <IP>"
    print ""
    print "Options:"
    print "--------"
    print ""
    print "-h\tShow this help"
    print "-p\tTo specify the port to check"
    print "-x\tTo specify the range of the variable x"
    print "-y\tTo specify the range of the variable y"
    print ""
    print "Examples:"
    print "---------"
    print ""
    print "\t-> Checking if the port 80 is open in the ip 192.168.1.18"
    print '\t   python pcheck.py -p 80 192.168.1.18'
    print ""
    print "\t-> Checking if the port 80 is open in a range of IPs with one variable x from 192.168.1.15 to 192.168.1.25 which is 11 ip to test"
    print '\t   python pcheck.py -x 15-25 -p 80 192.168.1.x'
    print ""
    print "\t-> Checking if the port 21 is open in a range of IPs with one variable x from 192.168.1.1 to 192.168.1.254 which is 254 ip to test"
    print '\t   python pcheck.py -p 21 -x 1-254 192.168.1.x'
    print ""
    print "\t-> Checking if the port 554 is open in a range of IPs with two variables x and y from 192.168.1.1 to 192.168.254.254 which is 64516 ip to test"
    print '\t   python pcheck.py -x 1-254 -y 1-254 -p 554 192.168.x.y'
    print ""
    print "\t-> Checking if the port 443 is open in a range of IPs with two variables x and y from 192.168.1.1 to 192.168.10.254 which is 2540 ip to test"
    print '\t   python pcheck.py -p 443 -x 1-10 -y 1-254 192.168.x.y'
    print ""
    sys.exit()

try:
    t1 = datetime.now()
    getArgs()
    print ""
    if "x" in ip and "y" in ip:
        for x in range(xStart, xEnd+1):
            xip = ip.replace("x", str(x))
            for y in range(yStart, yEnd+1):
                host = xip.replace("y", str(y))
                checkPort(host)
                num+=1
    elif "x" in ip and "y" not in ip:
        for x in range(xStart, xEnd+1):
            host = ip.replace("x", str(x))
            checkPort(host)
            num+=1
    else:
        checkPort(ip)
        num+=1

except KeyboardInterrupt:
    print HEADER+BLUE+INFO+ENDLINE+"Aborting ...\r"

except socket.gaierror:
    print HEADER+WARNING+ERROR+ENDLINE+'Hostname could not be resolved. Exiting'

except socket.error:
    print HEADER+WARNING+ERROR+ENDLINE+"Couldn't connect to server"

print ""
print HEADER+GREEN+INFO+ENDLINE+"Number of valid hosts : {}".format(hostsN)

if hostsN > 0:
    path = saveList()
    print HEADER+GREEN+INFO+ENDLINE+"Data saved in : "+path

t2 = datetime.now()
dt = t2-t1

print ""
print HEADER+BLUE+INFO+ENDLINE+'Scanning Completed in : ', dt
