function doPost(e) {
    let dict_eem = JSON.parse(e.postData.contents);
    writing(dict_eem);

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