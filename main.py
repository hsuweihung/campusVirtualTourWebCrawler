#install package
#pip3 install selenium
#pip3 install time
#pip3 install schedule

#import package
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#import pymysql
import time
import schedule

#initailize two list
last_title="" #default last_title is empty
titles = []

#function of scrape the news
def scrape_new_list():
    #conn =pymysql.connect()

    driver = webdriver.Chrome() #should install webdriver first 

    URL = "https://www.nycu.edu.tw/nycu/ch/app/news/list?module=headnews&id=2994"
    driver.get(URL)

    #connect to DB, currently failed by error code 1045
    '''conn = pymysql.connect(
        host='roundhouse.proxy.rlwy.net:50655',
        port=50655,
        user='root',
        passwd='6hdeFc364fACf--eeBC2H5aE3-2BA-Hb',
        db='railway',
        charset='utf8'
    )'''

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "newslist"))) #search all class name newslist
    
    #get the attribute name of title of li element
    for i in range(15):
        id_value = f"listImageNum{i}"
        element = driver.find_element(By.ID, id_value)
        title = element.get_attribute("title")
        titles.append(title)
        print(title)

    driver.quit()
    #conn.close()
    
#function that check the news title is different or not 
def review_title():
    global last_title
    if not last_title:
        print("第一次標題")
        scrape_new_list()
    elif set(titles) != set(last_title):
        print("標題有更新")
        scrape_new_list()
    else:
        print("無更新")
    
    last_title =titles

#automatic check
schedule.every(5).seconds.do(review_title)


while (1):
    schedule.run_pending()
    time.sleep(1)