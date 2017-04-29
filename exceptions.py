import quotes


class WrongNumberOfArgumentsException(TypeError):
    def __init__(self, expected, actual):
        self.value = quotes.WRONG_NUMBER_OF_ARGUMENTS.format(expected, actual)

    def __str__(self):
        return repr(self.value)


class NoSuchRecordException(KeyError):
    def __init__(self, record_id):
        self.value = quotes.NO_SUCH_RECORD.format(record_id)

    def __str__(self):
        return repr(self.value)


class InvalidArgumentFormatException(TypeError):
    def __init__(self):
        self.value = quotes.WRONG_NUMBER_OF_ARGUMENTS_COMMON

    def __str__(self):
        return repr(self.value)


class InvalidCostFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.INVALID_COST

    def __str__(self):
        return repr(self.value)


class InvalidDateFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.INVALID_DATE

    def __str__(self):
        return repr(self.value)


class InvalidIdFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.INVALID_ID

    def __str__(self):
        return repr(self.value)


class InvalidNumberFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.INVALID_NUMBER

    def __str__(self):
        return repr(self.value)


class InvalidUnitFormatException(InvalidArgumentFormatException):
    def __init__(self):
        self.value = quotes.INVALID_UNIT

    def __str__(self):
        return repr(self.value)
