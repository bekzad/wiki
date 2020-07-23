from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki_entry, name="wiki_entry"),
    path("search", views.search, name="search"),
    path("new/", views.new_page, name="new_page"),
    path("random/", views.random_page, name="random_page")
]
