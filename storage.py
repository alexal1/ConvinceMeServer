import sqlite3

from logger import logger
from models import Chat, Message, MessageType

DB_FILENAME = "storage.db"


def init():
    logger.debug("STORAGE: init")
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id TEXT PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id TEXT PRIMARY KEY,
                  chat_id TEXT,
                  text TEXT,
                  type TEXT,
                  FOREIGN KEY (chat_id) REFERENCES chats(id))''')
    conn.commit()
    c.close()


def get_chat(uuid):
    logger.debug("STORAGE: get_chat")
    create_chat(uuid)
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE chat_id=?", (uuid,))
    messages = [Message(MessageType.by(row[3]), row[2], row[0]) for row in c.fetchall()]
    chat = Chat(messages)
    c.close()
    return chat


def update_chat(uuid, message):
    logger.debug("STORAGE: update_chat")
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute("INSERT INTO messages (id, chat_id, text, type) VALUES (?, ?, ?, ?)",
              (message.id, uuid, message.text, message.type.value))
    conn.commit()
    c.close()


def create_chat(uuid):
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO chats (id) VALUES (?)", (uuid,))
    conn.commit()
    c.close()
