from typing import Optional

import httpx
from httpx import Response

from api import weather_cache
from api.weather_cache import get_weather
from models.validation_error import ValidationError

api_key: Optional[str] = None


async def get_report(city: str, country: str = 'pt', units: str = 'metric') -> dict:
    validate_units(units)

    if forecast := get_weather(city, country, units):
        return forecast

    query = f'{city},{country}'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        r: Response = await client.get(url)
        if r.status_code != 200:
            raise ValidationError(r.text, status_code=r.status_code)

    data = r.json()
    forecast = data['main']
    weather_cache.set_weather(city, country, units, forecast)
    return forecast


def validate_units(units: str):
    if units not in ('metric', 'imperial', 'standard'):
        raise ValidationError(error_msg=f'"{units}" is not a valid unit system.',
                              status_code=400)
