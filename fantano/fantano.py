"""Test getting Fantano's videos with the YouTube API."""
import json

import requests

from auth import yt_key

yt_base_url = 'https://www.googleapis.com/youtube/v3/'

def get_yt_videos():
    video_url = yt_base_url + 'playlistItems?'
    payload = {
                'part': 'snippet',
                'maxResults': 50,
                'playlistId': 'UUt7fwAhXDy3oNFTAzF2o8Pw',
                'key': yt_key
    }
    try:
        r = requests.get(video_url, params=payload)
        return r.json()
    except Exception as e:
        print('Error in get_yt_videos() with requests call: ', e)

def convert_json(video_json):
    # videos = json.loads(video_json)
    for video in video_json['items']:
            if 'ALBUM REVIEW' in video['snippet']['title']:
                print(video['snippet']['description'])

convert_json(get_yt_videos())
