import time, csv, os
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome(executable_path = os.path.abspath('.\webscrapying') + '\chromedriver.exe')
driver.get('http://inform.academic.hokudai.ac.jp/webinfo/p/SerchInfo.aspx?mode=cancel')
time.sleep(5)
search_box = driver.find_element_by_name('btnSerch')
search_box.click()
Sources = []
time.sleep(5)

while True:
    source = driver.page_source
    Sources.append(source)
    if 'value="次へ"' in source:
        if '<span>1</span>' in source:
            Search = driver.find_element_by_name('rdlGrid$gridList$ctl14$ctl01')
        else:
            Search = driver.find_element_by_name('rdlGrid$gridList$ctl14$ctl03')
        Search.click()
        time.sleep(5)
    else:
        break
driver.quit()

csvFile = open(".\FirstYear_NoLectInfo.csv",'w+',newline='', encoding='CP932', errors='ignore')
writer = csv.writer(csvFile)

try:
    for text in Sources:
        bsObj = BeautifulSoup(text, 'lxml')
        table = bsObj.findAll("table")[2]
        tr = table.findAll("tr")
        sptr = tr[1:-1]
        for trs in sptr:
            csvRow = []
            for td in trs.findAll("td"):
                tdstr = str(td)
                if '<br/>' in tdstr:
                    tdspbr = tdstr.split("<br/>")
                    csvex = [""] * 4
                    for cell, i in zip(tdspbr, range(4)):
                        cellbso = BeautifulSoup(cell, "lxml")
                        celllet = cellbso.get_text()
                        csvex[i] = celllet
                    el1 = csvex[1]
                    el2 = csvex[2]
                    csvex[1] = el2
                    csvex[2] = el1
                    if ',' in csvex[0]:
                        csvex2 = csvex[0].split(",")
                        csvex[0] = csvex2[0]
                        csvex[1] = csvex2[1]
                    if ',' in csvex[2]:
                        csvex3 = csvex[2].split(",")
                        csvex[2] = csvex3[0]
                        csvex[3] = csvex3[1]
                    csvRow.extend(csvex)
                else: 
                    cellbso = BeautifulSoup(tdstr, "lxml")
                    celllet = cellbso.get_text()
                    csvRow.append(celllet)
            writer.writerow(csvRow)
finally:
    csvFile.close()