import sqlite3
from sqlite3 import Error

class TableCreation():

    def create_table(conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object returned from create_connection
        :param create_table_sql: a CREATE TABLE statement as a string
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def clear_tables(conn):
        conn.cursor()
        
        artClear = """DROP TABLE artist;"""
        conn.execute(artClear)
        albClear = """DROP TABLE album;"""
        conn.execute(albClear)
        usrsngClear = """DROP TABLE user_song"""
        conn.execute(usrsngClear)
        songClear = """DROP TABLE song;"""
        conn.execute(songClear)
        usrClear = """DROP TABLE user;"""
        conn.execute(usrClear)

    def setup(conn):
        
        albTbl = '''CREATE TABLE album(
            albumID VARCHAR(255) PRIMARY KEY,
            albumTitle VARCHAR(255)
        );'''
        TableCreation.create_table(conn, albTbl)

        artTbl = '''CREATE TABLE artist(
            artistID VARCHAR(255) PRIMARY KEY,
            artistName VARCHAR(255),
            artistPopularity INTEGER
        );'''
        TableCreation.create_table(conn, artTbl)

        usrTbl = '''CREATE TABLE user(
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            userName VARCHAR(255)
        );'''
        TableCreation.create_table(conn, usrTbl)

        songTbl = '''CREATE TABLE song(
            songID VARCHAR(255) PRIMARY KEY,
            songTitle VARCHAR(255),
            songPopularity INTEGER,
            artistID VARCHAR(255),
            albumID VARCHAR(255),
            FOREIGN KEY (artistID) REFERENCES artist(artistID),
            FOREIGN KEY (albumID) REFERENCES album(albumID)
        );'''
        TableCreation.create_table(conn, songTbl)
        
        usrSong = '''CREATE TABLE user_song(
            user_songID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            songID VARCHAR(255),
            FOREIGN KEY (userID) REFERENCES user(userID),
            FOREIGN KEY (songID) REFERENCES song(songID)
        );'''
        TableCreation.create_table(conn, usrSong)
