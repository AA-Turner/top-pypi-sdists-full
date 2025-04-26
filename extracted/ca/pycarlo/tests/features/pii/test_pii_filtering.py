import json
import os
from datetime import date
from typing import Dict, cast
from unittest import TestCase

from pycarlo.features.pii import PiiFilterer


class PiiFilteringTests(TestCase):
    FILTERS_1 = {
        "active": [
            {
                "name": "a",
                "pattern": "n[am]+e",
            },
            {
                "name": "b",
                "pattern": "su[ab]",
            },
            {
                "name": "c",
                "pattern": "ag",
            },
            {"name": "us_ssn", "pattern": r"([0-6]\d{2}|7[0-6]\d|77[0-2])([ \-]?)(\d{2})\2(\d{4})"},
            {
                "name": "ccard",
                "pattern": (
                    r"((4\d{3})|(5[1-5]\d{2}))(-?|\040?)(\d{4}(-?|\040?)){3}|(3[4,7]\d{2})(-?|\040?)"
                    r"\d{6}(-?|\040?)\d{5}"
                ),
            },
            {"name": "email", "pattern": r"[\w.%+-]+@[\w.-]+\.[\w]{2,4}"},
        ]
    }
    FILTERS_2 = {
        "active": [
            {"name": "us_ssn", "pattern": r"\d{3}-\d{2}-\d{4}"},
            {
                "name": "ccard",
                "pattern": (
                    r"((4\d{3})|(5[1-5]\d{2}))(-?|\040?)(\d{4}(-?|\040?)){3}|(3[4,7]\d{2})(-?|\040?)"
                    r"\d{6}(-?|\040?)\d{5}"
                ),
            },
            {"name": "email", "pattern": r"[\w.%+-]+@[\w.-]+\.[\w]{2,4}"},
            {"name": "test_col", "pattern": r"COL_\d{5}_\d{2}"},
        ]
    }
    FILTERS_COUNTRY_CODE = {
        "active": [
            {"name": "country_code", "pattern": "[A-Z]{3}"},
        ]
    }

    JSON_MSG_SIMPLE = {
        "a": "This is my Name: my name",
        "b": [
            "age: 38",
            "and my personal email address is: user_id_09@server.com",
            "This IS a valid SSN: 111-11-1111.",
            "Please charge it to VISA 4321-9876-9876-9876.",
        ],
        "c": "this is another email address: user-id@server.com",
        "d": "This IS a valid SSN: 111-11-1111.",
        "e": "Please charge it to VISA 4321-1234-9876-9876.",
        "f": date(2022, 10, 25),
        "age": 50,
    }
    JSON_MSG_STR_LIST = [
        "my personal email address is: user_id_09@server.com",
        "This IS a valid SSN: 111-11-1111.",
    ]
    JSON_MSG_OBJ_LIST = [
        {
            "c": "this is another email address: user-id@server.com",
            "d": "This IS a valid SSN: 111-11-1111.",
        },
        {
            "c": "my personal email address is: user_id_09@server.com",
            "e": "Please charge it to VISA 4321-1234-9876-9876.",
            "f": date(2022, 10, 25),
        },
    ]
    JSON_MSG_NESTED = {
        "values": [
            [
                {"x": "age: 38", "y": "and my personal email address is: user_id_09@server.com"},
                {
                    "c": "this is another email address: user-id@server.com",
                    "f": date(2022, 10, 25),
                    "age": 50,
                },
            ],
            [
                {
                    "d": "This IS a valid SSN: 111-11-1111.",
                    "e": "Please charge it to VISA 4321-1234-9876-9876.",
                }
            ],
        ],
        "more_values": [
            {
                "nested_values": [
                    "my personal email address is: user_id_09@server.com",
                    "This IS a valid SSN: 111-11-1111.",
                ]
            }
        ],
    }

    def test_simple_object_filtering(self):
        f = PiiFilterer(self.FILTERS_1)

        filtered = cast(Dict, f.filter_message(self.JSON_MSG_SIMPLE))
        self.assertEqual("This IS a valid SSN: <filtered:us_ssn>.", filtered["d"])
        self.assertEqual("Please charge it to VISA <filtered:ccard>.", filtered["e"])
        self.assertEqual(self.JSON_MSG_SIMPLE["f"], filtered["f"])
        self.assertEqual(self.JSON_MSG_SIMPLE["age"], filtered["<filtered:c>e"])
        self.assertEqual("<filtered:c>e: 38", filtered["b"][0])
        self.assertEqual("and my personal email address is: <filtered:email>", filtered["b"][1])
        self.assertEqual("This IS a valid SSN: <filtered:us_ssn>.", filtered["b"][2])
        self.assertEqual("Please charge it to VISA <filtered:ccard>.", filtered["b"][3])

        m = filtered["pii_metrics"]  # equivalent to f.metrics
        self.assertEqual(1, m["a"]["replacements"])
        self.assertEqual(0, m["b"]["replacements"])
        self.assertEqual(2, m["c"]["replacements"])
        self.assertEqual(2, m["us_ssn"]["replacements"])
        self.assertEqual(2, m["email"]["replacements"])
        self.assertEqual(9, m["_total"]["replacements"])
        self.assertGreater(m["_total"]["time_taken_ms"], 0)

    def test_string_list_filtering(self):
        f = PiiFilterer(self.FILTERS_1)

        filtered = f.filter_message(self.JSON_MSG_STR_LIST)  # type: ignore
        self.assertEqual("my personal email address is: <filtered:email>", filtered[0])
        self.assertEqual("This IS a valid SSN: <filtered:us_ssn>.", filtered[1])

    def test_object_list_filtering(self):
        f = PiiFilterer(self.FILTERS_1)

        filtered = cast(Dict, f.filter_message(self.JSON_MSG_OBJ_LIST))  # type: ignore
        self.assertEqual("this is another email address: <filtered:email>", filtered[0]["c"])
        self.assertEqual("This IS a valid SSN: <filtered:us_ssn>.", filtered[0]["d"])
        self.assertEqual("my personal email address is: <filtered:email>", filtered[1]["c"])
        self.assertEqual("Please charge it to VISA <filtered:ccard>.", filtered[1]["e"])
        self.assertEqual(self.JSON_MSG_OBJ_LIST[1]["f"], filtered[1]["f"])

    def test_nested_object_filtering(self):
        f = PiiFilterer(self.FILTERS_1)

        filtered = cast(Dict, f.filter_message(self.JSON_MSG_NESTED))
        self.assertEqual("<filtered:c>e: 38", filtered["values"][0][0]["x"])
        self.assertEqual(
            "and my personal email address is: <filtered:email>", filtered["values"][0][0]["y"]
        )
        self.assertEqual(
            "this is another email address: <filtered:email>", filtered["values"][0][1]["c"]
        )
        self.assertEqual(self.JSON_MSG_NESTED["values"][0][1]["f"], filtered["values"][0][1]["f"])
        self.assertEqual(
            self.JSON_MSG_NESTED["values"][0][1]["age"], filtered["values"][0][1]["<filtered:c>e"]
        )
        self.assertEqual("This IS a valid SSN: <filtered:us_ssn>.", filtered["values"][1][0]["d"])
        self.assertEqual(
            "Please charge it to VISA <filtered:ccard>.", filtered["values"][1][0]["e"]
        )

        self.assertEqual(
            "my personal email address is: <filtered:email>",
            filtered["more_values"][0]["nested_values"][0],
        )
        self.assertEqual(
            "This IS a valid SSN: <filtered:us_ssn>.",
            filtered["more_values"][0]["nested_values"][1],
        )

        m = filtered["pii_metrics"]
        self.assertEqual(2, m["us_ssn"]["replacements"])
        self.assertEqual(3, m["email"]["replacements"])
        self.assertEqual(1, m["ccard"]["replacements"])
        self.assertEqual(2, m["c"]["replacements"])
        self.assertEqual(8, m["_total"]["replacements"])

    def test_filter_md_events(self):
        f = PiiFilterer(self.FILTERS_2)

        dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_events")
        event_files = os.listdir(dir_name)
        email_count = 0
        for event_file in event_files:
            if not event_file.endswith(".json"):
                continue
            with open(os.path.join(dir_name, event_file), "r") as file:
                data = json.load(file)
                filtered_data = cast(Dict, f.filter_message(data))
                metrics = filtered_data["pii_metrics"]
                email_count += metrics.get("email")["replacements"]

        self.assertGreaterEqual(
            email_count, 1
        )  # there's at least one email in sample_query_log_01.json

    def test_filter_tuples_single_column(self):
        data = {"rows": [("4",), ("3",), ("USA",)]}
        f = PiiFilterer(self.FILTERS_COUNTRY_CODE)
        filtered_data = cast(Dict, f.filter_message(data))

        self.assertEqual("4", filtered_data["rows"][0][0])
        self.assertEqual("3", filtered_data["rows"][1][0])
        self.assertEqual("<filtered:country_code>", filtered_data["rows"][2][0])

    def test_filter_tuples_three_columns(self):
        data = {
            "rows": [
                (date(2022, 12, 1), "4", 23),
                (date(2022, 12, 2), "3", 15),
                (date(2022, 12, 3), "USA", 35),
            ]
        }
        f = PiiFilterer(self.FILTERS_COUNTRY_CODE)
        filtered_data = cast(Dict, f.filter_message(data))

        self.assertEqual(data["rows"][0][0], filtered_data["rows"][0][0])
        self.assertEqual(data["rows"][0][1], filtered_data["rows"][0][1])
        self.assertEqual(data["rows"][0][2], filtered_data["rows"][0][2])

        self.assertEqual(data["rows"][2][0], filtered_data["rows"][2][0])
        self.assertEqual("<filtered:country_code>", filtered_data["rows"][2][1])
        self.assertEqual(data["rows"][2][2], filtered_data["rows"][2][2])

    def test_filter_bytes_utf(self):
        data = "[\u00f1\u00f1] This IS a valid SSN: 111-11-1111.".encode("utf8")
        f = PiiFilterer(self.FILTERS_2)
        filtered_data = f.filter_data(data)  # default encoding is utf8
        filtered_text = filtered_data.decode("utf8")
        self.assertEqual("[\u00f1\u00f1] This IS a valid SSN: <filtered:us_ssn>.", filtered_text)

    def test_filter_str(self):
        text = "This IS a valid SSN: 111-11-1111."
        f = PiiFilterer(self.FILTERS_2)
        filtered_text = f.filter_str(text)
        self.assertEqual("This IS a valid SSN: <filtered:us_ssn>.", filtered_text)

    def test_no_filter_bytes(self):
        text = "[\u00f1\u00f1] This IS a valid SSN: 111-11-1111."
        data = text.encode("utf8")
        f = PiiFilterer(filters_config=None)
        filtered_data = f.filter_data(data)  # default encoding is utf8
        filtered_text = filtered_data.decode("utf8")
        self.assertEqual(text, filtered_text)

    def test_no_filter_str(self):
        text = "This IS a valid SSN: 111-11-1111."
        f = PiiFilterer(filters_config=None)
        filtered_text = f.filter_str(text)
        self.assertEqual(text, filtered_text)

    def test_no_filter_object(self):
        f = PiiFilterer(filters_config=None)

        filtered = f.filter_message(self.JSON_MSG_SIMPLE)
        self.assertEqual(filtered, self.JSON_MSG_SIMPLE)

    def test_filter_bytes_ascii(self):
        enc = "iso-8859-1"
        data = "[\u00f1\u00f1] This IS a valid SSN: 111-11-1111.".encode(enc)
        f = PiiFilterer(self.FILTERS_2)
        filtered_data = f.filter_data(data, enc)
        filtered_text = filtered_data.decode(enc)
        self.assertEqual("[\u00f1\u00f1] This IS a valid SSN: <filtered:us_ssn>.", filtered_text)
