import requests
from bs4 import BeautifulSoup
import re
import time
import logging

logger = logging.getLogger(__name__)

BASE_URL = "http://english.spravkaru.net"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

def get_russian_city_mappings():
    try:
        res = requests.get(BASE_URL + "/russia.html", headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        city_map = {}
        code_map = {}
        
        for a in soup.select("a[href^='/']"):
            text = a.text.strip()
            match = re.match(r"(.+)\s\(\+7\s?\d+\)", text)
            if match:
                city = match.group(1).strip()
                code = match.group(0).split('+7')[-1].strip('() ')
                # Create multiple variations of the city name
                city_variations = [
                    city.lower().replace(" ", "_").replace("-", "_").replace("/", "_"),
                    city.lower().replace(" ", "").replace("-", "").replace("/", ""),
                    city.lower()
                ]
                formatted = f"{city_variations[0]}_7_{code}"
                for variation in city_variations:
                    city_map[variation] = formatted
                code_map[code] = formatted
                
        logger.info(f"Found {len(city_map)} city mappings")
        return city_map, code_map
    except Exception as e:
        logger.error(f"Error getting city mappings: {str(e)}")
        return {}, {}

def format_search_url(name, formatted_city, page=1):
    # Format the name properly
    name_parts = name.lower().split()
    formatted_name = "_".join(name_parts)
    return f"{BASE_URL}/w/{formatted_name}/{formatted_city}/" if page == 1 else f"{BASE_URL}/w/{formatted_name}/{formatted_city}/{page}"

def normalize_phone(phone: str) -> str:
    return re.sub(r"[^\d]", "", phone)

def scrape_city_results(url, phone_filter="", address_filter=""):
    try:
        logger.info(f"Scraping URL: {url}")
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        li_tags = soup.select("ol > li")
        results = []
        phone_filter = normalize_phone(phone_filter)
        address_filter = address_filter.lower()
        
        for li in li_tags:
            try:
                name = li.find("a", class_="break-link").text.strip()
                phone = re.search(r"\+7\s?\(\d+\)\s?\d+", li.text)
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
                    "address": address,
                    "additional_info": li.get_text(" ", strip=True)
                })
            except Exception as e:
                logger.error(f"Error processing result: {str(e)}")
                continue
                
        logger.info(f"Found {len(results)} results on page")
        return results
    except Exception as e:
        logger.error(f"Error scraping city results: {str(e)}")
        return []

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

def russian_search(city_name=None, area_code=None, search_name="ivan", max_pages=None, phone_filter="", address_filter="", results_limit=None):
    try:
        logger.info(f"Starting Russian search for: {search_name} in {city_name or 'all cities'}")
        
        if not max_pages:
            max_pages = 50
        if not results_limit:
            results_limit = 200
            
        city_map, code_map = get_russian_city_mappings()
        all_results = []
        
        if city_name:
            # Try different variations of the city name
            city_variations = [
                city_name.lower().replace(" ", "_").replace("-", "_"),
                city_name.lower().replace(" ", "").replace("-", ""),
                city_name.lower()
            ]
            
            formatted_city = None
            for variation in city_variations:
                if variation in city_map:
                    formatted_city = city_map[variation]
                    break
                    
            if not formatted_city:
                logger.warning(f"City not found: {city_name}")
                return []
                
            all_results = scrape_all_pages(formatted_city, search_name, max_pages, phone_filter, address_filter, results_limit)
            
        elif area_code:
            area_code = re.sub(r"\D", "", area_code)
            formatted_city = code_map.get(area_code)
            if not formatted_city:
                logger.warning(f"Area code not found: {area_code}")
                return []
            all_results = scrape_all_pages(formatted_city, search_name, max_pages, phone_filter, address_filter, results_limit)
            
        else:
            for city_key, formatted_city in city_map.items():
                try:
                    city_results = scrape_all_pages(formatted_city, search_name, max_pages, phone_filter, address_filter, results_limit)
                    all_results.extend(city_results)
                    if results_limit and len(all_results) >= results_limit:
                        break
                except Exception as e:
                    logger.error(f"Error searching city {city_key}: {str(e)}")
                    continue
                    
        logger.info(f"Search completed. Found {len(all_results)} results")
        return all_results[:results_limit]
        
    except Exception as e:
        logger.error(f"Error in russian_search: {str(e)}")
        return [] 