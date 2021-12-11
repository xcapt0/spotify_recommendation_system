#!/usr/bin/env python

from flask import Flask, render_template, request
from flask_mobility import Mobility

from api.spotify import SpotifyAPI


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
Mobility(app)

spotify = SpotifyAPI(
    client_id='CLIENT_ID',
    client_secret='CLIENT_SECRET',
    refresh_token='REFRESH_TOKEN'
)


@app.route('/')
@app.route('/tracks', methods=['GET'])
@app.route('/recs', methods=['GET'])
def spotify_app():
    if request.path == '/tracks' and request.args.get('q'):
        if request.args.get('offset'):
            search_results = spotify.search(request.args)
        else:
            search_results = spotify.search(request.args.get('q'))
        return render_template('track_list.html', tracks=search_results)
    elif request.path == '/recs' and request.args.get('id'):
        track_ids = spotify.recommend(request.args.get('id'))
        return render_template('recommendations.html', track_ids=track_ids)
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')