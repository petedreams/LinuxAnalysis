#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# send_darllozpacket.py
#
#

from scapy.all import *
import random
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

conf.iface='vboxnet0'
#IP_DST='94.2.172.225'
#IP_DST='173.194.117.152'
IP_DST='192.168.56.101'

#RSTパケットを送信しない
#rule = "iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 192.168.56.101 -j DROP"
#os.system(rule)

#count = 1

#os.system("sudo tcpdump -i vboxnet0 host 192.168.56.1 -w test%s.pcap")%count

SP = random.randint(49152,65535) # srcport
SEQ = random.randint(0,4294967295) # sequence number

#syn送信
packet_syn = IP(dst=IP_DST)/TCP(sport=4000,dport=80,seq=10000,ack=20000)/Raw(load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
send(packet_syn,iface='vboxnet0')

#ack送信
#my_ack = packet_synack.seq + 1
#packet_ack = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,flags='A',seq=SEQ+1,ack=my_ack)
#send(packet_ack)

#data送信
#packet_data = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,flags='PA',seq=SEQ+1,ack=my_ack)/Raw(load=DATA)
#send(packet_data)

#count += 1

#os.system("killall tcpdump")%count
#ルール消去
#rule2 = "iptables -D OUTPUT -p tcp --tcp-flags RST RST -s 192.168.56.101 -j DROP"
#os.system(rule2)
