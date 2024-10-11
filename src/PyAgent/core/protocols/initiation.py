from typing import Any, Dict, List, Union
import websockets
import socket
import os
import uuid
import getpass

from PyAgent.core.message import Message, MessageType

class Initiation:
    def __init__(self, client: Any, tags: List[str] = []) -> None:
        self.parent_client = client
        self.payload = None
        self.tags = tags

    async def client(self, websocket: websockets.WebSocketClientProtocol, payload: Union[Dict, None] = None) -> Any:
        if not payload:
            # SYN
            self.payload = {
                    "message": "Hello from Client!",
                    "hostname": socket.gethostname(),
                    "username": getpass.getuser(),
                    "cwd": os.getcwd(),
                    "path": os.path.dirname(os.path.abspath(__file__)),
                    "tags": self.tags
                }
            syn = Message(
                type=MessageType.INITIATION,
                token=self.parent_client.token,
                payload=self.payload
            )
            await websocket.send(syn.model_dump_json())
        else:
            # ACK
            self.parent_client.uuid = payload["uuid"]
            self.parent_client.server = payload["server"]
            self.parent_client.hostname = payload["hostname"]
            self.parent_client.username = payload["username"]

    async def server(self, message: Message, server_as: str) -> Any:
        self.parent_client.hostname = message.payload["hostname"]
        self.parent_client.username = message.payload["username"]
        self.parent_client.cwd = message.payload["cwd"]
        self.parent_client.path = message.payload["path"]
        self.parent_client.tags = message.payload["tags"]

        self.parent_client.uuid = uuid.uuid4()
        existing_uuids = self.parent_client.__manager__.all_uuid()

        while str(self.parent_client.uuid) in existing_uuids:
            self.parent_client.uuid = uuid.uuid4()

        response_message = Message(
            type=MessageType.INITIATION,
            token=message.token,
            payload={
                "status": "received", 
                "uuid": self.parent_client.uuid,
                "server": server_as,
                "hostname": socket.gethostname(),
                "username": os.getlogin() if self.parent_client.__critical_data_exposure__ else "*****",
            }
        )
        await self.parent_client.__websocket__.send_text(response_message.json())
