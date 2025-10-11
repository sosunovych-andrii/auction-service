from datetime import datetime, timezone

from sqlalchemy import select

from src.database.models.lot import LotModel, LotStatusEnum
from src.database.settings import AsyncSessionLocal
from src.websockets.manager import manager


async def close_expired_lots():
    async with AsyncSessionLocal() as db:
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(LotModel).where(
                LotModel.status == LotStatusEnum.running,
                LotModel.end_time <= now
            )
        )
        expired_lots = result.scalars().all()

        for lot in expired_lots:
            lot.status = LotStatusEnum.ended
            await manager.close_connections(lot.id, {
                "type": "lot_ended",
                "lot_id": lot.id
            })

        if expired_lots:
            await db.commit()
