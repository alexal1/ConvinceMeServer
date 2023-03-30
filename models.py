import json
import uuid
from enum import Enum, unique
from typing import Optional

from logger import logger


class Chat:

    _messages = []

    def __init__(self):
        self._messages: list['Message'] = []

    def is_empty(self):
        return len(self._messages) == 0

    def add_user_message(self, message) -> bool:
        if message.type != MessageType.USER:
            logger.error("Cannot add a user message: wrong type")
            return False

        if len(self._messages) == 0 or self._messages[-1].type == MessageType.USER:
            logger.error("Cannot add a user message because chat is empty or the last message is from user")
            return False

        self._messages.append(message)
        return True

    def add_engine_message(self, message) -> bool:
        if message.type != MessageType.ENGINE:
            logger.error("Cannot add an engine message: wrong type")
            return False

        if len(self._messages) > 0 and self._messages[-1].type == MessageType.ENGINE:
            logger.error("Cannot add an engine message because the last message is from engine")
            return False

        self._messages.append(message)
        return True

    def get_last_engine_message(self) -> Optional['Message']:
        for i in range(len(self._messages) - 1, -1, -1):
            message = self._messages[i]
            if message.type == MessageType.ENGINE:
                return message
        logger.error("Strange, no engine message in a chat...")
        return None

    def get_last_message(self) -> Optional['Message']:
        if len(self._messages) == 0:
            return None

        return self._messages[-1]

    def to_chat_gpt_format(self):
        result = []
        for message in self._messages:
            result.append(message.to_chat_gpt())
        return result


class Message:
    id: str
    text: str
    type: 'MessageType'

    def __init__(self, type, text):
        self.id = str(uuid.uuid4())
        self.type = type
        self.text = text

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "text": self.text
        })

    def to_chat_gpt(self):
        return {
            "role": "user" if self.type == MessageType.USER else "assistant",
            "content": self.text
        }


@unique
class MessageType(Enum):
    USER = "user"
    ENGINE = "engine"
