import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace YOUR_API_KEY with your Musixmatch API key
API_KEY = "41a14b0d4d727720f9553b7f5c0aff25"

def get_lyrics(artist, song_title):
  # Make a request to the Musixmatch API to search for the song
  search_url = "https://api.musixmatch.com/ws/1.1/track.search"
  search_params = {
      "apikey": API_KEY,
      "q_artist": artist,
      "q_track": song_title
  }
  search_response = requests.get(search_url, params=search_params)
  search_data = search_response.json()

  # Extract the track id from the search results
  track_id = search_data["message"]["body"]["track_list"][0]["track"]["track_id"]

  # Make a request to the Musixmatch API to get the lyrics for the track
  lyrics_url = "https://api.musixmatch.com/ws/1.1/track.lyrics.get"
  lyrics_params = {
      "apikey": API_KEY,
      "track_id": track_id
  }
  lyrics_response = requests.get(lyrics_url, params=lyrics_params)
  lyrics_data = lyrics_response.json()

  # Extract the lyrics from the API response
  lyrics = lyrics_data["message"]["body"]["lyrics"]["lyrics_body"]

  return lyrics

def lyrics(update, context):
  # Extract the artist and song title from the user's message
  message = update.message.text
  parts = message.split(" - ")
  if len(parts) != 2:
    update.message.reply_text("Invalid format. Please use the format 'Artist - Song Title'")
    return
  artist = parts[0]
  song_title = parts[1]

  # Get the lyrics for the song
  lyrics = get_lyrics(artist, song_title)

  # Send the lyrics to the user
  update.message.reply_text(lyrics)

def main():
  # Create the Updater and pass it your bot's token.
  # Make sure to set use_context=True to use the new context based callbacks
  # Post version 12 this will no longer be necessary
  updater = Updater("5898438900:AAH4oo2Ok1elgzd0gDgJqPsbJ0y5mFCEOZM", use_context=True)

  # Get the dispatcher to register handlers
  dp = updater.dispatcher

  # Add command handler to respond to the user's /lyrics command
  dp.add_handler(CommandHandler("lyrics", lyrics))

  # Add a message handler to respond to user messages that contain the string "lyrics"
  dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'lyrics'), lyrics))

  # Start the bot
  updater.start_polling()

 
