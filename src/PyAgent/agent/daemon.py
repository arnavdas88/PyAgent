import time
import asyncio
import websockets

from rich.console import Console

from PyAgent.core.message import Message, MessageType

from PyAgent.core.protocols.initiation import Initiation
from PyAgent.core.protocols.heartbeat import Heartbeat
from PyAgent.core.protocols.config import Config
from PyAgent.core.protocols.log import Log

class WebSocketDaemon:
    def __init__(self, uri, token, tags = [], cookies = {}):
        self.console = Console()

        self.uri = uri

        self.uuid = None
        self.token = token
        self.server = None
        self.hostname = None
        self.username = None

        self.tags = tags
        self.cookies = cookies

        self.protocol_list = {
            MessageType.INITIATION: Initiation(self, self.tags),
            MessageType.HEARTBEAT: Heartbeat(self),
            MessageType.LOG: Log(self),
            MessageType.CONFIG: Config(self),
        }

    async def connect(self):
        async with websockets.connect(self.uri, extra_headers = {"cookie": "; ".join( self.cookies )}, ) as websocket:

            with self.console.status("Initializing...") as spinner:
                initiation = self.protocol_list[MessageType.INITIATION]
                await initiation.client(websocket)

                while True:
                    time.sleep(.5)
                    await self.loop(websocket)
                    if self.uuid:
                        break

                heartbeat = self.protocol_list[MessageType.HEARTBEAT]
                asyncio.create_task(heartbeat.client(websocket))


            self.console.print(f"[ + ] Handshake Successful with server \"{self.server}\"")

            initiation = self.protocol_list[MessageType.INITIATION]
            self.console.print_json(
                data = {
                    "token": self.token,
                    "tags": self.tags,
                    "server": 
                    {
                        "server": self.server,
                        "hostname": self.hostname,
                        "username": self.username,
                    },
                    "client":{
                        "uuid": self.uuid,
                        "hostname": initiation.payload["hostname"],
                        "username": initiation.payload["username"],
                    },

                }
            )

            while True:
                await self.loop(websocket)
    
    async def loop(self, websocket):
        try:
            response = await websocket.recv()
            message = Message.model_validate_json(response)

            proto = self.protocol_list[message.type]
            await proto.client(websocket, message.payload)
        except websockets.ConnectionClosedError as ex:
            self.console.print("[ i ] Agent abruptly disconnected.")
            for _ in range(10):
                self.console.print("[   ] Trying to reconnect...")
                try:
                    await self.connect()
                except Exception as ex:
                    await asyncio.sleep(5)
                    pass
            self.console.print("[ x ] Unable to reconnect.")
            exit(1)
        except Exception as ex:
            pass



    