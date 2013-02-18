""" Three hosts, two switches: highest level MiniNet API, see if we can get this working.

H1 -- S1 -- H2 -- S2 -- H3 """

from mininet.topo import Topo

class ProtoTester(Topo):
    def __init__(self):
        
        # Initialise topology
        Topo.__init__(self)

        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

  h1.setIP('10.0.1.1', 24)
	h2.setIP('10.0.2.1', 24)
	h3.setIP('10.0.3.1', 24)

        # Add links
        self.addLink(h1, s1)
        self.addLink(s1, h2)
        self.addLink(h2, s2)
        self.addLink(s2, h3)

topos = {'prototester': (lambda: ProtoTester())}
