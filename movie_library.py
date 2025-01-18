import json
from collections import Counter

#eccezione per film non trovati
class MovieNotFoundError(Exception):
    pass

class MovieLibrary:
    def __init__(self, json_file: str):
        self.json_file = json_file
        try:
            with open(self.json_file, 'r') as file:
                self.movies = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.json_file}")

#salvo i dati della collezione sul file JSON
    def _save_to_file(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.movies, file, indent=4)

#restituisco l'intera collezione di film
    def get_movies(self):
        return self.movies

#aggiungo i film nella collezione e aggiorna il file JSON
    def add_movie(self, title: str, director: str, year: int, genres: list):
        new_movie = {
            "title": title,
            "director": director,
            "year": year,
            "genres": genres
        }
        self.movies.append(new_movie)
        self._save_to_file()

#rimuovo un film dalla collezione e aggiorno il file
    def remove_movie(self, title: str):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                self.movies.remove(movie)
                self._save_to_file()
                return movie
        raise MovieNotFoundError("Movie was not found")

#aggiorno i dati di un film che esiste già e salvo le modifiche
    def update_movie(self, title: str, director=None, year=None, genres=None):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                if director is not None:
                    movie["director"] = director
                if year is not None:
                    movie["year"] = year
                if genres is not None:
                    movie["genres"] = genres
                self._save_to_file()
                return movie
        raise MovieNotFoundError("Movie was not found")

#restituisco i titoli dei film
    def get_movie_titles(self):
        return [movie["title"] for movie in self.movies]

#restituisco il numero totale dei film
    def count_movies(self):
        return len(self.movies)

#restituisco un film che corrisponde al titolo, senza al case sensitive
    def get_movie_by_title(self, title: str):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                return movie
        raise MovieNotFoundError("Movie was not found")

#restituisco i film con il loro titolo che hanno una sottostringa case sensitive
    def get_movies_by_title_substring(self, substring: str):
        return [movie for movie in self.movies if substring in movie["title"]]

#restituisco i film di un certo anno
    def get_movies_by_year(self, year: int):
        return [movie for movie in self.movies if movie["year"] == year]

#conto i film fatti da un director, non case sensitive
    def count_movies_by_director(self, director: str):
        return sum(1 for movie in self.movies if movie["director"].lower() == director.lower())

#restituisco i film dello stesso genere
    def get_movies_by_genre(self, genre: str):
        return [movie for movie in self.movies if genre.lower() in map(str.lower, movie["genres"])]

#restituisco il titolo del film più vecchio 
    def get_oldest_movie_title(self):
        oldest_movie = min(self.movies, key=lambda x: x["year"], default=None)
        return oldest_movie["title"] if oldest_movie else None

#calcolo la media degli anni di pubblicazione dei film nella collezione
    def get_average_release_year(self):
        if not self.movies:
            return 0.0
        return sum(movie["year"] for movie in self.movies) / len(self.movies)

#restituisco il titolo più lungo della collezione
    def get_longest_title(self):
        return max(self.movies, key=lambda x: len(x["title"]), default={"title": None})["title"]

#restituisco i film pubblicati dellìanno di inizio e anno fine
    def get_titles_between_years(self, start_year: int, end_year: int):
        return [movie["title"] for movie in self.movies if start_year <= movie["year"] <= end_year]

#restituisco l'anno più comune tra i film
    def get_most_common_year(self):
        if not self.movies:
            return None
        year_counts = Counter(movie["year"] for movie in self.movies)
        return year_counts.most_common(1)[0][0]