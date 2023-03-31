from django.urls import path

from .views import *


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("categories/<slug:slug>/", CategoryView.as_view(), name="category_detail"),
    path("news/<slug:slug>/", NewsDetailView.as_view(), name="news_detail"),
]
