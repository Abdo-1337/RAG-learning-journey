import argparse
import json
import string
from nltk.stem import PorterStemmer


    

def normalize(text):
    return text.lower().translate(str.maketrans("", "", string.punctuation))

def tokenize(text):
    return text.split()

def process(query: str, movies: str, stop_words: list):
    stemmer = PorterStemmer()

    tokens = [stemmer.stem(token) for token in tokenize(query) if token not in stop_words]
    return [
        movie
        for movie in movies
        if any(token in normalize(movie["title"]) for token in tokens)]

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="search movies using keywords")

    search_parser.add_argument("query", type=str, help="search query")

    args = parser.parse_args()

    with open("data/movies.json", "r") as f:
        data = json.load(f)
        movies = data["movies"]

    with open("data/stopwords.txt", "r") as f:
        data = f.read()
        stop_words = [normalize(line) for line in data.splitlines()]

    match args.command:
        case "search":
            query = normalize(args.query)
            results = process(query, movies, stop_words)

            print(f"Searching for: {args.query}")

            for i, movie in enumerate(results[:5], start=1):
                print(f"{i}. {movie['title']}")
            
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()