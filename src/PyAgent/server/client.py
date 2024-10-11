import uuid, socket, os

from fastapi import FastAPI, WebSocket
from typing import Any, Dict, List
from fastapi.websockets import WebSocketState
from pydantic import BaseModel

from datetime import datetime, timedelta

from .connection import ConnectionManager
from PyAgent.core.message import Message, MessageType

from PyAgent.core.protocols.initiation import Initiation
from PyAgent.core.protocols.heartbeat import Heartbeat
from PyAgent.core.protocols.config import Config
from PyAgent.core.protocols.log import Log

from nicegui import ui

class TaskPayload(BaseModel):
    client_id: int
    task_id: str
    task: str
    args: List[Any]
    kwargs: Dict[str, Any]

class ClientModel(BaseModel):
    uuid: uuid.UUID
    heartbeat: str # DateTime
    alive: bool
    hostname: str
    username: str
    cwd: str
    path: str
    tags: List[str]
    avg_beat_interval: float

class Client:
    def __init__(self, websocket: WebSocket, manager: ConnectionManager, critical_data_exposure = False):
        self.__websocket__ = websocket
        self.__manager__ = manager
        self.__beat_interval__ = []
        self.__BEAT_INTERVAL_STACK_SIZE__ = 10 # Stack of 10, used to calculate average beat interval
        self.__critical_data_exposure__ = critical_data_exposure

        self.uuid = None
        self.last_heartbeat = None
        self.hostname = None
        self.username = None
        self.cwd = None
        self.path = None
        self.tags = []

        self.protocol_list = {
            MessageType.INITIATION: Initiation(self),
            MessageType.HEARTBEAT: Heartbeat(self),
            MessageType.CONFIG: Config(self),
            MessageType.LOG: Log(self),
        }


    async def connect(self, ):
        await self.__websocket__.accept()
    
    @property
    def avg_beat_interval(self, ):
        if not self.__beat_interval__:
            return 2
        return sum(self.__beat_interval__)/len(self.__beat_interval__)
    
    @property
    def is_alive(self, ):
        if not self.last_heartbeat:
            return False
        return datetime.now() < self.last_heartbeat + timedelta( microseconds= (2 * self.avg_beat_interval) )

    @property
    def is_active(self, ):
        if not (self.__websocket__.application_state == WebSocketState.CONNECTED and self.__websocket__.client_state == WebSocketState.CONNECTED):
            return False
        return True
    
    async def initiation(self, server_as : str):
        data = await self.__websocket__.receive_text()
        message = Message.model_validate_json(data)

        proto = self.protocol_list[MessageType.INITIATION]
        await proto.server(message, server_as)

    async def process(self, message: Message):
        proto = self.protocol_list[message.type]
        await proto.server(message)
        # self.create_client_card.refresh()

    def to_model(self, ):
        return ClientModel(
            uuid = self.uuid,
            heartbeat = self.last_heartbeat,
            alive = self.is_active,
            hostname = self.hostname,
            username = self.username,
            cwd = self.cwd,
            path = self.path,
            tags = self.tags,
            avg_beat_interval = self.avg_beat_interval
        )

    @ui.refreshable
    def create_client_card(self):
        text_color = "text-slate-600"
        if not self.is_alive:
            text_color = "text-slate-300"

        tag_color = "indigo-5"
        if not self.is_alive:
            tag_color = "indigo-1"
            
        with ui.card():
            with ui.row().classes("flex"):
                ui.label(self.hostname).classes(f"text-lg font-semibold h-9 flex items-center justify-center {text_color}")
                ui.space()
                if self.is_alive:
                    ui.icon('check_circle', size="sm").props('color=green')
                     
            with ui.list().props('dense separator'):
                ui.label(self.uuid).classes(text_color)
                ui.html(f'Running as <strong>{self.username}</strong> user').classes(text_color)
            
            ui.space()

            with ui.row().classes("flex gap-1"):
                for tag in self.tags:
                    ui.chip(tag, icon='label', color=tag_color).props('outline')

            