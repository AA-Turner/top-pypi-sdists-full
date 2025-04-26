import unittest
from dataclasses import dataclass
from unittest.mock import patch

from tecton._internals.sdk_decorators import deprecated


class TestSdkDecorators(unittest.TestCase):
    @patch("tecton._internals.sdk_decorators.logger.warning")
    def test_deprecated(self, mock_warning):
        @deprecated(version="1.0", reason="She is sad", warning_message=None)
        def lillys_sad_func():
            print("hi")

        self.assertEqual(lillys_sad_func._deprecation_metadata, {"version": "1.0", "reason": "She is sad"})

        lillys_sad_func()
        mock_warning.assert_not_called()

    @patch("tecton._internals.sdk_decorators.logger.warning")
    def test_deprecated_class_with_warning(self, mock_warning):
        @deprecated(version="1.0", reason="She is sad with a warning", warning_message="deprecation warning")
        @dataclass
        class LillysSadClass:
            def __init__(self):
                pass

        self.assertEqual(
            LillysSadClass._deprecation_metadata, {"version": "1.0", "reason": "She is sad with a warning"}
        )

        LillysSadClass()
        mock_warning.assert_called_once()


if __name__ == "__main__":
    unittest.main()
