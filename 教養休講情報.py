import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

csvFile = open("files/ëSäwã≥àÁãxçuèÓïÒ.csv",'w+',newline='')
writer = csv.writer(csvFile)

driver = webdriver.Chrome(r'C:\Users\Tomoyuki Fujiwara\Downloads\chromedriver_win32\chromedriver')
driver.get('http://inform.academic.hokudai.ac.jp/webinfo/p/SerchInfo.aspx?mode=cancel');
time.sleep(5)
Sesrch = driver.find_element_by_name('btnSerch').click()
html_source = driver.page_source
driver.quit()

bsObj = BeautifulSoup(html_source, 'lxml')
bsObj.find('br').replace_with(',')
table = bsObj.findAll("table")[2]
row = table.findAll("tr")
rowcus = row[1:]

try:
    for rows in rowcus:
        csvRow = []
        for cell in rows.findAll("td"):
            cellstr = str(cell)
            if cellstr in '<br/>':
                cellsbr = cellstr.split("<br/>")
                for celldbr in cellsbr:
                    cellbso = BeautifulSoup(celldbr, "lxml")  
            else: 
                cellbso = BeautifulSoup(cellstr, "lxml")
                let = cellbso.get_text()
                csvRow.append(let)
        writer.writerow(csvRow) 
finally:
    csvFile.close()