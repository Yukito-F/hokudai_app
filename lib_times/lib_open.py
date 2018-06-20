from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# 凡例の辞書とテーブルをリターンする関数
def make_legend_dict(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    calendar = soup.findAll(id="hokudaiCal")[0]
    tbody = calendar.findAll("tbody")[0]

    styles = calendar.findAll("style")[0]
    css_styles = styles.get_text()

    tdlist = re.findall("td\.[a-z0-9_]+\t{ background\-color: [a-z]+; }", css_styles)
    class2color = {}
    for td in tdlist:
        name, color = td.split('\t')
        name = name[3:]
        color = re.findall("[a-z]+;", color)[0][:-1]
        class2color[name] = color

    legend = calendar.findAll("div")[-1]

    color2time = {}

    lefts = legend.findAll("span")
    colors = []
    for lg in lefts:
        lg_style = lg.get("style")
        if lg_style[:6] == "color:":
            lg_style = lg_style[6:-1]
            colors.append(lg_style)

    times = re.findall("：[0-9]+:[0-9]+\-[0-9]+:[0-9]+|：閉館|：閉室", legend.get_text())
    times = [t[1:] for t in times]

    # assert len(colors) == len(times)
    for i in range(len(times)):
        color = colors[i]
        if times[i] == "閉館":
            color2time[color] = ["close", ""]
        else:
            op, cl = times[i].split('-')
            color2time[color] = [op, cl]

    # tbody: 今月のカレンダーが格納されたテーブル, class2color: classと背景色の対応辞書, color2time: 背景色と営業時間の対応辞書
    return tbody, class2color, color2time
