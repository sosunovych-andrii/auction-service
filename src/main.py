from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from src.routers.lots import lot_router
from src.routers.bids import bid_router
from src.websockets.ws_lots import ws_router
from src.tasks import close_expired_lots


scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(func=close_expired_lots, trigger="interval", seconds=30)
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(lifespan=lifespan)


app.include_router(router=lot_router)
app.include_router(router=bid_router)
app.include_router(router=ws_router)
