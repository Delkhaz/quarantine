# this is how we will parse urls
# urls can be from spotify youtube or applemusic.

from Song import Song
from collections import defaultdict
import time
import bs4
import requests
import json

page_cache = defaultdict()

#parsing this sucks
def cache(url):
    if url not in page_cache:
        respone = requests.get(url)
        page_cache[url] = bs4.BeautifulSoup(respone.text, "html.parser")
    return page_cache[url]

def to_json(string, part1, part2):
    rv = string.partition(part1)[2].partition(part2)[0] + '"}'
    return json.loads(rv)
    
class Parse(Song):
    def __init__(self, url, download=True):

        # maps music platform to function 
        # based on which 
        music_map = {
            'spotify': self.parse_spotify,
            'youtube': self.parse_youtube,
            'music.apple.com': self.parse_apple_music
        }
        self.url = url

        #decide which function to call based on url
        #theres a better way to do this
        for k,v in music_map.items():
            if k in url.lower():
                parsed = v
                break
        
        self.download = download
        parsed()

    def parse_spotify(self):
        page = cache(self.url)

        part1 = "Spotify.Entity = "
        part2 = '"};'

        spotify_data = to_json(str(page), part1, part2) 

        # to parse look at the json dump
        #print(json.dumps(spotify_data, indent=4, sort_keys=True))


        if 'album' in spotify_data:
            spotify_data = spotify_data['album']
        
        self.artist = spotify_data['artists'][0]['name']
        self.song = page.title.string.partition(", a ")[0]
        self.album = spotify_data['name']
        self.album_art = spotify_data["images"][0]['url']
        self.year = spotify_data["release_date"].partition("-")[0]
        self.song_info = "{}_{}".format(self.artist.replace(" ", "-"), self.song.replace(" ", "-")).lower()
        self.time_added = int(time.time())
        #self.song_info = (self.artist.replace(" ", "-")+ '_' + self.song.replace(" ", "-")).lower()

    # going to work on spotify only for rn
    def parse_youtube(self):
        pass

    def parse_apple_music(self):
        pass

