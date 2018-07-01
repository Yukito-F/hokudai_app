from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector

try:
    #指定したURLのHTMLソースをbeautiful soup固有のオブジェクトとして格納、
    html = urlopen("https://www.eng.hokudai.ac.jp/lecinfo/")
    bsObj = BeautifulSoup(html, "lxml")

    # データの選別（最初のtbodyタブを選択)
    rows = bsObj.findAll("tbody")[0]

    # データの整理
    data_table = []
    for row in rows.findAll("tr"):
        data_record = []
        for cell in row.findAll("td"): 
            text = cell.get_text()
            data_record.append(text)
        data_table.append(data_record)

    # データベース接続
    con = mysql.connector.connect(
        host='127.0.0.1',
        db='hokudai_app',
        user='writer',
        passwd='write'
    )

    """
    「hokudai_app」データベースに「engineering_nolectinfo」テーブルがある場合はそのまま
    なければ
    CREATE TABLE engineering_nolectinfo (日付 VARCHAR(15), 講時 VARCHAR(2), 区分 VARCHAR(50), 講義科目名 VARCHAR(100), 担当 VARCHAR(50), 講義室 VARCHAR(50), 備考 VARCHAR(200), 更新 VARCHAR(17));
    で作成
    """

    # 辞書型カーソル取得
    cur = con.cursor(dictionary=True)
    # データの削除
    cur.execute('delete from engineering_nolectinfo')
    # データの入力
    cur.executemany("insert into engineering_nolectinfo (日付, 講時, 区分, 講義科目名, 担当, 講義室, 備考, 更新) values (%s, %s, %s, %s, %s, %s, %s, %s)", data_table)
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
    cur.execute('delete from engineering_nolectinfo')
    # エラーメッセージ表示
    print('Error!!')

finally:    
    # 切断
    cur.close()
    con.close()