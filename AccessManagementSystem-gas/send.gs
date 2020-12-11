//指定された日のデータのみを選択
function SelectTodayDate(){
  let d = new Date();
  const sheet = SpreadsheetApp.getActive().getSheetByName('todayLog');
  const lastRow = sheet.getLastRow();
  const year = d.getFullYear();
  const month = d.getMonth() + 1;
  const date = d.getDate();
  const inputDate = "=QUERY(EEMLog!A:D,\"select * where A like'" + year + "-" + month + "-" + date + "%'\",1)";
  sheet.getRange(1, 1, 1, 1).setFormula(inputDate);
  
  //get-script
  
  if(sheet.getRange(2, 1).isBlank()){
      return "今日は入退室者がいなかったようです。";
  }else{
    return sheet.getRange(2, 1, lastRow - 1, 3).getValues();
  }

}

//指定のメールアドレスへのデータ送信
function sendMail(sendData) {
  const recipient = 'test@example.com';
  const recipientName = '入退室管理app'; 
  const subject = '本日の入退室';
  
  GmailApp.sendEmail(recipient, subject, sendData);
}


//Slackへのデータ送信
function sendSlack(jsonSendData){
  const webHookUrl = "//slackのwebhookURL";
  
  let options =
      {
        "method" : "post",
        "contentType" : "application/json",
        "payload" : jsonSendData
      };
  
  
  UrlFetchApp.fetch(webHookUrl, options);
}