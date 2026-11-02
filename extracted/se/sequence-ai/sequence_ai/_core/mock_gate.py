"""
Whether a base URL asks for the mock tier, and whether it may have it - the SDK's own tests alone, from its source tree.

The mock tier (mock_direct.py and its _mock_assets/, seq/_mock.py) is the SDK's internal test fixture: the wheel and the
sdist leave it out (pyproject.toml), and it answers only with SEQ_INTERNAL_MOCK=1, as tests/conftest.py sets. This is
what every shipped caller asks first, so none imports the fixture before it is allowed; asked for anywhere else - no
SEQ_INTERNAL_MOCK, or an installed package that has no fixture to start - InvalidRequest says it is not for users.


"""
from __future__ import annotations

import importlib.util
import os
from typing import Optional

INTERNAL = "SEQ_INTERNAL_MOCK"
NOT_FOR_USERS = ("the base URL 'mock' is not available: the mock tier is the SDK's internal test fixture, not for "
                 "users. Leave the base URL unset to use the platform, with your API key (SEQUENCES_API_KEY).")

FIXTURE = "sequence_ai._core.mock_direct"


def is_mock(base_url: Optional[str]) -> bool:
    """True if `base_url` selects the offline mock tier (`mock` or a `mock:…` form) and the SDK's own tests run it:
    asked for anywhere else, InvalidRequest says it is not for users."""
    if not isinstance(base_url, str):
        return False
    b = base_url.strip()
    if not (b == "mock" or b.startswith("mock:")):
        return False
    if os.environ.get(INTERNAL) != "1" or importlib.util.find_spec(FIXTURE) is None:
        from sequence_ai.errors import InvalidRequest

        raise InvalidRequest(NOT_FOR_USERS)
    return True
