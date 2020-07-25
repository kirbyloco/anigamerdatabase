import requests
import re
from lxml import etree

def checklastpage():
    a = etree.HTML(html.text)
    return a.xpath('//div[@class="page_number"]/a')[-1].text

def getrealvideoid(url):
    html = requests.get('https://ani.gamer.com.tw/' + url)
    if html.text.find('18UP') == -1: #檢測是否為R-18
        return re.findall("=(\d*)", html.url)[0]
    else:
        return '' + re.findall("=(\d*)", html.url)[0]

def getdata(_):
    b = ''
    ANIGAMER_URL = 'https://ani.gamer.com.tw/animeList.php?page=' + str(_) + '&c=0&sort=0'
    html = requests.get(ANIGAMER_URL)
    a = etree.HTML(html.text)
    animelist = a.xpath('//ul[@class="anime_list"]/li')
    for _ in animelist:
        with open('sn_list.txt', 'a', encoding='UTF-8') as f:
            f.write('{0} all {1}\n'.format(getrealvideoid(_.xpath('a')[0].get('href')), _.xpath('div[@class="info"]/b')[0].text))

def cleansntxt():
    with open('sn_list.txt', 'w+', encoding='UTF-8') as f:
        f.write('')

def getlastpageid():
    ANIGAMER_URL = 'https://ani.gamer.com.tw/animeList.php'
    html = requests.get(ANIGAMER_URL)
    a = etree.HTML(html.text)
    return int(a.xpath('//div[@class="page_number"]/a')[-1].text) + 1

if __name__ == '__main__':
    print('清除舊的sn_list.txt')
    cleansntxt()
    for _ in range(1, getlastpageid()):
        print('正在抓取第{0}頁'.format(_))
        getdata(_)
