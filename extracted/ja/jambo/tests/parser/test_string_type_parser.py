from jambo.exceptions import InvalidSchemaException
from jambo.parser import StringTypeParser

from pydantic import AnyUrl, EmailStr

from datetime import date, datetime, time, timedelta, timezone
from ipaddress import IPv4Address, IPv6Address, ip_address
from unittest import TestCase
from uuid import UUID


class TestStringTypeParser(TestCase):
    def test_string_parser_no_options(self):
        parser = StringTypeParser()

        properties = {"type": "string"}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, str)

    def test_string_parser_with_options(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "maxLength": 10,
            "minLength": 1,
            "pattern": "^[a-zA-Z]+$",
            "examples": ["test", "TEST"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, str)
        self.assertEqual(type_validator["max_length"], 10)
        self.assertEqual(type_validator["min_length"], 1)
        self.assertEqual(type_validator["pattern"], "^[a-zA-Z]+$")
        self.assertEqual(type_validator["examples"], ["test", "TEST"])

    def test_string_parser_with_default_value(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": "default_value",
            "maxLength": 20,
            "minLength": 5,
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, str)
        self.assertEqual(type_validator["default"], "default_value")
        self.assertEqual(type_validator["max_length"], 20)
        self.assertEqual(type_validator["min_length"], 5)

    def test_string_parser_with_invalid_default_value_type(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": 12345,  # Invalid default value
            "maxLength": 20,
            "minLength": 5,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_string_parser_with_default_invalid_maxlength(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": "default_value",
            "maxLength": 2,
            "minLength": 1,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_string_parser_with_default_invalid_minlength(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": "a",
            "maxLength": 20,
            "minLength": 2,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_string_parser_with_email_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "email",
            "examples": ["test@example.com"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, EmailStr)
        self.assertEqual(type_validator["examples"], ["test@example.com"])

    def test_string_parser_with_uri_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "uri",
            "examples": ["test://domain/resource"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, AnyUrl)
        self.assertEqual(type_validator["examples"], [AnyUrl("test://domain/resource")])

    def test_string_parser_with_ip_formats(self):
        parser = StringTypeParser()

        formats = {"ipv4": IPv4Address, "ipv6": IPv6Address}
        examples = {"ipv4": ["192.168.1.1"], "ipv6": ["::1"]}

        for ip_format, expected_type in formats.items():
            example = examples[ip_format]

            properties = {
                "type": "string",
                "format": ip_format,
                "examples": example,
            }

            type_parsing, type_validator = parser.from_properties(
                "placeholder", properties
            )

            self.assertEqual(type_parsing, expected_type)
            self.assertEqual(
                type_validator["examples"], [ip_address(e) for e in example]
            )

    def test_string_parser_with_uuid_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "uuid",
            "examples": ["ab71aaf4-ab6e-43cd-a369-cebdd9f7a4c6"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, UUID)
        self.assertEqual(
            type_validator["examples"], [UUID("ab71aaf4-ab6e-43cd-a369-cebdd9f7a4c6")]
        )

    def test_string_parser_with_time_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "time",
            "examples": ["14:30:00", "09:15:30.500", "10:00:00+02:00"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, time)
        self.assertEqual(
            type_validator["examples"],
            [
                time(hour=14, minute=30, second=0),
                time(hour=9, minute=15, second=30, microsecond=500_000),
                time(hour=10, minute=0, second=0, tzinfo=timezone(timedelta(hours=2))),
            ],
        )

    def test_string_parser_with_pattern_based_formats(self):
        parser = StringTypeParser()

        format_types = {
            "hostname": "example.com",
        }

        for format_type, example_type in format_types.items():
            properties = {
                "type": "string",
                "format": format_type,
                "examples": [example_type],
            }

            type_parsing, type_validator = parser.from_properties(
                "placeholder", properties
            )

            self.assertEqual(type_parsing, str)
            self.assertIn("pattern", type_validator)
            self.assertEqual(
                type_validator["pattern"], parser.format_pattern_mapping[format_type]
            )
            self.assertEqual(type_validator["examples"], [example_type])

    def test_string_parser_with_unsupported_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "unsupported-format",
        }

        with self.assertRaises(InvalidSchemaException) as context:
            parser.from_properties("placeholder", properties)

        self.assertEqual(
            str(context.exception),
            "Invalid JSON Schema: Unsupported string format: unsupported-format (invalid field: format)",
        )

    def test_string_parser_with_date_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "date",
            "examples": ["2025-11-17", "1999-12-31", "2000-01-01"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, date)
        self.assertEqual(
            type_validator["examples"],
            [
                date(year=2025, month=11, day=17),
                date(year=1999, month=12, day=31),
                date(year=2000, month=1, day=1),
            ],
        )

    def test_string_parser_with_datetime_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "date-time",
            "examples": [
                "2025-11-17T11:15:00",
                "2025-11-17T11:15:00+01:00",
                "2025-11-17T11:15:00.123456-05:00",
            ],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, datetime)
        self.assertEqual(
            type_validator["examples"],
            [
                datetime(year=2025, month=11, day=17, hour=11, minute=15, second=0),
                datetime(
                    year=2025,
                    month=11,
                    day=17,
                    hour=11,
                    minute=15,
                    second=0,
                    tzinfo=timezone(timedelta(hours=1)),
                ),
                datetime(
                    year=2025,
                    month=11,
                    day=17,
                    hour=11,
                    minute=15,
                    second=0,
                    microsecond=123456,
                    tzinfo=timezone(timedelta(hours=-5)),
                ),
            ],
        )

    def test_string_parser_with_invalid_example_value(self):
        with self.assertRaises(InvalidSchemaException):
            StringTypeParser().from_properties(
                "placeholder",
                {
                    "type": "string",
                    "format": "email",
                    "examples": ["invalid-email"],
                },
            )

    def test_string_parser_with_timedelta_format(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "format": "duration",
            "examples": ["P1Y2M3DT4H5M6S", "PT30M", "P7D", "PT0.5S"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, timedelta)
        self.assertEqual(
            type_validator["examples"],
            [
                timedelta(days=428, hours=4, minutes=5, seconds=6),
                timedelta(minutes=30),
                timedelta(days=7),
                timedelta(seconds=0.5),
            ],
        )
