from jambo.exceptions.internal_assertion_exception import InternalAssertionException

from unittest import TestCase


class TestInternalAssertionException(TestCase):
    def test_inheritance(self):
        self.assertTrue(issubclass(InternalAssertionException, RuntimeError))

    def test_message(self):
        message = "This is an internal assertion error."

        expected_message = (
            f"Internal Assertion Failed: {message}\n"
            "This is likely a bug in Jambo. Please report it at"
        )

        with self.assertRaises(InternalAssertionException) as ctx:
            raise InternalAssertionException(message)

        self.assertEqual(str(ctx.exception), expected_message)
