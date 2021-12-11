import requests as r
from base64 import b64encode
import random
import time

from preprocessing import prepare_data
from api.model import most_similar_tracks


class SpotifyAPI:
    def __init__(self, client_id, client_secret, refresh_token):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__refresh_token = refresh_token
        self.__last_updated = time.time()
        self.__update_token()

    # find tracks by track's name
    def search(self, track_name):
        url = 'https://api.spotify.com/v1/search'
        if isinstance(track_name, dict):
            track = track_name.get('q').replace('track:', '')
            search_data = self.__str_to_search_data(track, offset=track_name.get('offset'))
            tracks_data = self._api_request(url).json().get('tracks')
        else:
            search_data = self.__str_to_search_data(track_name)
        tracks_data = self._api_request(url, params=search_data).json().get('tracks')

        return self.__search_response(tracks_data)

    # recommend tracks by liked track
    def recommend(self, track_id, n_artists=5):
        liked_track = self.__collect_all_data([track_id])
        related_tracks = self.__collect_related_tracks_data(liked_track, n_artists)
        df_liked_track, df_related_tracks = prepare_data(liked_track, related_tracks)
        similar_tracks = most_similar_tracks(df_liked_track, df_related_tracks)
        return similar_tracks

    def _api_request(self, *args, **kwargs):
        self.__check_if_token_expired()
        return self.__fetch(*args, **kwargs)

    def __fetch(self, url, params=None, data=None, headers_type='api', request_type='get'):
        headers = self.__get_headers(headers_type)
        if request_type.lower() == 'get':
            return r.get(url, headers=headers, params=params)
        elif request_type.lower() == 'post':
            return r.post(url, headers=headers, data=data)
        else:
            raise ValueError('Invalid request type. Only GET and POST are supported')

    def __update_token(self):
        url = 'https://accounts.spotify.com/api/token'
        auth_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.__refresh_token,
            'redirect_uri': 'http://localhost:8888/callback'
        }
        auth_data = self._api_request(url, data=auth_data, headers_type='auth', request_type='post')
        assert auth_data.status_code == 200, auth_data.json()['error_description']
        self.__access_token = auth_data.json()['access_token']

    def __get_headers(self, headers_type):
        if headers_type.lower() == 'api':
            return {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.__access_token}'
            }
        elif headers_type.lower() == 'auth':
            auth_token = b64encode(str.encode(f'{self.__client_id}:{self.__client_secret}'))
            return {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {auth_token.decode("utf-8")}'
            }
        else:
            raise ValueError('Invalid headers type. Only "api" and "auth" are supported')

    def __check_if_token_expired(self):
        seconds, minutes = 60, 60
        time_passed_hours = (time.time() - self.__last_updated) / seconds / minutes
        if time_passed_hours > 50:
            self.__update_token()

    # get all tracks' data like tracks' info, tracks' artist and tracks' features
    def __collect_all_data(self, track_ids_list):
        assert isinstance(track_ids_list, list), "parameter 'track_ids_list' must be list of track ids"

        data = {}
        track_ids = ','.join(track_ids_list)
        urls = [
            f'https://api.spotify.com/v1/tracks?ids={track_ids}',  # tracks' info
            f'https://api.spotify.com/v1/audio-features?ids={track_ids}'  # tracks' features
        ]

        for url in urls:
            json_tracks_data = self._api_request(url).json()
            data.update(json_tracks_data)

        artist_tracks = self.__artist_tracks(data['tracks'])
        data.update(artist_tracks)
        return data

    def __artist_tracks(self, tracks):
        artist_ids = [track['album']['artists'][0]['id'] for track in tracks]
        ids_query = ','.join(artist_ids)
        url = f'https://api.spotify.com/v1/artists?ids={ids_query}'
        return self._api_request(url).json()

    def __collect_related_tracks_data(self, liked_track, n_artists):
        artists = self.__related_artists(liked_track, n_artists)
        track_ids = self.__related_artist_tracks(artists)
        tracks_data = self.__collect_all_data(track_ids)
        return tracks_data

    def __related_artists(self, liked_track, n_artists):
        artist_id = liked_track['tracks'][0]['album']['artists'][0]['id']
        url = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
        artists = self._api_request(url).json()
        return random.sample(artists['artists'], n_artists)

    def __related_artist_tracks(self, artists):
        track_ids = []

        for artist in artists:
            artist_id = artist['id']
            url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=es'
            top_tracks = self._api_request(url).json()
            track_ids += [track['id'] for track in top_tracks['tracks']]

        return track_ids

    # prepare api's links
    @staticmethod
    def __search_response(data):
        replacements = [
            ('https://api.spotify.com/v1/search', '/tracks'),
            ('query', 'q')
        ]

        for key in ['previous', 'next']:
            for old_str, new_str in replacements:
                if data[key]:
                    data[key] = data[key].replace(old_str, new_str)

        return {
            'items': data['items'],
            'previous': data['previous'],
            'next': data['next']
        }

    @staticmethod
    def __str_to_search_data(track_name, limit=10, offset=0):
        q = f'track:{track_name.lower()}'
        return {'q': q, 'type': 'track', 'limit': limit, 'offset': offset}
