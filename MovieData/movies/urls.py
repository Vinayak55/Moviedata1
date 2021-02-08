from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^movie-search-by-title/',views.MoviesSearchApi.as_view(), name='movie-search-by-title'),
    re_path(r'^movie-search-by-local-db/',views.MoviesSearchApiInLocalDb.as_view(), name='movie-search-by-local-db'),

     ]