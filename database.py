import json
import threading
import quotes

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
    try:
        semaphore.acquire()

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


def find_records(chat_id):
    chat_id = str(chat_id)
    try:
        semaphore.acquire()

        all_records = ""
        if not contains(chat_id):
            all_records = quotes.empty_database
            semaphore.release()
            return quotes.empty_database
        with open(db_path) as db:
            database = json.load(db)

        for record_id in database[chat_id]['records']:
            record = database[chat_id]['records'][record_id]
            all_records += '[' + record_id + '] '
            all_records += record[0] + ' ед. '
            all_records += record[1][:10] + ': "'
            all_records += record[2] + '"\n'

        if all_records == "":
            all_records = quotes.empty_database
    finally:
        semaphore.release()
    return all_records
