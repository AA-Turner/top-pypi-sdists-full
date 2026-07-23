import base64
import hashlib
import json
from datetime import datetime, timezone
from myPyllant.utils import datetime_parse, solve_altcha_challenge
from zoneinfo import ZoneInfo

"""
Tests for the `datetime_parse` function from the `myPyllant.utils` module.

Functions:
    test_datetime_parse:
        Verifies that `datetime_parse` correctly parses ISO 8601 datetime strings
        with UTC timezone into `datetime` objects.

    test_datetime_parse_local_datetime:
        Ensures that `datetime_parse` correctly parses ISO 8601 datetime strings
        with a specified local timezone and returns a `datetime` object with the
        appropriate timezone information.

    test_datetime_parse_zulu_datetime:
        Tests that `datetime_parse` correctly handles ISO 8601 datetime strings
        with a "Z" (Zulu) timezone and converts them to the specified local timezone.
"""


async def test_datetime_parse() -> None:
    assert isinstance(
        datetime_parse("2022-03-28T19:37:12.27334Z", timezone.utc), datetime
    )
    assert isinstance(datetime_parse("2022-03-28T19:37:12Z", timezone.utc), datetime)


async def test_datetime_parse_local_datetime():
    london_timezone = ZoneInfo("Europe/London")
    date_string = "2025-04-10T18:00:03+01:00"
    parsed_date = datetime_parse(date_string, None)
    assert isinstance(parsed_date, datetime)
    assert parsed_date == datetime(2025, 4, 10, 18, 0, 3, tzinfo=london_timezone)


async def test_datetime_parse_zulu_datetime():
    london_timezone = ZoneInfo("Europe/London")
    date_string = "2025-04-10T17:00:03Z"
    parsed_date = datetime_parse(date_string, london_timezone)
    assert isinstance(parsed_date, datetime)
    assert parsed_date == datetime(2025, 4, 10, 18, 0, 3, tzinfo=london_timezone)


def test_solve_altcha_challenge():
    """
    Uses a low `cost` and a one-byte `keyPrefix` so the proof-of-work solves
    almost instantly, then checks the returned payload against the same
    PBKDF2 derivation the Vaillant login server verifies it with.
    """
    challenge = {
        "parameters": {
            "algorithm": "PBKDF2/SHA-256",
            "cost": 10,
            "keyLength": 32,
            "keyPrefix": "00",
            "nonce": "19398d35354f4059a03226019c7b9915",
            "salt": "df78709ec7a451e5eacc099b09e2e9a7",
        },
        "signature": "some-server-signature",
    }

    payload = solve_altcha_challenge(challenge)
    decoded = json.loads(base64.b64decode(payload))

    assert decoded["challenge"]["parameters"] == challenge["parameters"]
    assert decoded["challenge"]["signature"] == challenge["signature"]

    solution = decoded["solution"]
    parameters = challenge["parameters"]
    password = bytes.fromhex(parameters["nonce"]) + solution["counter"].to_bytes(
        4, byteorder="big"
    )
    expected_key = hashlib.pbkdf2_hmac(
        "sha256",
        password,
        bytes.fromhex(parameters["salt"]),
        parameters["cost"],
        dklen=parameters["keyLength"],
    )
    assert solution["derivedKey"] == expected_key.hex()
    assert expected_key.startswith(bytes.fromhex(parameters["keyPrefix"]))
