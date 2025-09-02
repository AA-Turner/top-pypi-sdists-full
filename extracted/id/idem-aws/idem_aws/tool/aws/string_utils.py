def unescape_ascii(hub, input_str: str):
    """
    If '*' and '@' are present in any attribute values, boto3 API returns the attribute values
    with ASCII equivalent of '*' and '@'. we need to replace ASCII characters with equivalent string characters
    to compare with user input.

    Args:
        input_str: value of the attribute

    Returns:
        cleaned attribute value by replacing the ASCII characters with equivalent string characters

    """
    return input_str.encode("utf-8").decode("unicode_escape")
