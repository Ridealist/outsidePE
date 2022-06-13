from django.urls import path
from . import views

app_name = 'kakaochat'
urlpatterns = [
    path('', views.random_function, name='random'),
]