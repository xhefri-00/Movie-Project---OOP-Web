from movie_app import MovieApp
from storage.storage_csv import StorageCsv


def main():
    """
    Main function to initialize the storage and the MovieApp instance,
    and start running the application.
    """
    storage = StorageCsv('data/movies.csv')
    app = MovieApp(storage)
    app.run()


if __name__ == "__main__":
    main()
