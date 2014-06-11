#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## make_result.py SHA256 starttime exetime
##

import subprocess,sys,os

IN_PCAP = '/home/ylab/MDA/data/out.pcap'
RESULT_DIR = '/home/ylab/MDA/data/sandbox_result/'

sha = sys.argv[1]
starttime = sys.argv[2]
exetime = sys.argv[3]

if(not os.path.exists(RESULT_DIR+sha)):
    subprocess.call(['mkdir',RESULT_DIR+sha])
#else:
#    dir_num = int(max(os.listdir(RESULT_DIR+sha)))+1
#    sav_dir=RESULT_DIR+sha+'/'+str(dir_num)
    
sav_dir=RESULT_DIR+sha+'/'+starttime+'__sec-'+exetime
subprocess.call(['mkdir',sav_dir])
subprocess.call(['mv',IN_PCAP,sav_dir+'/'+sha+'.pcap'])

