from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.load_entry, name="load_entry"),
    path("results", views.results, name="results"),
    path("newpage", views.newpage, name="newpage"),
    path("edit", views.edit, name="edit"),
    path("edited", views.edited, name="edited"),
    path("random_page", views.random_page, name="random_page")
]
