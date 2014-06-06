#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## 実行方法 "./analysis.py 検体パス 実行時間"
##

import subprocess,paramiko,sys,time

HOST = '192.168.100.50'
USER = 'iouser'
PASS = '8ik,.lo9'

try:
    filepath = sys.argv[1]
    time = sys.argv[2]
except:
    print "./analysis [検体パス(managerの)] [実行時間]"

#vm起動
subprocess.Popen(["VBoxManage","controlvm","guest-ubuntu10.04","poweroff"]).wait()
subprocess.Popen(["VBoxManage","snapshot","guest-ubuntu10.04","restore","GUEST"]).wait()
subprocess.call(["VBoxManage","startvm","guest-ubuntu10.04"])

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST,username=USER,password=PASS)
command = "echo koidekun |sudo -S ./analysis_manager.py %s %s" % (time,filepath)
ssh.exec_command(command)
ssh.close()


#強制終了
count = time + 30

print "強制終了 は Hit Ctrl-C"
try:
    for i in range(0,count):
        sleep(1) 
    print('正常終了しました。')
except KeyboardInterrupt:
    raw_input('終了します Hit Enter:')
    print('強制終了しました。')
