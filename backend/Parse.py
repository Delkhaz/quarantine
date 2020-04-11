# this is how we will parse urls
# urls can be from spotify youtube or applemusic.

from Song import Song
from collections import defaultdict

import requests
import bs4
import json
import os
import random
import time

page_cache = defaultdict(int)

# we parse off this
def cache(url):
    if url not in page_cache:
        respone = requests.get(url)
        page_cache[url] = bs4.BeautifulSoup(respone.text, "html.parser")
    return page_cache[url]

def to_json(string, part1, part2):
    rv = string.partition(part1)[2].partition(part2)[0] + '"}'
    return json.loads(rv)

def split_between(string, part1, part2):
    return string.partition(part1)[2].partition(part2)[0]

class Parse(Song):
    def __init__(self, url, download=True):

        # maps music platform to function
        music_map = {
            'spotify': self.parse_spotify
            #'youtube': self.parse_youtube
            #'music.apple.com': self.parse_apple_music,
        }

        self.url = url

        # if its not valid link then error
        parsed = self.parse_error

        # decide which function to call based on url
        # theres a better way to do this...
        for key, val in music_map.items():
            if key in url.lower():
                parsed = val
                break

        self.time_added = int(time.time())
        parsed()

    def parse_error(self):
        raise Exception("Error parsing URL: {}".format(self.url))

    def parse_spotify(self):
        page = cache(self.url)
                
        spotify_data = to_json(str(page), "Spotify.Entity = ", '"};')

        if 'album' in spotify_data:
            spotify_data = spotify_data['album']
        self.artist = spotify_data["artists"][0]["name"]
        self.song = page.title.string.partition(", a ")[0]
        self.album = spotify_data["name"]
        self.album_art = spotify_data["images"][0]['url']
        self.year = spotify_data["release_date"].partition("-")[0]
        self.song_info = "{}_{}".format(self.artist.replace(" ", "-"), self.song.replace(" ", "-")).lower()

        self.download()


    def download(self):
        if not os.path.exists("songs/{}.mp3".format(self.song_info)):
            os.system('youtube-dl --extract-audio --audio-format mp3 -o "songs/{}.%(ext)s" "ytsearch:{} {} lyrics"'.format(self.song_id, self.artist, self.song))
