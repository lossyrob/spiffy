# Spiffy: Make spotify playlists and such

Chat with Chat GPT to craft a playlist.

Then say:

```
Create a CSV of the playlist for me to 
download with two columns, "Artist" and "Track". 
The CSV should have a header. 
If there are multiple artists, separate their names by a comma. 
If a track features an artists, add them to the artist 
column and don't mention they are featured in the track title.
```

and then run:

```shell
> spiffy create-playlist -n "Chatbot Dreams of Electronica Sheep" path_to_playlist.csv
```

This will create a playlist for your spotify account.

## Setup

In a virtual environment, run

```
> python install -e .
```

Then create an .env with the following values:

```
SPIFFY_CLIENT_ID={Your Spotify Client App ID}
SPIFFY_CLIENT_SECRET={Your Spotify Client App ID}
SPIFFY_REDIRECT_URI=http://localhost:8080/callback
SPIFFY_USER_ID={Your Spotify User ID}
```

Ask Chatbot how to set up a spotify developer account and get your User ID.
