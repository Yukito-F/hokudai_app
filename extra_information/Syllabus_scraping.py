import time, os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import Select
from datetime import datetime

# 「name」を名前に持つフォームの「value」を選択する関数
def forminput(name, value, driver):
    form = driver.find_element_by_name(name)
    form_select = Select(form)
    form_select.select_by_value(value)

# 「name」を名前に持つボタンをクリックする関数
def buttonclick(name, driver):
    button = driver.find_element_by_name(name)
    button.click()


# webdriverを起動しdriverを返す関数
def setup(option = True):
    # ウェブドライバー起動
    options = ChromeOptions()
    if option:
        options.add_argument('--headless')
    driver = Chrome(options = options, executable_path = os.path.abspath(r'.\webscrapying') + r'\chromedriver.exe')
    return driver


# 必要なページ遷移を行い、そのソースを返す関数
def scraping(grade, department, driver):
    # 年、月を取得
    year = datetime.now().year
    month = datetime.now().month

    # 学期の判別
    if month >= 3 and month <= 8:
        semester = '1'  
    elif month <= 2 or month >= 9:
        semester = '2'
    
    # シラバスのページにアクセス
    driver.get('http://syllabus01.academic.hokudai.ac.jp/Syllabi/Public/Syllabus/SylSearch.aspx')
    # 年度
    forminput('ctl00$phContents$ucSylSearchuc$ddl_year', str(year), driver)
    # 区分    02:学士課程, 11:修士課程, 12:博士後期課程, 13:専門職大学院, 14:法科大学院
    forminput('ctl00$phContents$ucSylSearchuc$ddl_org', '02', driver)
    time.sleep(5)
    #年次
    forminput('ctl00$phContents$ucSylSearchuc$ddl_grad', grade, driver)
    time.sleep(5)
    # 学部    00：全学教育,02:総合教育部,05:文学部,07:教育学部,11:現代日本学プログラム課程,15:法学部,17:経済学部,22:理学部,25:工学部,34,農学部,36:獣医学部,38:水産学部,43:歯学部,44:薬学部,74:国際本部
    forminput('ctl00$phContents$ucSylSearchuc$ddl_fac', department, driver)
    time.sleep(5)
    #学期
    forminput('ctl00$phContents$ucSylSearchuc$ddl_open', semester, driver)
    time.sleep(5)

    #ジャンプ
    buttonclick('ctl00$phContents$ucSylSearchuc$ctl89$btnSearch', driver)
    time.sleep(5)
    try:
        #全表示
        forminput('ctl00$phContents$ucSylList$DDLLine$ddl', '0', driver)
        time.sleep(5)
        # HTMLソースを格納
        html_source = driver.page_source
    except:
        html_source = 0

    return html_source

def end(driver):
    driver.quit()  