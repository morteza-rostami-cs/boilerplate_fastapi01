from typing import List
from fastapi import WebSocket

class ConnectionManager:
  def __init__(self):
    # list of connections
    self.active_connections: List[WebSocket] = []

  # accept a connection and push it in connections
  async def connect(self, websocket: WebSocket):
    # accept connection
    await websocket.accept()
    # push into connections
    self.active_connections.append(websocket)

  # remove a client from active connections
  def disconnect(self, websocket: WebSocket):
    if (websocket in self.active_connections):
      self.active_connections.remove(websocket)

  # send message to specific client
  async def send_client_message(self, message: str, websocket: WebSocket):
    await websocket.send_text(message)

  # broadcast to all connected clients
  async def broadcast(self, message: str) -> None:
    for connection in self.active_connections:
      await connection.send_test(message)

# singleton manager
socketService = ConnectionManager()