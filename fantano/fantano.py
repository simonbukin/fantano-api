"""Get Fantano's music reviews with the YouTube API."""
import re

import requests

from auth import yt_key

yt_base_url = 'https://www.googleapis.com/youtube/v3/'


def get_all_yt_videos():
    """Generates a dump of all videos a channel contains."""
    next_page = None
    while True:
        vid_json = get_yt_videos(next_page=next_page)
        next_page = vid_json.get('nextPageToken')
        yield vid_json['items']
        if not next_page:
            break


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
    try:
        r = requests.get(video_url, params=payload)
        return r.json()
    except Exception as e:
        print('Error in get_yt_videos() with requests call: ', e)


def filter_snippets(json_dict):
    """Filter just snippets for YouTube API JSON"""
    return [item['snippet'] for item in json_dict]


def filter_reviews(json_dict):
    """Filter just EP/ALBUM reviews and NOT GOODs from all given videos."""
    filtered = []
    for video in json_dict:
        title = video['title'].lower()
        if 'review' in title or 'not good' in title:
            if ' ep ' in title:
                video['type'] = 'ep'
            else:
                video['type'] = 'album'
            filtered.append(video)
    return filtered


def update_rating(json_dict):
    """Update JSON dict with Fantano's rating."""
    rating_re = re.compile(r'\n*(\d+\/\d+)\n*')
    desc = json_dict['description']
    re_matches = rating_re.findall(desc)
    if re_matches:  # for all matches
        # length has to be less than 5 to match format of review
        # e.g. 10/10 -> 5 characters
        num_ratings = [match for match in re_matches if len(match) <= 5]
        for rating in num_ratings:
            rating_split = rating.split('/')
            if rating_split[-1] == '10':  # out of 10
                json_dict['rating'] = int(rating_split[0])
                return True
                break
    return False


def update_artist_album(json_dict):
    """Update a JSON file by parsing albums and artists."""
    bad_words = ['album', 'review']
    try:
        title = json_dict['title']
        title = [t for t in title.split() if t.lower() not in bad_words]
        title = ' '.join(title)
        artist, album, *rest = title.split('- ')
        json_dict['artist'], json_dict['album'] = artist.strip(), album.strip()
        return True
    except ValueError:
        return False


def update_batch(videos_json):
    """Update a batch of videos."""
    # Just snippets and only album reviews
    videos = filter_reviews(filter_snippets(videos_json))
    for video in videos:
        # only yield if both tests pass
        if update_rating(video) and update_artist_album(video):
            yield video
