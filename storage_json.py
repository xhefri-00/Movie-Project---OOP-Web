import requests
from istorage import IStorage
import json

OMDB_API_KEY = "1db3c1d7"

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path


    def _load_movies(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}


    def _save_movies(self, movies):
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)


    def list_movies(self):
        return self._load_movies()


    def add_movie(self, title):
        movies = self._load_movies()
        # Fetch movie details from OMDb API
        try:
            response = requests.get(f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&{title}")
            response.raise_for_status()  # Raise HTTPError for bad responses

            movie_data = response.json()
            if movie_data.get('Response') == "False":
                print(f"Movie '{title}' not found in OMDb API.")
                return

            # Extract details from API response
            movie_title = movie_data.get('Title', title)
            movie_rating = movie_data.get('rating', "N/A")
            movie_year = movie_data.get('year', "N/A")
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
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")


    def update_movie(self, title, rating):
        movies = self._load_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")
