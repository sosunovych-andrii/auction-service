from datetime import datetime, timedelta, timezone
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.database.models.lot import LotStatusEnum


class LotCreateSchema(BaseModel):
    start_price: Decimal = Field(gt=0)
    end_time: datetime

    @field_validator("end_time")
    @classmethod
    def end_time_min_half_hour(cls, value: datetime) -> datetime:
        if not isinstance(value, datetime):
            raise TypeError("end_time must be a datetime object")

        now = datetime.now(timezone.utc)
        if value < now + timedelta(minutes=30):
            raise ValueError("end_time must be at least 30 minutes from now")

        return value


class LotReadSchema(BaseModel):
    id: int
    start_price: Decimal
    status: LotStatusEnum
    created_at: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)
