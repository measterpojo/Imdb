from django.contrib import admin

from .models import Movie, Review, Genre, Rating

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Rating)