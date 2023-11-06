
from pydantic import BaseModel, Field
from datetime import datetime as dt
from pytz import timezone as tz


class ReleaseSchema(BaseModel):
    # additional validation for the inputs
    version: str = Field(..., min_length=3, max_length=50)
    branch: str = Field(..., min_length=3, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    url: str = Field(..., min_length=2, max_length=200)
    created_date: str = dt.now(tz("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M")


class ReleaseDB(ReleaseSchema):
    id: int
