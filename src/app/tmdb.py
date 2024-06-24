import requests
from flask import session

class TMDBClient:
    BASE_URL = 'https://api.themoviedb.org/3'

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def verify_api_key(api_key):
        url = f'{TMDBClient.BASE_URL}/movie/popular?api_key={api_key}'
        response = requests.get(url)
        return response.status_code == 200

    def fetch_data(self, endpoint, id_param=None, params=None):
        url = f'{self.BASE_URL}/{endpoint}'
        if id_param:
            url += f'/{id_param}'
        params = params or {}
        params['api_key'] = self.api_key
        response = requests.get(url, params=params)
        return response.json()

    def fetch_media_list(self, media_type, search_query=None, genre_id=None):
        if search_query:
            endpoint = f'search/{media_type}'
            params = {'query': search_query}
        else:
            endpoint = f'discover/{media_type}'
            params = {'with_genres': genre_id} if genre_id else {}
        return self.fetch_data(endpoint, params=params)['results']

    def fetch_genres(self, media_type):
        endpoint = f'genre/{media_type}/list'
        return self.fetch_data(endpoint)['genres']

