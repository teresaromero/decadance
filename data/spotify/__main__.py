from constants import CWD
import pandas as pd
import os
import utils


def search_main():
    """main, this uses the search query by genre POP and year variable between 1900 and 2021"""

    # create dataset from spotify api responses
    csv_path_by_year = os.path.join(CWD, "csv/by_year")
    os.makedirs(name=csv_path_by_year, exist_ok=True)
    csv_path = os.path.join(os.path.abspath(
        os.getcwd()), "csv")
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
    downloads_path = os.path.join(CWD, "mp3")
    os.makedirs(name=downloads_path, exist_ok=True)

    utils.download_preview_urls(df, downloads_path)

    return


if __name__ == "__main__":
    search_main()
