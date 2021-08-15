import imdb
import pandas as pd

ia = imdb.IMDb()
movie = ia.search_movie('A Place in the Sun')
movie_ID = movie[0].movieID
movie_info = ia.get_movie(movie_ID)
genre = movie_info['genre']
cast = movie_info['cast']
cast_top = cast[:5]
# for actor in cast_top:
#     print(actor)
director = movie_info['director']

df = pd.read_csv(r'P:\git_repos\guardian_film_reviews\data\all_reviews.csv')



