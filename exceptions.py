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


class InvalidArgumentFormatException(BaseException):
    def __init__(self):
        self.value = ''

    def __str__(self):
        return repr(self.value)


class InvalidCostFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.invalid_cost

    def __str__(self):
        return repr(self.value)


class InvalidDateFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.invalid_date

    def __str__(self):
        return repr(self.value)


class InvalidIdFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.invalid_id

    def __str__(self):
        return repr(self.value)


class InvalidNumberFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.invalid_number

    def __str__(self):
        return repr(self.value)


class InvalidUnitFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.invalid_unit

    def __str__(self):
        return repr(self.value)
