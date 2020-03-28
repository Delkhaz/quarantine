from collections import defaultdict
import requests
import json
import bs4


# caching the page so it doesnt get load so much
page_cache = defaultdict()

def cache(url):
    if url not in page_cache:
        respone = requests.get(url)
        page_cache[url] = bs4.BeautifulSoup(respone.text)
    return page_cache[url]

class Controller():

    def __init__(self):
        self.count = defaultdict()
        self.songs = defaultdict()
        self.queue = []
        return

    def add(self, song):
        pass

    def play_next(self):
        pass

    def play_current(self):
        pass

    def get_next(self):
        pass

    def reset(self):
        pass


def main():
    pass