#from flask import Flask
from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session, send_file

from Controller import Controller
from Parse import Parse

import random
import time
 


app = Flask(__name__, template_folder='../frontend')

#init list testing
song_list = []
song_list.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')
song_list.append('https://open.spotify.com/track/0BSPhsCKfwENstErymcD80?si=lFu4ibWpRRi6a8xCf3OAvw')
song_list.append('https://open.spotify.com/track/1QFw2xxyQtgKjlrMCEqsNj?si=PC7TJMbUS7Sy-jJycXOueg')
song_list.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')

song_controller = Controller()
for songs in song_list:
    song = Parse(songs)
    song_controller.add(vars(song))


@app.route('/post_song', methods = ["POST"])
def post_song():
    data = request.get_json()
    url = data['url']
    parsed_song = vars(Parse(url))
    song_controller.add(parsed_song)

    return 'yes sir'
    
@app.route('/get_curr_album_art', methods = ["GET"])
def get_curr_album_art():
    if not song_controller.queue:
        return ''
    return song_controller.queue[0]['album_art']

@app.route('/play', methods=["GET"])
def playy():
    return send_file("songs/{}.mp3".format(song_controller.play()))

@app.route('/play_next', methods=["GET"])
def next_song():
    song_controller.play_next()
    return send_file("songs/{}.mp3".format(song_controller.play()))

@app.route('/player', methods=['GET'])
def player():
    return render_template('home.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)