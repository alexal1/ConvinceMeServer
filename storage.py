import multiprocessing

from models import Chat

_chats: dict[str, 'Chat'] = {}


lock = multiprocessing.Lock()


def get_chat(uuid):
    with lock:
        return _chats.get(uuid)


def update_chat(uuid, chat):
    with lock:
        _chats[uuid] = chat
