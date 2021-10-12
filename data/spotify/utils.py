from time import time
import requests
import pandas as pd
import os
import client as spotify


def parse_track_info(tracks: list[dict], decade: str) -> list[dict]:
    result = list()
    for track in tracks:
        info = dict()
        info["track_id"] = track["id"]
        info["uri"] = track["uri"]
        info["popularity"] = track["popularity"]
        info["title"] = track["name"]
        info["duration_ms"] = track["duration_ms"]
        info["artists"] = [a["name"] for a in track["artists"]]
        info["release_date"] = track["album"]["release_date"]
        info["release_date_precision"] = track["album"]["release_date_precision"]
        info["preview_url"] = track["preview_url"]
        info["decade"] = decade
        result.append(info)
    return result


def parse_audio_analysis(tracks: list[dict]) -> list[dict]:
    result = list()
    for track in tracks:
        analysis = spotify.audio_analysis(track["track_id"])
        result.append({**track, **analysis})
    return result


def parse_audio_features(tracks: list[dict]) -> list[dict]:
    result = list()
    for track in tracks:
        features = spotify.audio_features(track["track_id"])
        result.append({**track, **features})
    return result


def get_playlist_tracks(playlist_id: str) -> list[dict]:
    return spotify.playlist_tracks(playlist_id)


def get_raw_dataset(years: list, csv_path_by_year: str, csv_path: str) -> pd.DataFrame:
    df = pd.DataFrame()
    for year in years:
        tracks = spotify.search(year)
        if len(tracks) != 0:
            p_df = pd.DataFrame(tracks)
            p_df.to_csv(
                os.path.join(
                    csv_path_by_year, f'{year}_tracks.csv'),
                index=False, index_label=False)
            df = df.append(p_df)
            # Save into global dataset df in each iteration
            df.to_csv(
                os.path.join(
                    csv_path, 'dataset.csv'),
                index=False, index_label=False)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df.drop_duplicates("id", inplace=True)
    df.dropna(subset=["preview_url"], inplace=True)
    df["release_year"] = df["album.release_date"].apply(
        lambda x: x[:4])
    df["decade"] = df["release_year"].apply(lambda x: x[:3]+"0")

    return df


def download_preview_urls(df: pd.DataFrame, downloads_path: str):
    df_urls = df[["id", "decade", "preview_url"]]
    urls = [tuple(r) for r in df_urls.to_numpy()]
    print(f"Found {len(urls)} urls")

    def get_url_data(data: tuple):
        filename, folder, url = data

        res = requests.get(url, stream=True)

        path = os.path.join(downloads_path, f"{folder}")
        os.makedirs(name=path, exist_ok=True)

        with open(os.path.join(path, f"{filename}.mp3"), 'wb') as f:
            for ch in res:
                f.write(ch)

    start = time()
    for x in urls:
        get_url_data(x)

    print(f"Time to download: {time() - start}")
