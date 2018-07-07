import mysql.connector,os
from Record_scraping import setup, scraping, end
from Record_data import data_make
from datetime import datetime

department_num_list = ['00', '25'] #,'02','05','07','11','15','17','22','34','36','38','43','44','74',"42"]
department_name_list = ['全学教育', '工学部'] #'総合教育部','文学部','教育学部','現代日本学プログラム課程','法学部','経済学部','理学部','農学部','獣医学部','水産学部','歯学部','薬学部','国際本部','医学部'

# 年、月を取得
year = datetime.now().year
month = datetime.now().month

oldyear = year - 1

# 学期の判別
if month >= 3 and month <= 8:
    semester = '1'  
elif month <= 2 or month >= 9:
    semester = '2'

semester_num = str(oldyear)+str(semester)

# ウェブドライバー起動
driver = setup(False)

# データベース接続
con = mysql.connector.connect(
    host = '127.0.0.1',
    db = 'hokudai_app',
    user = 'writer',
    passwd = 'write'
    )

# 辞書型カーソル取得
cur = con.cursor(dictionary=True)

for department_name, department_num in zip(department_name_list, department_num_list):
    # データ取得
    source = scraping(semester = semester_num, department = department_num, driver = driver) # html_source

    # 例外処理
    if source == 0:
        # 以降無視
        pass

    # データ加工
    data_table = data_make(source) # data

    # テーブルの作成
    cur.execute('create table Record_' + department_name + '_' + semester_num)
    # データの入力
    cur.executemany('insert into Record_' + department_name + '_' + semester_num + '(list,CourseTitle,CourseSubTitle,class,teacher,member,A_plus,A,A_minus,B_plus,B,B,C_plus,C,D,D_minus,F,GPA) values (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data_table)
    # コミットして変更を確定
    con.commit()

# データベース切断
cur.close()
con.close()

# 終了
end(driver)