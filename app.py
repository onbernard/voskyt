from flask import Flask, render_template, request, jsonify

from youtube import get_video_metadata, list_youtube_tracks
from video_processing import process_video
from config import initialize_vosk, available_languages


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/transcript', methods=['POST'])
def transcript():
    # TODO: maybe check further validity of inputs
    url = request.form['url']
    if not url:
        return jsonify({'success': False, 'error': 'No url supplied'})
    yt_track = request.form['yt']
    if not yt_track:
        return jsonify({'success': False, 'error': 'No subtitle track supplied'})
    ml_model = request.form['ml']
    if not ml_model:
        return jsonify({'success': False, 'error': 'No ml model supplied'})
    try:
        transcript = process_video(url, (int(ml_model)))
    except Exception as e:
        content = {
            'success': False, 
            'error': 'There was a problem processing the video: ' + str(e)
        }
        return jsonify(content)
    else:
        content = {
            'success': True,
            'transcript': render_template('transcript.html', yt_captions=transcript['yt'], ml_captions=transcript['vosk'])
        }
        return jsonify(content)


@app.route('/tracks', methods=['POST'])
def get_tracks():
    # TODO: maybe check further validity of inputs
    url = request.form['url']
    if not url:
        content = {
            'success': False,
            'error': 'No url supplied'
        }
        return jsonify(content)
    try:
        yt_tracks = list_youtube_tracks(url)
        meta = get_video_metadata(url)
    except Exception as e:
        content = {
            'success': False,
            'error': 'There was a problem retrieving video metadata: ' + str(e)
        }
        return jsonify(content)
    else:
        content = {
            'success': True,
            'yt_tracks': yt_tracks,
            'ml_tracks': available_languages,
            'thumbnail': meta['thumbnail']
        }
        return jsonify(content)

if __name__=="__main__":
    # initialize_vosk()
    app.run()
