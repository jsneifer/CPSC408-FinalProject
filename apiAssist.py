import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

class apiAssist():
    def get_user_name(sp):
        userName = sp.current_user()['display_name']
        return userName

    ## top_tracks: 3D array
    # #[[song name, songID, album name, albumID, artist name, artistID, songPopularity, artistPopularity]]
    def get_track_features(sp, i):
        meta = sp.track(i)
        # get meta data
        name = meta['name']
        if '\'' in name:
            name = name.replace('\'', '')

        nameID = meta['id']
        album = meta['album']['name']
        if '\'' in album:
            album = album.replace('\'', '')

        albumID = meta['album']['id']
        artist = meta['album']['artists'][0]['name']
        if "\'" in artist:
            artist = artist.replace('\'', '')

        artistID = meta['album']['artists'][0]['id']

        songPopularity = meta['popularity']
        artistPopularity = sp.artist(artistID)['popularity']

        track = [name, nameID, album, albumID, artist, artistID, songPopularity, artistPopularity]
        return track

    ## Returns a list of users top songs
    def get_top_songs(sp):
        top_tracks_short = sp.current_user_top_tracks(limit=10, offset=0, time_range="short_term")
        
        track_ids = []
        for song in top_tracks_short['items']:
            track_ids.append(song['id'])

        top_tracks = []
        for i in track_ids:
            track = apiAssist.get_track_features(sp, i)
            top_tracks.append(track)
        
        return top_tracks

    def get_song(sp, song_url):
        track = apiAssist.get_track_features(sp, sp.track(song_url)['id'])
        return track

    def get_songImage(sp, songID):
        imageURL = sp.track(songID)['album']['images'][0]['url']
        return imageURL

    def get_artistImage(sp, artistID):
        imageURL = sp.artist(artistID)['images'][0]['url']
        return imageURL