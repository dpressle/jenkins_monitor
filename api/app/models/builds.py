
from pydantic import BaseModel, Field
from datetime import datetime as dt
from pytz import timezone as tz


class BuildSchema(BaseModel):
    # additional validation for the inputs
    job_name: str = Field(..., min_length=3, max_length=50)
    build_number: int
    state: str = Field(..., min_length=2, max_length=50)
    url: str = Field(..., min_length=2, max_length=200)
    parameters: str = Field(..., max_length=250)
    causes: str = Field(..., max_length=150)
    status: str = "NA"
    created_date: str = dt.now(tz("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M")


class BuildDB(BuildSchema):
    id: int
