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
[Googleスプレッドシート](https://docs.google.com/spreadsheets/d/1_2pXymswEs1JbpSYCkQ7J-i6-daQV1kEKH--eJBHpRM/edit?usp=sharing)


## プレゼン動画(OECUでのみ閲覧可能)
https://drive.google.com/file/d/1iLeQqFqhRwqwDHbqyT9RK_AQpUWrt29U/view?usp=sharing

## 参考にさせていただいたサイト
### 学籍番号の読み取り
[Raspberry Pi 3にPaSoRiを接続してSuicaカードをダンプする](https://tomosoft.jp/design/?p=8288)

[nfcpyを使って学生証から学籍番号を読み取る](https://aizu-vr.hatenablog.com/entry/2019/08/02/nfcpy%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E5%AD%A6%E7%94%9F%E8%A8%BC%E3%81%8B%E3%82%89%E5%AD%A6%E7%B1%8D%E7%95%AA%E5%8F%B7%E3%82%92%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8B)

[nfc公式ドキュメント:Type 3 tag](https://nfcpy.readthedocs.io/en/stable-0.11/modules/tag.html#module-nfc.tag.tt3)

[nfcpy で複数の System Code を持つ NFC タグを扱う方法](https://uchan.hateblo.jp/entry/2016/11/18/190237)

[FeliCa から情報を吸い出してみる - FeliCaの仕様編](https://qiita.com/YasuakiNakazawa/items/3109df682af2a7032f8d)


## 音楽
[くらげ工匠](http://www.kurage-kosho.info/index.html)
