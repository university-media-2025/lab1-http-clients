"""Парсинг новостных RSS-лент."""

import pprint
import requests
from xml.etree import ElementTree as ET


def get_alternative_news_rss(limit=None):
    """
    Альтернативные RSS-источники новостей.
    """
    rss_sources = [
        'https://www.kommersant.ru/RSS/news.xml',
        'https://ria.ru/export/rss2/archive/index.xml',
        'https://lenta.ru/rss/news',
        'https://www.vedomosti.ru/rss/news',
        'https://tass.ru/rss/v2.xml'
    ]

    for rss_url in rss_sources:
        try:
            print(f'Пробуем: {rss_url}')
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()

            # Парсим RSS
            root = ET.fromstring(response.text)
            news_items = []

            for item in root.findall('.//item'):
                news = {
                    'title': item.find('title').text,
                    'url': item.find('link').text,
                    'description': item.find('description').text,
                    'pub_date': item.find('pubDate').text
                }
                news_items.append(news)

            print(f'Успешно получено {len(news_items)} новостей')

            if limit is None:
                return news_items
            else:
                return news_items[:limit]

        except Exception as e:
            print(f'Ошибка: {e}')
            continue

    print('Все источники недоступны')
    return []


pprint.pprint(get_alternative_news_rss(limit=3))
