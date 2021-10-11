from constants import PLAYLISTS
import client as spotify
import pandas as pd
import os


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


def main():
    df = pd.DataFrame()
    csv_path = os.path.join(os.path.abspath(os.getcwd()), "data/spotify/csv")
    os.makedirs(csv_path)
    for playlist in PLAYLISTS:
        print(f'Processing playlist {playlist["decade"]}')
        p_tracks = get_playlist_tracks(playlist["playlist_id"])
        p_tracks = parse_track_info(p_tracks, playlist["decade"])
        p_tracks = parse_audio_analysis(p_tracks)
        p_tracks = parse_audio_features(p_tracks)
        p_df = pd.DataFrame(p_tracks)
        p_df.to_csv(
            os.path.join(
                csv_path, f'{playlist["decade"]}.csv'),
            index=False, index_label=False)
        df = df.append(p_df)
        print(
            f'Decade: {playlist["decade"]}, Success retrieving {len(p_tracks)} tracks')
        df.to_csv(
            os.path.join(
                csv_path, 'dataset.csv'),
            index=False, index_label=False)
        print(
            f'Dataset: {playlist["decade"]} added to dataset csv')


def search_main():
    df = pd.DataFrame()
    csv_path = ""
    try:
        csv_path = os.path.join(os.path.abspath(
            os.getcwd()), "data/spotify/csv/by_year")
        os.makedirs(csv_path)
    except Exception as err:
        if isinstance(err, FileExistsError):
            print("path already exists")

    years = range(1900, 2022)
    for year in years:
        print("Year", year)
        tracks = spotify.search(year)
        if len(tracks) != 0:
            p_df = pd.DataFrame(tracks)
            p_df.to_csv(
                os.path.join(
                    csv_path, f'{year}_tracks.csv'),
                index=False, index_label=False)
            df = df.append(p_df)
            df.to_csv(
                os.path.join(
                    csv_path, 'dataset.csv'),
                index=False, index_label=False)
    return


if __name__ == "__main__":
    search_main()
