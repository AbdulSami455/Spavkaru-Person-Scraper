from scrapers.russian import russian_search

if __name__ == "__main__":
    results = russian_search(city_name="Moscow", search_name="Ivan Ivanovich", results_limit=20)
    for r in results:
        print(r)
