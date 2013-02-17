#!/usr/bin/python

"""
Build a simple network from scratch, using mininet primitives.
This is more complicated than using the higher-level classes,
but it exposes the configuration details and allows customization.

For most tasks, the higher-level API will be preferable.
"""

from mininet.net import Mininet
from mininet.node import Node
from mininet.link import Link
from mininet.log import setLogLevel, info
from mininet.util import quietRun

from time import sleep

def scratchNet( cname='controller', cargs='-v ptcp:' ):
    "Create network from scratch using Open vSwitch."

    info( "*** Creating nodes\n" )
    controller = Node( 'c0', inNamespace=False )
    switch0 = Node( 's0', inNamespace=False )
    switch1 = Node('s1', inNamespace=False)
    h0 = Node( 'h0' )
    h1 = Node( 'h1' )
    cellLink = Node('cellLink')

    info( "*** Creating links\n" )
    Link( h0, switch0 )
    Link( h1, switch1 )
    Link(cellLink, switch0)
    Link(cellLink, switch1)

    info( "*** Configuring hosts\n" )   
    
    info( str( h0 ) + '\n' )
    info( str( h1 ) + '\n' )
    info( str( cellLink ) + '\n' )

    info( "*** Starting network using Open vSwitch\n" )
    controller.cmd( cname + ' ' + cargs + '&' )
    switch0.cmd( 'ovs-vsctl del-br dp0' )
    switch0.cmd( 'ovs-vsctl add-br dp0' )
    for intf in switch0.intfs.values():
        print switch0.cmd( 'ovs-vsctl add-port dp0 %s' % intf )

    switch1.cmd( 'ovs-vsctl del-br dp1' )
    switch1.cmd( 'ovs-vsctl add-br dp1' )
    for intf in switch1.intfs.values():
        print switch1.cmd( 'ovs-vsctl add-port dp1 %s' % intf )

    # Note: controller and switch are in root namespace, and we
    # can connect via loopback interface
    switch0.cmd( 'ovs-vsctl set-controller dp0 tcp:127.0.0.1:6633' )
    switch1.cmd( 'ovs-vsctl set-controller dp1 tcp:127.0.0.1:6634' )

    info( '*** Waiting for switch to connect to controller' )
    while 'is_connected' not in quietRun( 'ovs-vsctl show' ):
        sleep( 1 )
        info( '.' )
    info( '\n' )
    h0.cmdPrint('ip link')
    h1.cmdPrint('ip link')
    cellLink.cmdPrint('ip link')
    h0.cmdPrint('ifconfig h0-eth0 10.0.1.1 netmask 255.255.255.0')
    h1.cmdPrint('ifconfig h1-eth0 10.0.2.1 netmask 255.255.255.0')
    cellLink.cmdPrint('ifconfig cellLink-eth0 10.0.1.2 netmask 255.255.255.0')
    cellLink.cmdPrint('ifconfig cellLink-eth1 10.0.2.2 netmask 255.255.255.0')
    h0.cmdPrint('ping -c 5 10.0.1.2')
    h0.cmdPrint('route')
    h1.cmdPrint('route')
    cellLink.cmdPrint('route')

   # info( "*** Running test\n" )
   # h0.cmdPrint( 'ping -c1 ' + h1.IP() )

   # info( "*** Stopping network\n" )
   #controller.cmd( 'kill %' + cname )
   # switch.cmd( 'ovs-vsctl del-br dp0' )
   # switch.deleteIntfs()
   # info( '\n' )

if __name__ == '__main__':
    setLogLevel( 'info' )
    info( '*** Scratch network demo (kernel datapath)\n' )
    Mininet.init()
    scratchNet()
