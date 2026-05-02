import re

WORD_PATTERN = re.compile(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])|[0-9]+')
UNWANTED_PATTERN = re.compile(r"[^a-zA-Z0-9\s]")
ILLEGAL_CHARS = re.compile(r"[^A-Za-z0-9_\s]+")


def remove_illegal_chars(value: str) -> str:
    return ILLEGAL_CHARS.sub('', value)


def is_camelcase(value):
    return re.match(r"^[A-Za-z0-9]+\s?(?:[A-Za-z0-9])*$", value.strip()) is not None


def to_camel_case(s: str) -> str:
    """to_camel_case.

        Converts a phrase into CamelCase Format.

    Args:
        s (str): The string to convert.

    Returns:
        The converted string in CamelCase format.
    """
    # Remove unwanted characters
    # s = re.sub(, "", s)
    s = UNWANTED_PATTERN.sub("", s)
    # Convert to CamelCase
    s = "".join(word.capitalize() for word in s.split())
    return s

def is_snakecase(value):
    ## already in snake case:
    return re.match(r"^[a-zA-Z][a-zA-Z0-9_]+_[a-zA-Z0-9]*$", value.strip()) is not None


def to_snake_case(s: str) -> str:
    """to_snake_case.

        Converts an string into snake_case format.

    Args:
        s (str): The string to convert.

    Returns:
        The converted string in snake_case format.
    """
    # Remove unwanted characters
    s = UNWANTED_PATTERN.sub("", s)

    # Find all words in the string
    words = WORD_PATTERN.findall(s)

    # Join the words with underscores
    s = '_'.join(words)

    return s.lower()


def camelcase_split(value):
    """camelcase_split.

    Splits a CamelCase word in other words.
    """
    if bool(re.match(r"[A-Z]+$", value)):
        return re.findall(r"[A-Z]+$", value)
    elif bool(re.search(r"\d", value)):
        return re.findall(r"[A-Z](?:[a-z]+[1-9]?|[A-Z]*(?=[A-Z])|$)", value)
    elif value[0].isupper():
        return re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", value)
    else:
        return re.findall(r"^[a-z]+|[A-Z][^A-Z]*", value)
