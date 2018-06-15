import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.eng.hokudai.ac.jp/lecinfo/")
bsObj = BeautifulSoup(html, "lxml")

tbody = bsObj.findAll("tbody")[0]

csvFile = open("files/çHäwïîçuã`èÓïÒ.csv",'w+',newline='')
writer = csv.writer(csvFile)

try:
    for rows in tbody.findAll("tr"):
        csvRow = []
        for cell in rows.findAll("td"):   
            let = cell.get_text()
            csvRow.append(let)
            print(csvRow)
        writer.writerow(csvRow) 
finally:
    csvFile.close()