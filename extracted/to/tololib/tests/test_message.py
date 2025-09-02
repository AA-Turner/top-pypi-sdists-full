from unittest import TestCase

from tololib.enums import Command
from tololib.message import Message


class MessageTest(TestCase):
    def test_init(self) -> None:
        self.assertRaises(ValueError, Message, Command.SET_TARGET_TEMPERATURE, b"12", b"\xff")

    def test_generate_crc(self) -> None:
        self.assertEqual(Message.generate_crc(b"\xaa\xaaa\x00\xffUU"), b"\x9e")

        self.assertNotEqual(Message.generate_crc(b"\xaa\xaaa\x00\xffUU"), 0)

    def test_validate_crc(self) -> None:
        self.assertTrue(Message.validate_crc(b"\xaa\xaaa\x00\xffUU\x9e"))

        self.assertFalse(Message.validate_crc(b"\xaa\xaaa\x00\xffUU\x00"))

    def test_validate_meta(self) -> None:
        self.assertTrue(Message.validate_meta(b"\xaa\xaaa\x00\xffUU\x9e"))
        self.assertTrue(Message.validate_meta(b"\xaa\xaaFOOBAR\xffUU\xe8"))

        self.assertFalse(Message.validate_meta(b"\xaa\xaaa\x00\xffUU\x00"))
        self.assertFalse(Message.validate_meta(b"\xaaa\x00\xffU\x9e"))
        self.assertFalse(Message.validate_meta(b"\xaa\xaaa\x00\xffVV\x9e"))

    def test_to_bytes(self) -> None:
        bytes_data = b"\xaa\xaaa\x00\xffUU\x9e"
        message = Message.from_bytes(bytes_data)
        self.assertEqual(bytes_data, message.to_bytes())
        self.assertEqual(bytes_data, bytes(message))

    def test_repr(self) -> None:
        command = Command.SET_TARGET_TEMPERATURE
        message = Message(command, command.value_handler.native2byte(42), b"\xff")
        self.assertEqual(repr(message), "<Message SET_TARGET_TEMPERATURE(b'*'): b'\\xff'>")
