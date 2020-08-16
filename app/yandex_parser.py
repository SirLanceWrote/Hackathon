import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import random
import json

https_p = [ '46.151.108.6:41171', '89.223.20.202:5836', '91.216.66.70:32306', 
 '176.62.188.158:56351', 
'185.21.66.212:80'
]


def yandex_parser(m_class):
    global https_p
    _https = https_p.copy()
    help = ["", " page 0", " page 1", " page 2"]
    urls = set()
    flag = True
    while(flag):
        try:
            htps = random.choice(_https)
            _https.remove(htps)
            proxies = {
            'https': "https://" + htps
    }       
            count = 0
            for i in help:
                url = "https://yandex.ru/images/search?text=" + str(m_class) + i
                print(htps)
                page = requests.get(url, headers=Headers().generate(), proxies=proxies)
                soup = BeautifulSoup(page.text, "html.parser")
                
                result = soup.find_all("div", {"class":"serp-item"}, limit=50)
                for r in result:
                    # if count >12:
                    #     return list(urls)
                    jsonify = json.loads(r["data-bem"])
                    urls.add(jsonify['serp-item']['preview'][0]['url'])
                    if len(urls)>=1:
                        flag = False
                        count+=1
                    else:
                        continue
                    print(len(urls))
            urls = list(urls)
        except:
            pass
        print(urls)
    return urls
