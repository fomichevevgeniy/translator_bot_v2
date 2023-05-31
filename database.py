import sqlite3


def connect_database():
    db = sqlite3.connect('bot.db')
    cursor = db.cursor()
    return cursor, db


def create_table():
    cursor, db = connect_database()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bot(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        original_text TEXT,
        src TEXT,
        dest TEXT,
        translated_text TEXT
    )''')
    db.commit()
    db.close()


create_table()

def save_data(chat_id, original_text, src, dest, translated_text):
    cursor, db = connect_database()
    cursor.execute('''
        INSERT INTO bot(chat_id, original_text, src, dest, translated_text) VALUES
        (?,?,?,?,?)
    ''', (chat_id, original_text, src, dest, translated_text))
    db.commit()
    db.close()


def get_history(chat_id):
    cursor, db = connect_database()
    cursor.execute('''
    SELECT original_text, src, dest, translated_text FROM bot WHERE chat_id = ?
    ''', (chat_id, ))
    history = cursor.fetchall()
    db.close()
    return history










