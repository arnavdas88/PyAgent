import enum
from pydantic import BaseModel
from datetime import datetime

class MessageType(enum.StrEnum):
    LOG = "log"
    CONFIG = "config"
    HEARTBEAT = "heartbeat"
    INITIATION = "initiation"
    # QUERY = "query"
    # ANSWER = "answer"
    # UPDATE = "update"
    # CONSENSUS = "consensus"

class Message(BaseModel):
    type: MessageType
    token: str
    payload: dict
    timestamp: str

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)
