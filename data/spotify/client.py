import requests
import os
from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
AUTH_URL = os.getenv("SPOTIFY_AUTH_URL")
API_URL = os.getenv("SPOTIFY_API_URL")

token = ""


def _get_token() -> str:
    res = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    data = res.json()
    status_code = res.status_code
    if status_code == 200:
        return data['access_token']
    return ""


def __auth(origin: str) -> str:
    global token
    while token == "":
        print(f"Setting up the token {origin}")
        t = _get_token()
        token = t
    return token


def audio_analysis(track_id: str) -> dict:
    token = __auth("audio_analysis")
    res = requests.get(f"{API_URL}/audio-analysis/{track_id}",
                       headers={"Authorization": f"Bearer {token}"})
    data = res.json()
    status_code = res.status_code

    if status_code != 200:
        print(
            f"ERROR: spotify.audio_analysis(): status {status_code} - {data}")
        return

    ignored_fields = [
        "codestring",
        "code_version",
        "echoprintstring",
        "synchstring",
        "synch_version",
        "rhythmstring",
        "rhythm_version"
    ]
    return {x: data["track"][x] for x in data["track"] if x not in ignored_fields}


def audio_features(track_id: str) -> dict:
    token = __auth("audio_features")
    res = requests.get(f"{API_URL}/audio-features/{track_id}",
                       headers={"Authorization": f"Bearer {token}"})
    data = res.json()
    status_code = res.status_code

    if status_code != 200:
        print(
            f"ERROR: spotify.audio_features(): status {status_code} - {data}")
        return

    ignored_fields = [
        "track_href",
        "analysis_url",
        "uri",
        "type",
        "id",
    ]
    return {x: data[x] for x in data if x not in ignored_fields}


def playlist_tracks(playlist_id: str) -> list[dict]:
    token = __auth("playlist_tracks")
    res = requests.get(f"{API_URL}/playlists/{playlist_id}/tracks?offset=0&limit=100",
                       headers={"Authorization": f"Bearer {token}"})
    data = res.json()
    status_code = res.status_code

    if status_code != 200:
        print(f"ERROR: spotify.playlist_tracks: status {status_code} - {data}")
        return

    required_fields = [
        "id", "uri", "popularity", "name", "duration_ms", "artists", "album", "preview_url"
    ]
    tracks = [i["track"] for i in data["items"]]
    result = [{x: track[x] for x in track if x in required_fields}
              for track in tracks]
    return result


def search(year: str, required_items: int = 100) -> list[dict]:
    token = __auth("search")
    offset = 0
    batch = 50
    retrieved = 0
    next_batch = False

    def param_request(year, batch, offset, token):
        return requests.get(f"{API_URL}/search?q=year:{year}+genre:pop&type=track&market=ES&limit={batch}&offset={offset}",
                            headers={"Authorization": f"Bearer {token}"})
    result = list()
    while retrieved < required_items and not next_batch:
        res = param_request(year, batch, offset, token)
        data = res.json()["tracks"]
        status_code = res.status_code

        if status_code != 200:
            print(f"ERROR: spotify.search: status {status_code} - {data}")
            return

        next_batch = data["next"] == "null"
        items = data["items"]

        required_fields = [
            "id", "uri", "name", "artists", "album.name", "album.release_date", "album.release_date_precision", "preview_url"
        ]

        for track in items:
            res = dict()
            for f in required_fields:
                field_split = f.split(".")
                if len(field_split) == 2:
                    res[f] = track[field_split[0]][field_split[1]]
                elif f == "artists":
                    res[f] = [a["name"] for a in track[f]]
                else:
                    res[f] = track[field_split[0]]
            result.append(res)

        offset += batch
        retrieved += batch

    return result
