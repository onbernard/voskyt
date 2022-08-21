from vosk import KaldiRecognizer, Model
import tempfile 
import ffmpeg
import json
from youtube_transcript_api import YouTubeTranscriptApi
import youtube_dl
import os

from youtube import extract_id_from_url, make_ydl_options
from config import available_languages


def process_video(url, model_value):
    model = Model(lang=available_languages[model_value]['lang'])
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)
    vosk_transcript = []
    yt_transcript = YouTubeTranscriptApi.get_transcript(extract_id_from_url(url))
    with tempfile.TemporaryDirectory() as tempdirname, youtube_dl.YoutubeDL(make_ydl_options(tempdirname)) as ydl:
        meta = ydl.extract_info(url, download=True)
        id = meta['id']
        ext = meta['ext']
        video_duration = meta['duration']
        audio_decode = (
                ffmpeg
                .input(os.path.join(tempdirname, f"{id}.{ext}"))
                .output('pipe:', format='s16le', ac=1, ar='16k')
                .run_async(pipe_stdout=True)
            )
        while True:
            data = audio_decode.stdout.read(4000)
            if not data:
                break 
            if rec.AcceptWaveform(data):
                vosk_transcript.append(json.loads(rec.FinalResult()))
        audio_decode.wait()
    all_transcripts = {'vosk': process_vosk_transcript(vosk_transcript,video_duration), 'yt': process_yt_transcript(yt_transcript,video_duration)}
    with open('log.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(all_transcripts, indent=4))
    return all_transcripts

def process_yt_transcript(transcript, video_duration):
    captions = []
    for line in transcript:
        captions.append({
            'text': line['text'],
            'start': line['start'],
            'end': line['start'] + line['duration'],
            'duration': line['duration']
        })
    for i,line in enumerate(captions):
        if i==len(captions)-1:
            line['height'] = video_duration - line['start']
        else:
            line['height'] = (captions[i+1]['start'] - line['start'])
    for line in captions:
        line['style'] = gen_container_style(line)
    outp = {}
    if len(captions)!=0:
        h = captions[0]['start']
        outp['offset'] = f"min-height: {h*4:.2f}rem; height:{h*4:.2f}rem;"
    outp['captions'] = captions
    return outp

def process_vosk_transcript(transcript, video_duration):
    captions = []
    for _,line in enumerate(transcript):
        if 'result' in line.keys():
            captions.append({
                'text': line['text'],
                'start': line['result'][0]['start'],
                'end': line['result'][-1]['end'],
                'duration': line['result'][-1]['end'] - line['result'][0]['start']
            })
    for i,line in enumerate(captions):
        if i==len(captions)-1:
            line['height'] = video_duration - line['start']
        else:
            line['height'] = (captions[i+1]['start'] - line['start'])
    for line in captions:
        line['style'] = gen_container_style(line)
    outp = {}
    if len(captions)!=0:
        h = captions[0]['start']
        outp['offset'] = f"min-height: {h*4:.2f}rem; height:{h*4:.2f}rem;"
    outp['captions'] = captions
    return outp

def gen_container_style(line):
    return f"min-height: {line['height']*4:.2f}rem; height:{line['height']*4:.2f}rem;"