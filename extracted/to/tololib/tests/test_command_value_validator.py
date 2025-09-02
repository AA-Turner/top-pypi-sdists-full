from unittest import TestCase

from tololib.command_value_handler import CommandValueHandler
from tololib.enums import LampMode


class CommandValidatorValidatorTest(TestCase):
    def test_init(self) -> None:
        self.assertRaises(ValueError, CommandValueHandler[int], none_equivalent=b"12")

    def test_byte2native(self) -> None:
        int_validator = CommandValueHandler[int]()
        self.assertEqual(int_validator.byte2native(b"\x03"), 3)
        self.assertRaises(ValueError, int_validator.byte2native, b"12")

        bool_validator = CommandValueHandler[bool]()
        self.assertEqual(bool_validator.byte2native(b"1"), True)
        self.assertEqual(bool_validator.byte2native(b"\x01"), True)
        self.assertEqual(bool_validator.byte2native(b"\x00"), False)

        enum_validator = CommandValueHandler[LampMode]()
        self.assertEqual(enum_validator.byte2native(b"\x00"), LampMode.MANUAL)
        self.assertEqual(enum_validator.byte2native(b"\x01"), LampMode.AUTOMATIC)
        self.assertRaises(ValueError, enum_validator.byte2native, b"\x02")

    def test_native2byte(self) -> None:
        int_validator = CommandValueHandler[int]()
        self.assertEqual(int_validator.native2byte(3), b"\x03")

        bool_validator = CommandValueHandler[bool]()
        self.assertEqual(bool_validator.native2byte(True), b"\x01")
        self.assertEqual(bool_validator.native2byte(False), b"\x00")

        enum_validator = CommandValueHandler[LampMode]()
        self.assertEqual(enum_validator.native2byte(LampMode.MANUAL), b"\x00")
        self.assertEqual(enum_validator.native2byte(LampMode.AUTOMATIC), b"\x01")
        self.assertRaises(ValueError, enum_validator.native2byte, None)

        self.assertRaises(ValueError, enum_validator.native2byte, "foobar")

    def test_chr2int(self) -> None:
        self.assertRaises(ValueError, CommandValueHandler.chr2int, b"12")
        self.assertRaises(ValueError, CommandValueHandler.chr2int, "s")

        self.assertEqual(CommandValueHandler.chr2int(b"\x00"), 0)
        self.assertEqual(CommandValueHandler.chr2int(b"\x01"), 1)
        self.assertEqual(CommandValueHandler.chr2int(b"\x03"), 3)
        self.assertEqual(CommandValueHandler.chr2int(b"\xff"), 255)

    def test_int2chr(self) -> None:
        self.assertRaises(ValueError, CommandValueHandler.int2chr, -1)
        self.assertRaises(ValueError, CommandValueHandler.int2chr, 256)

        self.assertEqual(CommandValueHandler.int2chr(0), b"\x00")
        self.assertEqual(CommandValueHandler.int2chr(1), b"\x01")
        self.assertEqual(CommandValueHandler.int2chr(3), b"\x03")
        self.assertEqual(CommandValueHandler.int2chr(255), b"\xff")
