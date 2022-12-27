# Install the required libraries
!pip install requests telegram json

import requests
import telegram
import json

# Replace YOUR_TELEGRAM_BOT_TOKEN with your bot's token
bot = telegram.Bot(token='5898438900:AAEYr7RKj3rpX-f4ZayS0nCBKPBbErQZRVs')

# Replace YOUR_GENIUS_API_TOKEN with your Genius API token
api_key = 'SuKMl854hIUgGOTrJTAw12mHLB8nTEckXEKzM-ngHaU-lQD2xQopqTeBtIjsiKnm'

# This function will be called to search for lyrics
def search_lyrics(song_name, artist_name):
  # Call the Genius API to search for the song
  api_endpoint = 'https://api.genius.com/search'
  params = {
    'q': f'{song_name} {artist_name}',
    'access_token': api_key
  }
  response = requests.get(api_endpoint, params=params)
  data = response.json()

  # Get the first song from the search results
  song = data['response']['hits'][0]['result']

  # Get the song's lyrics
  song_id = song['id']
  api_endpoint = f'https://api.genius.com/songs/{song_id}/lyric_annotations'
  params = {'access_token': api_key}
  response = requests.get(api_endpoint, params=params)
  data = response.json()
  annotations = data['response']['lyric_annotations']

  # Format the synced lyrics
  lyrics = ''
  for annotation in annotations:
    line = annotation['lyric'].strip()
    time = annotation['time']
    lyrics += f'[{time}] {line}\n'

  return lyrics

# This function will be called whenever the bot receives a message
def handle_message(message):
  # Check if the message is a command to download lyrics
  if message.text.startswith('/lyrics'):
    # Get the chat ID and the song name from the message
    chat_id = message.chat.id
    song_name = message.text[len('/lyrics'):].strip()
    
    # Call the Genius API to search for the song
    lyrics = search_lyrics(song_name, '')
    
    # Send the lyrics back to the user
    bot.send_message(chat_id=chat_id, text=lyrics)


# Start the bot's message loop
bot.set_update_listener(handle_message)
bot.polling()
