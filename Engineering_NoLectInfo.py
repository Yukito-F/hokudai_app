import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

csvFile = open("files/Engineering_NoLectInfo.csv",'w+',newline='')
writer = csv.writer(csvFile)

html = urlopen("https://www.eng.hokudai.ac.jp/lecinfo/")
bsObj = BeautifulSoup(html, "lxml")
tbody = bsObj.findAll("tbody")[0]

try:
    forÅ@tbodys in tbody.findAll("tr"):
        csvRow = []
        for cell in tbodys.findAll("td"):   
            celllet = cell.get_text()
            csvRow.append(celllet)
        writer.writerow(csvRow) 
finally:
    csvFile.close()