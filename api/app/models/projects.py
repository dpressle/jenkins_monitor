
from pydantic import BaseModel, Field
from datetime import datetime as dt
from pytz import timezone as tz


class ProjectSchema(BaseModel):
    # additional validation for the inputs
    name: str = Field(..., min_length=3, max_length=50)


class ProjectDB(ProjectSchema):
    id: int
