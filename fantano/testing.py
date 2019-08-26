from fantano import get_all_yt_videos, filter_snippets


for videos in get_all_yt_videos():
    filter_videos = filter_snippets(videos)
    for video in filter_videos:
        title = video['title'].lower()
        if ' ep ' in title or 'not good' in title:
            print(title)
