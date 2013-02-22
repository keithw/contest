#!/usr/bin/python

#Which of these statements do I need/are there more that should be here?
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

from subprocess import Popen, PIPE
from time import sleep, time

import sys
import os
import math

#How do I set up the network to be prototester?
net = Mininet(topo=topo, host=Host, link=TCLink)

def set_all_IP(net):
    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    h3 = net.getNodeByName('h3')

    h1.sendCmd("ifconfig h1-eth0 10.0.1.1 netmask 255.255.255.0")
    h1.waitOutput()
    h2.sendCmd("ifconfig h2-eth0 10.0.1.2 netmask 255.255.255.0")
    h2.waitOutput()
    h2.sendCmd("ifconfig h2-eth1 10.0.2.2 netmask 255.255.255.0")
    h3.sendCmd("ifconfig h3-eth0 10.0.2.1 netmask 255.255.255.0")

def run_Cellsim(net):
    h2 = net.getNodeByName('h2')
    #What should go in the http line?
    proc = h2.popen("python http/whatshouldgohere.py", shell=True)
    sleep(1)
    return [proc]
