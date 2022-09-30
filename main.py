import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(".env")
sp = spotipy.Spotify(
        auth_manager= SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=os.getenv("REDIRECT_URI"),
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            show_dialog=True,
            cache_path=".cache"
        )
)

user = sp.current_user()
user_id = user["id"]

date = input("Which year would you like to listen to? YYYY-MM-DD:\n")

url = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url)
billboard_data = response.text
soup = BeautifulSoup(billboard_data, "html.parser")
song_list = [song.getText().strip("\n \t") for song in soup.find_all(name="h3", class_="a-no-trucate")]

year = date.split('-')[0]
song_uris = []
for song in song_list:
    try:
        song_data = sp.search(q=f"track: {song}, year: {year}", type="track")
        song_uri = song_data["tracks"]["items"][0]["uri"]
        song_uris.append(song_uri)
    except IndexError:
        print("Track not found on Spotify.")
        continue

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print(playlist["external_urls"]["spotify"])
