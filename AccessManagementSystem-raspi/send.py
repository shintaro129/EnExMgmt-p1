#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import
import requests
import json
import collections as collect
import datetime

#送り先のURLを記述したファイル
URLFILEPATH = "privacy/URLFILE"
#送り先のURLを読み込み
URLfile = open(URLFILEPATH,'r')
URL = URLfile.readline()
URLfile.close()

#GSSへデータ送信
def postData(data,size):
	#当日分のデータがなければ
	if(data is None):
		print("params is empty")
		return False
	#データをJson形式に変換
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

	#GSSへ送信
	response = requests.post(URL, data=json.dumps(datedata), headers=headers)

	#GSSからの返答
	if(response.status_code == 200 and response.text == "connect"):
		print(response.text)
		print("post success!")
		return True
	print(response.text)
	print("post failed")
	return False

if __name__ == "__main__":
	#日付を取得
	day = "".join(list(map(str,str(datetime.datetime.now())))[:10])
	#当日の入退室記録が書き込まれたファイル
	LOG = "log/"+day+".dat"

	#当日分のログデータを取得整形。
	data = list()
	LOGDATA = open(LOG, 'r')
	for line in LOGDATA.readlines():
		log = list(map(str,line.rstrip().split(",")))
		print(log)
		data.append(log)
	#GSSへデータ送信
	postData(data,len(data))
