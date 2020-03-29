from collections import defaultdict
from Parse import Parse

#song info is artist name + song title essentially 
class Controller():

    def __init__(self):
        self.count = defaultdict()
        self.songs_db = defaultdict()
        self.queue = []
        return

    def add(self, song):
        if self.queue:
            prev = str(self.queue[0]['song_info'])
        else:
            prev = 'None'
        
        #song data is artist + song name
        song_data = song['song_info']
        print("Adding {} to the queue".format(song_data))

        if song_data not in self.count:
            self.count[song_data] = 0
        self.count[song_data] += 1

        if song_data not in self.songs_db:
            self.songs_db[song_data] = song

        while self.queue:
            self.queue.pop()

        # say you added papaoutai twice and tous les même once
        # count list would be [2,1]
        # not to be confused with self.count dict
        counts_list = sorted(list(set(self.count.values())))[::-1]
        #print(counts_list)

        while counts_list:
            temp = []
            for artist_song, song_data in self.songs_db.items():
                if self.count[artist_song] == counts_list[0]:
                    temp.append(song_data)

            counts_list.pop(0)
            temp.sort(key=lambda l: l['time_added'])

            for s in temp:
                self.queue.append(s)

            if str(self.queue[0]['song_info']) != prev:
                print("order has been changed: {} is now next".format(self.queue[0]['song_info']))

            
    def play_next(self):
        pass

    def play_current(self):
        pass

    def get_next(self):
        pass

    def reset(self):
        pass



def main():
    song_list = []
    song_list.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')
    song_list.append('https://open.spotify.com/track/1QFw2xxyQtgKjlrMCEqsNj?si=PC7TJMbUS7Sy-jJycXOueg')
    song_list.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')

    song_controller = Controller()
    for songs in song_list:
        song_info = Parse(songs)
        song_controller.add(vars(song_info))

main()



