import csv
from istorage import IStorage

class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
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
        return self._load_movies()

    def add_movie(self, title, rating, year, poster_url):
        movies = self._load_movies()
        movies[title] = {
            'rating': rating,
            'year': year,
            'poster': poster_url
        }
        self._save_movies(movies)

    def delete_movie(self, title):
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")

    def update_movie(self, title, rating=None, year=None):
        movies = self._load_movies()
        if title in movies:
            if rating is not None:
                movies[title]['rating'] = rating
            if year is not None:
                movies[title]['year'] = year
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")
