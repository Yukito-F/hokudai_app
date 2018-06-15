import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www2.lit.kyushu-u.ac.jp/~syllabus/cgi-bin/class-schedule.cgi?kubun=1")
bsObj = BeautifulSoup(html, "lxml")
bsObj.find('br').replace_with(',')

table = bsObj.findAll("table")[3]
row = table.findAll("tr")
rowcus = row[1:]

csvFile = open("files/ï∂äwïîãxçuèÓïÒ.csv",'w+',newline='')
writer = csv.writer(csvFile)

try:
    for rows in rowcus:
        csvRow = []
        for cell in rows.findAll("td"):
            cellcus = str(cell)
            cellx = cellcus.split("<br/>")
            for cellf in cellx:
                letter = BeautifulSoup(cellf, "lxml")
                let = letter.get_text()
                csvRow.append(let)
        writer.writerow(csvRow) 
finally:
    csvFile.close()