# coding=utf-8

from collections import defaultdict
from Parse import Parse
import requests
import bs4
import json
import time
import os
import random




examples = []
examples.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')
examples.append('https://open.spotify.com/track/0BSPhsCKfwENstErymcD80?si=lFu4ibWpRRi6a8xCf3OAvw')
examples.append('https://open.spotify.com/track/1QFw2xxyQtgKjlrMCEqsNj?si=PC7TJMbUS7Sy-jJycXOueg')
examples.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')



# This is going to do the song ranking
class Controller():

	def __init__(self):
		self.count = defaultdict(int)
		self.songs_db = defaultdict(int)
		self.queue = []
		return

	def add(self, song):
		#print(song)
		if self.queue:
			prev = str(self.queue[0]['song_info'])
		else:
			prev = 'None'
		
		#for now each song item is identified by the artist + song name
		#example stomae_tous-les-memes
		song_id = song['song_info']
		print("Adding {} to the queue".format(song_id))

		# add to queue, if its the songs first time in the queue then its count is 0
		# if its already in the queue then we inc the counter
		if song_id not in self.queue:
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
			temp.sort(key=lambda k: k['time_added'])

			for s in temp:
				self.queue.append(s)

		if str(self.queue[0]['song_info']) != prev:
			print("queue order changed!: {} is now next".format(self.queue[0]['song_info']))

	def play_next(self):
		if not self.queue:
			return None
		
		next_song = self.queue.pop(0)
		
		del self.songs_db[next_song['song_info']]
		del self.count[next_song['song_info']]
		return next_song['song_info']
		

	def play_current(self):
		return self.queue[0]['song_info'] if self.queue else None

	def get_next(self):
		return self.queue[0]['song_info'] if self.queue else None


def main():
	song_controller = Controller()
	
	for song in examples:
		parsed_song = Parse(song)
		song_controller.add(vars(parsed_song))

	for i in range(4):
		song = song_controller.play_next()
		print("Playing: {} | Next Song: {}".format(song, song_controller.get_next()))

