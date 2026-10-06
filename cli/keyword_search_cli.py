import argparse
import json
import string
import pickle
import os
from typing import List
from nltk.stem import PorterStemmer



def normalize(text):
    return text.lower().translate(str.maketrans("", "", string.punctuation))

def tokenize(text) -> List[str]:
    valid_tokens = []
    tokens = text.split()
    for token in tokens:
        if token:
            valid_tokens.append(token)
    
    return valid_tokens

def load_movies() -> List:
    with open("data/movies.json", "r") as f:
        data = json.load(f)
        movies = data["movies"]

    return movies

def load_stop_words() -> List:
    with open("data/stopwords.txt", "r") as f:
        data = f.read()
        stop_words = [normalize(line) for line in data.splitlines()]

    return stop_words

def process(query: str):
    stemmer = PorterStemmer()
    movies = load_movies()
    stop_words = load_stop_words()

    tokens = [stemmer.stem(token) for token in tokenize(query) if token not in stop_words]
    return [
        movie
        for movie in movies
        if any(token in normalize(movie["title"]) for token in tokens)]

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        stemmer = PorterStemmer()
        stop_words = load_stop_words()

        tokens = [stemmer.stem(token) for token in tokenize(text) if token not in stop_words]
    
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, term):
        return sorted(self.index[term])

    def build(self):
        movies = load_movies()
        for movie in movies:
            self.__add_document(movie["id"], f"{movie['title']} {movie['description']}")
            self.docmap[movie["id"]] = movie

    def save(self):
        os.makedirs("cache", exist_ok=True)
        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)

        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)


def build_command():
    inverted_index = InvertedIndex()

    inverted_index.build()
    inverted_index.save()
    docs_set = inverted_index.index['merida']
    docs = list(docs_set)

    print(f"First document for token 'merida' = {docs[0]}")
        
def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="search movies using keywords")

    build_parser = subparsers.add_parser("build", help="build the inverted index and save it to disk")

    search_parser.add_argument("query", type=str, help="search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            query = normalize(args.query)
            results = process(query)

            print(f"Searching for: {args.query}")

            for i, movie in enumerate(results[:5], start=1):
                print(f"{i}. {movie['title']}")

        case "build":
            build_command()
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()