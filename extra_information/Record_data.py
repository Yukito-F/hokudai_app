from bs4 import BeautifulSoup

# htmlソースを最小単位まで分解し、データベースに適合させた形で返す関数
def data_make(source):
# ＜データ整理＞
    # データの選別
    bsObj = BeautifulSoup(source, "lxml")
    table = bsObj.findAll("table")[6]
    rows = table.findAll("tr")

    # 必要なものだけ選別
    specific_rows = rows[2::2][0:-1]

    # データの整理
    data = []
    for row in specific_rows:
        data_record = []
        for cell in row.findAll("td"):
            text = cell.get_text()
            data_record.append(text)
        data.append(data_record)

    return data