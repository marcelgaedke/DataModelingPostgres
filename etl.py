import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Reads a single Song JSON File and populates song and artist tables."""
    # open song file
    df = pd.read_json(filepath,lines=True)

    # insert song record
    song_data_df = df[['song_id', 'title', 'artist_id','year','duration']]
    for i,row in song_data_df.iterrows():
        song_data = list(row)
        cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data_df = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]
    for i,row in artist_data_df.iterrows():
        artist_data = list(row)
        cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Reads a single Log JSON File and polulates time, users and songplays tables."""
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    time_data = ([int(ts.timestamp()), ts.hour, ts.day,ts.week,ts.month,ts.year,ts.weekday()] for ts in t)
    column_labels = (['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday'])
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, list(row))

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)

        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Gets a list of all files in filepath and subdirectories and calls a function on all the files."""
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Main Function to process all song- and log Data."""
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()