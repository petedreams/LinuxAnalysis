#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## 実行方法 "./analysis.py 検体パス 実行時間"
##

import subprocess,paramiko,sys,time

#manager
HOST = '192.168.100.50'
USER = 'iouser'
PASS = '8ik,.lo9'

try:
    filepath = sys.argv[1]
    time = sys.argv[2]
except:
    print "./analysis [検体パス(managerの)] [実行時間]"

#vm終了・SS復元・起動
subprocess.Popen(["VBoxManage","controlvm","guest-ubuntu10.04","poweroff"]).wait()
subprocess.Popen(["VBoxManage","snapshot","guest-ubuntu10.04","restore","GUEST"]).wait()
subprocess.call(["VBoxManage","startvm","guest-ubuntu10.04"])

#SSHでマネージャ接続
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST,username=USER,password=PASS)
command = "echo koidekun |sudo -S ./analysis_manager.py %s %s" % (time,filepath)
ssh.exec_command(command)

#Ctrl-Cで強制終了 count秒で正常終了
count = time + 30

print "強制終了 は Hit Ctrl-C"
try:
    for i in range(0,count):
        sleep(1) # could use a backward counter to be preeety :)
    print('正常終了しました。')
except KeyboardInterrupt:
    raw_input('終了します Hit Enter:')
#
#   ここで終了処理
#
   print('強制終了しました。')

ssh.close()
