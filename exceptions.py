import quotes


class WrongNumberOfArgumentsException(BaseException):
    def __init__(self, expected, actual):
        self.value = quotes.wrong_number_of_arguments.format(expected, actual)

    def __str__(self):
        return repr(self.value)

class NoSuchRecordExcpetion(BaseException):
    def __init__(self, record_id):
        self.value = quotes.no_such_record.format(record_id)

    def __str__(self):
        return repr(self.value)


class InvalidDateException(BaseException):
    def __init__(self):
        self.value = quotes.wrong_date

    def __str__(self):
        return repr(self.value)


class InvalidUnitException(BaseException):
    def __init__(self):
        self.value = quotes.wrong_unit

    def __str__(self):
        return repr(self.value)
