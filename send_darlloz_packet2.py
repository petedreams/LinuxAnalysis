#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# send_darllozpacket.py
#
#

from scapy.all import *
import random,subprocess,time

IP_DST='192.168.56.112'

DATA=['\x00\x02\x00\x15','\x01\x01\x00\x20','\x05','\x01\x02\x00\x15','\x00\x01\x00\x20','\x01\x00\x05','\x01\x02\x00\x20','\x01\x02\x00\x15','\x00\x00\x00\x20']
#DATA=["hello"]
#DATA=["\x01"]

#RSTパケットを送信しない
rule = "iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 192.168.56.1 -j DROP"
os.system(rule)

count = 1
for d in DATA:
    
    p=subprocess.Popen(["tcpdump","-i","vboxnet0","host","192.168.56.1","-w","test"+str(count)+".pcap"])
    #p=subprocess.Popen(["tcpdump","-nni","vboxnet0","host","192.168.56.1"])
    SP = random.randint(49152,65535) # srcport
    SEQ = random.randint(0,4294967295) # sequence number
    
    #syn送信
    packet_syn = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,seq=SEQ)
    packet_synack = sr1(packet_syn)
    
    #ack送信
    my_ack = packet_synack.seq + 1
    packet_ack = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,flags='A',seq=SEQ+1,ack=my_ack)
    send(packet_ack)
    
    #data送信
    packet_data = IP(dst=IP_DST)/TCP(sport=SP,dport=58455,flags='PA',seq=SEQ+1,ack=my_ack)/Raw(load=d)
    send(packet_data)
    
    time.sleep(5)
    p.terminate()

    count += 1
    #time.sleep(5)

#ルール消去
rule2 = "iptables -D OUTPUT -p tcp --tcp-flags RST RST -s 192.168.56.1 -j DROP"
os.system(rule2)
