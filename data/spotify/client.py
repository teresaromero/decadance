import requests
import os
from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
AUTH_URL = os.getenv("SPOTIFY_AUTH_URL")
API_URL = os.getenv("SPOTIFY_API_URL")


def __auth(origin: str) -> str:
    print(f"Retrieve token for {origin}")
    res = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    data = res.json()
    status_code = res.status_code

    if status_code != 200:
        raise Exception(f"Error Access Token: {data}")

    return data['access_token']


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
