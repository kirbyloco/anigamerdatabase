import json

import requests

db = {}

anime_url = "https://api.gamer.com.tw/mobile_app/anime/v1/video.php?sn=16844&anime_sn=0"
total_page = 1
sess = requests.Session()
sess.headers.update(
    {
        "user-agent": "Animad/1.16.16 (tw.com.gamer.android.animad; build: 328; Android 14) okHttp/4.4.0",
        "x-bahamut-app-android": "tw.com.gamer.android.animad",
        "x-bahamut-app-version": "328",
    }
)


def cleansntxt():
    with open("sn_list.txt", "w+", encoding="UTF-8") as f:
        f.write("")


def get_total_page():
    global total_page
    total_page = sess.get(
        "https://api.gamer.com.tw/anime/v1/anime_list.php?page=1"
    ).json()["data"]["totalPage"]


def get_anime_list(page: int = 1):
    anime_list = sess.get(
        f"https://api.gamer.com.tw/anime/v1/anime_list.php?page={page}"
    ).json()["data"]["animeList"]
    return anime_list


def get_anime_detail(sn: int, title: str):
    anime = sess.get(
        f"https://api.gamer.com.tw/mobile_app/anime/v4/video.php?sn={sn}"
    ).json()
    with open("sn_list.txt", "a", encoding="UTF-8") as f:
        if anime["data"]:
            f.write(f'{anime["data"]["video"]["videoSn"]} all {title}\n')
        else:
            return

    for _type in anime["data"]["anime"]["episodes"]:
        for _sn in anime["data"]["anime"]["episodes"][_type]:
            if _type == "0":
                db[title][_sn["episode"]] = int(_sn["videoSn"])
            elif _type == "1":  # 電影
                db[title][f'電影{_sn["episode"]}'] = int(_sn["videoSn"])
            elif _type == "2":  # 特別篇
                db[title][f'特別篇{_sn["episode"]}'] = int(_sn["videoSn"])
            elif _type == "3":  # 中文配音
                db[title][f'中文配音{_sn["episode"]}'] = int(_sn["videoSn"])
            elif _type == "4":  # 中文電影
                db[title][f'中文電影{_sn["episode"]}'] = int(_sn["videoSn"])
            elif _type == "5":  # 中文特別篇
                db[title][f'中文特別篇{_sn["episode"]}'] = int(_sn["videoSn"])
            else:  # 未知分類
                db[title][f'未知分類str(_sn["episode"])'] = int(_sn["videoSn"])


if __name__ == "__main__":
    cleansntxt()
    get_total_page()
    for page in range(1, total_page + 1):
        anime_list = get_anime_list(page)
        if anime_list:
            for _anime in anime_list:
                db[_anime["title"]] = {}
                get_anime_detail(_anime["videoSn"], _anime["title"])
                if not db[_anime["title"]]:
                    del db[_anime["title"]]
        else:
            break
    with open("anigamer.json", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)
