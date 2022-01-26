import unittest
import sys
import os
import yaml
import pandas as pd

path = os.path.dirname(sys.path[0])
sys.path.insert(0, path)
sys.path.insert(1, os.path.join(path, 'api'))

from api.spotify import SpotifyAPI
from api.preprocess import prepare_data


class TestSpotify(unittest.TestCase):
    def setUp(self):
        config = yaml.safe_load(open('config.yml'))

        self.spotify = SpotifyAPI(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            refresh_token=config['refresh_token']
        )

    def test_update_token(self):
        self.spotify._update_token()
        self.assertIsNotNone(self.spotify._access_token)

    def test_collect_all_data(self):
        track_ids = ['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ', '2takcwOaAZWiXQijPHIx7B']
        data = self.spotify._collect_all_data(track_ids)
        self.assertIsNone(data.get('error'))

        with self.assertRaises(AssertionError):
            self.spotify._collect_all_data([])
            self.spotify._collect_all_data('[]')

    def test_str_to_search_data(self):
        expected = {'q': 'track:test track', 'type': 'track', 'limit': 10, 'offset': 0}
        self.assertEqual(self.spotify._str_to_search_data('test track'), expected)

    def test_collect_related_tracks_data(self):
        n_artists = 5
        track_ids = ['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ', '2takcwOaAZWiXQijPHIx7B']
        liked_tracks = self.spotify._collect_all_data(track_ids)['tracks']
        data = self.spotify._collect_related_tracks_data({'tracks': liked_tracks}, n_artists)

        self.assertEqual(list(data.keys()), ['tracks', 'audio_features', 'artists'])
        self.assertGreater(len(data['tracks']), 0)
        self.assertGreater(len(data['audio_features']), 0)
        self.assertGreater(len(data['artists']), 0)

    def test_prepare_data(self):
        track_id = ['7ouMYWpwJ422jRcDASZB7P']
        liked_track = self.spotify._collect_all_data(track_id)
        related_tracks = self.spotify._collect_related_tracks_data(liked_track, 1)
        data = prepare_data(liked_track, related_tracks)

        self.assertIsInstance(data[0], pd.DataFrame)
        self.assertIsInstance(data[1], pd.DataFrame)
        self.assertGreater(len(data[1]), 0)


if __name__ == '__main__':
    unittest.main()