function changeText(todayData){
  let text = "時刻/学籍番号/入退室\n";
  let i = 0;
  const size = Object.keys(todayData).length;
  for(i = 0;i<size;i++){
    let time = todayData[i].time;
    let check = todayData[i].check;
    let ID = todayData[i].ID; 
    text += time + "/" + ID + "/" + check + "\n";
  }

  return text;
}


//指定のメールアドレスへのデータ送信
function sendMail(title, text) {
  const recipient = 'GP20A129@oecu.jp';
  const recipientName = '入退室管理app'; 
  const subject = title;
  
  GmailApp.sendEmail(recipient, subject, text);
}


//Slackへのデータ送信
function sendSlack(title, text){
  const webHookUrl = "https://hooks.slack.com/services/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";
  
  let payload = JSON.stringify({
    "text": title + text
  });
  
  let options = {
    "method" : "post",
    "contentType" : "application/json",
    "payload" : payload
  }
  UrlFetchApp.fetch(webHookUrl, options);
}
