import datetime

from pydantic import BaseModel


class ImageIdentification(BaseModel):
    tracked_on: datetime.date
    metric: str
    value: float

