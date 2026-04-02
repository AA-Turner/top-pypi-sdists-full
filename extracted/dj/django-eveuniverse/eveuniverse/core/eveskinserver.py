"""Wrapper for accessing eveskinserver API."""

_EVE_SKIN_SERVER_URL = "https://eveskinserver.kalkoken.net"
_DEFAULT_IMAGE_SIZE = 32


def type_icon_url(type_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """icon image URL for the given SKIN type ID"""
    if not size or size < 32 or size > 1024 or (size & (size - 1) != 0):
        raise ValueError(f"Invalid size: {size}")
    return f"{_EVE_SKIN_SERVER_URL}/skin/{int(type_id)}/icon?size={size}"
