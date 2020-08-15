import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import random
import json

https_p = ['185.117.118.39:5836', '92.252.187.146:8080', '46.151.108.6:41171', '89.223.20.202:5836',
'31.44.12.20:5836', '91.216.66.70:32306']
http_p = ['109.167.226.107:38608']

def yandex_parser(m_class):
    global https_p, http_p
    _http = http_p.copy()
    _https = https_p.copy()
    help = ["", " page 0", " page 1", " page 2"]
    urls = set()
    flag = True
    while(flag):
        htp = random.choice(_http)
        htps = random.choice(_https)
        _http.remove(htp)
        _https.remove(htps)
        proxies = {
        'http': "http://" + htp,
        'https': "https://" + htps
    }
        for i in help:
            url = "https://yandex.ru/images/search?text=" + str(m_class) + i
            print(htps)
            page = requests.get(url, headers=Headers().generate(), proxies=proxies)
            soup = BeautifulSoup(page.text, "html.parser")
            
            result = soup.find_all("div", {"class":"serp-item"}, limit=50)
            for r in result:
                jsonify = json.loads(r["data-bem"])
                urls.add(jsonify['serp-item']['preview'][0]['url'])
                print(len(urls))
        urls = list(urls)
        if len(urls)>1:
            flag = False
    return urls

print(len(yandex_parser('лошадь')))