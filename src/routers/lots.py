from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.lot import LotModel, LotStatusEnum
from src.database.settings import get_db
from src.schemas.lots import LotReadSchema, LotCreateSchema

lot_router = APIRouter(prefix="/lots")


@lot_router.post(
    path="/",
    response_model=LotReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_lot(
        lot_data: LotCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    new_lot = LotModel(
        start_price=lot_data.start_price,
        end_time=lot_data.end_time
    )
    db.add(new_lot)
    await db.commit()
    await db.refresh(new_lot)

    return new_lot


@lot_router.get(
    path="/",
    response_model=list[LotReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_lots(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LotModel)
        .where(LotModel.status == LotStatusEnum.running)
        .order_by(LotModel.end_time)
    )
    lots = result.scalars().all()

    return lots
