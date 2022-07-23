from selenium import webdriver
from bs4 import BeautifulSoup as bs
from linebot.models import *
from flex_msg import *
from config import *
import time
import json
import random
import string
import os


def youtube_vedio_parser(keyword):
    #建立url跟目錄
    urlfake = 'https://tw.youtube.com/'
    url = "https://www.dcard.tw/service/api/v2/posts?popular=true&limit=10"

    #建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    #設定瀏覽器的語言為utf-8中文
    #chromeOption.add_argument("--lang=zh-CN.UTF8")
    #設定瀏覽器的user agent
    chromeOption.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    chromeOption.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chromeOption.add_argument("--headless")  # 無頭模式
    chromeOption.add_argument("--disable-dev-shm-usage")
    chromeOption.add_argument("--no-sandbox")

    #開啟Chrome瀏覽器
    #driver = webdriver.Chrome(options=chromeOption)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chromeOption)
    #調整瀏覽器視窗大小
    driver.set_window_size(1024, 960)

    #======================依關鍵字在Dcard網站上搜尋API===========================
    #進入指定網址
    driver.get(urlfake)
    time.sleep(2)
    driver.get(url)
    time.sleep(6)
    #等待網頁讀取


    # ======================擷取網站API資訊===========================

    # 整個網頁資訊
    html_doc = driver.page_source

    # 解析網頁資訊
    page = bs(html_doc, 'html.parser')

    # print(page.prettify())

    # print(page.pre.string)

    # 取得json格式
    jsoon = page.pre.string

    # 讀取json
    reqsjson = json.loads(jsoon.text)

    # 列印篇數
    total_num = len(reqsjson)
    print(total_num)
    print('-' * 30)

    # ======================從網頁獲取文章連結===========================
    # 文章URL前墜
    Post_Urlfront = "https://www.dcard.tw/f/talk/p/"
    # 狄卡logo
    D_logo = "https://imgur.com/L5JSIaF"
    # 建立文章url列表
    vedio_url_list = []
    # 建立縮圖列表
    yt_vedio_images = []
    # 建立標題與副標列表
    yt_title_list = []
    yt_channel_infos_names = []
    # 小縮圖(圖片)
    yt_channel_infos_image_urls = []

    # 將每個文章連結放入連結list
    # print(len(yt_vedio_urls))

    #----------------------
    for i in range(0, total_num):
        # 判斷這文章圖的數量
        media_num = len(reqsjson[i]["media"])
        # 取得文章連結

        idd = reqsjson[i]["id"]
        okid = str(idd)
        vedio_url_list.append(Post_Urlfront+okid)

        # 取得文章標題

        title = reqsjson[i]["title"]
        yt_title_list.append(title)

        # 取得文章副標題

        post2_num = len(reqsjson[i]["excerpt"])
        if post2_num != 0:
            excerpt = reqsjson[i]["excerpt"]
            yt_channel_infos_names.append(excerpt)
        else:
            text = '...'
            yt_channel_infos_names.append(text)

        # 取得文章圖片連結


        if media_num != 0:
            image_url = reqsjson[i]['media'][0]['url']
            yt_vedio_images.append(image_url)

        else:
            print("狀態:沒有圖QQ")
            yt_vedio_images.append(D_logo)

        # 小圓縮圖取得

        yt_channel_infos_image_urls.append(D_logo)

        #print('-' * 30)

    print("爬完收工")

    print(len(vedio_url_list), '文章連結')
    print(len(yt_vedio_images), '圖片連結')
    print(len(yt_title_list), '標題')
    print(len(yt_channel_infos_names), '副標')
    print(len(yt_channel_infos_image_urls), 'last')

    #關閉瀏覽器連線
    driver.close()

    #==============將爬取到的資訊以FlexMessage回傳至主程式===================
    message = []   

    #回傳搜尋結果的FlexMessage
    message.append(image_carousel('YT搜尋結果',yt_vedio_images,vedio_url_list,yt_title_list,yt_channel_infos_image_urls,yt_channel_infos_names))
    return message
   
    
#可於本機中直接執行python web_crawler.py進行單元測試，但必須先將CHANNEL_ACCESS_TOKEN、USERID都在config.py設定好
if __name__=='__main__':
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *
    message = youtube_vedio_parser('Maso的萬事屋')
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID,message)
    