from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.bid import BidModel
from src.database.models.lot import LotStatusEnum, LotModel
from src.database.settings import get_db
from src.schemas.bids import BidReadSchema, BidCreateSchema
from src.websockets.manager import manager

bid_router = APIRouter()


@bid_router.post(
    path="/lots/{lot_id}/bids/",
    response_model=BidReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_bid_for_specific_lot(
        lot_id: int,
        bid_data: BidCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    result_lot = await db.execute(
        select(LotModel)
        .where(LotModel.id == lot_id)
    )
    lot = result_lot.scalar_one_or_none()
    if not lot or lot.status != LotStatusEnum.running:
        raise HTTPException(
            detail="Lot not found or not active",
            status_code=status.HTTP_404_NOT_FOUND
        )

    result_bids = await db.execute(
        select(BidModel)
        .where(BidModel.lot_id == lot_id)
        .order_by(desc(BidModel.amount))
        .limit(1)
    )
    highest_bid = result_bids.scalar_one_or_none()
    min_amount = (
        lot.start_price
        if not highest_bid
        else highest_bid.amount
    )
    if bid_data.amount <= min_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bid must be higher than current highest bid ({min_amount})"
        )

    new_bid = BidModel(
        bidder=bid_data.bidder,
        amount=bid_data.amount,
        lot_id=lot_id
    )

    db.add(new_bid)
    lot.end_time += timedelta(minutes=30)
    await db.commit()
    await db.refresh(lot)
    await db.refresh(new_bid)

    await manager.broadcast(
        lot_id,
        message={
            "type": "bid_placed",
            "lot_id": lot_id,
            "bidder": new_bid.bidder,
            "amount": float(new_bid.amount)
        }
    )

    return new_bid
