# this is how we will parse urls
# urls can be from spotify youtube or applemusic.

import time


class Parse():
    def __init__(self, url, download=True):

        # maps music platform to function 
        # based on which 
        music_map = {
            'spotify': self.parse_spotify,
            'youtube': self.parse_youtube,
            'music.apple.com': self.parse_apple_music
        }
        self.url = url

        for k,v in music_map.items():
            if k in url.lower():
                parsed = v
                break
        
        self.download = download

    def parse_spotify(self):
        pass

    # going to work on spotify only for rn
    def parse_youtube(self):
        pass

    def parse_apple_music(self):
        pass


def main():
    #test here
    pass

main()