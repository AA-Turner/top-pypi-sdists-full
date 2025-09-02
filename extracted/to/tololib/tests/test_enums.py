from unittest import TestCase

from tololib.enums import Command


class CommandTest(TestCase):
    def test_from_code(self) -> None:
        self.assertEqual(Command.SET_POWER_ON, Command.from_code(14))

        self.assertRaises(ValueError, Command.from_code, 255)

    def test_ne(self) -> None:
        self.assertNotEqual(Command.SET_POWER_ON, Command.SET_FAN_ON)
