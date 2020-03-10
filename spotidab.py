import json
import os
import sys
from time import sleep
import spotipy
import configparser
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from secrets import id, secret

class spotidab:

    def __init__(self, usrnm):
        self.sorting = [[],[]]
        self.username = usrnm
        self.liste_genre = []
        self.listArtist = []
        self.songs = []
        self.artists = []
        scope = 'user-library-read user-library-modify playlist-modify-private playlist-modify-public'
        token = util.prompt_for_user_token(self.username,
                           scope,
                           client_id=id,
                           client_secret=secret,
                           redirect_uri='https://google.com/')
        self.sp = spotipy.Spotify(auth=token)

    #get all the liked song from spotify for a user and save them into a list
    def get_liked(self):
        avalaible = True
        i = 0
        limite = 50
        while avalaible:
            offset = 50*i
            results = self.sp.current_user_saved_tracks(limit=str(limite), offset=str(offset))
            limite = len(results['items'])
            for item in results['items']:
                track = item['track']
                #self.song
                self.songs.append(track)
                #print(track['name'] + ' - ' + track['artists'][0]['name'])
            i += 1
            #stop the while when there's not 50 tracks left
            if limite != 50:
                avalaible = False
        print(">>>>> songs saved from liked : %d <<<<<\n"%len(self.songs))

    #Get the artist of each song and put it's ID in a list
    def get_all_artist(self):
        for result in self.songs:
            artist_id = (result['artists'])[0]['id']
            self.listArtist.append(artist_id)


    #find genre of the artist to link it to the song
    def find_genre(self):
        #get every genre list of every artist and store it in a list
        for elements in self.listArtist:
            genre = (self.sp.artist(elements))['genres']
            self.liste_genre.append(genre)

        #contains each "general" genre that ll be found
        self.sorting = [["hip hop"],["pop"]]
        found = False
        #Find genres that could be considered "general" in the list
        #go through each line of liste_genre
        for y in range(len(self.liste_genre)):
            index = 0
            #go through each genre in a line of liste_genre
            for z in range(len(self.liste_genre[y])):
                #go through the sorting array
                for i in range(len(self.sorting)):
                    if len(self.liste_genre[y])>0:
                        if (self.sorting[i][0]in self.liste_genre[y][z]):
                            found = True
                            index = i
                            break
                    if found:
                        break
            if not found:
                if len(self.liste_genre[y])>0:
                    recup = (self.liste_genre[y])[0].split()
                    #we add the last word of the genre if it's a composed genre
                    self.sorting.append([recup[len(recup)-1]])
                    self.sorting[len(self.sorting)-1].append((self.songs[y])['id'])
            else:
                found = False
                self.sorting[index].append((self.songs[y])['id'])

    def add_songs(self, songsid, playlistId):
        for i in range(len(songsid)-1):
            self.sp.user_playlist_add_tracks(self.username, playlistId,[songsid[i+1]], None)

    def create_playlist(self,numbers):
        for i in numbers:
            name = self.sorting[i-1][0]
            self.sp.user_playlist_create(user=self.username,name=name,public=True,description=name+" song genre")
            playlist = self.sp.user_playlists(user=self.username, limit=1)
            playlist = (playlist["items"])
            playlist = playlist[0]['id']
            self.add_songs(self.sorting[i-1],playlist)

    def afficher_genre(self):
        for i in range(len(self.sorting)):
            print(str(i+1) + ")" + self.sorting[i][0] + " - ", end='')
            print("") if (i+1)%10 == 0 else None

    def clean(self):
        self.liste_genre = None
        self.listArtist = None
        self.songs = None
        self.artists = None
