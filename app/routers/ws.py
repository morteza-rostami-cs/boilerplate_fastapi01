from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# service
from app.services.connection_manager import socketService

router = APIRouter(prefix='/ws', tags=["websocket"])

# echo some socket message => a client opens a websocket connection to /echo 
@router.websocket("/echo")
async def websocket_echo(websocket: WebSocket):
  # accept the connection
  await websocket.accept()

  try:
    # runs for ever => waiting for new messages => through this connection
    while True:
      # wait for client message and read
      # if: client close the connection => .receive_text() raise an exception called: WebSocketDisconnect
      data = await websocket.receive_text()
      # send message back to the client
      await websocket.send_text(F"Echo: {data}")
  except WebSocketDisconnect:
    print("client disconnected")

# broadcast to multiple connected clients
@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
  # connect and push to connections
  await socketService.connect(websocket=websocket)

  try:
    # listen for messages and broadcast to all
    while True:
      data = await websocket.receive_text()
      # broadcast to all connected clients
      await socketService.broadcast(f"client says: {data}")

  except WebSocketDisconnect:
    # remove from connections
    socketService.disconnect(websocket=websocket)
    # broadcast disconnection
    await socketService.broadcast("client disconnected")

