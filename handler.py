from typing import Optional

from engine import engine
from logger import logger
from models import Message, MessageType
from storage import chats


def get_latest_engine_message(uuid: str) -> Optional['Message']:
    chat = chats.get(uuid)
    if chat is None:
        return engine.start_new_chat(uuid)
    else:
        last_engine_message = chat.get_last_engine_message()
        logger.error("get_latest_engine_message: uuid = " + uuid + ", message id = " + last_engine_message.id + ", message content = " + last_engine_message.text)
        return chat.get_last_engine_message()


def post_new_user_message(uuid: str, json_message) -> bool:
    chat = chats.get(uuid)
    if chat is None:
        return False

    if json_message is None:
        return False

    text = json_message.get("text")
    if text is None:
        return False

    message = Message(MessageType.USER, text)
    chat.add_user_message(message)
    return engine.generate_new_message_by_chat(chat)
