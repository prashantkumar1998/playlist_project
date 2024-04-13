GET
http://127.0.0.1:8000/api/songs


POST
http://127.0.0.1:8000/api/users/1/playlist
{
    "name":"devotional"

}

GET
http://127.0.0.1:8000/api/users/1/playlist

PATCH
http://127.0.0.1:8000/api/users/1/playlist
{
    "playlist_id":"1",
    "name":"devotional2"
}

DELETE
http://127.0.0.1:8000/api/users/1/playlist
{
    "playlist_id":"1",
}

PATCH
http://127.0.0.1:8000/api/playlists
{
    "playlist_id":"1",
    "name":"devotional2"
}

POST
http://127.0.0.1:8000/api/playlists
{
    "playlist":"3",
    "song":"2",
    "play_order": 2
}

GET
http://127.0.0.1:8000/api/playlists
{
    "playlist_id":"3",
}

DELETE
http://127.0.0.1:8000/api/playlists
{
    "playlist_id":"3",
    "song_id":"2"
}
