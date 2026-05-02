# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 07:23:58 2023

@author: bebissig@gmail.com
References:
    - https://spotipy.readthedocs.io/
    - https://phoenixnap.com/kb/windows-set-environment-variable
    - https://www.section.io/engineering-education/spotify-python-part-1/#:~:text=The%20first%20step%20is%20to,can%20be%20whatever%20you%20want.
    - https://spotipy.readthedocs.io/en/2.22.1/?highlight=recently#spotipy.client.Spotify.current_user_recently_played
    
    - Apparently no API access to more then the 50 most recently played songs: https://community.spotify.com/t5/Spotify-for-Developers/Now-that-users-can-view-their-recently-played-tracks-in-the-apps/td-p/5181981
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import datetime
import time
import argparse
import os
from pathlib import Path
#from cred import client_id, client_secret, redirect_uri, username

def import_credentials():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    print(client_id)
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    username = os.getenv("SPOTIFY_USERNAME")
    redirect_uri = 'http://localhost:9000'
    return client_id, client_secret, redirect_uri, username
    
def get_playlist_tracks(sp,username,playlist_id):
    '''
    sp... spotipy API client instance
    username... spotify username
    playlist_id... playlist id (not name)
    '''
    playlist = sp.user_playlist(user=username,playlist_id=playlist_id) # dict with keys 'tracks'
    track_list = playlist['tracks']  #dict with key 'items', which values are the tracks
    tracks_list_items=track_list['items']

    while track_list['next']:
        print('next page')
        track_list=sp.next(track_list) # use the sp (the client) to go to next page, weird however why this needs be done on ['tracks'] level
        tracks_list_items.extend(track_list['items'])
    # tracks_list_items is a list of dicts. Each dict is a track. 
        # item in the list has keys: dict_keys(['added_at', 'added_by', 'is_local', 'primary_color', 'track', 'video_thumbnail'])
        # item['track'] in the list has keys: dict_keys(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'episode', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'])
        # item['track']['name'] is the tracks name
        # item['track']['artists'] can be a list of dicts of contributors
    return tracks_list_items

def get_playlist(sp,username,list_name):
    playlists=sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name']=='Mit Star bewertet':
            the_list=playlist
    return the_list 


def create_api_session(scope,client_id,client_secret, redirect_uri):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    return sp

def export_spotify_playlists(username,sp):
   
#    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    playlists = sp.user_playlists(username)

    # Create a dictionary to store the playlist titles and their tracks
    all_playlists = {}

    for playlist in playlists["items"]:
        if playlist["owner"]["id"] == username:
            playlist_title = playlist["name"]
            print(playlist_title)
            playlist_tracks_short = []
            playlist_tracks = get_playlist_tracks(sp=sp,username=username,playlist_id=playlist['id'])

            for item in playlist_tracks:     
#                print('\n')
#                print(item)
#                print(item['track']['name'])
                track_name = item['track']['name']
                artist_name = item["track"]["artists"][0]["name"]
                playlist_tracks_short.append((track_name,artist_name))
            all_playlists[playlist_title] = playlist_tracks_short

#    print(all_playlists)
    return all_playlists


def get_savepath_downloads(filename):


    # Get the user's profile directory
    user_profile = os.environ.get("USERPROFILE")
    # Create a path to the Downloads directory
    downloads_directory = Path(user_profile) / "Downloads"    
    # Create a path to the file in the Downloads directory
    file_path = downloads_directory / filename
    return file_path

def playlists_to_dataframe(all_playlists,to_clipboard = False, savefile="playlists.xlsx"):
    # Initialize an empty list to store the rows of the DataFrame
    rows = []
    
    # Iterate over each playlist in the all_playlists dictionary
    for playlist_title, playlist_tracks in all_playlists.items():
        # Iterate over each track in the playlist
        for track in playlist_tracks:
            # Split the track name and artist name using the " - " separator
            artist, title = track[0],track[1]
            # Append a new row to the list of rows
            rows.append({"Playlist": playlist_title, "Artist": artist, "Title": title})
    
    # Convert the list of rows into a pandas DataFrame
    df = pd.DataFrame(rows)
    savepath = get_savepath_downloads(savefile)
    
    if to_clipboard == True:
        df.to_clipboard()
    if savefile != None:
        df.to_excel(savepath, index=False)

    return df

def recently_played_to_dataframe(all_tracks,to_clipboard = False, savefile="recently_played.xlsx"):
    # Initialize an empty list to store the rows of the DataFrame
    rows = []
    # Iterate over each playlist in the all_playlists dictionary
    for track in all_tracks:
        # Split the track name and artist name using the " - " separator
        artist, title, date_played = track[0],track[1],track[2]
        # Append a new row to the list of rows
        rows.append({"Artist": artist, "Title": title,'Date_played':date_played})
    
    # Convert the list of rows into a pandas DataFrame
    df = pd.DataFrame(rows)
    savepath = get_savepath_downloads(savefile)
    
    if to_clipboard == True:
        df.to_clipboard()
    if savefile != None:
        df.to_excel(savepath, index=False)

    return df

def recently_played(sp,timestamp):   
    '''
    Problem: Only tracks that have been played to the end are on this list.
    '''
    # Get the user's recently played tracks
    number_tracks=50
    results = sp.current_user_recently_played(limit=number_tracks,after=timestamp)
#    print(results.keys())
#    print(results['next'])

    tracks_list = []
    while results['next']:
        print('next page of {}'.format(number_tracks))
        for item in results['items']:
#            print(item)
            track = item['track']
#            print(track['name'], '-', track['artists'][0]['name'],item['played_at'])
            tracks_list.append((track['name'], track['artists'][0]['name'],item['played_at']))
        results=sp.next(results)

#    print(tracks_list)
    return tracks_list

def datestring_to_timestamp(datestring):
    # Convert input date to datetime object
    dt = datetime.datetime.strptime(datestring, '%Y-%m-%d')
    # Convert datetime object to Unix timestamp in milliseconds
    unix_timestamp = int(time.mktime(dt.timetuple()))*1000    
    return unix_timestamp

def now_as_string():
    now = datetime.datetime.now()
    print('Now is: {}'.format(now.strftime("%y%m%d_%H%M%S")))
    return now.strftime("%y%m%d_%H%M%S")


def main(playlists_file='playlists',recently_file='recently_played', date_string='2023-01-01'):
    date_timestamp = datestring_to_timestamp(date_string)
    now_string = now_as_string()

    client_id, client_secret, redirect_uri, username = import_credentials()

    # Get and save playlists
    scope = "playlist-read-private"
    sp = create_api_session(scope=scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    all_playlists = export_spotify_playlists(username,sp)
    df_playlists = playlists_to_dataframe(all_playlists,to_clipboard = False, savefile="{}_{}.xlsx".format(now_string,playlists_file))

    # Get and save recently played (since date_string in yyyy-mm-dd)
    scope = "user-read-recently-played"
    sp = create_api_session(scope=scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    recently_list=recently_played(sp,date_timestamp)
    df_recently = recently_played_to_dataframe(recently_list,to_clipboard = False, savefile="{}_{}.xlsx".format(now_string,recently_file))

    return df_playlists, df_recently

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--playlistsfile', type=str, default='playlists', help='Description of arg1')
    parser.add_argument('--recentlyfile', type=str, default ='recently_played',help='Description of arg2')
    parser.add_argument('--datestring', type=str, default='2023-01-01',help='Description of arg2')
    args = parser.parse_args()
    print(args)


    playlist_file=args.playlistsfile
    recently_file=args.recentlyfile
    date_string=args.datestring
    main(playlist_file, recently_file, date_string)