from django.http.response import JsonResponse
from django.shortcuts import render, reverse, get_object_or_404

from django.http import HttpResponseRedirect
# Create your views here.
from .forms import RateForm
from django.db.models import Avg
from .models import Movie, Genre, Rating, Review

from actor.models import Actor
from user.models import Profile

from django.contrib.auth.models import User

from django.core.paginator import Paginator
import requests

from django.utils.text import slugify

def index(request):



    return render(request, 'movie/index.html')



def movieDetails(request, imdb_id):
    
    if Movie.objects.filter(imdbID=imdb_id).exists():
        movie_data = Movie.objects.get(imdbID=imdb_id)
        reviews = Review.objects.filter(movie=movie_data)
        reviews_arg = reviews.aggregate(Avg('rate'))
        reviews_count = reviews.count()
        our_dp = True

        context = {
            'movie_data': movie_data,
            'reviews':reviews,
            'reviews_avg': reviews_arg,
            'reviews_count': reviews_count,
            'our_db': our_dp,
        }
    else:
        url = 'http://www.omdbapi.com/?apikey=a8e92936&i=' + imdb_id
        response = requests.get(url)
        movie_data = response.json()

        #Inject to our database bellow:

        ratings_objs = []
        genre_objs = []
        actor_objs = []

        #For the actors
        actor_list = [x.strip() for x in movie_data['Actors'].split(',')]

        for actor in actor_list:
            a , created = Actor.objects.get_or_create(name=actor)
            actor_objs.append(a)

        #For the Genre or Categories
        genre_list = list(movie_data['Genre'].replace(" ","").split(','))

        for genre in genre_list:
            genre_slug = slugify(genre)
            g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
            genre_objs.append(g)
        
        #For the Rate
        for rate in movie_data['Ratings']:
            r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
            ratings_objs.append(r)


        if movie_data['Type'] == 'movie':
            m, created = Movie.objects.get_or_create(
                Title = movie_data['Title'],
                Year = movie_data['Year'],
                Rated = movie_data['Rated'],
                Released = movie_data['Released'],
                Runtime = movie_data['Runtime'],
                Director = movie_data['Director'],
                Writer = movie_data['Writer'],
                Plot = movie_data['Plot'],
                Language = movie_data['Language'],
                Country = movie_data['Country'],
                Awards = movie_data['Awards'],
                Poster_url = movie_data['Poster'],
                Metascore = movie_data['Metascore'],
                imdbRating=movie_data['imdbRating'],
                imdbVotes=movie_data['imdbVotes'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                DVD=movie_data['DVD'],
                BoxOffice=movie_data['BoxOffice'],
                Production = movie_data['Production'],
                Website = movie_data['Website'],
                )
            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(ratings_objs)
        elif movie_data['Type'] == 'series':
            m, created = Movie.objects.get_or_create(
                Title = movie_data['Title'],
                Year = movie_data['Year'],
                Rated = movie_data['Rated'],
                Released = movie_data['Released'],
                Runtime = movie_data['Runtime'],
                Director = movie_data['Director'],
                Writer = movie_data['Writer'],
                Plot = movie_data['Plot'],
                Language = movie_data['Language'],
                Country = movie_data['Country'],
                Awards = movie_data['Awards'],
                Poster_url = movie_data['Poster'],
                Metascore = movie_data['Metascore'],
                imdbRating=movie_data['imdbRating'],
                imdbVotes=movie_data['imdbVotes'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                totalSeasons=movie_data['totalSeasons'],
                )
            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(ratings_objs)
        else:            
            m, created = Movie.objects.get_or_create(
                Title = movie_data['Title'],
                Year = movie_data['Year'],
                Rated = movie_data['Rated'],
                Released = movie_data['Released'],
                Runtime = movie_data['Runtime'],
                Director = movie_data['Director'],
                Writer = movie_data['Writer'],
                Plot = movie_data['Plot'],
                Language = movie_data['Language'],
                Country = movie_data['Country'],
                Awards = movie_data['Awards'],
                Poster_url = movie_data['Poster'],
                Metascore = movie_data['Metascore'],
                imdbRating=movie_data['imdbRating'],
                imdbVotes=movie_data['imdbVotes'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                )
            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(ratings_objs)



        for actor in actor_objs:
            actor.movies.add(m)
            actor.save()
        

        m.save()
        
        our_db = False


        context = {
            'movie_data': movie_data,
            'our_db': our_db
        }

    return render(request, 'movie/movie_details.html', context)


def Rate(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.movie = movie
            rate.save()
            return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))
    else:
        form = RateForm()
    
    context = {
        'form': form,
        'movie': movie
    }

    return render(request, 'movie/rate.html', context)



def genres(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    movies= Movie.objects.filter(Genre=genre)

    #pagination
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'genre': genre
    }

    return render(request, 'movie/genre.html', context)

def addMoviesToWatch(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.is_ajax():
        profile.to_watch.add(movie)
        return JsonResponse({})

    return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

def addMoviesWatched(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.is_ajax():
        if profile.to_watch.filter(imdbID=imdb_id).exists():
            profile.to_watch.remove(movie)
            profile.watched.add(movie)
        else:
            profile.watched.add(movie)
        return JsonResponse({})
    return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))


#Hybrid
# def pagination_results(request, query, page_number):

#     if request.is_ajax():
#         visible = 9
#         upper = page_number
#         lower = upper - visible
        

#         url = 'http://www.omdbapi.com/?apikey=a8e92936&s=' + query 
#         response = requests.get(url)
#         movie_data = response.json()

#         size = response.json().count()
        
  

#         return JsonResponse({'size':size, 'movie_data': movie_data[lower]})

#     return render(request, 'movie/search_results.html', {})



#Orginal
# def pagination_results(request, query, page_number):

#     url = 'http://www.omdbapi.com/?apikey=a8e92936&s=' + query + '&page=' + str(page_number)
#     response = requests.get(url)
#     movie_data = response.json()
#     page_number = int(page_number) + 1
    
#     context = {
#         'query':query,
#         'movie_data': movie_data,
#         'page_number':page_number, 
#     }

#     return render(request, 'movie/search_results.html', context)


# def index(request):

#     query = request.GET.get('q')

#     if query:
#         url = 'http://www.omdbapi.com/?apikey=a8e92936&s=' + query
#         # a8e92936
#         response = requests.get(url)
#         movie_data = response.json()

#         context = {
#             'query': query,
#             'movie_data': movie_data,
#             'page_number': 2,


#             }
#         return render(request, 'movie/search_results.html', context)
#     return render(request, 'movie/index.html')









     