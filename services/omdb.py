import requests
from typing import List, Dict, Optional


OMDB_BASE_URL = "http://www.omdbapi.com/"


def search_movies(title: str, year: Optional[str], apikey: str) -> List[Dict]:
    """Search OMDb for movies by title and optional year.

    Returns a list of dicts: {id, title, year, poster}
    """
    if not title:
        return []
    params: Dict[str, str] = {"s": title, "type": "movie", "apikey": apikey}
    if year and year.isdigit():
        params["y"] = year
    resp = requests.get(OMDB_BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("Response") != "True":
        return []
    results = []
    for m in data.get("Search", []) or []:
        poster = m.get("Poster")
        results.append(
            {
                "id": m.get("imdbID"),
                "title": m.get("Title"),
                "year": m.get("Year"),
                "poster": None if not poster or poster == "N/A" else poster,
            }
        )
    return results


def get_movie_by_id(imdb_id: str, apikey: str) -> Dict:
    """Get detailed OMDb info by IMDb ID."""
    params = {"i": imdb_id, "plot": "short", "apikey": apikey}
    resp = requests.get(OMDB_BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
