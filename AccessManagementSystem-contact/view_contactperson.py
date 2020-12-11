import requests

#アクセス先
fetchURL = ""

def postData():
    print("検索する人の学籍番号を入力してください。")
    serchperson = input()
    url = fetchURL+"?text="+serchperson
    r = requests.get(url)
    data = list(map(str,r.text.split(",")))
    for i in range(len(data)):
        print(data[i])    

if __name__ == "__main__":
    postData()