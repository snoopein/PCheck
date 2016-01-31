PCheck
===
A python script that checks if a TCP Port is open in a single IP or a range of IPs and saves the hosts where the port is open in a file in form of a JSON array

Usage
===

    $ python pcheck.py [Options] -p <Port> <IP>

Options
===

    -h    Show the help message
    -p    To specify the port to check
    -x    To specify the range of the variable x
    -y    To specify the range of the variable y

Examples
===

Checking if the port 22 is open in the ip 192.168.1.18

    $ python pcheck.py -p 22 192.168.1.18
   
Checking if the port 80 is open in a range of IPs with one variable x from 192.168.1.15 to 192.168.1.25 which is 11 ip to test

    $ python pcheck.py -x 15-25 -p 80 192.168.1.x
   
Checking if the port 21 is open in a range of IPs with one variable x from 192.168.1.1 to 192.168.1.254 which is 254 ip to test

    $ python pcheck.py -p 21 -x 1-254 192.168.1.x

Checking if the port 554 is open in a range of IPs with two variables x and y from 192.168.1.1 to 192.168.254.254 which is 64516 ip to test

    $ python pcheck.py -x 1-254 -y 1-254 -p 554 192.168.x.y"

Checking if the port 443 is open in a range of IPs with two variables x and y from 192.168.1.1 to 192.168.10.254 which is 2540 ip to test

    $ python pcheck.py -p 443 -x 1-10 -y 1-254 192.168.x.y


Screenshots
===

![01](http://i.imgur.com/ysVf25B.png)
