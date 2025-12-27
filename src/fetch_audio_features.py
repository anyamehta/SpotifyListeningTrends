import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Set up API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
))

# Load unique tracks
df = pd.read_csv('../data/clean_streaming_history.csv')
unique = df[['track', 'artist']].drop_duplicates()

audio_data = []

for _, row in unique.iterrows():
    query = f"track:{row['track']} artist:{row['artist']}"
    result = sp.search(q=query, type='track', limit=1)

    if result['tracks']['items']:
        track_id = result['tracks']['items'][0]['id']
        features = sp.audio_features(track_id)[0]
        if features:
            audio_data.append({
                'track': row['track'],
                'artist': row['artist'],
                **features
            })

pd.DataFrame(audio_data).to_csv('../data/audio_features.csv', index=False)
