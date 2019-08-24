from flask import Flask
from flask_restful import Resource, Api

from fantano import open_db_connection, get_all_artist_ratings

app = Flask(__name__)
api = Api(app)


class GetRatingsByArtist(Resource):
    def get(self, artist):
        try:
            reviews = {}
            artist_tuple = (artist,)
            db = open_db_connection('fantano.db')
            reviews['reviews'] = get_all_artist_ratings(db, artist_tuple)
            return reviews
        except Exception as e:
            print(e)
            return {'error': e}


api.add_resource(GetRatingsByArtist, '/artists/<artist>')


if __name__ == '__main__':
    app.run(debug=True)
