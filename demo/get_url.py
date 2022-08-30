from cProfile import label
from urllib.parse import urljoin
import requests
import bs4
import re

lables = ['要闻','观点']
pages_list =  [['http://tw.people.com.cn/',
            'http://hm.people.com.cn/',
            'http://military.people.com.cn/',
            'http://world.people.com.cn/',],
            ['http://ent.people.com.cn/',
            'http://society.people.com.cn/',
            'http://finance.people.com.cn/',]]
for lable, pages in zip(lables, pages_list):
    f = open("./data/renmin_data/"+lable+".txt", 'w', encoding='utf-8')
    for page in pages:
        r = requests.get(page)
        r.encoding = r.apparent_encoding
        bs = bs4.BeautifulSoup(r.text, "html.parser")
        news = bs.findAll(class_="hdNews")
        for i in news:
            f.write(i.find("a").text)
            f.write(i.find("a").get("href"))
            f.write("\n")
        next_page = bs.find('a', string="下一页")
        if next_page:
            next_page_url = next_page.get("href")
            next_page_url = next_page_url if next_page_url.startswith(
                "http") else urljoin(page, next_page_url)
            r = requests.get(next_page_url)
            r.encoding = r.apparent_encoding
            bs = bs4.BeautifulSoup(r.text, "html.parser")
            news = bs.findAll(class_="hdNews")
            for i in news:
                f.write(i.find("a").text)
                f.write(i.find("a").get("href"))
                f.write("\n")
    f.close()