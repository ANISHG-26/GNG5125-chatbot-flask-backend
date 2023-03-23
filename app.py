from flask import Flask, jsonify, request
import re
import urllib.request
import urllib.parse
import pandas as pd
import random

# initialize our Flask application
app = Flask(__name__)


#Function for recommending other songs by a given artist
def songByArtist(content):
  artist = content['queryResult']['parameters']['music-artist'].lower()
  df = pd.read_csv('music_db.csv')
  #query the df to get the songs by a particular artist
  #output shows as [['shake it off'], ['you belong with me'], ['blank space'],...]]
  songs_by_artist = df.loc[df.artist.str.contains(artist),
                           ['song']].values.tolist()
  msg = ""
  if len(songs_by_artist) > 0:
    random.shuffle(songs_by_artist)
    songs = []
    
    for r in songs_by_artist:
      if len(songs_by_artist) > 3 and len(songs) < 3:   #for artists with more than 3 songs in the csv, list out just 3 songs
        songs.append(r[0].title())  #to get the list in the correct format
      elif len(songs_by_artist) < 3:    #for artists with less than 3 songs in the csv
        songs.append(r[0].title())
      
      
    if len(songs) > 0:   #if we know any songs by the artist
        msg = "Here are a few songs by " + artist.title() 
        for i in songs:
            msg+=", "+i

  else:   #if we don't know the artist
        msg = "I don't have any suggestions for this artist, sorry!"

  fulfilment_response = {"fulfillmentMessages": [{"text": {"text": [msg]}}]}
  return jsonify(fulfilment_response)


#Function for recommending popular song by artist
def popularSong(content):
  artist = content['queryResult']['parameters']['music-artist'].lower()
  df = pd.read_csv('music_db.csv')
  #query the df to get the songs by a particular artist where the popularity column is set as 1
  songs_by_artist = df.loc[(df.artist.str.contains(artist)) &
                           (df['popularity'] == 1), ['song']].values.tolist()
  if len(songs_by_artist) > 0:
    msg = songs_by_artist[0][0].title() + " is one of the popular songs by " + artist

  else:
    msg = "I'm sorry, I haven't heard of that artist."

  fulfilment_response = {"fulfillmentMessages": [{"text": {"text": [msg]}}]}
  return jsonify(fulfilment_response)




#Function for recommending song by genre
def songByGenre(content):
  genre = content['queryResult']['parameters']['music-genre'].lower()
  df = pd.read_csv('music_db.csv')
  #query the df to get the songs by a particular genre
  songs_list = df.loc[df.genre.str.contains(genre), ['song']].values.tolist()
  random.shuffle(songs_list)
  if len(songs_list) > 0:
    msg = songs_list[0][0].title() + " is one of the popular " + genre + " songs right now."

  else:
    msg = "I'm sorry, I don't have any data for that genre."

  fulfilment_response = {"fulfillmentMessages": [{"text": {"text": [msg]}}]}
  return jsonify(fulfilment_response)




#Function for recommending song by mood
def songByMood(content):
  mood = content['queryResult']['parameters']['mood'].lower()
  df = pd.read_csv('music_db.csv')
  #query the df to get the songs by a particular mood
  songs_list = df.loc[df.mood.str.contains(mood), ['song']].values.tolist()
  random.shuffle(songs_list)
  if len(songs_list) > 0:
    msg = songs_list[0][0].title() + " is one of the popular " + mood + " songs right now."

  else:
    msg = "I'm sorry, I don't have any data for that mood."

  fulfilment_response = {"fulfillmentMessages": [{"text": {"text": [msg]}}]}
  return jsonify(fulfilment_response)



#Function for recommending albums by artist
def getAlbum(content):
  artist = content['queryResult']['parameters']['music-artist'].lower()
  df = pd.read_csv('music_db.csv')
  #query the df to get the albums by a particular artist
  albums_by_artist = df.loc[df.artist.str.contains(artist),
                           ['album']]
  albums_by_artist = albums_by_artist.drop_duplicates()   #To stop albums from being repeated in the response we drop duplicates and empty values
  albums_by_artist = albums_by_artist.dropna()
  albums_by_artist = albums_by_artist.values.tolist()
  msg = ""
  if len(albums_by_artist) > 0:
    random.shuffle(albums_by_artist)
    albums = []
    
    for r in albums_by_artist:
      if len(albums_by_artist) > 3 and len(albums) < 3:   #for artists with more than 3 albums in the csv, list out just 3 albums
        albums.append(r[0].title())  #to get the list in the correct format
      elif len(albums_by_artist) < 3:    #for artists with less than 3 albums in the csv
        albums.append(r[0].title())
      
      
    if len(albums) > 0:   #if we know any albums by the artist
        msg = "Here are a few albums by " + artist.title() 
        for i in albums:
            msg+=", "+i

  else:   #if we don't know the artist
        msg = "I don't have any suggestions for this artist, sorry!"

  fulfilment_response = {"fulfillmentMessages": [{"text": {"text": [msg]}}]}
  return jsonify(fulfilment_response)




#Function for getting YT link of a song
def getYTLink(content):
  track = content['queryResult']['parameters']['song_name'].lower()
  artist = content['queryResult']['parameters']['music-artist'].lower()
  input = urllib.parse.urlencode({'search_query': track + ' by ' + artist})
  html = urllib.request.urlopen("http://www.youtube.com/results?" + input)
  try:
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    fulfilment_response = {
      "fulfillmentMessages": [{
        "text": {
          "text": [
            "Sure, here is the link to the music video for " + track.title() +
            " by " + artist.title() + "\n\n" +
            "https://www.youtube.com/watch?v=" + video_ids[0]
          ]
        }
      }]
    }
    return jsonify(fulfilment_response)
  except:
    fulfilment_response = {
      "fulfillmentMessages": [{
        "text": {
          "text": [
            "Sorry, I couldn't find that song on YouTube. Try again with a different song or artist"
          ]
        }
      }]
    }
    return jsonify(fulfilment_response)


@app.route('/')
@app.route('/home')
def home():
  return "App is running"


@app.route('/redirect', methods=["POST"])
def redirectToURLs():
  content = request.json
  intent = content['queryResult']['intent']['displayName'].lower()
  resp = {}
  if intent == 'youtube link':
    resp = getYTLink(content)
  elif intent == 'songbyartist':
    resp = songByArtist(content)
  elif intent == 'popular-song':
    resp = popularSong(content)
  elif intent == 'genres':
    resp = songByGenre(content)
  elif intent == 'mood':
    resp = songByMood(content)
  elif intent == 'album':
    resp = getAlbum(content)
  return resp


if __name__ == '__main__':
  app.run()