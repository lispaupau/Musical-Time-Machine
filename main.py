import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
SPOTIPY_DISPLAY_NAME = os.environ.get('SPOTIPY_DISPLAY_NAME')

date = input('Which year do you want to travel to? Type the date this format YYYY-MM-DD: ')
URL = f'https://www.billboard.com/charts/hot-100/{date}/'

response = requests.get(url=URL).text

soup = BeautifulSoup(response, 'html.parser')
song_names_span = soup.select('li ul li h3')
song_names = [song.get_text().strip() for song in song_names_span]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path='token.txt',
        username=SPOTIPY_DISPLAY_NAME
    )
)
user_id = sp.current_user()['id']

song_uris = []
year = date.split('-')[0]
for song in song_names:
    result = sp.search(q=f'track:{song} year:{year}', type='track')
    print(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f'{song} doesn`t exist in Spotify. Skipped.')

playlist = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
