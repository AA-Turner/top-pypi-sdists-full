from jambo.exceptions.invalid_schema_exception import InvalidSchemaException

from unittest import TestCase


class TestInternalAssertionException(TestCase):
    def test_inheritance(self):
        self.assertTrue(issubclass(InvalidSchemaException, ValueError))

    def test_message(self):
        message = "This is an internal assertion error."

        expected_message = f"Invalid JSON Schema: {message}"

        with self.assertRaises(InvalidSchemaException) as ctx:
            raise InvalidSchemaException(message)

        self.assertEqual(str(ctx.exception), expected_message)

    def test_invalid_field(self):
        message = "This is an internal assertion error."
        invalid_field = "testField"

        expected_message = (
            f"Invalid JSON Schema: {message} (invalid field: {invalid_field})"
        )

        with self.assertRaises(InvalidSchemaException) as ctx:
            raise InvalidSchemaException(message, invalid_field=invalid_field)

        self.assertEqual(str(ctx.exception), expected_message)

    def test_cause(self):
        message = "This is an internal assertion error."
        cause = ValueError("Underlying cause")

        expected_message = (
            f"Invalid JSON Schema: {message} (caused by ValueError: Underlying cause)"
        )

        with self.assertRaises(InvalidSchemaException) as ctx:
            raise InvalidSchemaException(message, cause=cause)

        self.assertEqual(str(ctx.exception), expected_message)
