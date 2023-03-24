import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify API client
client_id = 'xxx'
client_secret = 'xxx'
redirect_uri = 'xxx'
scopes = [
    'ugc-image-upload',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'app-remote-control',
    'streaming',
    'playlist-modify-public',
    'playlist-modify-private',
    'playlist-read-private',
    'playlist-read-collaborative',
    'user-follow-modify',
    'user-follow-read',
    'user-library-modify',
    'user-library-read',
    'user-read-email',
    'user-read-private'
]

scope_string = ' '.join(scopes)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope_string))

# Prompt user for genre and playlist name
genre = input("Enter a genre: ")
playlist_name = input("Enter a playlist name: ")

# Create new playlist
playlist_data = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=False)

# Get playlist ID from the response JSON
playlist_id = playlist_data['id']
print(f"Created playlist '{playlist_name}' with ID: {playlist_id}")

# Set up query parameters for genre search
params = {
    'q': f"genre:{genre}",
    'type': 'track',
    'market': 'US',
    'limit': 50,
    'offset': 0 # Add an initial value for the offset key
}

# Make GET requests to Spotify Web API to search for songs in genre
tracks_added = 0
while True:
    response = sp.search(**params)
        
    # Check if request was successful
    if response['tracks']['items'] == []:
        break
        
    # Parse the response JSON and add the tracks to the playlist
    tracks = response['tracks']['items']
    track_uris = [track['uri'] for track in tracks]
    sp.playlist_add_items(playlist_id, track_uris)
    tracks_added += len(track_uris)
        
    # Get the next page of results
    params['offset'] += params['limit'] # Update the offset value
    
print(f"Added {tracks_added} tracks to playlist '{playlist_name}'.")
