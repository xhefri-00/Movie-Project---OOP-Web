import requests
from dotenv import load_dotenv
import os


load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


class MovieApp:
    def __init__(self, storage):
        """Initialize with a storage instance."""
        self._storage = storage


    def command_list_movies(self):
        """Lists all movies."""
        movies = self._storage.list_movies()
        if movies:
            print("\nList of movies:")
            for movie, details in movies.items():
                print(f"{movie}: {details['rating']}, {details['year']}")
        else:
            print("No movies found.")
        print()


    def command_add_movie(self):
        """Adds a movie by fetching details from OMDb API using just the movie title."""
        movie_title = input("Enter movie name: ").strip()
        try:
            # Fetch movie details from OMDb API
            details = self.fetch_movie_from_api(movie_title)

            if not details:
                print(f"Movie '{movie_title}' not found.")
                return

            # Extract details from the API response
            poster = details.get('Poster', "https://via.placeholder.com/100x150?text=No+Poster")
            title = details['Title']
            year = details['Year']
            rating = details.get('imdbRating', 'N/A')

            # Ask user if they want to provide their own rating
            use_custom_rating = input(f"The API returned a rating of {rating}. Would you like to provide your own rating? (yes/no): ").lower()

            if use_custom_rating == 'yes':
                rating = input("Enter your custom rating: ").strip()
            # Add movie to storage (save to file)
            self._storage.add_movie(title, rating, year, poster)
            print(f"Movie '{title}' added successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")


    def fetch_movie_from_api(self, movie_name):
        """Fetches movie details from OMDb API."""
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data['Response'] == "True":
                return data
            else:
                print(f"Movie '{movie_name}' not found.")
                return None
        else:
            print("Error accessing OMDb API.")
            return None


    def command_delete_movie(self):
        """Deletes a movie."""
        movie_name = input("Enter the movie name to delete: ").strip()
        try:
            self._storage.delete_movie(movie_name)
            print(f"'{movie_name}' has been deleted.")
        except ValueError as e:
            print(e)
        print()


    def command_movie_stats(self):
        """Shows statistics for the movies."""
        movies = self._storage.list_movies()
        ratings = []
        for details in movies.values():
            try:
                rating = float(details["rating"])
                ratings.append(rating)
            except ValueError:
                continue  # Skip movies with invalid ratings like "N/A" or "rating"

        if ratings:
            average_rating = sum(ratings) / len(ratings)
            sorted_ratings = sorted(ratings)
            median_rating = sorted_ratings[len(ratings) // 2] if len(ratings) % 2 != 0 else \
                (sorted_ratings[len(ratings) // 2 - 1] + sorted_ratings[len(ratings) // 2]) / 2
            max_movie = max(movies, key=lambda x: float(movies[x]['rating']) if movies[x]['rating'] != "N/A" else 0)
            min_movie = min(movies, key=lambda x: float(movies[x]['rating']) if movies[x]['rating'] != "N/A" else 0)

            print(f"Average rating: {average_rating}")
            print(f"Median rating: {median_rating}")
            print(f"Highest rated movie: {max_movie} ({movies[max_movie]['rating']})")
            print(f"Lowest rated movie: {min_movie} ({movies[min_movie]['rating']})")
        else:
            print("No movies found to generate statistics.")
        print()


    def command_update_movie(self):
        """Allows the user to update the rating of an existing movie."""
        movie_title = input("Enter the name of the movie to update: ").strip()

        # Fetch the list of movies from storage (case-insensitive search)
        movies = self._storage.list_movies()

        # Check if the movie exists (case-insensitive search)
        movie_title_lower = movie_title.lower()
        matching_movie = None

        for title in movies:
            if title.lower() == movie_title_lower:
                matching_movie = title
                break

        if matching_movie:
            # Ask the user for the new rating
            new_rating = input(f"Enter new rating for '{matching_movie}': ").strip()

            try:
                # Update the movie rating
                self._storage.update_movie(matching_movie, rating=new_rating)
                print(f"Movie '{matching_movie}' rating updated to {new_rating}.")
            except ValueError as e:
                print(f"Error updating movie: {e}")
        else:
            print(f"Movie '{movie_title}' not found in the list.")


    def command_movie_stats(self):
        """Shows statistics for the movies."""
        movies = self._storage.list_movies()
        ratings = []
        for details in movies.values():
            try:
                ratings.append(float(details["rating"]))
            except ValueError:
                continue  # Skip movies with invalid ratings like "N/A" or "rating"

        if ratings:
            average_rating = sum(ratings) / len(ratings)
            sorted_ratings = sorted(ratings)
            median_rating = sorted_ratings[len(ratings) // 2] if len(ratings) % 2 != 0 else \
                (sorted_ratings[len(ratings) // 2 - 1] + sorted_ratings[len(ratings) // 2]) / 2
            max_movie = max(movies, key=lambda x: float(movies[x]['rating']) if movies[x]['rating'] != "N/A" else 0)
            min_movie = min(movies, key=lambda x: float(movies[x]['rating']) if movies[x]['rating'] != "N/A" else 0)

            print(f"Average rating: {average_rating}")
            print(f"Median rating: {median_rating}")
            print(f"Highest rated movie: {max_movie} ({movies[max_movie]['rating']})")
            print(f"Lowest rated movie: {min_movie} ({movies[min_movie]['rating']})")
        else:
            print("No movies found to generate statistics.")
        print()

    def generate_website(self):
        """Generates an HTML page to display movies using a template."""
        movies = self._storage.list_movies()

        try:
            # Load the HTML template
            with open("index_template.html", "r") as template_file:
                template_content = template_file.read()

            # Replace the title placeholder
            template_content = template_content.replace("__TEMPLATE_TITLE__", "My Movie Website")

            # Build the movie grid content
            movie_grid_content = ""
            for movie, details in movies.items():
                # Ensure poster URL is available or provide a placeholder
                poster_url = details.get('poster', "https://via.placeholder.com/100x150?text=No+Poster")
                movie_grid_content += f"""
                <li>
                    <div class="movie">
                        <img src="{poster_url}" alt="{movie} Poster" style="width:100px;">
                        <h2>{movie}</h2>
                        <p><strong>Rating:</strong> {details['rating']}</p>
                        <p><strong>Year:</strong> {details['year']}</p>
                    </div>
                </li>
                """
            # Replace the movie grid placeholder
            template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_content)

            # Write the final content to the index.html file
            with open("index.html", "w") as output_file:
                output_file.write(template_content)

            print("Website was generated successfully.")

        except Exception as e:
            print(f"An error occurred while generating the website: {e}")

    def run(self):
        """Runs the movie app menu and handles commands."""
        while True:
            print("\n------ Menu ------")
            print("0. Exit")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie Rating")
            print("5. Show Movie Stats")
            print("6. Generate Website")

            choice = input("Enter choice (0-6): ").strip()

            if choice == '0':
                print("Exiting... Bye!")
                break
            elif choice == '1':
                self.command_list_movies()
            elif choice == '2':
                self.command_add_movie()
            elif choice == '3':
                self.command_delete_movie()
            elif choice == '4':
                self.command_update_movie()
            elif choice == '5':
                self.command_movie_stats()
            elif choice == '6':
                self.generate_website()
            else:
                print("Invalid choice, try again.")
