from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Any, Dict, List
import uuid, time

from PyAgent.core.message import Message, MessageType
from PyAgent.server.connection import ConnectionManager
from PyAgent.server.client import Client, ClientModel

from PyAgent.server.admin import Admin

app = FastAPI()
manager = ConnectionManager()
admin = Admin(app, manager)

SERVER = "STANDALONE-1"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client = Client(websocket, manager)
    await manager.connect( client )

    try:
        await client.initiation(SERVER)
        while True:
            data = await websocket.receive_text()
            message = Message.model_validate_json(data)
            await client.process(message)
    except WebSocketDisconnect:
        manager.disconnect(client)
        print(f"Client {client.uuid} disconnected")

@app.get("/all_clients")
async def all_clients():
    result = []
    for client in manager.active_clients:
        result.append( client.to_model() )
    return result

@app.get("/client/{client_id}")
async def client_detail(client_id: uuid.UUID):
    client = list(filter( lambda client: client.uuid == client_id, manager.active_clients))
    if len(client) == 0 :
        # Raise Exception
        pass
    elif len(client) > 1:
        # Raise Exception
        pass
    client = client[0]
    return client.to_model()

@app.get("/")
async def index():
    return { "Hello": "World" }



