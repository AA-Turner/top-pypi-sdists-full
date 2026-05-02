"""Test cases for test_pagination_utils.

Those cases cover scenarios for ``decode_pagination`` function.
"""


def case_decode_empty() -> str:
    """Empty token gives no pagination."""
    token = "90"
    return token
