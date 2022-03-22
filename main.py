#SPDX-License-Identifier: MIT

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

date = input('Which year would you like to go back to, type in YYYY-MM-DD format.\n')
year = date.split('-')[0]
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

data = requests.get(URL).text
soup = BeautifulSoup(data,'html.parser')
raw_songs = soup.select('li h3')
songs = []
for song in raw_songs:
    songs.append(song.getText().strip())
songs = songs[:-7]
print(songs)

redirect_url = 'https://www.yigitbatki.com/'
client_id = 'YOUR_ID'
client_secret = 'YOUR_SECRET_KEY'
authorize_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/token'
scope = 'playlist-modify-private,playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_url,scope=scope,cache_path='token.txt'))
id = sp.current_user()['id']

end_songs = []

for e in songs:
    e = f'track:{e} year:{year}'
    search = sp.search(q=e,type='track',market='US')
    if len(search['tracks']['items']) > 0:
        song_id = search['tracks']['items'][0]['uri']
        end_songs.append(song_id)
print(len(end_songs))

playlist_name = f'{date} Top 100 songs'

sp.user_playlist_create(id,playlist_name,True,False,'This playlist was created with an automated script that was created with a ton of tears and blood shed.')
playlist_id = None

pprint.pprint(sp.user_playlists(id))
for e in sp.user_playlists(id)['items']:
    if e['name'] == playlist_name:
        playlist_id = e['id']
        break

print(end_songs)

for e in end_songs:
    sp.playlist_add_items(playlist_id,[e])
