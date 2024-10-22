import requests
from istorage import IStorage
import json
from dotenv import load_dotenv
import os


load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


class StorageJson(IStorage):
    """
    A class that implements the IStorage interface for managing movie data using a JSON file.
    """
    def __init__(self, file_path):
        """
        Initializes the StorageJson with the path to the JSON file.

        Args:
            file_path (str): Path to the JSON file.
        """
        self.file_path = file_path

    def _load_movies(self):
        """
        Loads the movies from the JSON file.

        Returns:
            dict: A dictionary of movies with titles as keys and their details as values.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_movies(self, movies):
        """
        Saves the movies dictionary to the JSON file.

        Args:
            movies (dict): Dictionary of movie data to be saved.
        """
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        """
        Lists all movies in the storage.

        Returns:
            dict: Dictionary of movies.
        """
        return self._load_movies()

    def add_movie(self, title):
        """
        Adds a movie to the storage by fetching its details from the OMDb API.

        Args:
            title (str): Title of the movie.

        Raises:
            requests.exceptions.RequestException: If there is an issue with the API request.
        """
        movies = self._load_movies()
        try:
            response = requests.get(f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}")
            response.raise_for_status()  # Raise HTTPError for bad responses

            movie_data = response.json()
            if movie_data.get('Response') == "False":
                print(f"Movie '{title}' not found in OMDb API.")
                return

            movie_title = movie_data.get('Title', title)
            movie_rating = movie_data.get('imdbRating', "N/A")
            movie_year = movie_data.get('Year', "N/A")
            movie_poster = movie_data.get('Poster', "")  # Empty if not available

            # Save the movie details in the JSON file
            movies[movie_title] = {
                "rating": movie_rating,
                "year": movie_year,
                "poster": movie_poster
            }

            self._save_movies(movies)
            print(f"Movie '{movie_title}' added successfully.")

        except requests.exceptions.RequestException as e:
            print(f"Error accessing OMDb API: {e}")

    def delete_movie(self, title):
        """
        Deletes a movie from the storage.

        Args:
            title (str): Title of the movie to delete.

        Raises:
            ValueError: If the movie is not found.
        """
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")

    def update_movie(self, title, rating):
        """
        Updates the rating of a movie in the storage.

        Args:
            title (str): Title of the movie to update.
            rating (float): New rating of the movie.

        Raises:
            ValueError: If the movie is not found.
        """
        movies = self._load_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")
