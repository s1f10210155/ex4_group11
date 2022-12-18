from django.urls import path
from . import views

#参考：https://houdoukyokucho.com/2020/05/22/post-1025/

urlpatterns = [
    path("", views.pub_home, name="pub_home"),
    path("priv_home", views.priv_home, name="priv_home"),
    path("search", views.search, name="search"),
    path("create_room", views.create_room, name="create_room"),
    path("<int:user_id>", views.users, name="users"),
]