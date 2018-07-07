import time, os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import Select

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
def scraping(semester, department, driver):
    # 成績分布のページにアクセス
    driver.get('http://educate.academic.hokudai.ac.jp/seiseki/GradeDistSerch.aspx')
    time.sleep(5)
    
    # 学期指定
    forminput('ddlTerm', semester, driver)
    time.sleep(5)
    # 課程指定
    forminput('ddlDiv', '02', driver)
    time.sleep(5)
    # 学部指定
    forminput('ddlFac', department, driver)
    time.sleep(5)
    # 分類指定
    forminput('ddlDataKind', '1', driver)
    time.sleep(5)
    # 内容指定
    forminput('ddlContents', '0', driver)
    time.sleep(5)
    # ジャンプ
    buttonclick('btnSerch', driver)
    time.sleep(10)

    try:
        #全表示
        forminput('ddlLine$ddl', '0', driver)
        time.sleep(5)
        # HTMLソースを格納
        html_source = driver.page_source
    except:
        html_source = 0

    return html_source

def end(driver):
    driver.quit()