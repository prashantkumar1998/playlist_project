from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Playlist, Song

from .serializers import PlaylistSerializer, SongSerializer, PlaylistSongSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# to create/update/delete and list playlist for a user
class UserPlaylistView(APIView):
    def post(self, request, user_id):
        data = request.data
        data["user"] = user_id
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        playlists = Playlist.objects.filter(user__user_id=user_id)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def patch(self, request, user_id):
        playlist_id = request.data.get("playlist_id")
        if playlist_id is None:
            return Response(
                {"message": "playlist_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            playlist = Playlist.objects.get(
                playlist_id=playlist_id, user__user_id=user_id
            )
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        playlist_id = request.data.get("playlist_id")
        if playlist_id is None:
            return Response(
                {"message": "playlist_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            playlist = Playlist.objects.get(
                playlist_id=playlist_id, user__user_id=user_id
            )
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# to add/list and delete song from playlist
class PlaylistView(APIView):
    pagination_class = CustomPagination

    def post(self, request):
        serializer = PlaylistSongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        playlist_id = request.data.get("playlist_id")
        playlists = Playlist.objects.get(playlist_id=playlist_id)
        songs = playlists.songs.all()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(songs, request)

        serializer = SongSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def delete(self, request):
        song_id = request.data.get("song_id")
        playlist_id = request.data.get("playlist_id")
        if song_id is None:
            return Response(
                {"message": "song_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            playlist = Playlist.objects.get(playlist_id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            song = Song.objects.get(song_id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if song not in playlist.songs.all():
            return Response(
                {"message": "Song does not exist in the playlist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        playlist.songs.remove(song)
        playlist.save()
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# list all song
class SongView(APIView):
    import pdb

    # pdb.set_trace()
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ["name", "song_id"]

    def get(self, request):
        paginator = self.pagination_class()
        queryset = Song.objects.all()
        page = paginator.paginate_queryset(queryset, request)

        search_filter = self.filter_backends[0]()
        if self.search_fields and "search" in request.query_params:
            queryset = search_filter.filter_queryset(self.request, queryset, self)

        serializer = SongSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
