import time, os
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import mysql.connector

# 「name」を名前に持つボタンをクリックする関数
def buttonclick(name):
    button = driver.find_element_by_name(name)
    button.click()

try:
    # ＜データの取得＞
    # ウェブドライバー起動
    options = ChromeOptions()
    options.add_argument('--headless')
    driver = Chrome(options = options, executable_path = os.path.abspath(r'.\webscrapying') + r'\chromedriver.exe')
    driver.get('http://inform.academic.hokudai.ac.jp/webinfo/p/SerchInfo.aspx?mode=cancel')
    time.sleep(5)
    # 目標のページに移動
    buttonclick('btnSerch')
    time.sleep(5)

    # 最終的にデータベースのテーブルとなる配列
    all_rows = []
    while True: 
        # HTMLソースをbeautifulsoup固有のオブジェクトとして格納
        source = driver.page_source
        bsObj = BeautifulSoup(source, 'lxml')
        # データの選別
        table = bsObj.findAll("table")[2]
        rows = table.findAll("tr")
        specific_rows = rows[1:-1]

        # データ格納
        all_rows.append(specific_rows)

        # ページ遷移の処理
        if 'value="次へ"' in source:
            if '<span>1</span>' in source:
                buttonclick('rdlGrid$gridList$ctl14$ctl01')
            else:
                buttonclick('rdlGrid$gridList$ctl14$ctl03')
            time.sleep(5)
        else:
            break

    # ドライバー切断
    driver.quit()
    
    # ＜データ整理＞
    # all_rowsを要素ごとに分割し、全てを一つの配列にまとめたdata_tableを作成する
    data_table = []
    for rows in all_rows:
        for row in rows:
            data_record = []
            for element in row.findAll("td"):
                element_str = str(element)
                # 細分したデータに<br/>が含まれていた場合の例外処理
                if '<br/>' in element_str:
                    element_spbr = element_str.split("<br/>")
                    element_ex = [""] * 4
                    for spc_element, i in zip(element_spbr, range(4)):
                        element_bso = BeautifulSoup(spc_element, "lxml")
                        element_let = element_bso.get_text()
                        element_ex[i] = element_let
                    el1 = element_ex[1]
                    el2 = element_ex[2]
                    element_ex[1] = el2
                    element_ex[2] = el1
                    if ',' in element_ex[0]:
                        element_ex2 = element_ex[0].split(",")
                        element_ex[0] = element_ex2[0]
                        element_ex[1] = element_ex2[1]
                    if ',' in element_ex[2]:
                        element_ex3 = element_ex[2].split(",")
                        element_ex[2] = element_ex3[0]
                        element_ex[3] = element_ex3[1]
                    data_record.extend(element_ex)
                # 問題がなければそのままdata_record配列の一要素として格納
                else: 
                    element_bso = BeautifulSoup(element_str, "lxml")
                    element_let = element_bso.get_text()
                    data_record.append(element_let)
            del data_record[13]
            data_table.append(data_record)
    
    # ＜データベースへの格納＞
    # データベース接続
    con = mysql.connector.connect(
        host='127.0.0.1',
        db='hokudai_app',
        user='writer',
        passwd='write'
    )

    """
    「hokudai_app」データベースに「firstyear_nolectinfo」テーブルがある場合はそのまま
    なければ
    CREATE TABLE firstyear_nolectinfo (休講日 VARCHAR(10), 曜日・時限 VARCHAR(2), 曜日・時限2 VARCHAR(2), Day・Period  VARCHAR(4), Day・Period2  VARCHAR(4), 科目名 VARCHAR(50), 講義題目 VARCHAR(100), CourseTitle VARCHAR(50), CourseSubTitle VARCHAR(100), 教員名 VARCHAR(50), Instructor VARCHAR(50));
    で作成
    """

    # 辞書型カーソル取得
    cur = con.cursor(dictionary=True)
    # データの削除
    cur.execute('delete from firstyear_nolectinfo')
    # データの入力
    cur.executemany("insert into firstyear_nolectinfo (休講日, 曜日・時限, 曜日・時限2, Day・Period, Day・Period2, 科目名, 講義題目, CourseTitle, CourseSubTitle, 教員名, Instructor) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data_table)
    # コミットして変更を確定
    con.commit()

except:
    # どこかでエラーが発生した場合、データを削除し「Error」を入力しておく
    # データベース接続
    con = mysql.connector.connect(
        host='127.0.0.1',
        db='hokudai_app',
        user='writer',
        passwd='write'
    )
    # カーソル取得
    cur = con.cursor()
    # データの削除
    cur.execute('delete from firstyear_nolectinfo')
    # エラーメッセージ表示
    print('Error!!')

finally:    
    # データベース切断
    cur.close()
    con.close()
    print('Done')