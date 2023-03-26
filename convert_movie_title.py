import requests
import json
from pprint import pprint
import ast


class TMDB:
    def __init__(self, token):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json;charset=utf-8'}        
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'
        
    def _json_by_get_request(self, url, params={}):
        res = requests.get(url, headers=self.headers_, params=params)
        print(res.url)
        return json.loads(res.text)   
    
    def search_movies(self, query):
        params = {'query': query}
        url = f'{self.base_url_}search/movie'
        return self._json_by_get_request(url, params)                    
        


token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZTUyMmM3MGFhYjNmMzZkNThkMTQ4NzBiN2UwZmQxZiIsInN1YiI6IjYzNDM3YTFkNjQ3NjU0MDA3ZjA4MjdmOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.8dSKKlYlOXjz04n_Y0uqIrdc_7yUfZ4ZRUleudXYVz4'

#ee522c70aab3f36d58d14870b7e0fd1f

api = TMDB(token)
res = api.search_movies("すずめの戸締り")
data_str = ",".join(map(str,res['results']))

#data = data_str.replace("'",'"')

#print(data_str)
rr = ast.literal_eval(data_str)

print(data_str)
print(rr['original_title'])

