import json
import re

import requests

db = {}

anime_url = 'https://api.gamer.com.tw/mobile_app/anime/v1/video.php?sn=16844&anime_sn=0'


def cleansntxt():
    with open('sn_list.txt', 'w+', encoding='UTF-8') as f:
        f.write('')


def get_anime_list():
    animedata = {}
    anime_list = requests.get(
        'https://api.gamer.com.tw/mobile_app/anime/v1/index.php').json()
    for _anime in anime_list['new_anime']['date']:
        animedata[_anime['anime_sn']] = _anime['title']
    anime_list = requests.get(
        'https://ani.gamer.com.tw/ajax/animeOutOfSeasonMore.php?offset=1&limit=999').json()['data']
    data = dict(zip(re.findall(r"sn=(\d*)", anime_list),
                    re.findall(r"ame'>(.*)<", anime_list)))
    for _sn, _title in data.items():
        animedata[_sn] = _title
    return animedata


def get_anime_detail(sn: int, title: str):
    anime = requests.get(
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
    anime_list = get_anime_list()
    # print(anime_list)
    for _anime_sn, _anime_title in anime_list.items():
        db[_anime_title] = {}
        get_anime_detail(_anime_sn, _anime_title)

    with open('anigamer.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)
