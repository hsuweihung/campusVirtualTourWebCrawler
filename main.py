# install package
# pip3 install selenium
# pip3 install pymysql
# pip3 install time
# pip3 install schedule

# import package
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule
import pymysql
import pymysql.cursors

# initailize two list
last_title = ""  # default last_title is empty
titles = []

# connect to local DB
conn = pymysql.connect(
    # put db info here
    host='localhost',
    port=3306,
    user='root',
    passwd='noho3224',
    db='NYCU360',
    charset='utf8'
)

# function of scrape the news


def scrape_new_list():
    driver = webdriver.Chrome()  # should install webdriver first
    URL = "https://www.nycu.edu.tw/nycu/ch/app/news/list?module=headnews&id=2994"
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    # search all class name newslist
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "newslist")))

    # get the attribute name of title of li element
    for i in range(15):
        id_value = f"listImageNum{i}"
        element = driver.find_element(By.ID, id_value)
        title = element.get_attribute("title")
        titles.append(title)
        cursor = conn.cursor()
        sql = 'insert into news_list(title) values(%s);'
        data = [title]
        try:
            cursor.execute(sql, title)
            conn.commit()
            print("connection success")
        except Exception as e:
            print("No connection")
            print("Error:", str(e))
            conn.rollback()
    driver.quit()
    conn.close()

# first time to scrapt the title


def first_scrapt():
    print("第一次標題")
    scrape_new_list()


# run the function
first_scrapt()

# function that check the news title is different or not


def review_title():
    global last_title
    if set(titles) != set(last_title):
        print("標題有更新")
        scrape_new_list()  # run the function
    else:
        print("無更新")

    last_title = titles


# run the function to automatic check
schedule.every(3).days.do(review_title)

while (1):
    schedule.run_pending()
    time.sleep(1)
