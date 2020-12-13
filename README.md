# EnExMgmt-p1
## 概要
大阪電気通信大学情報通信工学部でのハッカソン提出作品。
 
ハッカソンのお題は、研究室の入退室管理。
 
 
## チームメンバー
殿山,福田,前山,豫城,渡邊（50音順,敬称略）
 
 
## 処理の流れ
1.学生証から学籍番号を取得
 
2.入室ログを確認し、入室者か退室者かを識別
 
3.{学籍番号,読み取った日時,入室or退室}を(その日の日付.dat)に記録
 
4.1~3までの工程が成功した際に、成功音を鳴らす
 
 
## 記録用Googleスプレッドシート（ダウンロードしてご利用ください）
[Googleスプレッドシート](https://docs.google.com/spreadsheets/d/1bU7MB-2ilCXyXzAKiwMG6wuOpP0hoI-oNDFW0h_naJw/edit?usp=sharing)
 
 
## プレゼン動画(OECUでのみ閲覧可能)
https://drive.google.com/file/d/1iLeQqFqhRwqwDHbqyT9RK_AQpUWrt29U/view?usp=sharing
 
## セットアップ【使い方】
### ラズパイの設定
#想定OS
GUIが使えるもの(GASへのアクセスにアカウント認証が必要みたいです。)
 
#環境セットアップ
aptを最新版にしてください。(この時にGASの設定をするとスムーズかも)
 
pythonの環境を構築します。
```
sudo apt install python3-pip
pip3 install nfcpy
pip3 install soundplay
pip3 install requests
```
 
Pythonをクローンして、設置。
```
git clone https://github.com/shintaro129/EnExMgmt-p1/AccessManagementSystem-raspi.git
```
 
“privacy”フォルダ内のURLFILEにGoogleAppScripts(以下、GAS)で取得したfetchURLを記述する。
(`https://script.google.com/macros/s/~~~/exec`のように「""」や「''」等の修飾文字は付けなくて結構です。)
 
ntpの設定
```
タイムゾーンを Asia/Tokyo に設定
timedatectl set-timezone Asia/Tokyo
 
sudo apt install ntpdate
sudo ntpdate -u ntp.nict.jp
```
```
sudo nano /usr/bin/checkdate.sh
#!/bin/sh
/usr/sbin/ntpdate ntp.jst.mfeed.ad.jp
sudo chmod 700 /usr/bin/checkdate.sh
```
cron設定
```
crontab -e
```
```
45 23 * * * /which python3の絶対パス/python3 /絶対パス/send.py
55 23 * * * sh /usr/bin/checkdate.sh
56 23 * * * sudo /sbin/reboot
```
 
cronの起動と確認
```
sudo systemctl start cron.service
sudo systemctl enable cron.service
sudo systemctl status cron.service
```
 
再起動時、起動するファイルを指定
```
sudo chmod u+x /etc/rc.local
sudo nano /etc/rc.local
/which python3の絶対パス/python3 /絶対パス/scan.py
```
 
### GASの設定
 
「ウェブアプリケーションとして導入」から「`Project version:`」をNewにする。
(その際、「`Execute the app as:`」を「`Me`」に、「`Who has access to the app:`」を「`anyone, even anonymous`」にしておく。)
 
GASで取得したCurrent web app URLをラズパイ側に書き込んでください。
 
Main.gsのsendmail,sendslackのコメントアウトを外し、send.gsの該当部分の必要情報(mailなら送信先アドレス,slackならWebhook URL)を記述すると送られます。
 
#### SlackのWebhook URLの取得
Slackを開き「App」から「Incoming WebHooks」を追加。
「Slackに追加」をクリック。チャンネルを選択。
「Incoming Webhookインテグレーションの追加」をクリック。
Webhook URLが表示される。
 
参考サイト：
[GAS超入門⑤ - Slackに通知してみよう](https://note.com/skipla/n/na3f7f9cd9b7d)
 
 
### 列挙ツールの使いかた
python3環境に`requests`をインストールする。
`AccessManagementSystem-contact`内の`view_contactperson.py` をダウンロードして、設置したフォルダで、
```
python3 view_contactperson.py >> [記録したいファイル]
```
を実行する。
記録したいファイルに接触した可能性がある人が列挙されます。
 
 
## 参考にさせていただいたサイト
### 学籍番号の読み取り
[Raspberry Pi 3にPaSoRiを接続してSuicaカードをダンプする](https://tomosoft.jp/design/?p=8288)
 
[nfcpyを使って学生証から学籍番号を読み取る](https://aizu-vr.hatenablog.com/entry/2019/08/02/nfcpy%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E5%AD%A6%E7%94%9F%E8%A8%BC%E3%81%8B%E3%82%89%E5%AD%A6%E7%B1%8D%E7%95%AA%E5%8F%B7%E3%82%92%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8B)
 
[nfc公式ドキュメント:Type 3 tag](https://nfcpy.readthedocs.io/en/stable-0.11/modules/tag.html#module-nfc.tag.tt3)
 
[nfcpy で複数の System Code を持つ NFC タグを扱う方法](https://uchan.hateblo.jp/entry/2016/11/18/190237)
 
[FeliCa から情報を吸い出してみる - FeliCaの仕様編](https://qiita.com/YasuakiNakazawa/items/3109df682af2a7032f8d)
 
 
## 音楽
[くらげ工匠](http://www.kurage-kosho.info/index.html)
