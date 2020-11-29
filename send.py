#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import collections as collect
import datetime
day = "".join(list(map(str,str(datetime.datetime.now())))[:10])
URLFILEPATH = "/home/test/privacy/URLFILE"
LOG = "/home/test/log/log"+day+".dat"

URLfile = open(URLFILEPATH,'r')
URL = URLfile.readline()
URLfile.close()

# 暗号化するとしたらここ
def postData(data,size):
    if(data is None):
        print("params is empty")
        return False
    datedata = collect.OrderedDict()
    send = list()
    for i in range(size):
        senddata = collect.OrderedDict()

        datetime = data[i][0]
        senddata["time"] = datetime[11:]
        if(data[i][1] == "True"):
            senddata["check"] = "入室"
        elif(data[i][1] == "False"):
            senddata["check"] = "退室"
        else:
            return False
        senddata["ID"] = data[i][2]
        send.append(senddata)
    datedata["date"] = datetime[:10]
    datedata["info"] = send
    print("{}".format(json.dumps(datedata,indent=4)))

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(URL, data=json.dumps(datedata), headers=headers)
    if(response.status_code == 200 and response.text == "connect"):
        print(response.text)
        print("post success!")
        return True
    print(response.text)
    print("post failed")
    return False

if __name__ == "__main__":       
    i = 0
    data = []
    fp = open(LOG, 'r')
    for line in fp.readlines():
        log = list(map(str,line.rstrip().split(",")))
        print(log)
        data.append(log)
    postData(data,len(data))
