import requests
from bs4 import BeautifulSoup
import re
import time

BASE_URL = "http://english.spravkaru.net"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_belarus_city_mappings():
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    city_map = {}
    code_map = {}
    for a in soup.select("a[href^='/']"):
        text = a.text.strip()
        match = re.match(r"(.+)\s\(\+375\s?(\d+)\)", text)
        if match:
            city = match.group(1).strip()
            code = match.group(2)
            city_key = city.lower().replace(" ", "_").replace("-", "_").replace("/", "_")
            formatted = f"{city_key}_375_{code}"
            city_map[city_key] = formatted
            code_map[code] = formatted
    return city_map, code_map

def format_search_url(name, formatted_city, page=1):
    person = name.lower().replace(" ", "_")
    return f"{BASE_URL}/w/{person}/{formatted_city}/" if page == 1 else f"{BASE_URL}/w/{person}/{formatted_city}/{page}"

def normalize_phone(phone: str) -> str:
    return re.sub(r"[^\d]", "", phone)

def scrape_city_results(url, phone_filter="", address_filter=""):
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    li_tags = soup.select("ol > li")
    results = []
    phone_filter = normalize_phone(phone_filter)
    address_filter = address_filter.lower()
    for li in li_tags:
        try:
            name = li.find("a", class_="break-link").text.strip()
            phone = re.search(r"\+375\s?\(\d+\)\s?\d+", li.text)
            phone = phone.group(0) if phone else "N/A"
            phone_clean = normalize_phone(phone)
            address_parts = [a.get_text(strip=True) for a in li.find_all("a", class_="address")]
            appt = re.search(r"appt\.\s?\d+", li.get_text(" ", strip=True))
            if appt:
                address_parts.append(appt.group(0))
            address = ", ".join(address_parts) if address_parts else "N/A"
            if phone_filter and phone_filter != phone_clean:
                continue
            if address_filter and address_filter not in address.lower():
                continue
            results.append({
                "name": name,
                "phone": phone,
                "address": address
            })
        except:
            continue
    return results

def scrape_all_pages(formatted_city, name, max_pages, phone_filter="", address_filter="", results_limit=None):
    results = []
    for page in range(1, max_pages + 1):
        url = format_search_url(name, formatted_city, page)
        page_data = scrape_city_results(url, phone_filter, address_filter)
        if not page_data:
            break
        results.extend(page_data)
        if results_limit and len(results) >= results_limit:
            return results[:results_limit]
        time.sleep(1)
    return results

def belarus_search(city_name=None, area_code=None, search_name="ivan", max_pages=None, phone_filter="", address_filter="", results_limit=None):
    if not max_pages:
        max_pages = 50
    if not results_limit:
        results_limit = 200
    city_map, code_map = get_belarus_city_mappings()
    all_results = []
    if city_name:
        key = city_name.lower().replace(" ", "_").replace("-", "_")
        formatted_city = city_map.get(key)
        if not formatted_city:
            return []
        all_results = scrape_all_pages(formatted_city, search_name, max_pages, phone_filter, address_filter, results_limit)
    elif area_code:
        area_code = re.sub(r"\D", "", area_code)
        formatted_city = code_map.get(area_code)
        if not formatted_city:
            return []
        all_results = scrape_all_pages(formatted_city, search_name, max_pages, phone_filter, address_filter, results_limit)
    else:
        for city_key, formatted_city in city_map.items():
            try:
                city_results = scrape_all_pages(formatted_city, search_name, max_pages, phone_filter, address_filter, results_limit)
                all_results.extend(city_results)
                if results_limit and len(all_results) >= results_limit:
                    break
            except Exception:
                continue
    return all_results[:results_limit] 