''' 

project_one.entertainment_center
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module asks for the user's favorite movie genre,
then it goes ahead to fetch a few of the movies in the genre
from The Movie Database (TMDB) API (https://www.themoviedb.org/en)

Copyright [2017] [Hafiz Adewuyi]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. '''

import json
import os
import sys
import requests
import media
import fresh_tomatoes


API_KEY = os.environ['TMDB_API_KEY']
GENRES_URL = 'https://api.themoviedb.org/3/genre/movie/list'

GENRE_MOVIES_URL_FORMAT = 'https://api.themoviedb.org/3/genre/{}/movies'  # format with movie_id

# format with the file name e.g. 'titanic.jpg'
IMAGE_URL_FORMAT = "https://image.tmdb.org/t/p/w500{}"

# format with movie_id
MOVIE_VIDEOS_URL_FORMAT = 'https://api.themoviedb.org/3/movie/{}/videos'

# format with the video id name e.g. 'fhw380def'
VIDEO_URL_FORMAT = "https://www.youtube.com/watch?v={}"

NO_CONNECTION_MESSAGE = "Your computer seems to be offline."


def get_genres():
    """Gets a list of all movie Genres from the movie database API

    Returns:
        A list of genre dictionaries. Each list item is a dictionary
        having has the fields: 'id' and 'name'
    """
    params = dict(
        api_key=API_KEY,
        language='en-US'
    )

    try:
        resp = requests.get(url=GENRES_URL, params=params)
    except:
        print(NO_CONNECTION_MESSAGE)
        return False

    data = json.loads(resp.text)
    # print(data)
    return data['genres']


def show_genre_movies(genre):
    """Get and display 10 movies from the provided genre

    Args:
        genre: A dictionary containing the 'id' and 'name' of the genre

    """
    params = dict(
        api_key=API_KEY,
        language='en-US',
        include_adult='false',
        sort_by='created_at.asc'
    )
    try:
        resp = requests.get(url=GENRE_MOVIES_URL_FORMAT.format(
            genre['id']), params=params)
    except:
        print(NO_CONNECTION_MESSAGE)
        return False

    data = json.loads(resp.text)
    movies_raw = data['results']
    print("Hang in there while we fetch some movies we think you'll love")
    movies = []

    for movie in movies_raw:
        movies.append(extract_movie(movie))

    fresh_tomatoes.open_movies_page(movies)


def extract_movie(raw_movie):
    """Converts a TMDB movie instance to an entertainment centre Movie instance
    Args:
        raw_movie: A dictionary representing the TMDB movie

    Returns:
    A media.Movie instance formed from the provided TMDB movie
    """
    title = str(raw_movie['original_title'])
    poster_image_url = IMAGE_URL_FORMAT.format(raw_movie['poster_path'])

    trailer = get_movie_trailer(raw_movie['id'])
    trailer_url = VIDEO_URL_FORMAT.format(trailer)

    print("Movie '{}' {} a YouTube trailer...".format(
        title, "has" if trailer else "does not have"))
    movie = media.Movie(title, None, poster_image_url, trailer_url)
    return movie


def get_movie_trailer(movie_id):
    """Queries for and returns the Youtube video id of the movie #movie_id trailer, if any

    Args:
        The TMDB id of the movie'
    Returns:
        The Youtube video ID
    """
    params = dict(
        api_key=API_KEY,
        language='en-US'
    )
    try:
        resp = requests.get(
            url=MOVIE_VIDEOS_URL_FORMAT.format(movie_id), params=params)
    except:
        print(NO_CONNECTION_MESSAGE)
        return False

    data = json.loads(resp.text)

    trailer = data['results'][0]['key'] if data['results'] else None
    return trailer


def collect_genre(genres):
    """Allow the user to select one of the genres in the supplied list"""
    number = sys.stdin.readline()

    try:
        selected_genre = genres[int(number) - 1]
        print("You selected", selected_genre['name'])
    except ValueError:
        print("""You have to enter a number. Try again:""")
        selected_genre = collect_genre(genres)
    except IndexError:
        print("""You have to enter a number between 1 and {}. Try again:"""
              .format(len(genres)))
        selected_genre = collect_genre(genres)

    return selected_genre


def main():
    """The method that will be run on module start"""
    genres = get_genres()
    if genres:
        print("SELECT YOUR FAVORITE GENRE!")
        for index, genre in enumerate(genres):
            print("{}.".format(index + 1), genre['name'])

        selected_genre = collect_genre(genres)
        show_genre_movies(selected_genre)
    print("BYE!")


main()
