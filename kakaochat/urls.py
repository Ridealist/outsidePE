from django.urls import path
from . import views

app_name = 'kakaochat'
urlpatterns = [
    path('random/', views.random_function, name='random'),
    path('weather/', views.weather, name='weather')
]