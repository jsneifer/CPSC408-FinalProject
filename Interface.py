import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error
import MusicProgram


class Interface:
    def __init__(self, connection):
        self.conn = connection

    # @st.cache
    # def InitializeDF(conn):
    #     print("Intializing DF...")
    #     songIDs = MusicProgram.get_songIDs(conn)
    #     song_dsp = []
    #     for i in (songIDs):
    #         print('adding track: ' + str(i))
    #         Interface.appendTrack(conn, i)

    ##@st.cache(allow_output_mutation=True)
    def get_data(self):
        songIDs = MusicProgram.get_songIDs(self.conn)

        song_dsp = {'song': [], 'artist': [], 'album': []}
        for i in songIDs:
            song_dsp['song'].append(MusicProgram.get_songTitleFromID(self.conn, i))
            song_dsp['artist'].append(MusicProgram.get_artistFromSong(self.conn, i))
            song_dsp['album'].append(MusicProgram.get_albumFromSong(self.conn, i))
        df = pd.DataFrame(song_dsp)

        return df

    def show_table(self):
        df = self.get_data()
        st.table(df)

    # def appendTrack(conn, trackID):
    #     new_row = pd.Series({
    #         'song': MusicProgram.get_songTitleFromID(conn, trackID), 
    #         'artist': MusicProgram.get_artistFromSong(conn, trackID), 
    #         'album': MusicProgram.get_albumFromSong(conn, trackID)
    #     })
    #     print('appending')
    #     Interface.song_df = pd.concat([Interface.song_df, new_row.to_frame().T], ignore_index=True)

    def SongPage(self, conn):
        st.header('Favorite Songs')
        col1, col2 = st.columns([1, 2], gap='small')
        with col1:
            images = []
            for i in MusicProgram.get_songIDs(conn):
                images.append(MusicProgram.get_songImageURL(i))
            st.image(images, width=85)
        with col2:
            self.show_table()
        with st.sidebar:
            with st.form('Add Song', clear_on_submit=True):
                song_url = st.text_input('Song Link:', placeholder='URL')
                submit_button = st.form_submit_button(label='Add New Entry')
            if submit_button and len(song_url) != 0:
                MusicProgram.add_song(conn, song_url)
                st.experimental_rerun()
            with st.form('Delete Song', clear_on_submit=True):
                song_name = st.selectbox('Choose Song to Delete', 
                self.get_data()
                )
                submit_button2 = st.form_submit_button(label='Delete Entry')
            if submit_button2:
                print(song_name)
                MusicProgram.delete_song(conn, song_name)
                st.experimental_rerun()
            


    def ArtistPage(conn):
        st.header('Favorite Artists')
        col1, col2, col3 = st.columns([1,1,1], gap='small')

        IDs = MusicProgram.get_artistIDs(conn)
        x=0
        while x < len(IDs):
            with col1:
                st.subheader(MusicProgram.get_artistFromArtistID(conn, IDs[x]))
                st.image(MusicProgram.get_artistImageURL(IDs[x]), caption=('POPULARITY: ' + str(MusicProgram.get_artistPopFromID(conn, IDs[x]))), width=120)
            with col2:
                if x+1 < len(IDs):
                    st.subheader(MusicProgram.get_artistFromArtistID(conn, IDs[x+1]))
                    st.image(MusicProgram.get_artistImageURL(IDs[x+1]), caption=('POPULARITY: ' + str(MusicProgram.get_artistPopFromID(conn, IDs[x+1]))), width=120)
            with col3:
                if x+2 < len(IDs):
                    st.subheader(MusicProgram.get_artistFromArtistID(conn, IDs[x+2]))
                    st.image(MusicProgram.get_artistImageURL(IDs[x+2]), caption=('POPULARITY: ' + str(MusicProgram.get_artistPopFromID(conn, IDs[x+2]))), width=120)
            x+=3

    def pageLayout(self):
        st.title('Music for ' + MusicProgram.get_userName())
        pageOne, pageTwo = st.tabs(['SONGS', 'ARTISTS'])
        with pageOne:
            Interface.SongPage(self, self.conn)
        with pageTwo:
            Interface.ArtistPage(self.conn)

