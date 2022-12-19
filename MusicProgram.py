import sqlite3
from sqlite3 import Error
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from apiAssist import apiAssist

cid = '2eba5df1ad974211815b9a0c86016f87'
secret = '79db4a574be8495fa88b59d02c082814'
redirect = 'http://127.0.0.1:9090/'
scope = "user-top-read"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=cid, 
    client_secret=secret,
    redirect_uri=redirect,
    scope=scope)
)

def get_userName():
    return apiAssist.get_user_name(sp)

def add_current_user(conn):
    usrName = apiAssist.get_user_name(sp)
    sql = f'''INSERT INTO user(userName) VALUES('{usrName}');'''
    cur = conn.cursor()
    cur.execute(sql)

    print('---- Top Songs for ' + usrName + ' ----')
    ## Now automatically add the users top songs to the song DB
    ## track details: [
    # 0 : songTitle
    # 1: songID
    # 2: ablumTitle
    # 3: albumID 
    # 4: artistName
    # 5: artistID 
    # 6: songPopularity
    # 7: artistPopularity ]
    top_tracks = apiAssist.get_top_songs(sp)
    for i in range(len(top_tracks)):
        if top_tracks[i][5] not in get_artistIDs(conn):
            cur.execute(f'''INSERT INTO artist(artistID, artistName, artistPopularity) VALUES('{top_tracks[i][5]}','{top_tracks[i][4]}', '{top_tracks[i][7]}');''')
        
        if top_tracks[i][3] not in get_albumIDs(conn):
            cur.execute(f'''INSERT INTO album(albumID, albumTitle) VALUES('{top_tracks[i][3]}','{top_tracks[i][2]}');''')
        
        if top_tracks[i][1] not in get_songIDs(conn):
            cur.execute(f'''INSERT INTO song(songID, songTitle, songPopularity, artistID, albumID) VALUES('{top_tracks[i][1]}','{top_tracks[i][0]}', '{top_tracks[i][6]}','{top_tracks[i][5]}', '{top_tracks[i][3]}');''')
        print('    ' + str(i+1) + ': ' + top_tracks[i][0] + ' by ' + top_tracks[i][4] + ' (' + str(top_tracks[i][6]) + ', ' + str(top_tracks[i][7]) + ')')
    conn.commit()

def insert_track(conn, track):
    cur = conn.cursor()
    if track[3] not in get_albumIDs(conn):
        cur.execute(f'''INSERT INTO album(albumID, albumTitle) VALUES('{track[3]}','{track[2]}')''')
    if track[5] not in get_artistIDs(conn):
        cur.execute(f'''INSERT INTO artist(artistID, artistName, artistPopularity) VALUES('{track[5]}','{track[4]}', '{track[7]}')''')
    if track[1] not in get_songIDs(conn):
        cur.execute(f'''INSERT INTO song(songID, songTitle, artistID, albumID) VALUES('{track[1]}','{track[0]}', '{track[5]}','{track[3]}')''')
    conn.commit()


def add_song(conn, song_url):
    print('adding track')
    track = apiAssist.get_song(sp, song_url)
    insert_track(conn, track)

def delete_song(conn, trackName):
    cur = conn.cursor()
    cur.execute(f'''DELETE FROM song WHERE songTitle LIKE '{trackName}';''')
    conn.commit()

def select_all(conn):
    cur = conn.cursor()
    cur.execute(r"""SELECT * FROM user U JOIN user_song US ON U.userID = US.userID JOIN song S ON US.songID = S.songID JOIN artist AR ON S.artistID = AR.artistID JOIN album AL ON S.albumID = AL.albumID;""")
    results = cur.fetchall()
    i = 0
    for row in results:
        print(str(i) + ': ' + row[0])

## Returns list of song IDs
def get_songIDs(conn):
    cur = conn.cursor()
    cur.execute(r"""SELECT songID FROM song S JOIN artist A ON S.artistID = A.artistID ORDER BY artistPopularity""")
    results = cur.fetchall()
    ids = []
    for row in results:
        ids.append(row[0])
    return ids

## Returns list of song names
def get_songTitles(conn):
    cur = conn.cursor()
    cur.execute(r"""SELECT songTitle FROM song""")
    results = cur.fetchall()
    ids = []
    for row in results:
        ids.append(row[0])
    return ids

## Returns list of artist IDs
def get_artistIDs(conn):
    cur = conn.cursor()
    cur.execute(r"""SELECT artistID FROM artist""")
    results = cur.fetchall()
    ids = []
    for row in results:
        ids.append(row[0])
    return ids

##Returns list of artist names
def get_artistNames(conn):
    cur = conn.cursor()
    cur.execute(r"""SELECT artistName FROM artist""")
    results = cur.fetchall()
    ids = []
    for row in results:
        ids.append(row[0])
    return ids

## Returns list of album IDs
def get_albumIDs(conn):
    cur = conn.cursor()
    cur.execute(r"""SELECT albumID FROM album""")
    results = cur.fetchall()
    ids = []
    for row in results:
        ids.append(row[0])
    return ids

## Returns list of album names
def get_albumTitles(conn):
    cur = conn.cursor()
    cur.execute(r"""SELECT albumTitle FROM album""")
    results = cur.fetchall()
    ids = []
    for row in results:
        ids.append(row[0])
    return ids


def get_albumFromSong(conn, songID):
    cur = conn.cursor()
    cur.execute(f'''SELECT albumTitle FROM album A JOIN song S ON A.albumID = S.albumID WHERE S.songID LIKE '{songID}';''')
    results = cur.fetchone()
    return results[0]

def get_artistFromSong(conn, songID):
    cur = conn.cursor()
    cur.execute(f'''SELECT artistName FROM artist A JOIN song S ON A.artistID = S.artistID WHERE S.songID LIKE '{songID}';''')
    results = cur.fetchone()
    return results[0]

def get_songTitleFromID(conn, songID):
    cur = conn.cursor()
    cur.execute(f'''SELECT songTitle FROM song WHERE songID LIKE '{songID}';''')
    results = cur.fetchone()
    return results[0]

def get_songPopFromID(conn, songID):
    cur = conn.cursor()
    cur.execute(f'''SELECT songPopularity FROM song WHERE songID LIKE '{songID}';''')
    results = cur.fetchone()
    return results[0]

def get_songImageURL(songID):
    return apiAssist.get_songImage(sp, songID)

def get_songIDFromURL(conn, song_url):
    track = apiAssist.get_song(sp, song_url)
    return track[1]

def get_artistFromArtistID(conn, artistID):
    cur = conn.cursor()
    cur.execute(f'''SELECT artistName FROM artist WHERE artistID LIKE '{artistID}';''')
    results = cur.fetchone()
    return results[0]

def get_artistPopFromID(conn, artistID):
    cur = conn.cursor()
    cur.execute(f'''SELECT artistPopularity FROM artist WHERE artistID LIKE '{artistID}';''')
    results = cur.fetchone()
    return results[0]

def get_artistImageURL(artistID):
    return apiAssist.get_artistImage(sp, artistID)
