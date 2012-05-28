#!/usr/bin/python

"CS244 Assignment 3: Topology 1"

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, output
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, custom, quietRun, dumpNetConnections
from mininet.cli import CLI

from time import sleep, time
from multiprocessing import Process
from subprocess import Popen
import termcolor as T
import argparse

import sys
import os
from util.monitor import monitor_devs_ng

def cprint(s, color, cr=True):
    """Print in color
       s: string to print
       color: color to use"""
    if cr:
        print T.colored(s, color)
    else:
        print T.colored(s, color),

parser = argparse.ArgumentParser(description="Parking lot tests")
parser.add_argument('--bw', '-b',
                    type=float,
                    help="Bandwidth of network links",
                    required=True)

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    default="results")

parser.add_argument('-n',
                    type=int,
                    help=("Number of senders in the parking lot topo."
                    "Must be >= 1"),
                    required=True)

parser.add_argument('--cli', '-c',
                    action='store_true',
                    help='Run CLI for topology debugging purposes')

parser.add_argument('--time', '-t',
                    dest="time",
                    type=int,
                    help="Duration of the experiment.",
                    default=60)

# Expt parameters
args = parser.parse_args()

if not os.path.exists(args.dir):
    os.makedirs(args.dir)

lg.setLogLevel('info')

# Topology to be instantiated in Mininet
class Topo1(Topo):
    "Topo1 Topology"

    def __init__(self, n=1, cpu=.1, bw=10, delay=None,
                 max_queue_size=None, **params):

        # Initialize topo
        Topo.__init__(self, **params)

        # Host and link configuration
        hconfig = {'cpu': cpu}
        lconfig = {'bw': bw, 'delay': delay,
                   'max_queue_size': max_queue_size }

        # Switch ports 1:uplink 2:hostlink 3:downlink
        uplink, downlink = 1, 2

	# Hosts and switches
        s1 = self.add_switch('s1')
	#s2 = self.add_switch('s2')
	sender = self.add_host('sender', **hconfig)
	receiver = self.add_host('receiver')

	# Wire receiver
        self.add_link(receiver, s1,
                      port1=0, port2=downlink, **lconfig)
        #self.add_link(receiver, s2,
                      #port1=1, port2=downlink, **lconfig)

	# Wire first switch
	self.add_link(sender, s1,
			port1=0, port2=uplink, **lconfig)
	#self.add_link(sender, s2,
			#port1=1, port2=uplink, **lconfig)

def waitListening(client, server, port):
    "Wait until server is listening on port"
    if not 'telnet' in client.cmd('which telnet'):
        raise Exception('Could not find telnet')
    cmd = ('sh -c "echo A | telnet -e A %s %s"' %
           (server.IP(), port))
    while 'Connected' not in client.cmd(cmd):
        output('waiting for', server,
               'to listen on port', port, '\n')
        sleep(.5)

def progress(t):
       # Begin: Template code
    while t > 0:
        cprint('  %3d seconds left  \r' % (t), 'cyan', cr=False)
        t -= 1
        sys.stdout.flush()
        sleep(1)
    print

def start_tcpprobe():
    os.system("rmmod tcp_probe 1>/dev/null 2>&1; modprobe tcp_probe")
    Popen("cat /proc/net/tcpprobe > %s/tcp_probe.txt" % args.dir, shell=True)

def stop_tcpprobe():
    os.system("killall -9 cat; rmmod tcp_probe")

def run_parkinglot_expt(net, n):
    "Run experiment"

    seconds = args.time

    # Start the bandwidth and cwnd monitors in the background
    monitor = Process(target=monitor_devs_ng, 
            args=('%s/bwm.txt' % args.dir, 1.0))
    monitor.start()
    start_tcpprobe()

    # Get receiver and clients
    recvr = net.getNodeByName('receiver')
    sender = net.getNodeByName('sender')

    # Setup receiver IP configuration
    #recvr.cmd('ifconfig receiver-eth1 10.0.0.4 netmask 255.0.0.0')
    
    #recvr.cmd('ip rule add from 10.0.0.1 table 1')
    #recvr.cmd('ip rule add from 10.0.0.4 table 2')
    #recvr.cmd('ip route add 10.0.0.0/24 dev receiver-eth0 scope link table 1')
    #recvr.cmd('ip route add default via 10.0.0.1 dev receiver-eth0 table 1')
    #recvr.cmd('ip route add 10.0.0.0/24 dev receiver-eth1 scope link table 2')
    #recvr.cmd('ip route add default via 10.0.0.4 dev receiver-eth1 table 2')
    #recvr.cmd('ip route add scope global nexthop via 10.0.0.1 dev \
	    #receiver-eth1')

    # Setup sender IP configuration
    #sender.cmd('ifconfig sender-eth1 10.0.0.3 netmask 255.0.0.0')

    #sender.cmd('ip rule add from 10.0.0.2 table 1')
    #sender.cmd('ip rule add from 10.0.0.3 table 2')
    #sender.cmd('ip route add 10.0.0.0/24 dev sender-eth0 scope link table 1')
    #sender.cmd('ip route add default via 10.0.0.2 dev sender-eth0 table 1')
    #sender.cmd('ip route add 10.0.0.0/24 dev sender-eth1 scope link table 2')
    #sender.cmd('ip route add default via 10.0.0.3 dev sender-eth1 table 2')
    #sender.cmd('ip route add default scope global nexthop via 10.0.0.2 dev \
	    #sender-eth0')

    # Start the receiver
    port = 5001
    recvr.cmd('iperf -s -p', port,
              '> %s/iperf_server.txt' % args.dir, '&')

    waitListening(sender, recvr, port)

    sender.sendCmd('iperf -c %s -p %s -t %d -i 1 -yc > %s/iperf_%s.txt' %
	    (recvr.IP(), 5001, seconds, args.dir, recvr))
    sender.waitOutput()

    # TODO: start the sender iperf processes and wait for the flows to finish
    # Hint: Use getNodeByName() to get a handle on each sender.
    # Hint: Use sendCmd() and waitOutput() to start iperf and wait for them to finish
    # iperf command to start flow: 'iperf -c %s -p %s -t %d -i 1 -yc > %s/iperf_%s.txt' % (recvr.IP(), 5001, seconds, args.dir, node_name)
    # Hint (not important): You may use progress(t) to track your experiment progress

    recvr.cmd('kill %iperf')

    # Shut down monitors
    monitor.terminate()
    stop_tcpprobe()

def check_prereqs():
    "Check for necessary programs"
    prereqs = ['telnet', 'bwm-ng', 'iperf', 'ping']
    for p in prereqs:
        if not quietRun('which ' + p):
            raise Exception((
                'Could not find %s - make sure that it is '
                'installed and in your $PATH') % p)

def main():
    "Create and run experiment"
    start = time()

    topo = Topo1(n=args.n)

    host = custom(CPULimitedHost, cpu=.15)  # 15% of system bandwidth
    link = custom(TCLink, bw=args.bw, delay='1ms',
                  max_queue_size=200)

    net = Mininet(topo=topo, host=host, link=link)

    net.start()

    cprint("*** Dumping network connections:", "green")
    dumpNetConnections(net)

    cprint("*** Testing connectivity", "blue")

    net.pingAll()

    if args.cli:
        # Run CLI instead of experiment
        CLI(net)
    else:
        cprint("*** Running experiment", "magenta")
        run_parkinglot_expt(net, n=args.n)

    net.stop()
    end = time()
    os.system("killall -9 bwm-ng")
    cprint("Experiment took %.3f seconds" % (end - start), "yellow")

if __name__ == '__main__':
    check_prereqs()
    main()

