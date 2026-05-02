import msgpack
import pydantic
import pytest
import pytest_cases

from tests.utils.definitions import NextPageToken, Pagination


async def test_encode_empty_paginations() -> None:
    """Test if empty paginations are encoded to ``None`` token."""
    token = NextPageToken.from_paginations([]).token
    assert token is None


@pytest_cases.parametrize_with_cases(
    ["paginations"],
    cases=["tests.utils.test_pagination_encode_cases"],
)
async def test_encode_pagination(
    paginations: list[Pagination],
) -> None:
    """Test if token is created from valid input."""
    token = NextPageToken.from_paginations(paginations).token
    assert isinstance(token, str)


async def test_decode_none_token() -> None:
    """Test if ``None`` token gives empty paginations."""
    paginations = NextPageToken(None).paginations()
    assert paginations == []


@pytest_cases.parametrize_with_cases(
    ["token"],
    cases=["tests.utils.test_pagination_decode_cases"],
)
async def test_decode_token(
    token: str,
) -> None:
    """Test if token is correctly decoded from valid input."""
    paginations = NextPageToken(token).paginations()
    assert isinstance(paginations, list)


@pytest_cases.parametrize_with_cases(
    ["paginations"],
    cases=["tests.utils.test_pagination_duality_cases"],
)
async def test_decode_encode_pagination(
    paginations: list[Pagination],
) -> None:
    """Test duality of ``from_paginations`` and ``paginations``.

    This test simply checks if the input paginations can correctly be
    decoded.
    """
    decoded_paginations = NextPageToken.from_paginations(paginations).paginations()
    assert decoded_paginations == paginations


async def test_invalid_byte_token() -> None:
    """Test if invalid bytes are rejected as pagination token."""
    token = "1234567890abcdef"
    with pytest.raises((msgpack.exceptions.UnpackException, msgpack.exceptions.ExtraData)):
        NextPageToken(token).paginations()


async def test_valid_token_invalid_data() -> None:
    """Test if data that do not match pagination schema are rejected.

    The token contains incorrect key for ``page``, due to typo there is
    ``pgae``.
    """
    invalid_pagination = [
        {
            "endpoint": "/users",
            "pgae": 3,  # tpyo is here
        },
    ]
    token = msgpack.packb(invalid_pagination).hex()
    with pytest.raises(pydantic.ValidationError) as excinfo:
        NextPageToken(token).paginations()

    invalid_fields_with_error_types = [
        (error["loc"], error["type"]) for error in excinfo.value.errors()
    ]
    expected_errors = [
        (("page",), "missing"),
        (("pgae",), "extra_forbidden"),
    ]
    assert set(invalid_fields_with_error_types) == set(expected_errors)
