import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz

load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://hello_fastapi:hello_fastapi@postgres/hello_fastapi_dev")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

builds_table = Table(
    "builds",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("job_name", String(50)),
    Column("build_number", Integer),
    Column("state", String(50)),
    Column("url", String(250)),
    Column("parameters", String(250), default=""),
    Column("causes", String(150), default="NA"),
    Column("status", String(50), default="NA"),
    Column("created_date", String(50), default=dt.now(
        tz("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M"))
)

release_table = Table(
    "releases",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("version", String(50)),
    Column("branch", String(50)),
    Column("state", String(50)),
    Column("url", String(250)),
    Column("created_date", String(50), default=dt.now(
        tz("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M"))
)

# Databases query builder

database = Database(DATABASE_URL)
