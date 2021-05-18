from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator

from .models import Actor
from movie.models import Movie

from django.template import loader

def actors(request, actor_slug):
    actor = get_object_or_404(Actor, slug=actor_slug)
    movies = Movie.objects.filter(Actors=actor)

    paginator = Paginator(movies, 9)
    page_num = request.GET.get('page')
    movie_data = paginator.get_page(page_num)

    context = {
        'movie_data': movie_data,
        'actor': actor
    }

    return render(request, 'actor/actor.html', context)