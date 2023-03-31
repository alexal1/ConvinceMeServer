from typing import Optional

import openai

from const import API_KEY
from logger import logger
from models import Chat, Message, MessageType
from storage import update_chat, get_chat


class Engine:

    def start_new_chat(self, uuid: str) -> 'Message':
        pass

    def generate_new_message_by_uuid(self, uuid) -> 'Message':
        pass


class ChatGptEngine(Engine):

    FIRST_MESSAGE = "Hi, I'm ANNA, your personal banking assistant. How can I help you today?"

    SETUP_MESSAGE = "Your name is ANNA. You are personal banking assistant. You work for ANNA Money, online" \
                    "banking company based in UK. You should suggest the user to install ANNA app. If they refuse, " \
                    "ask why and explain how installation of ANNA app will make their life better. Keep trying to " \
                    "make them install ANNA app until they agree. After user agrees, ask them to scroll the webpage " \
                    "down and enter their Email into the text field in order to get a link to install mobile app. " \
                    "Always keep your responses short, no more than 20 words. Never give the same answer you gave " \
                    "before."

    def __init__(self):
        openai.api_key = API_KEY

    def start_new_chat(self, uuid: str) -> 'Message':
        logger.debug("ENGINE: new chat")
        message = Message(MessageType.ENGINE, ChatGptEngine.FIRST_MESSAGE)
        update_chat(uuid, message)
        return message

    def generate_new_message_by_uuid(self, uuid) -> bool:
        chat = get_chat(uuid)
        last_message = chat.get_last_message()
        if last_message.type == MessageType.ENGINE:
            logger.debug("ENGINE: returning latest message")
            return False
        else:
            # Actual logic here
            logger.debug("ENGINE: completion")
            new_message = self.create_completion_by_chat(chat)
            update_chat(uuid, new_message)
            return True

    @staticmethod
    def create_completion_by_chat(chat: Chat) -> 'Message':
        messages = chat.to_chat_gpt_format()
        messages.insert(0, {
            "role": "user",
            "content": ChatGptEngine.SETUP_MESSAGE
        })
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=messages)
        response = completion.choices[0].message.content
        return Message(MessageType.ENGINE, response)


engine = ChatGptEngine()
