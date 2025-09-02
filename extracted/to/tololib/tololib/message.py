from .enums import Command


class Message(object):
    """Class representing a message sent over network.

    By default, the TOLO App Box listens on UDP port 51500 for receiving control messages.
    Each messaged received by TOLO App Box is answered with a message with the same structure, but different values.
    This class represents such request/response messages and provides functionality for parsing, validating and
    creating messages.

    Each message has the following structure:
      * 2 bytes fixed `0xAAAA`
      * 1 byte command code (see CommandCode enum)
      * 1 byte command value
      * x bytes response message (depends on the command and the reply from TOLO App Box)
      * 2 bytes fixed `0x5555`
      * 1 byte checksum, byte-wise XOR of all previously mentioned data
    """

    PREFIX = b"\xaa\xaa"
    SUFFIX = b"\x55\x55"

    def __init__(self, command: Command, command_value: bytes, extra: bytes) -> None:
        if not isinstance(command_value, bytes) or len(command_value) != 1:
            raise ValueError("command value not bytes of length 1")

        self._command = command
        self._command_value = command_value
        self._extra = extra

    @property
    def command(self) -> Command:
        return self._command

    @property
    def command_value(self) -> bytes:
        return self._command_value

    @property
    def extra(self) -> bytes:
        return self._extra

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> "Message":
        command_code = Command.from_code(message_bytes[2])
        command_value = bytes([message_bytes[3]])
        extra = message_bytes[4:-3]

        return Message(command_code, command_value, extra)

    def to_bytes(self) -> bytes:
        data = self.PREFIX + bytes([self._command.code]) + self._command_value + self._extra + self.SUFFIX
        data += self.generate_crc(data)
        return data

    def __bytes__(self) -> bytes:
        return self.to_bytes()

    def __repr__(self) -> str:
        return f"<Message {self.command.name}({str(self.command_value)}): {str(self.extra)}>"

    @staticmethod
    def generate_crc(data: bytes) -> bytes:
        crc = 0x00
        for b in data:
            crc = crc ^ b
        return crc.to_bytes(1, byteorder="big")

    @classmethod
    def validate_crc(cls, raw_bytes: bytes) -> bool:
        return cls.generate_crc(raw_bytes[:-1]) == raw_bytes[-1].to_bytes(1, "big")

    @classmethod
    def validate_meta(cls, raw_bytes: bytes) -> bool:
        """Validates metadata of message bytes.

        The validation will check for prefix, suffix and CRC.
        It will NOT check for valid code or payload.

        Args:
            raw_bytes (bytes): binary data to be checked

        Returns:
            True if the check was successful and the metadata is as expected, False otherwise.
        """
        if not raw_bytes.startswith(cls.PREFIX):
            return False
        if not raw_bytes[:-1].endswith(cls.SUFFIX):
            return False
        return cls.validate_crc(raw_bytes)
