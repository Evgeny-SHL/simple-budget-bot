import json
import threading

import exceptions
import parsing
import quotes

db_path = 'db.json'
semaphore = threading.Semaphore()


def add(chat_id, cost, date, description):
    with semaphore:
        chat_id = str(chat_id)
        if not contains(chat_id):
            create_chat(chat_id)
        with open(db_path) as db:
            database = json.load(db)

        add_record(database, chat_id, [cost, date, description])

        with open(db_path, 'w') as db:
            json.dump(database, db)


def remove(chat_id, record_id):
    with semaphore:
        chat_id = str(chat_id)
        if not contains(chat_id):
            raise exceptions.NoSuchRecordExcpetion(record_id)
        with open(db_path) as db:
            database = json.load(db)

        remove_record(database, chat_id, record_id)

        with open(db_path, 'w') as db:
            json.dump(database, db)


def change(chat_id, record_id, cost, date, description):
    with semaphore:
        chat_id = str(chat_id)
        if not contains(chat_id):
            raise exceptions.NoSuchRecordExcpetion(record_id)
        with open(db_path) as db:
            database = json.load(db)

        change_record(database, chat_id, record_id, [cost, date, description])

        with open(db_path, 'w') as db:
            json.dump(database, db)


def find_records(chat_id):
    with semaphore:
        chat_id = str(chat_id)
        if not contains(chat_id):
            return quotes.empty_database
        with open(db_path) as db:
            database = json.load(db)

        all_records = find_all_records(database, chat_id)
        return all_records if all_records != '' else quotes.empty_database


def clear_before_date(chat_id, date):
    with semaphore:
        chat_id = str(chat_id)
        if not contains(chat_id):
            return
        with open(db_path) as db:
            database = json.load(db)

        clear_old_records(database, chat_id, date)

        with open(db_path, 'w') as db:
            json.dump(database, db)


def recently_outcome(chat_id, number, unit):
    with semaphore:
        chat_id = str(chat_id)
        if not contains(chat_id):
            return quotes.no_outcome

        with open(db_path) as db:
            database = json.load(db)

        last = parsing.find_last_day(unit)
        first = parsing.find_first_day(last, unit, int(number))
        outcome = find_recent_outcome(database, chat_id, first, last)
        if first == last:
            return quotes.say_last_day.format(first, outcome) if outcome != 0\
                else quotes.no_last_day_outcome.format(first, last)
        return quotes.say_recently.format(first, last, outcome) if outcome != 0\
            else quotes.no_recent_outcome.format(first, last)


def find_total_outcome(chat_id):
    with semaphore:
        chat_id = str(chat_id)
        if not contains(chat_id):
            return quotes.no_outcome
        with open(db_path) as db:
            database = json.load(db)

        outcome = sum_outcome(database, chat_id)
        return quotes.say_outcome.format(outcome) if outcome != 0\
            else quotes.no_outcome


def contains(chat_id):
    with open(db_path) as db:
        database = json.load(db)
    return chat_id in database


def create_chat(chat_id):
    with open(db_path) as db:
        database = json.load(db)

    add_chat(database, chat_id)

    with open(db_path, 'w') as db:
        json.dump(database, db)


def add_chat(database, chat_id):
    database[chat_id] = {
        'next_id': 0,
        'records': {
        }
    }


def add_record(database, chat_id, value):
    record_id = str(database[chat_id]['next_id'])
    database[chat_id]['next_id'] += 1
    database[chat_id]['records'][record_id] = value


def remove_record(database, chat_id, record_id):
    if record_id not in database[chat_id]['records']:
        raise exceptions.NoSuchRecordExcpetion(record_id)
    del database[chat_id]['records'][record_id]


def change_record(database, chat_id, record_id, value):
    if record_id not in database[chat_id]['records']:
        raise exceptions.NoSuchRecordExcpetion(record_id)
    database[chat_id]['records'][record_id] = value


def find_all_records(database, chat_id):
    records = find_sorted_records_list(database, chat_id)
    all_records = ''
    for record in records:
        all_records += quotes.say_record.format(record[0], record[1],
                                                record[2], record[3])
    return all_records


def find_sorted_records_list(database, chat_id):
    records = []
    for record_id in database[chat_id]['records']:
        record = database[chat_id]['records'][record_id]
        records.append([record_id, record[0], record[1], record[2]])
    return sorted(records, key=lambda x: x[2])


def clear_old_records(database, chat_id, date):
    new_records = {}
    for record_id in database[chat_id]['records']:
        record = database[chat_id]['records'][record_id]
        if record[1] >= date:
            new_records[record_id] = record
    database[chat_id]['records'] = new_records


def sum_outcome(database, chat_id):
    outcome = 0
    for record_id in database[chat_id]['records']:
        outcome += int(database[chat_id]['records'][record_id][0])
    return outcome


def find_recent_outcome(database, chat_id, first, last):
    outcome = 0
    for record_id in database[chat_id]['records']:
        record = database[chat_id]['records'][record_id]
        if first <= record[1] <= last:
            outcome += int(record[0])
    return outcome
