#!/usr/bin/python
import sys
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import time
import os
def myNetwork(N):

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c3=net.addController(name='c3',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    c1=net.addController(name='c1',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    c2=net.addController(name='c2',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    info( '*** Add links\n')
    h1s3 = {'bw':10,'delay':str(N),'loss':0,'max_queue_size':10}
    net.addLink(h1, s3, cls=TCLink , **h1s3)
    h2s4 = {'bw':10,'delay':str(N),'loss':0,'max_queue_size':10}
    net.addLink(h2, s4, cls=TCLink , **h2s4)
    s4s5 = {'bw':10,'delay':str(N),'loss':0,'max_queue_size':10}
    net.addLink(s4, s5, cls=TCLink , **s4s5)
    s3s5 = {'bw':10,'delay':str(N),'loss':0,'max_queue_size':10}
    net.addLink(s3, s5, cls=TCLink , **s3s5)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s5').start([c1])
    net.get('s4').start([c3])
    net.get('s3').start([c2])
    net.addNAT().configDefault()
    net.start()
    info( '*** Post configure switches and hosts\n')
    
    h1.cmd('cd server')
    m1=h1.cmd('python3 server.py 0.0.0.0 {} > log.txt &'.format(N//100+500))
    time.sleep(0.5)
    begin=time.time()
    m2=h2.cmd('cd client && python3 client.py 10.0.0.1 {} <test.txt'.format(N//100+500))
    print ('#'*100)
    print (m1)
    print ('*'*100)
    print (m2)
    return N,time.time()- begin
if __name__ == '__main__':
    setLogLevel( 'info' )
    f=open('result.txt','a')
    os.system('sudo mn -c')
    x,y=myNetwork(int (sys.argv[1]))
    f.write('{},{}\n'.format(x,y))

