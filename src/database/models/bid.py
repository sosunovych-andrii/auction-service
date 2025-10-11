from datetime import datetime

from sqlalchemy import Integer, String, DECIMAL, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import Base


class BidModel(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    bidder: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    amount: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    lot_id: Mapped[int] = mapped_column(
        ForeignKey("lots.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    lot: Mapped["LotModel"] = relationship(
        "LotModel",
        back_populates="bids",
    )

    def __repr__(self) -> str:
        return f"<Bid(id='{self.id}', bidder='{self.bidder}', amount='{self.amount}')>"
