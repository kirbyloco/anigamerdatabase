import json
import re

import requests
from lxml import etree

snlist = []
db = {}

def load_snlist():
    with open('sn_list.txt', 'r') as f:
        a = f.readlines()
    for _ in a:
        snlist.append(re.findall(r'(\d+)', _)[0])

def get_sn(sn):
    a = requests.get(f'https://ani.gamer.com.tw/animeVideo.php?sn={sn}')
    b = etree.HTML(a.text)
    animename = (re.findall(r'(.*) \[.*\] \[.*\]', b.xpath('//div[@class="anime_name"]/h1')[0].text) or re.findall(r'(.*) ', b.xpath('//div[@class="anime_name"]/h1')[0].text))[0]
    print(animename)
    db[animename] = {}
    index = []
    # len(b.xpath('//section[@class="season"]/p'))
    for _ in b.xpath('//section[@class="season"]/ul/li/a'):
        if _.text not in index:
            db[animename][_.text] = re.findall(r'(\d+)', _.get('href'))[0]
            index.append(_.text)
        else:
            db[animename][f'特別篇 {_.text}'] = re.findall(r'(\d+)', _.get('href'))[0]
        
    if db[animename] == {}:
        db[animename][re.findall(r'\[(.*)\]', b.xpath('//div[@class="anime_name"]/h1')[0].text)[0]] = sn

load_snlist()
for _sn in snlist:
    get_sn(_sn)
with open('anigamer.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=4)
