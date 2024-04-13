from django.urls import path
from . import views

urlpatterns = [
    path("users/<int:user_id>/playlist", views.UserPlaylistView.as_view()),
    path("playlists", views.PlaylistView.as_view()),
    path("songs", views.SongView.as_view()),
]
