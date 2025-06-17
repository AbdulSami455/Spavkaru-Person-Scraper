# Move all logic to scrapers/belarus.py
# This file will just be a CLI entrypoint now
from scrapers.belarus import belarus_search

if __name__ == "__main__":
    results = belarus_search(city_name="Minsk", search_name="Pushkin Alexander Sergeevich", results_limit=20)
    for r in results:
        print(r)
