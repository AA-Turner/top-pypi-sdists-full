import pytest

from snowflake.core._utils import fix_hostname, replace_function_name_in_name_with_args


def test_replace_function_name_in_name_with_args():
    assert replace_function_name_in_name_with_args(
        "function_name(arg1,arg2)",
        "new_function_name"
    ) == "new_function_name(arg1,arg2)"

    assert replace_function_name_in_name_with_args(
        "function_name()",
        "new_function_name"
    ) == "new_function_name()"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"()""",
        """new_function_name"""
    ) == "new_function_name()"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"(ar)""",
        """new_function_name"""
    ) == "new_function_name(ar)"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"(ar12)""",
        """new_function_name"""
    ) == "new_function_name(ar12)"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"(ar12,ar13)""",
        """\"()()()\""""
    ) == "\"()()()\"(ar12,ar13)"

    assert replace_function_name_in_name_with_args(
        """abc(ar12,ar13)""",
        """\"()()()\""""
    ) == "\"()()()\"(ar12,ar13)"

    assert replace_function_name_in_name_with_args(
        """abc()""",
        """\"()()()\""""
    ) == "\"()()()\"()"

@pytest.mark.parametrize(
    (
        "hostname",
        "expected_hostname",
    ),
    (
        # Negative cases
        (  # New URL used
            "org-account.snowflake.com",
            "org-account.snowflake.com",
        ),
        (  # New URL used with underscore in account locator
            "org-account_locator.snowflake.com",
            "org-account-locator.snowflake.com",
        ),
        (  # No underscore in account locator
            "account.snowflake.com",
            "account.snowflake.com",
        ),
        # Positive case
        (
            "account_identifier.snowflake.com",
            "account-identifier.snowflake.com",
        ),
    )
)
def test_hostname_fixes(hostname, expected_hostname):
    assert (
        fix_hostname(hostname)
    ) == expected_hostname
