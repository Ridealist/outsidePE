from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path("wrn_list/", views.WthrWrnList, name="wrn_list"),
    path("pwn_cd/", views.PwnCd, name="pwn_cd"),
    path("pwn_stat/", views.PwnStatus, name="pwn_stat"),
]
