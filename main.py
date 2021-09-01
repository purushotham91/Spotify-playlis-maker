import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

# Authentication with spotify
client_id = "Your client id"
client_secret = "Your client secret"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    client_id=client_id,
    client_secret=client_secret,
    show_dialog=True,
    cache_path="token.txt"))

user_id = sp.current_user()["id"]

# Scraping the web
date = input("input the date in format(YYYY-MM-DD): ")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url=billboard_url)
billboard_data = response.text

soup = BeautifulSoup(billboard_data, "html.parser")

title_tags = soup.find_all(name="span", class_="chart-element__information__song")
titles = []
for title in title_tags:
    titles.append(title.getText())

# Searching for songs
song_uris = []
year = date.split("-")[0]

# pp = pprint.PrettyPrinter(indent=4)

for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    ## For tesing Purposes ##
    # if(song=="Stay"):
    #     pp.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist on Spotify. Skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)