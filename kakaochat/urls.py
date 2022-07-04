from django.urls import path
from . import views

app_name = 'kakaochat'
urlpatterns = [
    path('random/', views.random_function, name='random'),
    path('weekday/', views.weekday, name='weekday'),
    path('srtncst/', views.UltraSrtNcst, name='ultrasrtncst'),
    path('srtfcst/', views.UltraSrtFcst, name='ultrasrtfcst'),
    path('vilagefcst/', views.VilageFcst, name='vilagefcst'),
    path('example/', views.template, name='template')
]