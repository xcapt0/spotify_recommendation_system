import joblib
from sklearn.metrics.pairwise import cosine_similarity


def most_similar_tracks(df_liked_track, df_related_tracks, max_tracks=10):
    kmeans = joblib.load('models/kmeans.joblib')

    for tracks in [df_liked_track, df_related_tracks]:
        tracks['cluster'] = kmeans.predict(tracks.drop('id', axis=1))

    df_liked_track_cluster = df_liked_track['cluster'].iloc[0]
    related_clusters = df_related_tracks[df_related_tracks['cluster'] == df_liked_track_cluster]

    related_track_ids = related_clusters['id']
    df_liked_track = df_liked_track.drop('id', axis=1)
    related_clusters = related_clusters.drop('id', axis=1)

    related_clusters['similarity'] = cosine_similarity(related_clusters, df_liked_track)
    related_clusters['id'] = related_track_ids
    related_clusters = related_clusters.sort_values('similarity', ascending=False)
    related_clusters = related_clusters[related_clusters['similarity'] < 1]
    similar_track_ids = related_clusters['id'].values[:max_tracks]
    return similar_track_ids
