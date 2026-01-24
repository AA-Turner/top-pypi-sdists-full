import pytest

from redshift_client.sql_client import (
    LoginUtils,
    TempCredsUser,
)


def test_handle_errors() -> None:
    user = TempCredsUser("region", "cluster", "db", "user")
    with pytest.raises(SystemExit):
        LoginUtils.get_temp_creds(user).compute()


def test_handle_errors_no_region() -> None:
    user = TempCredsUser(None, "cluster", "db", "user")
    with pytest.raises(SystemExit):
        LoginUtils.get_temp_creds(user).compute()
