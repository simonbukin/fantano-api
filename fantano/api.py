from flask import Flask
from flask_restful import Resource, Api

from fantano import (open_db_connection,
                     get_all_artist_reviews,
                     get_all_albums_by_rating,
                     get_album_reviews)


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(GetReviewsByArtist, '/artists/<artist>')
    api.add_resource(GetReviewsByRating, '/ratings/<rating>')
    api.add_resource(GetAlbumReview, '/albums/<album>')

    return app


class GetReviewsByArtist(Resource):
    """Get all reviews for a given artist name."""
    def get(self, artist):
        try:
            reviews = {}
            artist_tuple = (artist,)
            db = open_db_connection('fantano.db')
            reviews['reviews'] = get_all_artist_reviews(db, artist_tuple)
            return reviews
        except Exception as e:
            return {'error': e}


class GetReviewsByRating(Resource):
    """Get all reviews for a given rating."""
    def get(self, rating):
        try:
            reviews = {}
            rating_tuple = (rating,)
            db = open_db_connection('fantano.db')
            reviews['reviews'] = get_all_albums_by_rating(db, rating_tuple)
            return reviews
        except Exception as e:
            return {'error': e}


class GetAlbumReview(Resource):
    """
    Get a specific album review.
    Note: For duplicate album names, all matching albums are returned.
    """
    def get(self, album):
        try:
            reviews = {}
            album_tuple = (album,)
            db = open_db_connection('fantano.db')
            reviews['reviews'] = get_album_reviews(db, album_tuple)
            return reviews
        except Exception as e:
            return {'error': e}


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
