from typing import Any, Dict, Union
import websockets

from PyAgent.core.message import Message, MessageType

class Log:
    def __init__(self, client: Any) -> None:
        self.parent_client = client

    async def client(self, websocket: websockets.WebSocketClientProtocol, payload: Union[Dict, None] = None) -> Any:
        print("[LOG]", payload)


