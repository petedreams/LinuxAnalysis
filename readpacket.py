#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os,sys,dpkt,socket,binascii,string,re, operator,socket,datetime,time,struct
def header(file):

    f= open(file)
    pcap = dpkt.pcap.Reader(f)

    for ts,buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            continue

        if type(eth.data) == dpkt.ip.IP:
            ip = eth.data
            src_addr=socket.inet_ntoa(ip.src)
            dst_addr=socket.inet_ntoa(ip.dst)

            if type(ip.data) == dpkt.tcp.TCP:
                tcp = ip.data
                if tcp.flags == 24:
                    if len(tcp.data) < 8:
                        print binascii.hexlify(tcp.data)

if __name__ == '__main__':
    filename = sys.argv[1]
    if "/" in filename:
        infile =  filename[filename.rindex('/')+1:]
    else :
        infile = filename
    header(filename)
