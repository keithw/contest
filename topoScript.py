""" Three hosts, two switches: highest level MiniNet API, see if we can get this working.

H1 -- S1 -- H2 -- S2 -- H3 """

from mininet.topo import Topo

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
        
        #h1.setHostRoute('h2', 'h1-eth0')
	#h1.setHostRoute('h3', 'h1-eth0')
        #h2.setHostRoute('h1', 'h2-eth0')
	#h2.setHostRoute('h3', 'h2-eth1')
        #h3.setHostRoute('h2', 'h3-eth0')
        #h3.setHostRoute('h1', 'h3-eth0')

topos = {'prototester': (lambda: ProtoTester())}

# From command line run (how to integrate into script?):
# h1 ifconfig h1-eth0 10.0.1.1 netmask 255.255.255.0
# h2 ifconfig h2-eth0 10.0.1.2 netmask 255.255.255.0
# h2 ifconfig h2-eth1 10.0.2.2 netmask 255.255.255.0
# h3 ifconfig h3-eth0 10.0.2.1 netmask 255.255.255.0
