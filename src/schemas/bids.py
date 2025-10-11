from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class BidCreateSchema(BaseModel):
    bidder: str
    amount: Decimal = Field(gt=0)


class BidReadSchema(BaseModel):
    id: int
    bidder: str
    amount: Decimal
    created_at: datetime
    lot_id: int

    model_config = ConfigDict(from_attributes=True)
