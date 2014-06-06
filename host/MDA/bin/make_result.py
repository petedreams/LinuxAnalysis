#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## make_result.py
##

import subprocess,sys,os

IN_PCAP = '/home/ylab/MDA/data/out.pcap'
RESULT_DIR = '/home/ylab/MDA/data/sandbox_result/'

md5 = sys.argv[1]

if(not os.path.exists(RESULT_DIR+md5)):
    subprocess.call(['mkdir',RESULT_DIR+md5])
    sav_dir=RESULT_DIR+md5+'/1'
else:
    dir_num = int(max(os.listdir(RESULT_DIR+md5)))+1
    sav_dir=RESULT_DIR+md5+'/'+str(dir_num)
    
subprocess.call(['mkdir',sav_dir])
subprocess.call(['mv',IN_PCAP,sav_dir+'/'+md5+'.pcap'])

