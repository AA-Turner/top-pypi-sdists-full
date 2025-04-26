from typing import Optional

import pytest

from snowflake.core.managed_account import ManagedAccount, ManagedAccountCollection
from tests.integ.utils import backup_role
from tests.utils import random_string


def assert_managed_account_existence(temp_customer_account_managed_accounts, managed_account_name, should_exist=True):
    managed_account_names = [managed_account.name for managed_account in temp_customer_account_managed_accounts.iter()]
    if should_exist:
        assert managed_account_name.upper() in managed_account_names
    else:
        assert managed_account_name.upper() not in managed_account_names


def get_managed_account_template():
    return ManagedAccount(
        name=random_string(5, "test_create_managed_account_"),
        admin_name="user1",
        admin_password="Sdfed43da!444444",
        account_type="READER",
        comment="This is my managed account@$W%*#$()%",
    )


def create_managed_account(
    temp_customer_account_managed_accounts: ManagedAccountCollection,
    sf_cursor,
    temp_customer_account_cursor,
    managed_account: Optional[ManagedAccount] = None,
    exception: Optional[Exception] = None,
) -> ManagedAccount:
    if managed_account is None:
        managed_account = get_managed_account_template()
    blank_account_name = random_string(5, "test_create_blank_account_")
    with backup_role(sf_cursor):
        sf_cursor.execute("use role accountadmin;")
        sf_cursor.execute("alter session set QA_MODE=true;")
        sf_cursor.execute(f"CREATE ACCOUNT {blank_account_name} server_type=standard type=blank;")

        with backup_role(temp_customer_account_cursor):
            temp_customer_account_cursor.execute("use role accountadmin;")
            if exception is not None:
                with pytest.raises(exception):
                    temp_customer_account_managed_accounts.create(managed_account)
            else:
                temp_customer_account_managed_accounts.create(managed_account)
        sf_cursor.execute("alter session unset QA_MODE;")

    if exception is None:
        assert_managed_account_existence(temp_customer_account_managed_accounts, managed_account.name.upper())
    return managed_account


def cleanup_managed_accounts_completely(temp_customer_account_cursor):
    with backup_role(temp_customer_account_cursor):
        temp_customer_account_cursor.execute("use role accountadmin;")
        managed_accounts_to_drop = temp_customer_account_cursor.execute(
            "SHOW MANAGED ACCOUNTS like 'test_create_managed_account_%';"
        ).fetchall()
        for managed_account_to_drop in managed_accounts_to_drop:
            temp_customer_account_cursor.execute(f"DROP MANAGED ACCOUNT IF EXISTS {managed_account_to_drop[0]};")
