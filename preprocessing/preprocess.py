import pandas as pd
import joblib


# prepare data to use in model
def prepare_data(liked_track, related_tracks):
    preprocessor = joblib.load('models/preprocessor.joblib')
    liked_track = obtain_track_details(liked_track)
    related_tracks = obtain_track_details(related_tracks)
    df_liked_track = preprocess_df(preprocessor, to_df(liked_track))
    df_related_tracks = preprocess_df(preprocessor, to_df(related_tracks))
    return df_liked_track, df_related_tracks


# get track's data like track's info, features and genre
def obtain_track_details(tracks_data):
    track_details = []
    tracks = tracks_data['tracks']
    track_features = tracks_data['audio_features']
    artists = tracks_data['artists']

    for track, features, artist in zip(tracks, track_features, artists):
        features.update({
            'release_date': track['album']['release_date'],
            'popularity': track['popularity'],
            'genre': grab_genre(artist['genres'])
        })
        track_details.append(features)

    return track_details


# get only available genres
def grab_genre(track_genres):
    available_genres = ['hardstyle', 'techhouse', 'trance', 'techno', 'dnb',
                        'underground rap', 'dark trap', 'rap', 'edm', 'latin',
                        'trap', 'rock', 'r&b', 'hip hop', 'pop', 'emo']
    for track_genre in track_genres:
        for genre in available_genres:
            if genre == track_genre or genre in track_genre:
                return genre

    return 'hip hop'


def to_df(tracks):
    return pd.DataFrame(tracks)


# clearing data for model
def preprocess_df(preprocessor, df):
    df['genre'] = df['genre'].replace({'r&b': 'rnb'})
    df['year'] = df['release_date'].apply(lambda date: date.split('-')[0]).astype('int')
    preprocessed = pd.DataFrame(
        preprocessor.transform(df),
        columns=preprocessor.get_feature_names_out()
    )
    preprocessed['id'] = df['id']
    return preprocessed
