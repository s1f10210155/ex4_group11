from django.urls import path
from . import views

urlpatterns = [
    path("pub_home", views.pub_home, name="pub_home"),
    path("priv_home", views.priv_home, name="priv_home"),
    path("search", views.search, name="search"),
]