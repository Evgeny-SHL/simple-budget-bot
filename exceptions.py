import quotes


class WrongNumberOfArgumentsException(BaseException):
    def __init__(self, expected, actual):
        self.value = quotes.wrong_number_of_arguments.format(expected, actual)

    def __str__(self):
        return repr(self.value)
