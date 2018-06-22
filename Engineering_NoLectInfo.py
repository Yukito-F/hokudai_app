import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

#csvファイルを展開（任意のディレクトリにて）及びwriterのセット
csvFile = open(".\Engineering_NoLectInfo.csv",'w+',newline='')
writer = csv.writer(csvFile)

#指定したURLのHTMLソースをbeautiful soup固有のオブジェクトとして格納、
html = urlopen("https://www.eng.hokudai.ac.jp/lecinfo/")
bsObj = BeautifulSoup(html, "lxml")

#「tbody」にtbodyタグの0番目の内容を格納
tbody = bsObj.findAll("tbody")[0]

try:
    #「tbodies」に「tbody」内のtrタグの内容を順に格納
    for tbodies in tbody.findAll("tr"):
        csvRow = []
        #「cell」に「tbodies」内のtdタグの内容を順に格納
        for cell in tbodies.findAll("td"):
            #「cell」からテキストデータのみを抽出し「csvRow」に配列として順次格納   
            celllet = cell.get_text()
            csvRow.append(celllet)
        #n番目のtrタグの内容をcsvファイルのn列に書き込み
        writer.writerow(csvRow) 

finally:
    #csvファイルを閉じ終了
    csvFile.close()