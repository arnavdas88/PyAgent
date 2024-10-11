from typing import Any, Dict, List, Union
import websockets
import socket
import os
import uuid
import getpass

from PyAgent.core.message import Message, MessageType

class Config:
    def __init__(self, client: Any, ) -> None:
        self.parent_client = client
        self.payload = None

    async def client(self, websocket: websockets.WebSocketClientProtocol, payload: Union[Dict, None] = None) -> Any:
        ...

    async def server(self, message: Message, ) -> Any:
        ...