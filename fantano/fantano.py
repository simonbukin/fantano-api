"""Test getting Fantano's videos with the YouTube API."""
import json
import re
import sqlite3

import requests

from auth import yt_key

yt_base_url = 'https://www.googleapis.com/youtube/v3/'


def load_json(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


def dump_json(filename, obj):
    with open(filename, 'w') as fp:
        json.dump(obj, fp, indent=2)


def get_all_yt_videos():
    """Return a JSON dump of all videos a channel contains."""
    next_page = None
    items = []
    while True:
        vid_json = get_yt_videos(next_page=next_page)
        next_page = vid_json.get('nextPageToken')
        items += vid_json['items']
        if not next_page:
            break
    return items


def get_yt_videos(next_page=None):
    """
        Return a JSON batch of videos with a given page.
        This is used a helper for get_all_yt_videos
    """
    video_url = yt_base_url + 'playlistItems?'
    payload = {
                'part': 'snippet',
                'maxResults': 50,
                'playlistId': 'UUt7fwAhXDy3oNFTAzF2o8Pw',
                'key': yt_key
    }
    if next_page:
        payload['pageToken'] = next_page
    print(payload)
    try:
        r = requests.get(video_url, params=payload)
        return r.json()
    except Exception as e:
        print('Error in get_yt_videos() with requests call: ', e)


def filter_snippets(source, dest):
    """Convert JSON to just contain snippets."""
    with open(source, 'r') as fp:
        items = json.load(fp)
    filtered = []
    for item in items:
        print(item['snippet'])
        filtered.append(item['snippet'])
    with open(dest, 'w') as fp:
        json.dump(filtered, fp, indent=2)


def get_album_reviews(source, dest):
    """Filter JSON down to just album reviews."""
    with open(source, 'r') as fp:
        videos = json.load(fp)
    album_reviews = []
    for video in videos:
        if 'ALBUM REVIEW' in video['title']:
            album_reviews.append(video)
    with open(dest, 'w') as fp:
        json.dump(album_reviews, fp, indent=2)


def update_ratings(file):
    """Update a JSON file by parsing ratings."""
    rating_re = re.compile(r'\n*(\d+\/\d+)\n*')
    for item in file:
        desc = item['description']
        re_ratings = rating_re.findall(desc)
        if re_ratings:
            num_ratings = [_ for _ in re_ratings if len(_) <= 5]
            for rating in num_ratings:
                rating_split = rating.split('/')
                if rating_split[-1] == '10':
                    item['rating'] = int(rating_split[0])
                    print(item)
                    break
    return file


def update_artist_album(file):
    """Update a JSON file by parsing albums and artists."""
    bad_words = ['album', 'review']
    err = 0
    for item in file:
        try:
            title = item['title']
            title = [t for t in title.split() if t.lower() not in bad_words]
            title = ' '.join(title)
            artist, album, *rest = title.split('- ')
            item['artist'], item['album'] = artist.strip(), album.strip()
        except ValueError:
            err += 1
    print(err)
    return file


def json_to_sqlite():
    pass


get_all_yt_videos()


# file = load_json('albums.json')
# update_ratings(file)
# update_artist_album(file)
# dump_json('updated.json', file)
