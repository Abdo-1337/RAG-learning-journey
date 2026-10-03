import argparse
import json
import string


def normalize(text):
    return text.lower().translate(str.maketrans("", "", string.punctuation))

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="search movies using keywords")

    search_parser.add_argument("query", type=str, help="search query")

    args = parser.parse_args()
    with open("data/movies.json", "r") as f:
        data = json.load(f)
        movies = data["movies"]




    match args.command:
        case "search":
            query = normalize(args.query)
            results = [
                movie
                for movie in movies
                if query in normalize(movie["title"])
                ]

            print(f"Searching for: {args.query}")

            for i, movie in enumerate(results[:5], start=1):
                print(f"{i}. {movie['title']}")
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()