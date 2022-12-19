import sqlite3
from sqlite3 import Error
import MusicProgram
from Interface import Interface
from TableCreation import TableCreation

def create_connection(db_fn):
        """ create a database connection to a SQLite database """
        conn = None # so our program doesn't crash later on if the connection was unsuccessful
        try:
            conn = sqlite3.connect(db_fn) # the actual connection step 
            print(sqlite3.version) # to check the version, not necessary 
            print ("Opened database successfully") 
            
        except Error as e:
                print(e) # if something goes wrong, tell the user what happened

        return conn

def main():

    conn = create_connection(r"userDB.db")


    # TableCreation.clear_tables(conn)
    # TableCreation.setup(conn)
    # MusicProgram.add_current_user(conn)

    ##MusicProgram.add_song(conn, 'https://open.spotify.com/track/2VsKJODsXzU1NtoFYIh9FM?si=93b368daf8104395')

    # MusicProgram.add_song(conn, 'https://open.spotify.com/track/5jyj2XKWILHQxDoz59ddCT?si=81c07b23cad541f8')

    

    print('database: ', MusicProgram.get_songTitles(conn))
    page = Interface(conn)
    print("Page load...")
    page.pageLayout()    

    conn.close()
    print("connection closed")
main()