#!/bin/bash

# Exit on any failure
set -e

# Check for uninitialized variables
set -o nounset

ctrlc() {
	killall -9 python
	mn -c
	exit
}

trap ctrlc SIGINT

start=`date`
exptid=`date +%b%d-%H:%M`
rootdir=parkinglot-$exptid
bw=10

# Note: you need to make sure you report the results
# for the correct port!
# In this example, we are assuming that each
# client is connected to port 2 on its switch.

for n in 1; do
    dir=$rootdir/n$n
<<<<<<< HEAD
    python topo_m01_noeth.py --bw $bw \
=======
    python topo_m005.py --bw $bw \
>>>>>>> 24862cb822ee0958605e82ac39e9f4b82bafe3a3
        --dir $dir \
        -t 60 \
        -n $n
    python util/plot_rate.py --rx \
        --maxy $bw \
        --xlabel 'Time (s)' \
        --ylabel 'Rate (Mbps)' \
        -i 's.*-eth2' \
        -f $dir/bwm.txt \
        -o $dir/rate.png
    python util/plot_tcpprobe.py \
        -f $dir/tcp_probe.txt \
        -o $dir/cwnd.png
done

echo "Started at" $start
echo "Ended at" `date`
echo "Output saved to $rootdir"
