#!/bin/bash

./mptcp.sh topo_m005.py 005 > 005.txt
./mptcp.sh topo_m01.py 01 > 01.txt
./mptcp.sh topo_m02.py 02 > 02.txt
./mptcp.sh topo_m05.py 05 > 05.txt

sysctl 'net.mptcp.mptcp_enabled=0'

./mptcp.sh topo_m005_wifi.py 005 > 005_tcp_wifi.txt
./mptcp.sh topo_m01_wifi.py 01 > 01_tcp_wifi.txt
./mptcp.sh topo_m02_wifi.py 02 > 02_tcp_wifi.txt
./mptcp.sh topo_m05_wifi.py 05 > 05_tcp_wifi.txt

./mptcp.sh topo_m005.py 005 > 005_tcp_3g.txt
./mptcp.sh topo_m01.py 01 > 01_tcp_3g.txt
./mptcp.sh topo_m02.py 02 > 02_tcp_3g.txt
./mptcp.sh topo_m05.py 05 > 05_tcp_3g.txt

