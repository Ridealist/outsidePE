from django.urls import path
from . import views

app_name = "air"
urlpatterns = [
    path("rltm_mesure/", views.RltmMesure, name="rltm_mesure"),
    path("sido_rltm_mesure/", views.CtprvnRltmMesure, name="sido_rltm_mesure"),
    path("dust_frcst/", views.DustFrcst, name="dust_frcst"),
    path("dust_week_frcst/", views.DustWeekFrcst, name="dust_week_frcst"),
]
