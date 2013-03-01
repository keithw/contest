#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import Link
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.util import ensureRoot

import sys

ensureRoot()

#Topology
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

    display_routes(net, h1, h2, h3)
    CLI(net)

    net.stop()

if __name__ == '__main__':
    test_cellsim()
