import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='a26c1fb030d47c3971b91dd7c8ab2b7',  # Replace with your Client ID
    client_secret='cc9251d714b54a238c34176a9bfc973e'  # Replace with your Client Secret
))


db_config = {
    'host': 'localhost',           # Change to your MySQL host
    'user': 'root',       # Replace with your MySQL username
    'password': 'dhivyaprabha',   # Replace with your MySQL password
    'database': 'spotify_db'       # Replace with your database name
}


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


track_url = "https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3"


track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)


track = sp.track(track_id)

track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)']
))
connection.commit()

print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")


cursor.close()
connection.close()

