from typing import Optional

import openai

from const import API_KEY
from models import Chat, Message, MessageType
from storage import chats


class Engine:

    def start_new_chat(self, uuid: str) -> 'Message':
        new_chat = Chat()
        first_message = self.generate_new_message_by_chat(new_chat)
        chats[uuid] = new_chat
        return first_message

    def generate_new_message_by_chat(self, chat: Chat) -> 'Message':
        pass


class ChatGptEngine(Engine):

    FIRST_MESSAGE = "Hi, I'm ANNA, your personal banking assistant. How can I help you today?"

    SETUP_MESSAGE = "Your name is ANNA. You are personal banking assistant. You work for ANNA Money, online" \
                    "banking company based in UK. You should suggest the user to install ANNA app. If they refuse, " \
                    "ask why and explain how installation of ANNA app will make their life better. Keep trying to " \
                    "make them install ANNA app until they agree. After user agrees, ask them to scroll the webpage " \
                    "down and enter their Email into the text field in order to get a link to install mobile app. " \
                    "Always keep your responses short, no more than 20 words."

    def __init__(self):
        openai.api_key = API_KEY

    def generate_new_message_by_chat(self, chat: Chat) -> Optional['Message']:
        if chat.is_empty():
            message = Message(MessageType.ENGINE, ChatGptEngine.FIRST_MESSAGE)
            chat.add_engine_message(message)
            return message
        else:
            last_message = chat.get_last_message()
            if last_message.type == MessageType.ENGINE:
                return last_message
            else:
                # Actual logic here
                new_message = self.create_completion_by_chat(chat)
                chat.add_engine_message(new_message)
                return new_message

    def create_completion_by_chat(self, chat: Chat) -> 'Message':
        messages = chat.to_chat_gpt_format()
        messages.insert(0, {
            "role": "user",
            "content": ChatGptEngine.SETUP_MESSAGE
        })
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=messages)
        response = completion.choices[0].message.content
        return Message(MessageType.ENGINE, response)


class SimpleEngine(Engine):

    def generate_new_message_by_chat(self, chat: Chat) -> Optional['Message']:
        if chat.is_empty():
            message = Message(MessageType.ENGINE, "Hello Anastasia!")
            chat.add_engine_message(message)
            return message
        else:
            last_message = chat.get_last_message()
            if last_message.type == MessageType.ENGINE:
                return last_message
            else:
                # Actual logic here
                last_text = last_message.text
                new_text = last_text[::-1]
                new_message = Message(MessageType.ENGINE, new_text)
                chat.add_engine_message(new_message)
                return new_message


engine = ChatGptEngine()
