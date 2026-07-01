"""Common utility for decoding unicode messages sent in chunks"""
from typing import Tuple


def careful_decode(byte_str: bytes) -> Tuple[str, bytes]:
    """Decode a byte string as UTF8, ignoring any errors at the start of the string

    Args:
        byte_str (bytes): The byte string to decode

    Returns:
        Tuple[str, bytes]: The decoded string + any remaining bytes that are not valid UTF8
    """
    try:
        return byte_str.decode('utf8'), b''
    except UnicodeDecodeError as e:
        if e.start == 0:
            # Error is at the start. Let's just ignore these bytes
            return careful_decode(byte_str[e.end:])
        else:
            remaining = byte_str[e.start:]
            decoded = byte_str[:e.start].decode('utf8')
            return decoded, remaining


class MessageDecoder:
    """Decode message chunks as UTF8
    """

    def __init__(self):
        # Remaining bytes from previous message
        self.remaining = b''

        # prev can be used to maintain things that come after the final linebreak.
        self.prev = ''

    def decode(self, message_bytes: bytes) -> str:
        """Decode a message chunk as UTF8

        Args:
            message_bytes (bytes): The message chunk to decode

        Returns:
            str: The decoded message chunk
        """
        # Add any previous hanging bytes
        byte_str: bytes = self.remaining + message_bytes

        # Decode whatever we can
        decoded, self.remaining = careful_decode(byte_str)

        # Combine with previous, if needed
        decoded, self.prev = self.prev + decoded, ''

        return decoded
