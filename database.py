import json
import threading

db_path = 'database.json'
semaphore = threading.Semaphore()


def contains(chat_id):
    with open(db_path) as db:
        database = json.load(db)

    return chat_id in database


def create_chat(chat_id):
    with open(db_path) as db:
        database = json.load(db)

    database[chat_id] = {
        'next_id': 0,
        'records': {
        }
    }

    with open(db_path, 'w') as db:
        json.dump(database, db)


def add(chat_id, cost, date, description):
    chat_id = str(chat_id)
    semaphore.acquire()
    try:
        if not contains(chat_id):
            create_chat(chat_id)

        with open(db_path) as db:
            database = json.load(db)

        record_id = str(database[chat_id]['next_id'])
        database[chat_id]['next_id'] += 1
        database[chat_id]['records'][record_id] = [cost, date, description]

        with open(db_path, 'w') as db:
            json.dump(database, db)
    finally:
        semaphore.release()
