from django.urls import path
from .views import (index, 
Rate, movieDetails, addMoviesWatched, 
addMoviesToWatch, genres, Rate)


urlpatterns = [
    path('', index, name='index'),
    path('<imdb_id>/rate', Rate, name='rate-movie'),
    path('<imdb_id>', movieDetails, name='movie-details'),
    path('<imdb_id>/addtomovieswatched', addMoviesToWatch,name='add-movies-to-watch'),
    path('<imdb_id>/addmoviewatched', addMoviesWatched, name='add-movies-watched'),
    path('genre/<slug:genre_slug>', genres, name='genres'),
    path('<imdb_id>/rate', Rate, name='rate-movie'),
    
]