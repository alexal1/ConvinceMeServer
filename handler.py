from typing import Optional

from engine import engine
from logger import logger
from models import Message, MessageType
from storage import get_chat, update_chat


def get_latest_engine_message(uuid: str) -> Optional['Message']:
    chat = get_chat(uuid)
    if chat is None:
        first_message = engine.start_new_chat(uuid)
        logger.error("NEW CHAT first_message: uuid = " + uuid + ", message id = " + first_message.id + ", message content = " + first_message.text)
        return engine.start_new_chat(uuid)
    else:
        last_engine_message = chat.get_last_engine_message()
        logger.error("get_latest_engine_message: uuid = " + uuid + ", message id = " + last_engine_message.id + ", message content = " + last_engine_message.text)
        return chat.get_last_engine_message()


def post_new_user_message(uuid: str, json_message) -> bool:
    chat = get_chat(uuid)
    if chat is None:
        return False

    if json_message is None:
        return False

    text = json_message.get("text")
    if text is None:
        return False

    message = Message(MessageType.USER, text)
    chat.add_user_message(message)
    update_chat(uuid, chat)
    return engine.generate_new_message_by_chat(chat)
