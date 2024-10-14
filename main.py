from movie_app import MovieApp
from storage_csv import StorageCsv

def main():
    storage = StorageCsv('data/movies.csv')
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()
