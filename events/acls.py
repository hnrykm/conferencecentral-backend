from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    query = {"query": f"{city}, {state}", "per_page": 1}
    response = requests.get(
        url,
        params=query,
        headers=headers,
    )
    content = response.json()
    try:
        photo_url = content["photos"][0]["src"]["original"]
        return {"photo_url": photo_url}
    except (KeyError, IndexError):
        return {"photo_url": None}


def get_weather_data():
    pass
