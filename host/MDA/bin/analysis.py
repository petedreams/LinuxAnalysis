#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## ~/MDA/bin/analysis.py
## 実行方法 "./analysis.py [検体パス(manager内)] [実行時間(秒)]"
## 検体パスの子ディレクトリは解析不可能
##

import subprocess,paramiko,sys,time,os

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

def analysis(malware_path,exetime,ssh):

    #vm終了・SS復元・起動
    subprocess.Popen(["VBoxManage","controlvm","guest-ubuntu10.04","poweroff"]).wait()
    subprocess.Popen(["VBoxManage","snapshot","guest-ubuntu10.04","restore","GUEST"]).wait()
    subprocess.call(["VBoxManage","startvm","guest-ubuntu10.04"])

    command = "echo 8ik,.lo9 |sudo -S "+SCRIPT_PATH+" %s %s" % (malware_path,exetime)
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

if __name__ == '__main__':

    try:
        filepath = sys.argv[1]
        exetime = sys.argv[2]
    except:
        print "./analysis [検体パス(manager内)] [実行時間(秒)]"
    
    #SSHでマネージャ接続
    ssh=sshconnect(HOST,USER,PASS)

    #検体パス内の検体を絶対パスを取得
    stdin, stdout, stderr = ssh.exec_command('find `pwd `cd '+filepath+'`` -type f -maxdepth 1 -mindepth 1| grep -v "\/\."')
    malware_path = []#検体絶対パス
    for l in stdout:
        malware_path.append(l.strip('\n'))
    malware_num = len(malware_path)#検体数

    print "解析中..."
    for m in malware_path:
        print os.path.basename(m)
        analysis(m,exetime,ssh)

    ssh.close()
