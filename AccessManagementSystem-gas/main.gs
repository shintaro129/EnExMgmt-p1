function main(dict_eem) {
  writing(dict_eem);
  let mainText = changeText(dict_eem.info);
  let title = dict_eem.date + "の入退室記録\n";
  //sendSlack(title, mainText);
  //sendMail(title, mainText);
}


function doPost(e) {
    let dict_eem = JSON.parse(e.postData.contents);
    main(dict_eem);
    return ContentService.createTextOutput('success');
}

function writing(dict_eem) {
    const sheet = SpreadsheetApp.getActive().getSheetByName('EEMLog');
    const today = dict_eem.date;
    let todayData = dict_eem.info;
    const size = Object.keys(todayData).length;
    for(var i = 0;i<size;i++){
      let time = todayData[i].time;
      let check = todayData[i].check;
      let ID = todayData[i].ID;
      sheet.appendRow([today,time,ID,check]);
    }
}
