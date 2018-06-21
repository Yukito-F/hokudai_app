from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import re
import os, sys
sys.path.append('..')
from webscrapying.webscrapying import get_soup_with_driver

# 現状、driver_pathはこのままでどのPCでもおそらく実行可能
soup = get_soup_with_driver(url='https://www.hokudai.seikyou.ne.jp/bhours/',
                            driver_path=os.path.abspath('../webscrapying') + '/chromedriver')

calendar = soup.findAll(id="schewrap")[0]
tbody = calendar.findAll("tbody")[0]

csvFile = open("./seikyo.csv", 'w+', newline='')
writer = csv.writer(csvFile)

tr_class_name = "a"
try:
    for trow in tbody.findAll("tr"):
        csvRow = []

        # 場所と店舗名を取得（例：北部店 購買北部店）
        current_class = trow.get("class")
        if tr_class_name != current_class:
            csvRow.append(trow.findAll("th")[0].get_text())
            csvRow.append(trow.findAll("th")[1].get_text())
            tr_class_name = current_class
        else:
            csvRow.append(" ")
            csvRow.append(trow.findAll("th")[0].get_text())

        # 10:00-18:00などのデータを格納
        times = trow.findAll("td")[0].get_text()

        # 空白文字の削除とコロンの半角修正
        times = re.sub("\s", "", times)
        times = re.sub("：", ":", times)
        op, cl = times.split('-')
        csvRow.extend([op, cl])
        writer.writerow(csvRow)

finally:
    csvFile.close()