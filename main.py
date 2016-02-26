#!/usr/bin/env python3
import time

import requests


def main():
    articles = get_articles()
    total = len(articles)
    print("About to download {} articles...".format(total))

    for i, article in enumerate(articles, start=1):
        print("\rDownloading {i}/{n}".format(i=i, n=total), end='')
        download_article(article)


def get_articles():
    resp = requests.get('https://mariadb.com/kb/en/mariadb/+descendants/?format=dash')
    resp.raise_for_status()
    return resp.json()

def download_article(article):
    resp = requests.get(article['url'])
    resp.raise_for_status()
    filename = '{}.html'.format(article['id'])

    with open(filename, 'w') as fp:
        fp.write(resp.text)


if __name__ == '__main__':
    main()
