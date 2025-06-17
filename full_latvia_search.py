from scrapers.latvia import latvia_search

if __name__ == "__main__":
    results = latvia_search(city_name="Riga", search_name="Janis Berzins", results_limit=20)
    for r in results:
        print(r) 