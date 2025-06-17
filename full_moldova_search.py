from scrapers.moldova import moldova_search

if __name__ == "__main__":
    results = moldova_search(city_name="Chisinau", search_name="Ion Popescu", results_limit=20)
    for r in results:
        print(r) 