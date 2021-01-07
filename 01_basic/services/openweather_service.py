from typing import Optional

import httpx

from api import weather_cache
from api.weather_cache import get_weather

api_key: Optional[str] = None


async def get_report(city: str, country: str, units: str) -> dict:
    if forecast := get_weather(city, country, units):
        return forecast

    query = f'{city},{country}'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()

    data = r.json()
    forecast = data['main']
    weather_cache.set_weather(city, country, units, forecast)
    return forecast
