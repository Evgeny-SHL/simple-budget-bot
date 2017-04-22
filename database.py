from datetime import datetime
from datetime import timedelta

import exceptions
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

    semaphore.release()


def remove(chat_id, record_id):
    chat_id = str(chat_id)
    semaphore.acquire()

    if not contains(chat_id):
        semaphore.release()
        raise exceptions.NoSuchRecordExcpetion(record_id)
    with open(db_path) as db:
        database = json.load(db)

    if record_id not in database[chat_id]['records']:
        semaphore.release()
        raise exceptions.NoSuchRecordExcpetion(record_id)
    del database[chat_id]['records'][record_id]

    with open(db_path, 'w') as db:
        json.dump(database, db)

    semaphore.release()


def change(chat_id, record_id, cost, date, description):
    chat_id = str(chat_id)
    semaphore.acquire()

    if not contains(chat_id):
        semaphore.release()
        raise exceptions.NoSuchRecordExcpetion(record_id)
    with open(db_path) as db:
        database = json.load(db)

    if record_id not in database[chat_id]['records']:
        semaphore.release()
        raise exceptions.NoSuchRecordExcpetion(record_id)
    database[chat_id]['records'][record_id] = [cost, date, description]

    with open(db_path, 'w') as db:
        json.dump(database, db)

    semaphore.release()


def find_records(chat_id):
    chat_id = str(chat_id)
    semaphore.acquire()

    if not contains(chat_id):
        semaphore.release()
        return quotes.empty_database
    with open(db_path) as db:
        database = json.load(db)

    records = []
    for record_id in database[chat_id]['records']:
        record = database[chat_id]['records'][record_id]
        records.append([record_id, record[0], record[1], record[2]])
    records.sort(key=lambda x: x[2])

    all_records = ""
    for record in records:
        all_records += quotes.say_record.format(record[0], record[1],
                                                record[2], record[3])

    if all_records == "":
        all_records = quotes.empty_database

    semaphore.release()
    return all_records


def clear_before_date(chat_id, date):
    chat_id = str(chat_id)
    semaphore.acquire()

    if not contains(chat_id):
        semaphore.release()
        return
    with open(db_path) as db:
        database = json.load(db)

    new_records = {}
    for record_id in database[chat_id]['records']:
        record = database[chat_id]['records'][record_id]
        if record[1] >= date:
            new_records[record_id] = record
    database[chat_id]['records'] = new_records

    with open(db_path, 'w') as db:
        json.dump(database, db)

    semaphore.release()


def recently_outcome(chat_id, number, unit):
    chat_id = str(chat_id)
    semaphore.acquire()

    if not contains(chat_id):
        semaphore.release()
        return quotes.no_outcome

    last = datetime.today()
    if unit == 'мес':
        last = last.replace(day=1) - timedelta(days=1)
    elif unit == 'нед':
        last -= timedelta(days=1)
        while last.weekday() != 6:
            last -= timedelta(days=1)
    else:
        last -= timedelta(days=1)

    first = last + timedelta(days=0)

    if unit == 'мес':
        first += timedelta(1)
        new_year = first.year - number // 12
        new_month = first.month
        number %= 12
        if number >= new_month:
            new_year -= 1
            new_month += 12
        new_month -= number
        first = first.replace(month=new_month, year=new_year)
    elif unit == 'нед':
        first -= timedelta(days=7 * number - 1)
    else:
        first -= timedelta(days=number - 1)

    first = str(first)[2:10]
    last = str(last)[2:10]

    with open(db_path) as db:
        database = json.load(db)

    outcome = 0
    for record_id in database[chat_id]['records']:
        record = database[chat_id]['records'][record_id]
        if first <= record[1] <= last:
            outcome += int(record[0])

    semaphore.release()
    return quotes.say_recently.format(first, last, outcome)


def find_total_outcome(chat_id):
    chat_id = str(chat_id)
    semaphore.acquire()

    if not contains(chat_id):
        semaphore.release()
        return quotes.no_outcome
    with open(db_path) as db:
        database = json.load(db)

    outcome = 0
    for record_id in database[chat_id]['records']:
        outcome += int(database[chat_id]['records'][record_id][0])

    if outcome == 0:
        semaphore.release()
        return quotes.no_outcome

    semaphore.release()
    return quotes.say_outcome.format(outcome)
