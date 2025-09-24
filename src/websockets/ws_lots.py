from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from src.websockets.manager import ConnectionManager

ws_router = APIRouter()
manager = ConnectionManager()


@ws_router.websocket(path="/ws/lots/{lot_id}/")
async def websocket_lot(websocket: WebSocket, lot_id: int):
    await manager.connect(lot_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(lot_id, websocket)
