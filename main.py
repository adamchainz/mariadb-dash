#!/usr/bin/env python3
import time
from pathlib import Path

import requests

BUILD = Path(__file__).parent.resolve() / 'build'


def main():
    print("Fetching article index JSON")
    articles = get_articles()

    print("Writing index.html")
    create_index(articles)

    total = len(articles)
    print("About to download {} articles...".format(total))

    for i, article in enumerate(articles, start=1):
        print("\rDownloading {i}/{n}".format(i=i, n=total), end='')
        download_article(article)


def get_articles():
    resp = requests.get('https://mariadb.com/kb/en/mariadb/+descendants/?format=dash')
    resp.raise_for_status()
    items = resp.json()
    return [item for item in items if item['type'] == 'article']


def create_index(articles):
    with open(str(BUILD / 'index.html'), 'w') as fp:
        fp.write('<html><body>')
        for article in articles:
            fp.write(
                '<a href="{id}.html">{id}</a>'.format(
                    id=article['id'],
                )
            )
        fp.write('</body></html>')


def download_article(article):
    resp = requests.get(article['url'])
    resp.raise_for_status()
    filename = BUILD / '{}.html'.format(article['id'])

    with open(str(filename), 'w') as fp:
        fp.write(resp.text)


if __name__ == '__main__':
    main()
