from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session, send_file
from Controller import Controller
from Parse import Parse
import random
import re
import datetime
import time
app = Flask(__name__, static_url_path='/static')


#init list testing
examples = []
examples.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')
examples.append('https://open.spotify.com/track/0BSPhsCKfwENstErymcD80?si=lFu4ibWpRRi6a8xCf3OAvw')
examples.append('https://open.spotify.com/track/1QFw2xxyQtgKjlrMCEqsNj?si=PC7TJMbUS7Sy-jJycXOueg')
examples.append('https://open.spotify.com/track/1GC1MIaRMW3kfVK9VyD5Ii?si=W9SEsuTcTH2zmgabE_8ajA')



song_controller = Controller()

for val in examples:
	songInfo = Parse(val)
	song_controller.add(vars(songInfo))

@app.route('/player', methods=['GET'])
def getPlayer():
	if not song_controller.queue:
		playing = None
	else:
		playing = song_controller.queue[0]
	return render_template("player.html", playing = playing, song_list = song_controller.queue[1:])


@app.route("/post_song", methods=["POST"])
def post_request():
	data = request.get_json()
	url = data['url']
	parsed_song = vars(Parse(url))
	song_controller.add(parsed_song)

	return 'yes ?'


@app.route("/get_current_album_artwork", methods=["GET"])
def get_current_album_artwork():
	return song_controller.queue[0]['album_art'] if song_controller.queue else ""


@app.route('/playCurrent', methods=["GET"])
def play_current_song():
	return send_file("songs/{}.mp3".format(song_controller.play_current()))

@app.route('/playNext', methods=["GET"])
def play_next_song():
	song_controller.play_next()
	#return "playing next"
	return send_file("songs/{}.mp3".format(song_controller.play_current()))


@app.route("/get_song_order", methods=["GET"])
def get_song_order():

	rv = ""
	for song in song_controller.queue[1:]:
		rv += '''
		<li href="#">

				<div class="song-detail">
				  <div class="row">
					<div class="col">
					  <h3>{}</h3>
					  <p><b>{}</b><br>{}</p>
					</div>
					<div class="col">
					  <div class="row mx-auto float-right float-right">
						<font size ="5"> {} </font>
					</div>
				  </div>
				</div>
			  </li>
			  <br>
		'''.format(song['song'], song['artist'], song['album'])
	return rv



@app.route("/get_current_song_info", methods=["GET"])
def get_current_song_info():
	if not song_controller.queue:
		return ""
	
	current_song = song_controller.queue[0]
	rv = """<center><div class="">
			  <h1>{}</h2>
			</div>
			<div class="">
			  <h3>{} | {}</h3>
			</div>
			""".format(current_song['song'], current_song['artist'], current_song['album'])
	return rv


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)
