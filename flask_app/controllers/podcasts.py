
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.podcast import Podcast
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv
import os

load_dotenv()

SCOPE = os.getenv('SCOPE')
USERNAME = os.getenv('USERNAME')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT = os.getenv('REDIRECT')




@app.route('/')
def display():
    return render_template('index.html')

@app.route('/podcast/search', methods=['POST'])
def podcast_search():
    if Podcast.validate_podcast(request.form) == False:
        return redirect('/')
    #take input from form
    podname = request.form['podcast_name']
    #create a token
    token = SpotifyOAuth(scope=SCOPE, username=USERNAME, client_id = CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = REDIRECT)
    spotifyObject = spotipy.Spotify(auth_manager = token)
    #take request.form input variable and pass into spotifyObject.search
    result = spotifyObject.search(q = podname, type = 'episode', limit = 1)
    print(json.dumps(result, sort_keys= 4, indent=4))
    
    #save json data to session
    session['podcast_img'] = result['episodes']['items'][0]['images'][0]['url']
    session['podcast_description'] = result['episodes']['items'][0]['description']

    return redirect('/')

@app.route('/save/podcast', methods=['POST'])
def save_podcast():
    podcast_data = {
        'img' : session['podcast_img'],
        'description' : session['podcast_description']
    }
    Podcast.save_podcast(podcast_data)
    return redirect('/saved/podcasts')

@app.route('/saved/podcasts')
def podcast_list():

    podcast_list = Podcast.get_all_podcasts()
    return render_template('saved_podcasts.html', podcast_list = podcast_list)

@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')