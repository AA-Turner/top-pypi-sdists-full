from jambo.exceptions.unsupported_schema_exception import UnsupportedSchemaException

from unittest import TestCase


class TestUnsupportedSchemaException(TestCase):
    def test_inheritance(self):
        self.assertTrue(issubclass(UnsupportedSchemaException, ValueError))

    def test_message(self):
        message = "This is an internal assertion error."

        expected_message = f"Unsupported JSON Schema: {message}"

        with self.assertRaises(UnsupportedSchemaException) as ctx:
            raise UnsupportedSchemaException(message)

        self.assertEqual(str(ctx.exception), expected_message)

    def test_unsupported_field(self):
        message = "This is an internal assertion error."
        invalid_field = "testField"

        expected_message = (
            f"Unsupported JSON Schema: {message} (unsupported field: {invalid_field})"
        )

        with self.assertRaises(UnsupportedSchemaException) as ctx:
            raise UnsupportedSchemaException(message, unsupported_field=invalid_field)

        self.assertEqual(str(ctx.exception), expected_message)
