from youtube_transcript_api import YouTubeTranscriptApi
import youtube_dl
import os
from urllib.parse import urlparse, parse_qs


def list_youtube_tracks(url):
    video_id = extract_id_from_url(url)
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    outp = []
    for index,tcpt in enumerate(transcripts):
            outp.append({'value':index, 'label':tcpt.language_code})
    return outp


def make_ydl_options(dirname=__file__):
    return {
        'format': 'bestaudio/best',
        'outtmpl': f'{os.path.join(dirname, "%(id)s.%(ext)s")}',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }]
    }

def get_video_metadata(url):
    with youtube_dl.YoutubeDL(make_ydl_options()) as ydl:
        meta = ydl.extract_info(url, download=False)
    return meta

def extract_id_from_url(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None