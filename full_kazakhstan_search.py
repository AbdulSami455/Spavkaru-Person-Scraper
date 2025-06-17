from scrapers.kazakhstan import kazakhstan_search

if __name__ == "__main__":
    results = kazakhstan_search(city_name="Almaty", search_name="Ivan Ivanov", results_limit=20)
    for r in results:
        print(r) 