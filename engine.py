from typing import Optional

from models import Chat, Message, MessageType
from storage import chats


class Engine:

    def start_new_chat(self, uuid: str) -> 'Message':
        pass

    def generate_new_message_by_chat(self, chat: Chat) -> 'Message':
        pass


class SimpleEngine(Engine):

    def start_new_chat(self, uuid: str) -> 'Message':
        new_chat = Chat()
        first_message = self.generate_new_message_by_chat(new_chat)
        chats[uuid] = new_chat
        return first_message

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


engine = SimpleEngine()
