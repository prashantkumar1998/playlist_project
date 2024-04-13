from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    playlists = models.ManyToManyField(
        Playlist, related_name="songs", through="PlaylistSong"
    )


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    play_order = models.IntegerField()
