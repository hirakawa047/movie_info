import requests
import json
from pprint import pprint

class TMDB:
    def __init__(self, token):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json;charset=utf-8'}        
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'

    def _json_by_get_request(self, url, params={}):
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)   

    def search_movies(self, query):
        params = {'query': query}
        url = f'{self.base_url_}search/movie'
        return self._json_by_get_request(url, params)                    

    def get_movie(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}'
        return self._json_by_get_request(url)

    def get_movie_account_states(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/account_states'
        return self._json_by_get_request(url)    

    def get_movie_alternative_titles(self, movie_id, country=None):
        url = f'{self.base_url_}movie/{movie_id}/alternative_titles'
        return self._json_by_get_request(url)    

    def get_movie_changes(self, movie_id, start_date=None, end_date=None):
        url = f'{self.base_url_}movie/{movie_id}'
        return self._json_by_get_request(url)    

    def get_movie_credits(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/credits'
        return self._json_by_get_request(url)   

    def get_movie_external_ids(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/external_ids'
        return self._json_by_get_request(url)

    def get_movie_images(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/images'
        return self._json_by_get_request(url)        

    def get_movie_keywords(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/keywords'
        return self._json_by_get_request(url)    

    def get_movie_release_dates(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/release_dates'
        return self._json_by_get_request(url)

    def get_movie_videos(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/videos'
        return self._json_by_get_request(url)

    def get_movie_translations(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/translations'
        return self._json_by_get_request(url)

    def get_movie_recommendations(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/recommendations'
        return self._json_by_get_request(url)

    def get_similar_movies(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/similar'
        return self._json_by_get_request(url)

    def get_movie_reviews(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/reviews'
        return self._json_by_get_request(url)

    def get_movie_lists(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/lists'
        return self._json_by_get_request(url)

    def get_latest_movies(self, language=None):
        url = f'{self.base_url_}movie/latest'
        return self._json_by_get_request(url)

    def get_now_playing_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/now_playing'
        return self._json_by_get_request(url)

    def get_popular_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/popular'
        return self._json_by_get_request(url)

    def get_top_rated_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/top_rated'
        return self._json_by_get_request(url)

    def get_upcoming_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/upcoming'
        return self._json_by_get_request(url)
    
def write_json_file(path,res,ascii_tf):
    if ascii_tf == False:
        file = open(path,mode='w')
        json.dump(res,file,indent=2,ensure_ascii=False)
        file.close()
    else:
        file = open(path,mode='w')
        json.dump(res,file,indent=2)
        file.close()

token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZTUyMmM3MGFhYjNmMzZkNThkMTQ4NzBiN2UwZmQxZiIsInN1YiI6IjYzNDM3YTFkNjQ3NjU0MDA3ZjA4MjdmOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.8dSKKlYlOXjz04n_Y0uqIrdc_7yUfZ4ZRUleudXYVz4'

api = TMDB(token) # tokenは発行された文字列を代入


'''
path_overview= './overview.json'
overview_file = open(path_overview,mode='w')
json.dump(overview,overview_file,indent=2,ensure_ascii=False)  #ensure_ascii=False
overview_file.close()

movie_id = overview['results'][0]['id']

detail = api.get_movie(movie_id)
path_detail= './detail.json'
detail_file = open(path_detail,mode='w')
json.dump(detail,detail_file,indent=2,ensure_ascii=False) #, ensure_ascii=False
detail_file.close()

alternative_titles = api.get_movie_alternative_titles(movie_id)
path_alternative_titles = './alternative_titles.json'
alternative_titles_file = open(path_alternative_titles,mode='w')
json.dump(alternative_titles,alternative_titles_file,indent=2) #, ensure_ascii=False
alternative_titles_file.close()

credit = api.get_movie_credits(movie_id)
path_credit= './credit.json'
credit_file = open(path_credit,mode='w')
json.dump(credit,credit_file,indent=2) #, ensure_ascii=False
credit_file.close()
'''

path_overview= './overview.json'
overview = api.search_movies("万引き家族")
write_json_file(path_overview,overview,False)

movie_id = overview['results'][0]['id']

path_detail= './detail.json'
detail = api.get_movie(movie_id)
write_json_file(path_detail,detail,False)

path_alternative_titles = './alternative_titles.json'
alternative_titles = api.get_movie_alternative_titles(movie_id)
write_json_file(path_alternative_titles,alternative_titles,True)

path_credit= './credit.json'
credit = api.get_movie_credits(movie_id)
write_json_file(path_credit,credit,True)