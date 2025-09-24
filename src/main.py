from fastapi import FastAPI

from src.routers.lots import lot_router
from src.routers.bids import bid_router
from src.websockets.ws_lots import ws_router

app = FastAPI()


app.include_router(router=lot_router)
app.include_router(router=bid_router)
app.include_router(router=ws_router)
