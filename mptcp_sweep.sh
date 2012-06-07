#!/bin/bash

sysctl 'net.mptcp.mptcp_enabled=1'

./mptcp.sh topo_measure.py 005 51200 > 005.txt
./mptcp.sh topo_measure.py 01 102400 > 01.txt
./mptcp.sh topo_measure.py 02 204800 > 02.txt
./mptcp.sh topo_measure.py 05 512000 > 05.txt

sysctl 'net.mptcp.mptcp_enabled=0'

./mptcp.sh topo_wifi.py 005 51200 > 005_tcp_wifi.txt
./mptcp.sh topo_wifi.py 01 102400 > 01_tcp_wifi.txt
./mptcp.sh topo_wifi.py 02 204800 > 02_tcp_wifi.txt
./mptcp.sh topo_wifi.py 05 512000 > 05_tcp_wifi.txt

./mptcp.sh topo_measure.py 005 51200 > 005_tcp_3g.txt
./mptcp.sh topo_measure.py 01 102400 > 01_tcp_3g.txt
./mptcp.sh topo_measure.py 02 204800 > 02_tcp_3g.txt
./mptcp.sh topo_measure.py 05 512000 > 05_tcp_3g.txt

sysctl 'net.mptcp.mptcp_enabled=1'
