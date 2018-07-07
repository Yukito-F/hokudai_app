from bs4 import BeautifulSoup

# htmlソースを最小単位まで分解し、データベースに適合させた形で返す関数
def data_make(source):
    # データの選別
    bsObj = BeautifulSoup(source, 'lxml')
    table = bsObj.findAll("table")[2]
    rows = table.findAll("tr")
    data_table = rows[1:-1]

# ＜データ整理＞
    # all_rowsを要素ごとに分割し、全てを一つの配列にまとめたdata_tableを作成する]
    data = []
    for row in data_table:
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
        data.append(data_record)

    return data