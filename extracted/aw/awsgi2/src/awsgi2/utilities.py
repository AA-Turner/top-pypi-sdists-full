"""Utilities"""
from urllib.parse import unquote
from base64 import b64encode


def clean_path_string(path: str) -> str:
    """
    Some WSGI applications expect paths to be unquoted before receiving them
    """
    return unquote(path)


def convert_b64(content: bytes) -> str:
    """Convert content to B64 but return as string instead of bytes"""
    return b64encode(content).decode("ascii")
