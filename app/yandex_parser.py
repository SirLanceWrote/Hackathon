import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

def yandex_parser(m_class):
    help = ["", " page 0", " page 1", " page 2"]
    urls = set()
    for i in help:
        url = "https://yandex.ru/images/search?text=" + str(m_class) + i
        page = requests.get(url, headers=Headers().generate())
        soup = BeautifulSoup(page.text, "html.parser")
        
        result = soup.find_all("div", {"class":"serp-item"}, limit=50)
        for r in result:
            jsonify = json.loads(r["data-bem"])
            urls.add(jsonify['serp-item']['preview'][0]['url'])
    return urls
