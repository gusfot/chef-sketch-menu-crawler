import datetime
import json
import logging
import random
import time

import requests
from bs4 import BeautifulSoup
from slack_webhook import Slack
import configparser

# import logging.handlers


# logger = logging.getLogger(__name__)
# formatter = logger.Fomatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
# streamHandler = logging.StreamHandler()
# fileHandler = logging.FileHandler('./crawling.log')
# streamHandler.setFormatter(formatter)
# fileHandler.setFormatter(formatter)
# logger.addHandler(streamHandler)
# logger.addHandler(fileHandler)
# logger.setLevel(level=logging.DEBUG)

logging.basicConfig(filename='./crawling.log', level=logging.DEBUG)

# r_times = [1,2,3,4,5,6]
r_times = list(range(1, 7))

web_url = 'https://m.blog.naver.com/rego/PopularPostBlockInfo.nhn?blogId=eogks9383'


def crawling():
    with open('config.json', 'r') as f:
        config = json.load(f)

    time.sleep(random.choice(r_times))

    html = requests.get(web_url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}).text
    soup = BeautifulSoup(html, 'html.parser')

    result_text = soup.text[6:-2]
    a = json.loads(result_text)
    postList = a['result']['popularPostBlockInfoList'][0]['postList']

    now = datetime.datetime.now()
    month = int(now.strftime('%m'))
    nowDate = now.strftime(
        (str(month) + '월%d일').encode('unicode-escape').decode()
    ).encode().decode('unicode-escape')

    for post in postList:
        if nowDate in post['titleWithInspectMessage']:
            img_src = post['thumbnailList'][0]['encodedThumbnailUrl']
            slack = Slack(url=config['WEBHOOK_URL'])

            today_menu = "쉐프스케치, " + "[" + nowDate + "] 오늘의 메뉴"
            slack.post(text=today_menu, channel="#오늘의메뉴", attachments=[{
                # "fallback": href,
                # "pretext": href,
                "color": "#00FFFF",
                "author_name": "",
                "title": today_menu,
                # "title_link": href,
                "image_url": img_src,
                "thumb_url": img_src,
                # "actions": [
                #     {
                #         "name": "action",
                #         "type": "button",
                #         "text": "Complete this task",
                #         "style": "",
                #         "value": "complete"
                #     },
                # ]
            }])


if __name__ == '__main__':
    crawling()
