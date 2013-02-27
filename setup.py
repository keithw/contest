#!/usr/bin/python

## TO DO: run sudo ./cellsim <uplink> <downlink> <h3 mac> <error> from xterm

## To run cellsim on this network: first, run this code. Then open xterms
## for all hosts by entering 'xterm h1 h2 h3' into the mininet prompt.
## In the xterm for h3 (the client host), enter the command 'ifconfig'
## and locate the host's MAC address.
## In the xterm for h2, cd into the directory where cellsim is stored,
## then run 'sudo ifconfig h2-eth0 up promisc' and 'sudo ifconfig h2-eth1
## up promisc' to set both ethernet ports to promiscuous mode. Next run
## 'sudo ./cellsim <uplink file> <downlink file> <client MAC address> 0.0'
## to start cellsim.

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import Link
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.util import ensureRoot

from subprocess import Popen, PIPE
from time import sleep, time

import sys
import os
import math

ensureRoot()

#Topology to run cellSim
#H1--S1--H2*--S2--H3

class ProtoTester(Topo):
    def __init__(self):
        
        # Initialise topology
        Topo.__init__(self)

        # Add hosts and switches
        h1 = self.addHost('h1', ip='10.0.1.1')
        h2 = self.addHost('h2', ip='10.0.1.2')
        h3 = self.addHost('h3', ip='10.0.2.1')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add links
        self.addLink(h1, s1)
        self.addLink(s1, h2)
        self.addLink(h2, s2)
        self.addLink(s2, h3)

def set_all_IP(net, h1, h2, h3):
    h1.sendCmd('ifconfig h1-eth0 10.0.1.1 netmask 255.255.255.0')
    h1.waitOutput()
    h2.sendCmd('ifconfig h2-eth0 10.0.1.2 netmask 255.255.255.0')
    h2.waitOutput()
    h2.sendCmd('ifconfig h2-eth1 10.0.2.2 netmask 255.255.255.0')
    h2.waitOutput()
    h3.sendCmd('ifconfig h3-eth0 10.0.2.1 netmask 255.255.255.0')
    h3.waitOutput()

def add_default_routes(net, h1, h3):
    h1.sendCmd('sudo route add default gw 10.0.1.2')
    h1.waitOutput()
    h3.sendCmd('sudo route add default gw 10.0.2.2')
    h3.waitOutput()

# Want this to run in an xterm for h2... is there a way to make that happen?
def run_cellsim(net):
    # Get user data for uplink and downlink files; get client MAC
    uplink = raw_input('Enter uplink filepath: ')
    downlink = raw_input('Enter downlink filepath: ')
    #clientMAC = raw_input('Enter client MAC address (in this setup,\
    #        H3 is the client): ')
    h3 = net.getNodeByName('h3')
    clientMAC = h3.MAC()
    
    h2 = net.getNodeByName('h2')
    h2.sendCmd('sudo ifconfig h2-eth0 up promisc')
    h2.waitOutput()
    h2.sendCmd('sudo ifconfig h2-eth1 up promisc')
    h2.waitOutput()
    startCellsim = 'sudo ./cellsim %(uplink)s %(downlink)s %(mac)s 0.0'%\
            {'uplink': uplink, 'downlink': downlink, 'mac': clientMAC}
    h2.cmd(startCellsim)

def stop_cellsim():
    Popen('killall -9 cat', shell=True).wait()
    Popen('sudo mn -c', shell=True).wait() 

def start_ping(net, h1, h2, h3):
    print 'Pinging h2 at 10.0.1.2 from h1...'
    h1.sendCmd('ping -c 5 10.0.1.2')
    print h1.waitOutput()
    print 'Pinging h3 at 10.0.2.1 from h2...'
    h2.sendCmd('ping -c 5 10.0.2.1')
    print h2.waitOutput()
    print 'Pinging h1 at 10.0.1.1 from h3...'
    h3.sendCmd('ping -c 5 10.0.1.1')
    print h3.waitOutput()

def display_routes(net, h1, h2, h3):
    print 'h1 route...'
    h1.sendCmd('route')
    print h1.waitOutput()
    print 'h2 route...'
    h2.sendCmd('route')
    print h2.waitOutput()
    print 'h3 route...'
    h3.sendCmd('route')
    print h3.waitOutput()

def test_cellsim():
    topo = ProtoTester()
    net = Mininet(topo=topo, host=Host, link=Link)
    net.start()

    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    h3 = net.getNodeByName('h3')

    set_all_IP(net, h1, h2, h3)
    add_default_routes(net, h1, h3)
    
    #Dump connections
    dumpNodeConnections(net.hosts)
    #Ping all pairs
    net.pingAll()

#    print "In case that didn't work..."
#    start_ping(net, h1, h2, h3)

    display_routes(net, h1, h2, h3)
#    run_cellsim(net)
#    sleep(5)
#    print "On mininet prompt, open xterms for H1, H2, and H3 by entering: \
#            xterm h1 h2 h3 . \
#            To run cellsim, switch to h2's xterm and enter: \
#            sudo run_cellsim.py"
    CLI(net)

##    stop_cellsim()
    net.stop()
##    Popen('pgrep -f cellsim.cc | xargs kill -9', shell=True).wait()

if __name__ == '__main__':
    test_cellsim()

