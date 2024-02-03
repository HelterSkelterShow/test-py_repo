from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData

from src.database import Base, metadata

operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String, nullable=False),
    Column("figi", String, nullable=False),
    Column("instriment_type", String, nullable=True),
    Column("date", TIMESTAMP, nullable=False),
    Column("type", String, nullable=False)
)