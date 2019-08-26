"""
fantano/query.py
Handles all queries to the Fantano db.
"""


def get_all_artist_reviews(db, artist):
    """Get all artist reviews given an artist name."""
    c = db.cursor()
    query = '''
        SELECT videoid, artist, album, rating FROM fantano WHERE artist=?
    '''
    c.execute(query, artist)
    reviews = []
    for review in c.fetchall():
        reviews.append({
            'video_id': review[0],
            'artist': review[1],
            'album': review[2],
            'rating': review[3]
        })
    return reviews


def get_all_albums_by_rating(db, rating):
    """Get all albums that have a specific rating."""
    c = db.cursor()
    query = '''
        SELECT videoid, artist, album, rating FROM fantano WHERE rating=?
    '''
    c.execute(query, rating)
    reviews = []
    for review in c.fetchall():
        reviews.append({
            'video_id': review[0],
            'artist': review[1],
            'album': review[2],
            'rating': review[3]
        })
    return reviews


def get_album_reviews(db, album):
    """Get all albums that match an album name."""
    c = db.cursor()
    query = '''
        SELECT videoid, artist, album, rating FROM fantano WHERE album=?
    '''
    c.execute(query, album)
    reviews = []
    for review in c.fetchall():
        reviews.append({
            'video_id': review[0],
            'artist': review[1],
            'album': review[2],
            'rating': review[3]
        })
    return reviews
