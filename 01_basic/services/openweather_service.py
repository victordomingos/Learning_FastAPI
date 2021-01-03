from typing import Optional

import httpx

api_key: Optional[str] = None


async def get_report(city: str, country: str, units: str) -> dict:
    query = f'{city},{country}'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()

    data = r.json()
    forecast = data['main']
    return forecast
