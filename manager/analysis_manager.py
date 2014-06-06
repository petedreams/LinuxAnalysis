#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# analysis_manager.py
#
#

import subprocess,paramiko,sys,os,time,hashlib

#victim
V_HOST = '192.168.228.240'
V_USER = 'iouser'
V_PASS = '8ik,.lo9'
REMOTE_PATH = "/home/iouser/malware"

#ホストOS
HOST = '192.168.100.60'
USER = 'ylab'
PASS = 'ylab920'
HOST_PCAP_PATH = '/home/ylab/MDA/data/out.pcap'
LOCAL_PCAP_PATH = '/home/iouser/analysis/out.pcap'

#SSH接続
def sshconnect(host,user,pswd):
    obj = paramiko.SSHClient()
    obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    obj.connect(host,username=user,password=pswd)
    return obj

#sftp転送
def filesftp(obj,localpath,remotepath):
    sftp = obj.open_sftp()
    sftp.put(localpath,remotepath)
    sftp.close()

if __name__ == '__main__':

    
    filepath = sys.argv[1]
    exetime = sys.argv[2]
    md5 = hashlib.md5(filepath).hexdigest()
    
    #iptables実行
    subprocess.Popen(["sudo","sh","iptables_manager.sh"]).wait()
    
    #victimにSSH,マルウェア転送
    vssh=sshconnect(V_HOST,V_USER,V_PASS)
    filesftp(vssh,filepath,REMOTE_PATH)
    
    #tcpdump実行
    #p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p=subprocess.Popen(['tcpdump','-i','eth1','not','host','192.168.228.1','-w',LOCAL_PCAP_PATH])
    
    #検体実行
    vssh.exec_command('chmod +x '+REMOTE_PATH)
    vssh.exec_command(REMOTE_PATH)
    
    time.sleep(int(exetime))
    p.terminate()
    vssh.close()

    #ホストにSSH,pcap転送
    hssh=sshconnect(HOST,USER,PASS)
    filesftp(hssh,LOCAL_PCAP_PATH,HOST_PCAP_PATH)
