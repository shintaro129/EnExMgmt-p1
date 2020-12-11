#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import
import os
import sys
import time
import datetime
import nfc
import binascii
from playsound import playsound
from multiprocessing import Process,Queue
sys.path.insert(1, os.path.split(sys.path[0])[0])

#キャッシュ用のファイル
CACHE = "EnterID.dat"
#入退室音再生起動用キュー
soundplay = Queue()

#記録用ファイルに書き込み
def logRecord(scan_time,check,scanID):
    #記録用ファイル
    LOGFILE = "log/"+scan_time[:10]+".dat"
    #記録内容
    log = scan_time+","+str(check)+","+scanID+"\n"
    
    #記録用ファイルへ書き込み
    wlog = open(LOGFILE,"a")
    wlog.write(log)
    wlog.close()	

#入退室判定
def checkRecord(scanID):
    #キャッシュ読み取り
    rlog = open(CACHE,"r")
    Enterlog = set(map(str,rlog.readline().split(",")))
    rlog.close()

    #入退室判定(True:入室,False:退室)
    if(scanID in Enterlog):
        Enterlog.remove(scanID)
        checkEntered = False
    else:
        Enterlog.add(scanID)
        checkEntered = True

    #キャッシュ更新
    rlog = open(CACHE,"w")
    rlog.writelines(",".join(Enterlog))
    rlog.close()

    return checkEntered

#カード読み取り
def connected(tag):
    #読み取り可能なカードかを判定
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        #読み取り開始
        try:
            #現在時刻取得
            date_time = list(map(str,str(datetime.datetime.now())))

            #カード情報読み取り
            service_code = 0x09CB
            sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
            bc = nfc.tag.tt3.BlockCode(0,service=0)
            scandata = tag.read_without_encryption([sc],[bc])

            #裏で動いている入退室音再生を起動
            soundplay.put(0)

            #書き込み用データ整形
            scan_time = "".join(date_time[:19])
            scanID = scandata[2:10].decode("utf-8")
            check = checkRecord(scanID)

            #記録用ファイルに書き込み
            logRecord(scan_time,check,scanID)
            print(scan_time,check,scanID)

        #なにかエラーが起こった時
        except Exception as e:
            print("error: %s" % e)
    #読み取り可能なカードではないとき
    else:
        print("error: tag isn't Type3Tag")

    return True	

#入退室音再生用 (並列で動かす)
def play(soundplay):
    sound = "sound/sound.mp3"
    while(True):
        #queueにputされたときに音を鳴らす
        queue = soundplay.get()
        if(queue == 0):
            playsound(sound)
        
#並列処理用のプロセス
p_play = Process(target=play,args=(soundplay,))

#main
if __name__ == "__main__":
    #接続するデバイス情報
    clf = nfc.ContactlessFrontend('usb:001:003')

    #並列処理開始
    p_play.start()

    #MainLoop
    while(True):
        clf.connect(rdwr={'on-connect': connected})
        time.sleep(3)