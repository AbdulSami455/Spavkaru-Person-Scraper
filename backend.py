from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from scrapers.belarus import belarus_search
from scrapers.kazakhstan import kazakhstan_search
from scrapers.latvia import latvia_search
from scrapers.moldova import moldova_search
from scrapers.russian import russian_search
from scrapers.ukraine import ukraine_search

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class SearchRequest(BaseModel):
    country: str
    search_name: str
    city_name: Optional[str] = None
    area_code: Optional[str] = None
    phone_filter: Optional[str] = None
    address_filter: Optional[str] = None
    max_pages: Optional[int] = None
    results_limit: Optional[int] = None

@app.post("/search")
def search_people(req: SearchRequest):
    country = req.country.lower()
    kwargs = {
        'city_name': req.city_name,
        'area_code': req.area_code,
        'search_name': req.search_name,
        'max_pages': req.max_pages,
        'phone_filter': req.phone_filter,
        'address_filter': req.address_filter,
        'results_limit': req.results_limit,
    }
    if country == 'belarus':
        results = belarus_search(**kwargs)
    elif country == 'kazakhstan':
        results = kazakhstan_search(**kwargs)
    elif country == 'latvia':
        results = latvia_search(**kwargs)
    elif country == 'moldova':
        results = moldova_search(**kwargs)
    elif country == 'russia' or country == 'russian':
        results = russian_search(**kwargs)
    elif country == 'ukraine':
        results = ukraine_search(**kwargs)
    else:
        raise HTTPException(status_code=400, detail="Unsupported country")
    return {"results": results} 