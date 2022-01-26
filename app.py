#!/usr/bin/env python

from flask import Flask, render_template, request
from flask_mobility import Mobility
import yaml
import sys
import os

path = os.path.dirname(sys.path[0])
sys.path.insert(0, os.path.join(path, 'api'))

from api.spotify import SpotifyAPI


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
Mobility(app)

config = yaml.safe_load(open('config.yml'))
spotify = SpotifyAPI(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    refresh_token=config['refresh_token']
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