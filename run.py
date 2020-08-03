from urllib.request import urlopen, Request  # Internet url open package
from bs4 import BeautifulSoup  # BS
from selenium import webdriver  # webdriver
import time  # Package for waiting time during crawling
import warnings  # Remove Warning message

# Web browser automation
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# For Save Data
import pymysql

# For hashtag crawling
import re

# For Search human
import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
import os

def ToEng(x): return {'광운대맛집': 'kw', '외대맛집': 'hufs', '연대맛집': 'yon','고대맛집': 'kor', '한성대맛집': 'hsu', '성신여대맛집': 'ss'}[x]  # File name Korean->English

def imread_hangul_path(path):
    with open(path, "rb") as fp:
        bytes = bytearray(fp.read())
        numpy_array = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)  # Imread if the file name is Korean

warnings.filterwarnings(action='ignore')  # Remove Warning message


# Create instagram url and open
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome('/Users/kimsoojin/Desktop/chromedriver',chrome_options=chrome_options)
driver.get("https://www.instagram.com")
assert "Instagram" in driver.title  #Exception handling

# Login
time.sleep(0.5)
driver.find_element_by_name('username').send_keys('soooojiinn')
time.sleep(0.5)
driver.find_element_by_name('password').send_keys('tnwlswkdzz12!')
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
time.sleep(3)

# 쓰잘데기없는 화면 넘기기
driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[1]/div/a').click()
time.sleep(3)
driver.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()

# Data
search_univ = ['광운대맛집', '외대맛집', '연대맛집', '고대맛집', '한성대맛집', '성신여대맛집']
univ = ['광운대학교', '한국외국어대학교', '연세대학교', '고려대학교', '한성대학교', '성신여자대학교']
like = []
content = []
date = []
place = []
tags = []
cur_url = []

for x in search_univ:
    eng_univ = ToEng(x)

    # Search HashTag
    elem = driver.find_element_by_css_selector(".XTCLo.x3qfX")
    elem.send_keys(x)
    time.sleep(2)
    elem.send_keys(Keys.RETURN)
    elem.send_keys(Keys.RETURN)

    # Set url
    baseUrl = "https://www.instagram.com/explore/tags/"
    plusUrl = x
    url = baseUrl + plusUrl
    driver.get(url)
    time.sleep(3)

    # Scroll Section and Save image to local
    body = driver.find_element_by_tag_name("body")
    num_of_pagedowns = 10
    n = 1
    url_temp = []

    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.7)
        num_of_pagedowns -= 1

        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html)
        insta = soup.select('.v1Nh3.kIKUG._bz0w')

        for i in insta:
            #print('https://www.instagram.com' + i.a['href'])
            imgUrl = i.select_one('.KL4Bh').img['src']
            if imgUrl in url_temp:
                print("Already Exist!") # Ignore duplicate photos
            else:
                with urlopen(imgUrl) as f:
                    with open('./main/static/img/' + eng_univ + str(n) + '.jpg', 'wb') as h:
                        img = f.read()
                        h.write(img)
                n += 1
                url_temp.append(imgUrl)



    # Delete photos that contain face or body
    face_cascade = cv2.CascadeClassifier(
        '/Users/kimsoojin/Desktop/data/haarcascades/haarcascade_frontalface_default.xml')
    bodies_cascade = cv2.CascadeClassifier(
        '/Users/kimsoojin/Desktop/data/haarcascades/haarcascade_fullbody.xml')

    n_temp = []
    for i in range(1, n):
        # Convert to gray image
        search_img = "./main/static/img/" + eng_univ + str(i) + '.jpg'
        image = cv2.imread(search_img, cv2.IMREAD_COLOR)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

        faces = face_cascade.detectMultiScale(grayImage, 1.1, 5)
        bodies = bodies_cascade.detectMultiScale(grayImage, 1.1, 10)

        # If faces detected, print image 
        if len(faces) > 0:
            print("Number of faces detected: " + str(faces.shape[0]))
            """
            for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

            cv2.rectangle(image, ((0,image.shape[0] -25)), 
                        (270, image.shape[0]), (255,255,255), -1)
            cv2.putText(image, "Face detected image", (0,image.shape[0] -10), 
                        cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)

            plt.figure(figsize=(12,12))
            plt.imshow(image, cmap='gray')
            plt.xticks([]), plt.yticks([])  # To hide tick values on X and Y axis
            plt.show()
            """
        # If bodies detected, print image
        if len(bodies) > 0:
            print(bodies.shape)
            print("Number of bodies detected: " + str(bodies.shape[0]))
            """
            for (x,y,w,h) in bodies:
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)

            plt.figure(figsize=(12,12))
            plt.imshow(image, cmap='gray')
            plt.xticks([]), plt.yticks([])  # To hide tick values on X and Y axis
            plt.show()
            """
        # Delete the file if you find the person's face
        if(len(faces) > 0 or len(bodies) > 0):
            if os.path.isfile(search_img):
                os.remove(search_img)
        else:
            n_temp.append(i)

    # Extract Hashtag, Like_num, Content, Date, Place, url Information
    first = driver.find_element_by_css_selector('div._9AhH0')
    first.click()
    time.sleep(3)
    search_num = 10

    for i in range(0, search_num):
        html = driver.page_source
        soup2 = BeautifulSoup(html, 'lxml')

        # Like_num
        try:
            like.insert(i, soup2.select('div.Nm9Fw > button')[0].text[4:-1])
        except:
            like.insert(i, 0)

        # Content
        try:
            content.insert(i, soup2.select('div.C4VMK > span')[0].text)
        except:
            content.insert(i, '')

        # Date
        try:
            date.insert(i, soup2.select('time._1o9PC.Nzb55')[
                        0]['datetime'][:10])  # 10 characters from the front
        except:
            date.insert(i, '')

        # Place
        try:
            place.insert(i, soup2.select('div.JF9hh')[0].text)
        except:
            place.insert(i, '')

        # Tags
        tags.insert(i, re.findall(r'#[^\s#,\\]+', str(content)))

        # Url
        try:
            cur_url.insert(i, driver.current_url)
        except:
            cur_url.insert(i, '')

        # Next
        if (i != search_num - 1):
            right = driver.find_element_by_css_selector(
                'a._65Bje.coreSpriteRightPaginationArrow')
            right.click()
            time.sleep(3)

    # Save image from local to MySQL
    # Save each information
    conn = pymysql.connect(host="localhost", user="root", password="1234", db='capstone', charset='utf8mb4')
    cur = conn.cursor()

    for i in range(0, search_num):
        if i+1 in n_temp:   # Only information from photos that have not been deleted
            # Pre-work before processing the number of likes
            if (like[i] == 0):
                continue
            if (like[i].find(",")):
                like[i] = like[i].replace(",", "")

            if (int(like[i]) > 200):
                #img_path = './main/static/img/' + eng_univ + str(i + 1) + '.jpg'
                
                img_path = url_temp[i]
                print(type(url_temp[i]))
                sql = "insert into insert_db5(univ, img_path, like_num, content, tags, place, write_date, cur_url) values(%s, %s, %s, %s, %s, %s, %s, %s)"
                print(type(img_path))
                insert_tags = " ".join(tags[i])
                var = [univ[search_univ.index(x)], img_path, like[i], "hello", "hello", place[i], date[i], cur_url[i]]
                cur.execute(sql, var)
                conn.commit()

driver.close()
conn.close()

