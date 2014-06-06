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
SCRIPT_PATH  = '/home/iouser/analysis/analysis_manager.py'

def sshconnect(host,user,pswd):
    obj = paramiko.SSHClient()
    obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    obj.connect(host,username=user,password=pswd)
    return obj

if __name__ == '__main__':

    try:
        filepath = sys.argv[1]
        exetime = sys.argv[2]
    except:
        print "./analysis [検体パス(managerの)] [実行時間]"
    
    #vm終了・SS復元・起動
    subprocess.Popen(["VBoxManage","controlvm","guest-ubuntu10.04","poweroff"]).wait()
    subprocess.Popen(["VBoxManage","snapshot","guest-ubuntu10.04","restore","GUEST"]).wait()
    subprocess.call(["VBoxManage","startvm","guest-ubuntu10.04"])
    
    #guestのネット接続待ち
    time.sleep(10)

    #SSHでマネージャ接続
    ssh=sshconnect(HOST,USER,PASS)
    command = "echo 8ik,.lo9 |sudo -S "+SCRIPT_PATH+" %s %s" % (filepath,exetime)
    ssh.exec_command(command)
    
    #Ctrl-Cで強制終了 count秒で正常終了
    count = int(exetime) + 30
    
    print "強制終了 は Hit Ctrl-C"
    try:
        for i in range(0,count):
            time.sleep(1) 
        print('正常終了しました。')
    except KeyboardInterrupt:
        raw_input('終了します Hit Enter:')
    #
    #   ここで終了処理
    #
        print('強制終了しました。')
    
    ssh.close()
