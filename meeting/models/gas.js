// GoogleAppsScript

// 各アイテム作成
function createItem(form, title, type, help, required) {
    if (type == 'ラジオボタン') {
        return form
            .addMultipleChoiceItem()
            .setTitle(title)
            .setHelpText(help)
            .setRequired(required);
    } else if (type == 'チェックボックス') {
        return form
            .addCheckboxItem()
            .setTitle(title)
            .setHelpText(help)
            .setRequired(required);
    } else if (type == 'プルダウン') {
        return form
            .addListItem()
            .setTitle(title)
            .setHelpText(help)
            .setRequired(required);
    } else if (type == '記述式') {
        return form
            .addTextItem()
            .setTitle(title)
            .setHelpText(help)
            .setRequired(required);
    } else if (type == '日付') {
        return form
            .addDateItem()
            .setTitle(title)
            .setHelpText(help)
            .setRequired(required);
    }
}

// フォーム内容&回答削除
function clearForm(form) {
    // フォーム内の質問をすべて削除
    var items = form.getItems();
    while (items.length > 0) {
        form.deleteItem(items[0]);
        items = form.getItems(); // ループのたびに items を再取得して残りのアイテムを確認
    }
    // フォームの回答を削除
    form.deleteAllResponses();

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    //シート名は置き換えてください。
    var sh = ss.getSheetByName('回答');
    //シートのすべてをクリアする
    sh.clear();
}

// メイン関数
function main() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    // // 概要シートからフォームのIDを取得する
    const formId = ss.getSheetByName('概要').getRange('B6').getValue();
    var form = FormApp.openById(formId);

    // フォーム内の質問と回答をクリア
    clearForm(form);

    // ここにフォームの編集コードを追加
    const formTitle = ss.getSheetByName('概要').getRange('B1').getValue();
    const formDescription = ss.getSheetByName('概要').getRange('B2').getValue();

    form.setTitle(formTitle);
    form.setDescription(formDescription);

    // 質問シートの値を取得
    const q_sheet = ss.getSheetByName('質問');
    const rows = q_sheet.getLastRow();
    const columns = q_sheet.getLastColumn();
    const q_values = q_sheet.getRange(1, 1, rows, columns).getValues();

    // パスワード作成
    const p_sheet = ss.getSheetByName('概要');
    var title = 'パスワード';
    var help = '今回のパスワードを入力してください';
    var password = p_sheet.getRange('B8').getValue();
    var pass = FormApp.createTextValidation();
    var valid = pass
        .requireTextMatchesPattern(password)
        .setHelpText('パスワードが違います')
        .build();
    createItem(form, title, '記述式', help, true).setValidation(valid);

    form.addPageBreakItem()
        .setTitle('議題')
        .setHelpText('以下の議題に回答してください．');

    // アイテムを追加する
    for (let i = 1; i < rows - 1; i++) {
        const title = q_values[i + 1][0];
        const type = q_values[i + 1][1];
        const help = q_values[i + 1][2];
        var required = q_values[i + 1][3];
        if (required != true) required = false;

        let choiceVals = [];
        for (let j = 2; j < columns - 2; j++) {
            const choiceVal = q_values[i + 1][j + 2];
            if (choiceVal == '') {
                break;
            } else {
                choiceVals.push(choiceVal);
            }
        }

        const item = createItem(form, title, type, help, required);

        if (
            choiceVals.length != 0 &&
            (type == 'ラジオボタン' ||
                type == 'チェックボックス' ||
                type == 'プルダウン')
        ) {
            item.setChoiceValues(choiceVals);
        }
    }
    // 初回フォームURL取得用
    ss.getSheetByName('概要').getRange('B4').setValue(form.getEditUrl());
    ss.getSheetByName('概要').getRange('B5').setValue(form.getPublishedUrl());
}

function onChange(e) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('概要');
    var lastB10Value = sheet.getRange('C8').getValue();
    var currentB10Value = sheet.getRange('B8').getValue();
    if (currentB10Value !== lastB10Value) {
        sheet.getRange('C8').setValue(currentB10Value);
        scriptProperties.setProperty('lastB10Value', currentB10Value);
        main();
    }
}
