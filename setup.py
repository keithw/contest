#!/usr/bin/python

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

class ProtoTester(Topo):
    def __init__(self):
        
        # Initialise topology
        Topo.__init__(self)

        # Add hosts and switches
        sender = self.addHost('sender', ip='10.0.1.1', mac='00:00:00:00:00:01')
        LTE = self.addHost('LTE', ip='0.0.0.0')
        receiver = self.addHost('receiver', ip='10.0.1.2', mac='00:00:00:00:00:02')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add links
        self.addLink(sender, s1)
        self.addLink(s1, LTE)
        self.addLink(LTE, s2)
        self.addLink(s2, receiver)

def set_all_IP(net, sender, LTE, receiver):
    sender.sendCmd('ifconfig sender-eth0 10.0.1.1 netmask 255.255.255.0')
    sender.waitOutput()
    LTE.sendCmd('ifconfig LTE-eth0 up')
    LTE.waitOutput()
    LTE.sendCmd('ifconfig LTE-eth1 up')
    LTE.waitOutput()
    receiver.sendCmd('ifconfig receiver-eth0 10.0.1.2 netmask 255.255.255.0')
    receiver.waitOutput()

    sender.sendCmd('echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6')
    sender.waitOutput()
    LTE.sendCmd('echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6')
    LTE.waitOutput()
    receiver.sendCmd('echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6')
    receiver.waitOutput()

def display_routes(net, sender, LTE, receiver):
    print 'sender route...'
    sender.sendCmd('route -n')
    print sender.waitOutput()
    print 'LTE route...'
    LTE.sendCmd('route -n')
    print LTE.waitOutput()
    print 'receiver route...'
    receiver.sendCmd('route -n')
    print receiver.waitOutput()

def run_cellsim(LTE):
    LTE.sendCmd('/home/ubuntu/multisend/sender/cellsim-setup.sh LTE-eth0 LTE-eth1')
    LTE.waitOutput()
    LTE.sendCmd('/home/ubuntu/multisend/sender/cellsim-runner.sh')
    LTE.waitOutput()

def test_cellsim():
    topo = ProtoTester()
    net = Mininet(topo=topo, host=Host, link=Link)
    net.start()

    sender = net.getNodeByName('sender')
    LTE = net.getNodeByName('LTE')
    receiver = net.getNodeByName('receiver')

    set_all_IP(net, sender, LTE, receiver)
    
    #Dump connections
    dumpNodeConnections(net.hosts)
    display_routes(net, sender, LTE, receiver)

    run_cellsim(LTE)

    CLI(net)

    net.stop()

if __name__ == '__main__':
    test_cellsim()
