import datetime

import exceptions

args_counts = {
    '/add': 3,
    '/remove': 1,
    '/change': 4,
    '/last': 2,
    '/clear': 1
}


def find_arguments(text, last_is_string=False):
    split = text.split()
    trimmed = list(map(lambda string: string.strip(), split))
    message = list(filter(lambda string: len(string) > 0, trimmed))
    command, arguments = message[0].split('@')[0], message[1:]
    if last_is_string and len(arguments) >= args_counts[command]:
        last_argument = ' '.join(arguments[args_counts[command] - 1:])
        arguments[args_counts[command] - 1:] = [last_argument]
    if len(arguments) != args_counts[command]:
        raise exceptions.WrongNumberOfArgumentsException(
            args_counts[command], len(arguments))
    return arguments


def get_cost(value):
    try:
        if int(value) <= 0:
            raise exceptions.InvalidCostFormatException
        return str(int(value))
    except:
        raise exceptions.InvalidCostFormatException


def get_date(value):
    try:
        return extract_yy_mm_dd(str(datetime.datetime.strptime(value,
                                                               '%y-%m-%d')))
    except:
        raise exceptions.InvalidDateFormatException


def get_description(value):
    return value


def get_id(value):
    try:
        if int(value) < 0:
            raise exceptions.InvalidCostFormatException
        return str(int(value))
    except:
        raise exceptions.InvalidIdFormatException


def get_number(value):
    try:
        if int(value) <= 0:
            raise exceptions.InvalidCostFormatException
        return str(int(value))
    except:
        raise exceptions.InvalidNumberFormatException


def get_unit(value):
    try:
        if value not in ['дн', 'нед', 'мес']:
            raise exceptions.InvalidUnitFormatException
        return value
    except:
        raise exceptions.InvalidUnitFormatException


def extract_yy_mm_dd(str_datetime):
    return str_datetime[2:10]


def find_last_day(unit):
    last = datetime.datetime.today()
    if unit == 'мес':
        last = last.replace(day=1)
    elif unit == 'нед':
        while last.weekday() != 0:
            last -= datetime.timedelta(days=1)
    elif unit == 'дн':
        pass
    else:
        raise exceptions.InvalidUnitFormatException
    last -= datetime.timedelta(days=1)
    return extract_yy_mm_dd(str(last))


def find_first_day(last, unit, number):
    first = datetime.datetime.strptime(last, '%y-%m-%d') +\
            datetime.timedelta(days=1)
    if unit == 'мес':
        month, year = subtract_months(first, number)
        first = first.replace(month=month, year=year)
    elif unit == 'нед':
        first -= datetime.timedelta(days=7 * number)
    elif unit == 'дн':
        first -= datetime.timedelta(days=number)
    else:
        raise exceptions.InvalidUnitFormatException
    return extract_yy_mm_dd(str(first))


def subtract_months(date, months):
    month = date.month - months % 12
    year = date.year - months // 12
    if month < 1:
        year -= 1
        month += 12
    return month, year
