import json

import requests

db = {}

anime_url = 'https://api.gamer.com.tw/mobile_app/anime/v1/video.php?sn=16844&anime_sn=0'
page = 1
sess = requests.Session()
sess.headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'})

def cleansntxt():
    with open('sn_list.txt', 'w+', encoding='UTF-8') as f:
        f.write('')


def get_anime_list():
    global page
    anime_list = sess.get(
        f'https://api.gamer.com.tw/mobile_app/anime/v1/list.php?page={page}').json()
    page += 1
    return anime_list


def get_anime_detail(sn: int, title: str):
    anime = sess.get(
        f'https://api.gamer.com.tw/mobile_app/anime/v1/video.php?&anime_sn={sn}').json()
    with open('sn_list.txt', 'a', encoding='UTF-8') as f:
        if 'anime' in anime:
            f.write(f'{anime["video"]["video_sn"]} all {title}\n')
        else:
            return

    for _type in anime['anime']['volumes']:
        for _sn in anime['anime']['volumes'][_type]:
            if _type == '0':
                db[title][_sn['volume']] = str(_sn["video_sn"])
            elif _type == '1' or _type == '4':
                db[title][anime["videoTypeList"]
                          [int(_type)]["name"]] = str(_sn["video_sn"])
            else:
                db[title][f'{anime["videoTypeList"][int(_type)]["name"]} {_sn["volume"]}'] = str(
                    _sn["video_sn"])


if __name__ == "__main__":
    cleansntxt()
    while True:
        anime_list = get_anime_list()
        if anime_list:
            for _anime_sn in anime_list:
                db[_anime_sn['title']] = {}
                get_anime_detail(_anime_sn['anime_sn'], _anime_sn['title'])
                if not db[_anime_sn['title']]:
                    del db[_anime_sn['title']]
        else:
            break
    with open('anigamer.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)
