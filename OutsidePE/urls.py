from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("weather/", include("weather.urls")),
    path("air/", include("air.urls")),
    path("news/", include("news.urls")),
]
