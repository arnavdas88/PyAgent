from typing import List, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from nicegui import ui, run


from PyAgent.core.message import Message

class ConnectionManager:
    def __init__(self):
        self.active_clients: List[Any] = []

    async def connect(self, client: Any):
        self.active_clients.append(client)
        await client.connect()
        # self.render.refresh()

    def disconnect(self, client: Any):
        if client in self.active_clients:
            self.active_clients.remove(client)
            # self.render.refresh()

    async def send_message(self, message: Message):
        for client in self.active_clients:
            await client.__websocket__.send_text(message.model_dump_json())

    def all_uuid(self, ):
        self.validate()
        return [client.uuid for client in self.active_clients]
    
    def validate(self, ):
        for client in self.active_clients:
            if not client.is_active:
                self.disconnect(client)

    @ui.refreshable
    def render(self, ):
        # Create cards for each client in the list
        for index, client in enumerate(self.active_clients):
            client.create_client_card()
