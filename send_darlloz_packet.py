#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# send_darllozpacket.py
#
#

from scapy.all import *
import random

IP_DST='192.168.56.1'
DATA="\x00\x01\x00\x20"
#DATA="hello"
SP = random.randint(49152,65535) # srcport
SEQ = random.randint(0,4294967295) # sequence number

#RSTパケットを送信しない
rule = "iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 192.168.56.101 -d 192.168.56.1 -j DROP"
os.system(rule)

#syn送信
packet_syn = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,seq=SEQ)
packet_synack = sr1(packet_syn)
#print "______synack_____"
#packet_synack.show()

#ack送信
my_ack = packet_synack.seq + 1
packet_ack = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,flags='A',seq=SEQ+1,ack=my_ack)
send(packet_ack)

#data送信
packet_data = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,flags='PA',seq=SEQ+1,ack=my_ack)/Raw(load=DATA)
send(packet_data)


#data送信
packet_data = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,flags='PA',seq=SEQ+1,ack=my_ack)/Raw(load=DATA)
send(packet_data)

#ルール消去
rule2 = "iptables -D OUTPUT -p tcp --tcp-flags RST RST -s 192.168.56.101 -d 192.168.56.1 -j DROP"
os.system(rule2)