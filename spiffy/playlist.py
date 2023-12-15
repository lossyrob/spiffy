from pathlib import Path
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .config import Config

def create_playlist(csv_path: str, playlist_name: str, dry_run: bool = False) -> None:
    """Create a Spotify playlist from a CSV file."""
    config = Config()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                                   client_secret=config.client_secret,
                                                   redirect_uri=config.redirect_uri,
                                                   scope='playlist-modify-public'), requests_timeout=10)

    playlist_df = pd.read_csv(csv_path)

    track_ids = []
    for _, row in playlist_df.iterrows():
        artist_search = row['Artist']#.replace(" & ", ",")
        query = f"artist:{artist_search} track:{row['Track']}"
        try_count = 0
        while True:
            try:
                search_result = sp.search(query, type='track')
                break
            except TimeoutError:                
                try_count += 1     
                if try_count > 1:
                    raise
                else:
                    print(f"Timeout error. Trying again ({try_count}/2)")
        tracks = search_result['tracks']['items']
        if tracks:
            track = tracks[0]
            track_id = tracks[0]['id']
            track_ids.append(track_id)
            if dry_run:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                print(f"{row['Artist']} - {row['Track']}  ->  {artists} - {track['name']}")
        else:
            print(f"Couldn't find {row['Artist']} - {row['Track']}")

    if not dry_run:
        playlist = sp.user_playlist_create(config.user_id, playlist_name, public=True)
        sp.playlist_add_items(playlist['id'], track_ids)

        print(f"Playlist {playlist_name} created.")

def download_playlist(playlist_name):
    """Download a Spotify playlist as a CSV file based on its name."""
    config = Config()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                                   client_secret=config.client_secret,
                                                   redirect_uri=config.redirect_uri,
                                                   scope='playlist-read-private'))

    # Fetch the current user's playlists
    playlists = sp.current_user_playlists()
    playlist_id = None
    for item in playlists['items']:
        if item['name'].lower() == playlist_name.lower():
            playlist_id = item['id']
            break

    if not playlist_id:
        return "No playlist found with that name in the user's playlists."

    # Download the playlist tracks
    results = sp.playlist_tracks(playlist_id)
    tracks_data = []
    for item in results['items']:
        track = item['track']
        tracks_data.append({'Artist': track['artists'][0]['name'], 'Track': track['name']})

    df = pd.DataFrame(tracks_data)
    playlist_dir = Path('./playlists')
    playlist_dir.mkdir(exist_ok=True)
    csv_path = playlist_dir / f'{playlist_name}.csv'
    df.to_csv(csv_path, index=False)
    return f"Playlist '{playlist_name}' downloaded successfully as {csv_path}"