import csv
import os, sys
sys.path.append('.')
from lib_open import make_legend_dict

"""
実行方法：python write_csv.y 水産学
-> 水産学のcsvファイルがカレントディレクトリに作成される
"""
query = sys.argv[1]

# 工学と低温は現段階で非対応

csvFile = open("./lib_hokudai.csv", 'w+', newline='')
writer = csv.writer(csvFile)
tbody, class2color, color2time = make_legend_dict(query)

try:
    for tbodys in tbody.findAll("tr"):
        for cell in tbodys.findAll("td"):
            csvRow = []
            opclass = cell.get("class")[0]
            if opclass == "empty":
                continue
            elif opclass == "memo":
                csvRow.append("memo")
                while cell.find("br") != None:
                    cell.find("br").replace_with("\n")
            date = cell.get_text()
            csvRow.append(date)

            if opclass != "empty" and opclass != "memo":
                csvRow.extend(color2time[class2color[opclass]])
            writer.writerow(csvRow)
finally:
    csvFile.close()