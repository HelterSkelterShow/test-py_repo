from pydantic import BaseModel
from datetime import datetime

class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instriment_type: str
    date: datetime
    type: str