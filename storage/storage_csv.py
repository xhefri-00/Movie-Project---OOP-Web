import csv
from istorage import IStorage


class StorageCsv(IStorage):
    """
    A class that implements the IStorage interface for managing movie data using a CSV file.
    """
    def __init__(self, file_path):
        """
        Initializes the StorageCsv with the path to the CSV file.

        Args:
            file_path (str): Path to the CSV file.
        """
        self.file_path = file_path

    def _load_movies(self):
        """
        Loads the movies from the CSV file.

        Returns:
            dict: A dictionary of movies with titles as keys and their details as values.
        """
        movies = {}
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert rating to float if it's available
                    try:
                        rating = float(row['rating']) if row['rating'] != 'N/A' else None
                    except ValueError:
                        rating = None  # Handle case where rating isn't a number

                    movies[row['title']] = {
                        'rating': rating,
                        'year': row['year'],
                        'poster': row.get('poster', '')  # Fetch poster if available
                    }
        except FileNotFoundError:
            return {}
        return movies

    def _save_movies(self, movies):
        """
        Saves the movies dictionary to the CSV file.

        Args:
            movies (dict): Dictionary of movie data to be saved.
        """
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'rating', 'year', 'poster'])
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    'title': title,
                    'rating': details['rating'],
                    'year': details['year'],
                    'poster': details['poster']
                })

    def list_movies(self):
        """
        Lists all movies in the storage.

        Returns:
            dict: Dictionary of movies.
        """
        return self._load_movies()

    def add_movie(self, title, rating, year, poster_url):
        """
        Adds a movie to the storage.

        Args:
            title (str): Title of the movie.
            rating (float): Rating of the movie.
            year (str): Year the movie was released.
            poster_url (str): URL of the movie's poster.
        """
        movies = self._load_movies()
        movies[title] = {
            'rating': rating,
            'year': year,
            'poster': poster_url
        }
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the storage.

        Args:
            title (str): Title of the movie to delete.
        """
        movies = self._load_movies()
        found_movie = False
        movie_to_delete = None

        # First, find the movie to delete without modifying the dictionary
        for movie_name in movies:
            if title.lower() == movie_name.lower():
                found_movie = True
                movie_to_delete = movie_name
                break

        # If a movie was found, delete it after the iteration
        if found_movie:
            del movies[movie_to_delete]
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")

    def update_movie(self, title, rating=None, year=None):
        """
        Updates a movie's rating and/or year in the storage.

        Args:
            title (str): Title of the movie to update.
            rating (float, optional): New rating of the movie.
            year (str, optional): New year of the movie.

        Raises:
            ValueError: If the movie is not found.
        """
        movies = self._load_movies()
        if title in movies:
            if rating is not None:
                movies[title]['rating'] = rating
            if year is not None:
                movies[title]['year'] = year
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")
