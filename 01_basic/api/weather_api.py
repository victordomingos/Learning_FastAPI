from typing import Optional

import fastapi
from fastapi import Depends

from models.location import Location
from models.validation_error import ValidationError
from services.openweather_service import get_report

router = fastapi.APIRouter()


@router.get('/api/weather/{city}')
async def weather(location: Location = Depends(), units: Optional[str] = 'metric'):
    """ A simple endpoint to get information about the weather in JSON
    Example:
        /api/weather/Braga?country=PT&units=metric
    """
    try:
        return await get_report(location.city, location.country, units)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as e:
        print(e)  # log this instead…
        return fastapi.Response(content='Error while procession the request',
                                status_code=500)
