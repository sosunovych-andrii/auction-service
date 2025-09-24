from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, lot_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        if lot_id not in self.active_connections:
            self.active_connections[lot_id] = []
        self.active_connections[lot_id].append(websocket)

    def disconnect(self, lot_id: int, websocket: WebSocket) -> None:
        if lot_id in self.active_connections and websocket in self.active_connections[lot_id]:
            self.active_connections[lot_id].remove(websocket)
            if not self.active_connections[lot_id]:
                del self.active_connections[lot_id]

    async def broadcast(self, lot_id: int, message: dict) -> None:
        if lot_id in self.active_connections:
            for connection in self.active_connections[lot_id]:
                await connection.send_json(message)

    async def close_connections(self, lot_id: int, message: dict) -> None:
        if lot_id not in self.active_connections:
            return
        for connection in self.active_connections[lot_id]:
            if message:
                await connection.send_json(message)
            await connection.close()
        del self.active_connections[lot_id]
