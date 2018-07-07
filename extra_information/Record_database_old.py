import mysql.connector,os
from Record_scraping import setup, scraping, end
from Record_data import data_make

semester_num_list = ["20171","20162"] #,"20161","20152","20151"] # 旧課程,"20142","20141","20132","20131","20122","20121","20112","20111","20102","20101","20092","20091","20082","20081","20072","20071","20062","20061","20052","20051"]
department_num_list = ['00', '25'] #,'02','05','07','11','15','17','22','34','36','38','43','44','74',"42"]
department_name_list = ['全学教育', '工学部'] #'総合教育部','文学部','教育学部','現代日本学プログラム課程','法学部','経済学部','理学部','農学部','獣医学部','水産学部','歯学部','薬学部','国際本部','医学部'

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

for semester_num in semester_num_list:
    for department_name, department_num in zip(department_name_list, department_num_list):
        # データ取得
        source = scraping(semester = semester_num, department = department_num, driver = driver) # html_source

        # 例外処理
        if source == 0:
            # データの削除
            cur.execute('delete from Record_' + department_name)
            # コミットして変更を確定
            con.commit()
            # 以降無視
            pass

        # データ加工
        data_table = data_make(source) # data

        """
        「hokudai_app」データベースに「Record_(学部)_(学期番号)」テーブルがある場合はそのまま
        なければ
        CREATE TABLE Record_(学部)_(学期番号) (list VARCHAR(5),CourseTitle VARCHAR(100),CourseSubTitle VARCHAR(100),class VARCHAR(50),teacher VARCHAR(50),member VARCHAR(3),A_plus VARCHAR(4),A VARCHAR(4),A_minus VARCHAR(4),B_plus VARCHAR(4),B VARCHAR(4),B_minus VARCHAR(4),C_plus VARCHAR(4),C VARCHAR(4),D VARCHAR(4),D_minus VARCHAR(4),F VARCHAR(4),GPA VARCHAR(4))        
        で作成
        """

        # データの削除
        cur.execute('delete from Record_' + department_name + '_' + semester_num + '(list VARCHAR(5),CourseTitle VARCHAR(100),CourseSubTitle VARCHAR(100),class VARCHAR(50),teacher VARCHAR(50),member VARCHAR(3),A_plus VARCHAR(4),A VARCHAR(4),A_minus VARCHAR(4),B_plus VARCHAR(4),B VARCHAR(4),B_minus VARCHAR(4),C_plus VARCHAR(4),C VARCHAR(4),D VARCHAR(4),D_minus VARCHAR(4),F VARCHAR(4),GPA VARCHAR(4))')
        # データの入力
        cur.executemany("insert into Record_" + department_name + '_' + semester_num + "(list,CourseTitle,CourseSubTitle,class,teacher,member,A_plus,A,A_minus,B_plus,B,B,C_plus,C,D,D_minus,F,GPA) values (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data_table)
        # コミットして変更を確定
        con.commit()

    # データベース切断
    cur.close()
    con.close()

# 終了
end(driver)