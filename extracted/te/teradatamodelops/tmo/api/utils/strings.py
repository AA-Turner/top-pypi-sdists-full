INPUT_MUST_BE_STRING_ERROR = "Input must be a string"


def camel_to_normalized(camel_str: str, joiner: str = " ") -> str:
    """
    Converts a camelCase string to a normalized format using the specified joiner (e.g., space, hyphen).

    Parameters:
        camel_str (str): The input string in camelCase.
        joiner (str): The string to insert between words (default is a space).

    Returns:
        str: The normalized string.
    """
    if not isinstance(camel_str, str):
        raise ValueError(INPUT_MUST_BE_STRING_ERROR)
    normalized_str = ""
    for i, char in enumerate(camel_str):
        if char.isupper() and i != 0:
            normalized_str += joiner
        normalized_str += char.lower()
    return normalized_str.strip()


def snake_to_normalized(snake_str: str, joiner: str = " ") -> str:
    """
    Converts a snake_case string to a normalized format using the specified joiner (e.g., space, hyphen).

    Parameters:
        snake_str (str): The input string in snake_case.
        joiner (str): The string to replace underscores with (default is a space).

    Returns:
        str: The normalized string.
    """
    if not isinstance(snake_str, str):
        raise ValueError(INPUT_MUST_BE_STRING_ERROR)
    return snake_str.lower().replace("_", joiner)


def snake_to_camel(snake_str: str, separator: str = "_") -> str:
    """
    Converts a snake_case string to camelCase.

    Parameters:
        snake_str (str): The input string in snake_case.
        separator (str): The character used to separate words in the input string (default is an underscore).

    Returns:
        str: The camelCase version of the input string.
    """
    if not isinstance(snake_str, str):
        raise ValueError(INPUT_MUST_BE_STRING_ERROR)
    components = snake_str.split(separator)
    return components[0].lower() + "".join(x.title() for x in components[1:])
