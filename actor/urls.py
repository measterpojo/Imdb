from django.urls import path

from .views import actors

urlpatterns = [

    path('<slug:actor_slug>', actors, name='actors')

]