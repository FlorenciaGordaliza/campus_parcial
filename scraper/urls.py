from django.urls import path
from .views import scraper_view

app_name = 'scraper'
urlpatterns = [path('scraper/', scraper_view, name='index')]