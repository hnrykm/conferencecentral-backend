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


def get_weather_data(city, state):
    # get the latitude and longitude of the city and state
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": f"{city}, {state}", "appid": OPEN_WEATHER_API_KEY}
    response = requests.get(url, params=params)
    content = response.json()
    try:
        lat = content[0]["lat"]
        lon = content[0]["lon"]
    except IndexError:
        return {"description": None, "temp": None}

    # use the latitude and longitude to get the weather
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "imperial",
        "appid": OPEN_WEATHER_API_KEY,
    }
    response = requests.get(url, params=params)
    content = response.json()
    try:
        description = content["weather"][0]["description"]
        temp = content["main"]["temp"]
        return {"description": description, "temp": temp}
    except IndexError:
        return {"description": None, "temp": None}
