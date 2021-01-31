from typing import Optional, List

import fastapi
from fastapi import Depends

from models.location import Location
from models.reports import Report, ReportSubmital
from models.validation_error import ValidationError
from services import report_service
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


@router.get('/api/reports', name="all_reports")
async def reports_get() -> List[Report]:
    # await report_service.add_report('A', Location(city='Braga'))  # fake data
    # await report_service.add_report('A', Location(city='New York', country='US'))
    return await report_service.get_reports()


@router.post('/api/reports', name="add_report", status_code=201)
async def reports_post(report_to_submit: ReportSubmital) -> Report:
    # await report_service.add_report('A', Location(city='Braga'))  # fake data
    # await report_service.add_report('A', Location(city='New York', country='US'))
    desc = report_to_submit.description
    loc = report_to_submit.location
    return await report_service.add_report(description=desc, location=loc)
