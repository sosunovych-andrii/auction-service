from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Integer,
    DECIMAL,
    DateTime,
    func,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class LotStatusEnum(str, Enum):
    running = "running"
    ended = "ended"


class LotModel(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    start_price: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=False
    )
    status: Mapped[LotStatusEnum] = mapped_column(
        SQLAlchemyEnum(LotStatusEnum),
        nullable=False,
        default=LotStatusEnum.running
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    bids: Mapped[list["BidModel"]] = relationship(
        "BidModel",
        back_populates="lot",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Lot(id='{self.id}', start_price='{self.start_price}', status='{self.status}')>"
