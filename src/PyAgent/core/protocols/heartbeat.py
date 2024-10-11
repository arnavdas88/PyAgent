from typing import Any
import websockets, asyncio
import datetime
import numpy as np

from PyAgent.core.message import Message, MessageType

class Heartbeat:
    def __init__(self, client: Any, beat_interval: int = 2) -> None:
        self.parent_client = client
        self.beat_interval = beat_interval

    async def client(self, websocket: websockets.WebSocketClientProtocol) -> Any:
        try:
            while True:
                heartbeat = Message(
                    type=MessageType.HEARTBEAT,
                    token=self.parent_client.token,
                    payload={"message": "Alive"}
                )
                await websocket.send(heartbeat.model_dump_json())
                await asyncio.sleep(self.beat_interval)
        except Exception as ex:
            pass
    
    async def server(self, message: Message) -> Any:
        if self.parent_client.last_heartbeat:
            interval = datetime.datetime.fromisoformat( message.timestamp ) - self.parent_client.last_heartbeat
            interval_microseconds = interval / datetime.timedelta(microseconds = 1)
            if not self.parent_client.__beat_interval__:
                self.parent_client.__beat_interval__.append(interval_microseconds) 
            else:
                std = np.std(self.parent_client.__beat_interval__)
                
                interval_acceptable_range_min = (min(self.parent_client.__beat_interval__) - 2*std)
                interval_acceptable_range_max = (max(self.parent_client.__beat_interval__) + 2*std)
                
                if interval_microseconds > interval_acceptable_range_min and interval_microseconds < interval_acceptable_range_max:
                    self.parent_client.__beat_interval__.append(interval_microseconds)
                    if len(self.parent_client.__beat_interval__) > self.parent_client.__BEAT_INTERVAL_STACK_SIZE__:
                        self.parent_client.__beat_interval__.pop(0)
        self.parent_client.last_heartbeat = datetime.datetime.fromisoformat( message.timestamp )


