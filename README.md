***Movie Management Application***
____________________________
This is a Python-based Movie Management Application that allows users to interact with a local movie database. It supports adding, deleting, updating, and displaying movies, as well as generating a website that showcases the movies with their posters, ratings, and release years. The app fetches movie details such as title, rating, year, and poster image automatically from the OMDb API.
____________________________
**Features**
- Add Movies: Users can add movies to the collection by entering the movie title. The application fetches additional details (rating, year, poster) from the OMDb API.
- Update Movie Rating: Users can update the rating of a movie. They can either use the rating fetched from the API or set their own rating.
- Delete Movies: Users can delete movies from the collection by title.
- Generate Website: The app generates a simple website that displays the movie collection with posters, titles, ratings, and release years.
- Movie Statistics: The app can calculate and display statistics like average rating, highest rating, and lowest rating for the movies in the collection.
- CSV Storage: Movie data is stored in a CSV file, making it easy to persist and load movie information.
____________________________
____________________________
**Prerequisites**
- Python 3.8+
- pip (Python package manager)
- OMDb API key