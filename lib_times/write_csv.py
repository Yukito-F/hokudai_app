import csv
import os, sys
sys.path.append('.')
from lib_open import make_legend_dict

"""
実行方法：python write_csv.y 水産学
-> 水産学のcsvファイルがカレントディレクトリに作成される
"""
query = sys.argv[1]

query2url = {
    "本館": "https://www.lib.hokudai.ac.jp/calendar/central-lib/",
    "北図書館": "https://www.lib.hokudai.ac.jp/calendar/north-lib/",
    "文学": "https://www.lib.hokudai.ac.jp/calendar/let/",
    "教育": "https://www.lib.hokudai.ac.jp/calendar/edu/",
    "経済": "https://www.lib.hokudai.ac.jp/calendar/eco/",
    "理学": "https://www.lib.hokudai.ac.jp/calendar/sci/",
    "医学": "https://www.lib.hokudai.ac.jp/calendar/med/",
    "歯学": "https://www.lib.hokudai.ac.jp/calendar/den/",
    "薬学": "https://www.lib.hokudai.ac.jp/calendar/pharm/",
    "農学": "https://www.lib.hokudai.ac.jp/calendar/agr/",
    "獣医学": "https://www.lib.hokudai.ac.jp/calendar/vet/",
    "水産学": "https://www.lib.hokudai.ac.jp/calendar/fish/",
    "地球環境科学": "https://www.lib.hokudai.ac.jp/calendar/env/",
    "北キャンパス": "https://www.lib.hokudai.ac.jp/calendar/northern-campus/",
    "スラブ-ユーラシア": "https://www.lib.hokudai.ac.jp/calendar/slv/",
    "保健科": "https://www.lib.hokudai.ac.jp/calendar/health/",
}
# 工学と低温は現段階で非対応

csvFile = open("./lib_hokudai.csv", 'w+', newline='')
writer = csv.writer(csvFile)
tbody, class2color, color2time = make_legend_dict(url=query2url[query])

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