from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path("wrn_list/", views.WthrWrnList, name="wrn_list"),
    path("wrn_msg/", views.WthrWrnMsg, name="wrn_msg"),
    path("wthr_info/", views.WthrInfo, name="wthr_info"),
    path("pwn_cd/", views.PwnCd, name="pwn_cd"),
    path("pwn_stat/", views.PwnStatus, name="pwn_stat"),
]
