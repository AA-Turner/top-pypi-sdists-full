from typing import Optional

import pytest

from snowflake.core.account import Account, AccountCollection
from tests.integ.utils import backup_role
from tests.utils import random_string


def assert_account_existence(temp_customer_account_accounts, account_name, should_exist=True):
    account_names = [account.name for account in temp_customer_account_accounts.iter()]
    if should_exist:
        assert account_name.upper() in account_names
    else:
        assert account_name.upper() not in account_names


def get_account_template():
    return Account(
        name=random_string(5, "test_create_account_"),
        comment="SNOWAPI_TEST_ACCOUNT",
        admin_name="SNOWAPI_TEST_ACCOUNT_ADMIN",
        admin_password="Password12345678",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test_email",
        edition="ENTERPRISE",
        must_change_password=True,
    )


def create_account(
    temp_customer_account_accounts: AccountCollection,
    sf_cursor,
    temp_customer_account_cursor,
    account: Optional[Account] = None,
    exception: Optional[Exception] = None,
    exec_info_match: Optional[str] = None,
) -> Account:
    if account is None:
        account = get_account_template()
    blank_account_name = random_string(5, "test_create_blank_account_")
    with backup_role(sf_cursor):
        sf_cursor.execute("use role accountadmin;")
        sf_cursor.execute("alter session set QA_MODE=true;")
        sf_cursor.execute(f"CREATE ACCOUNT {blank_account_name} server_type=standard type=blank;")

        with backup_role(temp_customer_account_cursor):
            temp_customer_account_cursor.execute("use role orgadmin;")
            if exception is not None:
                with pytest.raises(exception) as exec_info:
                    temp_customer_account_accounts.create(account)
                if exec_info_match is not None:
                    assert exec_info.match(exec_info_match)
            else:
                temp_customer_account_accounts.create(account)
        sf_cursor.execute("alter session unset QA_MODE;")

    if exception is None:
        assert_account_existence(temp_customer_account_accounts, account.name.upper())
    return account


def cleanup_accounts_completely(sf_cursor):
    with backup_role(sf_cursor):
        sf_cursor.execute("use role accountadmin;")
        accounts_to_drop = sf_cursor.execute("SHOW ACCOUNTS like 'test_create_account_%';").fetchall()
        for account_to_drop in accounts_to_drop:
            sf_cursor.execute(f"DROP ACCOUNT IF EXISTS {account_to_drop[0]};")
