import uuid
from datetime import datetime
from typing import List

from models.location import Location
from models.reports import Report

__reports: List[Report] = []  # simulate a database


async def get_reports() -> List[Report]:
    # async call to DB…
    return list(__reports)


async def add_report(description: str, location: Location) -> Report:
    report = Report(
        id=str(uuid.uuid4()),
        location=location,
        description=description,
        created_on=datetime.now())

    __reports.append(report)  # here we would save to DB (async/await)…
    __reports.sort(key=lambda x: x.created_on, reverse=True)
    return report
