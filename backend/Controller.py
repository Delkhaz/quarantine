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
        print(song)
        print('song')
        print('\n\n\n')
        if self.queue:
            prev = str(self.queue[0]['song_id'])
        else:
            prev = 'None'
        
        #for now each song is identifie by the artist + song name
        #example stromae_tous-les-mêmes
        song_id = song['song_id']
        
        print("Adding {} to the queue".format(song_id))

        if song_id not in self.count:
            self.count[song_id] = 0
        self.count[song_id] += 1

        if song_id not in self.songs_db:
            self.songs_db[song_id] = song

        while self.queue:
            self.queue.pop()

        # say you added papaoutai twice and tous les même once
        # count list would be [2,1]
        # not to be confused with self.count dict
        counts_list = sorted(list(set(self.count.values())))[::-1]
        #print(counts_list)

        while counts_list:
            temp = []
            for s_id, song_map in self.songs_db.items():
                if self.count[s_id] == counts_list[0]:
                    temp.append(song_map)

            counts_list.pop(0)
            temp.sort(key=lambda l: l['time_added'])

            for s in temp:
                self.queue.append(s)

            if str(self.queue[0]['song_id']) != prev:
                print("order changed: {} is next".format(self.queue[0]['song_id']))
        
        #print('\n\n')
        print('self.queue')
        '''
        for i in self.queue:
            for k,v in i.items():
                print(v)
        '''
            
    def play_next(self):
        if not self.queue:
            return None
        next_song = self.queue.pop(0)
        del self.songs_db[next_song['song_id']]
        del self.count[next_song['song_id']]
        return next_song['song_id']

    def play(self):
        return self.queue[0]['song_id'] if not self.queue else None





def main():
    song_list = []
    song_list.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')
    song_list.append('https://open.spotify.com/track/0BSPhsCKfwENstErymcD80?si=lFu4ibWpRRi6a8xCf3OAvw')
    song_list.append('https://open.spotify.com/track/1QFw2xxyQtgKjlrMCEqsNj?si=PC7TJMbUS7Sy-jJycXOueg')
    song_list.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')

    song_controller = Controller()
    for songs in song_list:
        song = Parse(songs)
        
        song_controller.add(vars(song))

    

#main()



