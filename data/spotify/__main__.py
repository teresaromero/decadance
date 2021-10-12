from constants import PLAYLISTS
import pandas as pd
import os
import utils


def main():
    """deprecated - this used playlist to get the data"""
    df = pd.DataFrame()
    csv_path = os.path.join(os.path.abspath(os.getcwd()), "data/spotify/csv")
    os.makedirs(csv_path)
    for playlist in PLAYLISTS:
        print(f'Processing playlist {playlist["decade"]}')
        p_tracks = utils.get_playlist_tracks(playlist["playlist_id"])
        p_tracks = utils.parse_track_info(p_tracks, playlist["decade"])
        p_tracks = utils.parse_audio_analysis(p_tracks)
        p_tracks = utils.parse_audio_features(p_tracks)
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
    """main, this uses the search query by genre POP and year variable between 1900 and 2021"""

    # create dataset from spotify api responses
    csv_path_by_year = os.path.join(os.path.abspath(
        os.getcwd()), "data/spotify/csv/by_year")
    os.makedirs(name=csv_path_by_year, exist_ok=True)
    csv_path = os.path.join(os.path.abspath(
        os.getcwd()), "data/spotify/csv")
    os.makedirs(name=csv_path, exist_ok=True)
    period = range(1900, 2022)
    df = utils.get_raw_dataset(
        period, csv_path_by_year, csv_path)

    # clean the dataset
    df = utils.clean_dataset(df)

    # save the clean df to csv
    final_dataset_path = os.path.join(csv_path, "final_dataset.csv")
    df.to_csv(final_dataset_path)

    # download mp3 preview files
    downloads_path = os.path.join(
        os.path.abspath(os.getcwd()), "data/spotify/mp3")
    os.makedirs(name=downloads_path, exist_ok=True)

    utils.download_preview_urls(df, downloads_path)

    return


if __name__ == "__main__":
    search_main()
