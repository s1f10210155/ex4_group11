from django.urls import path
from . import views
#app_name= 'home'
#参考：https://houdoukyokucho.com/2020/05/22/post-1025/

urlpatterns = [
    path("", views.display_rooms, name="pub_home"),
    path("create_room_page/", views.create_room_page, name="create_room_page"),
    #path("display_rooms/", views.display_rooms, name="display_rooms"),
    path("display_threads/<int:room_id>/", views.display_threads, name="display_threads"),
    path("display_comments/<int:thread_id>/", views.display_comments, name="display_comments"),

    path("create_room/", views.create_room, name="create_room"),
    path("create_thread/", views.create_thread, name="create_thread"),
    path("create_comment/", views.create_comment, name="create_comment"),

    path("priv_home/", views.priv_home, name="priv_home"),

    path("search/", views.search, name="search"),

    path('follow/<int:pk>/', views.followRoom, name='follow'),  
]