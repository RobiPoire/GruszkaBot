import random

import requests


def qwant_image(search: str, count_search: int = 10, count_result: int = 1, safesearch: int = 1) -> list[str]:
    r = requests.get("https://api.qwant.com/v3/search/images",
                     params={
                         'count': count_search,
                         'q': search,
                         't': 'images',
                         'safesearch': safesearch,
                         'locale': 'fr_FR',
                         'offset': 0,
                         'device': 'desktop'
                     },
                     headers={
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                          (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                     }
                     )
    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response]
    return random.choices(urls, k=count_result)
