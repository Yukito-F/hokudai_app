from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
# require Xvfb
# virtual display run only Linux(?)

# 仮想ディスプレイ(virtual=True)からブラウザを立ち上げ、指定されたurlのソースコードをBeautifulSoupの形式(soup)にしてreturnする
def get_soup_with_driver(url, driver_path="chromedriver", virtual=False):
    if virtual:
        display = Display(visible=0, size=(1024, 768))
        display.start()
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    source = driver.page_source

    driver.close()
    if virtual:
        display.stop()

    soup = BeautifulSoup(source, 'lxml')

    return soup