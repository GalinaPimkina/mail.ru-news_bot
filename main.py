from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import lxml
import requests
import json


ua = UserAgent()

headers = {
    "user-agent": ua.random
}


# response = requests.get(
#     url='https://mail.ru/?news=main&json=1&rb_SvoHitechShortNames=1&rb_cnyEnabled=true&rb_doodle=&rb_fakedoorAuth=false&rb_testOmicron=true&rb_widgetsExp=2&ph_addTargetToNaviData=true&updateHoro=1&build=70cbd58&isMainPageUserConfigEnable=1&cloudWidgetUpdateEnabled=1&newsTabsOrder=main,svo,regional,incident,finance,sport,lady,auto,cinema,hitech,games,interesting,health,pets')
# json_data = json.loads(response.text)
# html_response = json_data["update"]["news"]["main"]["html"]
#
# with open('main.html', 'w', encoding='utf-8') as file:
#     file.write(html_response)




with open('main.html', 'r', encoding='utf-8') as file:
    src = file.read()

    soup = BeautifulSoup(src, "lxml")
    news = soup.find_all("a", class_="news__list__item__link")

    for item in news:
        news_id = item.findPrevious("div", class_="news__list__item").get("data-value")
        news_title = item.text.strip()
        news_href = item.get("href")

        if news_title:
            print(news_id)
            print(news_title)
            print(news_href)
            print("-" * 20)









