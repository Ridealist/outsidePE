from django.urls import path
from . import views

app_name = 'kakaochat'
urlpatterns = [
    path('random/', views.random_function, name='random'),
    path('shrtncst/', views.SrtNcst, name='shrtncst'),
    path('vilagefcst/', views.VilageFcst, name='vilagefcst')
]