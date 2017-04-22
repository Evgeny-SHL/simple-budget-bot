import exceptions

args_counts = {
    '/add': 3,
    '/remove': 1,
    '/change': 4,
    '/last': 2,
    '/clear': 1
}


def get_arguments(text, last_is_string=False):
    split = text.split()
    trimmed = list(map(lambda string: string.strip(), split))
    message = list(filter(lambda string: len(string) > 0, trimmed))
    command, arguments = message[0], message[1:]
    if last_is_string and len(arguments) >= args_counts[command]:
        last_argument = ' '.join(arguments[args_counts[command] - 1:])
        arguments[args_counts[command] - 1:] = [last_argument]
    print(arguments)
    if len(arguments) != args_counts[command]:
        raise exceptions.WrongNumberOfArgumentsException(
            args_counts[command], len(arguments))
    return arguments
