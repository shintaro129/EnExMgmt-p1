#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
sys.path.insert(1, os.path.split(sys.path[0])[0])
import binascii
import nfc
import datetime
import json
import collections as cl
import pyaudio
import wave


CACHE = "EnterID.dat"

def logRecord(scantime,check,scanID):
    LOGFILE = scantime[:10]+".dat"
    wlog = open(LOGFILE,"a")
    log = scantime+","+str(check)+","+scanID+"\n"
    wlog.write(log)
    wlog.close()
    

def checkRecord(scanID):
    rlog = open(CACHE,"r")
    Enterlog = set(map(str,rlog.readline().split(",")))
    rlog.close()

    checkEntered = bool()
    if(scanID in Enterlog):
        Enterlog.remove(scanID)
        checkEntered = False
    else:
        Enterlog.add(scanID)
        checkEntered = True

    rlog = open(CACHE,"w")
    rlog.writelines(",".join(Enterlog))
    rlog.close()

    return checkEntered


def res_audio(audio_file):
    CHUNK = 44100
    audio = pyaudio.PyAudio()
    wf = wave.open(audio_file, 'rb')
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
    data = wf.readframes(CHUNK)

    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.close()
    audio.terminate()


def connected(tag):
  if isinstance(tag, nfc.tag.tt3.Type3Tag):
    try:
        service_code = 0x09CB
        scantime = "".join(list(map(str,str(datetime.datetime.now())))[:19])
        sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
        bc = nfc.tag.tt3.BlockCode(0,service=0)
        data = tag.read_without_encryption([sc],[bc])
        scanID = data[2:10].decode("utf-8")
        check = checkRecord(scanID)
        print(scantime,check,scanID)
        logRecord(scantime,check,scanID)
        #ここで音声鳴らす
        res_audio("se_maoudamashii_chime13.wav")
        if(check):
            #入室
            print("Enter")
        else:
            #退室
            print("Exit")


    except Exception as e:
      print("error: %s" % e)
  else:
    print("error: tag isn't Type3Tag")

if __name__ == "__main__":
    clf = nfc.ContactlessFrontend('usb:054c:06c3')
    while True:
        clf.connect(rdwr={'on-connect': connected})
        time.sleep(3)
