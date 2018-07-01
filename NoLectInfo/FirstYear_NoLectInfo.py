import time, os
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import mysql.connector

# 「name」を名前に持つボタンをクリックする関数
def buttonclick(name):
    button = driver.find_element_by_name(name)
    button.click()

try:
    # ウェブドライバー起動
    options = ChromeOptions()
    # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
    options.add_argument('--headless')
    # ChromeのWebDriverオブジェクトを作成する。
    driver = Chrome(options = options, executable_path = os.path.abspath(r'.\webscrapying') + r'\chromedriver.exe')
    driver.get('http://inform.academic.hokudai.ac.jp/webinfo/p/SerchInfo.aspx?mode=cancel')
    time.sleep(5)
    # 目標のページに移動
    buttonclick('btnSerch')
    time.sleep(5)

    # 最終的にデータベースのテーブルとなる配列
    data_table = []
    while True: 
        # HTMLソースをbeautifulsoup固有のオブジェクトとして格納
        source = driver.page_source
        bsObj = BeautifulSoup(source, 'lxml')
        # データの選別
        table = bsObj.findAll("table")[2]
        rows = table.findAll("tr")
        specific_rows = rows[1:-1]

        # データ整理
        for row in specific_rows:
            # 最終的にデータベースのレコードとなる配列
            data_record = []
            for cell in row.findAll("td"):
                cellstr = str(cell)
                # 細分したデータに<br/>が含まれていた場合の例外処理
                if '<br/>' in cellstr:
                    cellspbr = cellstr.split("<br/>")
                    cellex = [""] * 4
                    for cell, i in zip(cellspbr, range(4)):
                        cellbso = BeautifulSoup(cell, "lxml")
                        celllet = cellbso.get_text()
                        cellex[i] = celllet
                    el1 = cellex[1]
                    el2 = cellex[2]
                    cellex[1] = el2
                    cellex[2] = el1
                    if ',' in cellex[0]:
                        cellex2 = cellex[0].split(",")
                        cellex[0] = cellex2[0]
                        cellex[1] = cellex2[1]
                    if ',' in cellex[2]:
                        cellex3 = cellex[2].split(",")
                        cellex[2] = cellex3[0]
                        cellex[3] = cellex3[1]
                    data_record.extend(cellex)
                # 問題がなければそのままdata_record配列の一要素として格納
                else: 
                    cellbso = BeautifulSoup(cellstr, "lxml")
                    celllet = cellbso.get_text()
                    data_record.append(celllet)
            del data_record[10]
            del data_record[11]
            data_table.append(data_record)
        
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