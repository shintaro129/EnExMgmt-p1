#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import binascii
import time
import datetime
import json
import collections as cl
import wave
#---以下のものはpipでのインストールが必要です。
import nfc
from playsound import playsound

sys.path.insert(1, os.path.split(sys.path[0])[0])


#その日の入退室者ログ
def logRecord(scantime,check,scanID):
    #書き込むファイルを指定
    LOGFILE = "log/"+scantime[:10]+".dat"

    #file_open
    with open(LOGFILE, "a", encoding="utf-8") as alog:
        log = scantime+","+str(check)+","+scanID+"\n"
        alog.write(log)


#入退室判定
def checkRecord(scanID):
    CACHE = "EnterID.dat"
    checkEntered = bool()

    with open(CACHE, "r", encoding="utf-8")as rlog:
        Enterlog = set(map(str,rlog.readline().split(",")))

    if(scanID in Enterlog):
        Enterlog.remove(scanID)
        checkEntered = False
    else:
        Enterlog.add(scanID)
        checkEntered = True

    with open(CACHE, "w", encoding="utf-8")as wlog:
        wlog.writelines(",".join(Enterlog))

    return checkEntered


#レスポンス用に音を鳴らす
def res_audio(audio_file):
    playsound(audio_file)


#カード通信時の処理
def connected(tag):
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            #学籍番号が格納されている場所を指定
            service_code = 0x09CB
            
            #service_codeの場所から学籍番号のみを抽出。
            sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
            bc = nfc.tag.tt3.BlockCode(0,service=0)
            data = tag.read_without_encryption([sc],[bc])
            scanID = data[2:10].decode("utf-8")

            #打刻時間を取得
            scantime = "".join(list(map(str,str(datetime.datetime.now())))[:19])

            #入室か退室かの判定
            check = checkRecord(scanID)

            #その日の入退室者ログに記録
            logRecord(scantime,check,scanID)

            #入退室に合わせて、音を鳴らす
            if(check):
                #入室
                res_audio("se/se_maoudamashii_chime13.wav")
                print("Enter")
            else:
                #退室
                res_audio("se/se_maoudamashii_chime13.wav")
                print("Exit")
            print(scantime,check,scanID)
        except Exception as e:
                print("error: %s" % e)
    else:
        print("error: tag isn't Type3Tag")


if __name__ == "__main__":
    print("---program start---")
    clf = nfc.ContactlessFrontend('usb:054c:06c3')
    while True:
        print("---Scantable---")
        clf.connect(rdwr={'on-connect': connected})
        time.sleep(3)