# decadance

Core Code School - Machine Learning Bootcamp Final Project

## Project

The objective of this project is to make an analysis of the audio features of songs between the 40s and the 21s decades.

## Dataset

Dataset used for this project is retrieved from the [SpotifyAPI](https://developer.spotify.com/).

### 🪄 How is the dataset created?

By using the Search API in Spotify, querying by range of _years from 1900 to 2021_ od release date of tracks, filtered by _genre pop_

You can generate the csv and download the mp3 files used for the project by running:

```
$ python data/spotify
```

This will create the dir `csv` and `mp3` with the datasets and mp3 files of the preview-url of the tracks.

The dataset will be a collection of tracks of pop genre witch have been released between 1900 to 2021, tagged with the decade.

### 📆 Consideration on decade

According to Wikipedia, a decade is:

> Any period of ten years is a "decade"

There are two methods to group the years on decades:

- 0-to-9 decade
- 1-to-0 decade

For the purpose of this project, the **first one** is considered, so a decade will be all the years from 0 to 9.

For example:

- decade 1900 - from 1900 to 1909
- decade 2010 - from 2010 to 2019

You can read more about this [here](https://en.wikipedia.org/wiki/Decade)
