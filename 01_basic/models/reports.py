import uuid
from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from models.location import Location


class ReportSubmital(BaseModel):
    description: str
    location: Location


class Report(ReportSubmital):
    id: str
    created_on: Optional[datetime]
