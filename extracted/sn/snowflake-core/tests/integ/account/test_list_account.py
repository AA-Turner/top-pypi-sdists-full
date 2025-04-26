#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from tests.integ.account.utils import cleanup_accounts_completely, create_account

from ..utils import backup_role


pytestmark = [pytest.mark.internal_only, pytest.mark.skip_notebook]


def test_list_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor):
    with backup_role(temp_customer_account_cursor):
        try:
            temp_customer_account_cursor.execute("use role orgadmin;")
            # test happy path
            account = create_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor)

            temp_customer_account_accounts[account.name].drop(grace_period_in_days=4)

            # use history and the deleted account should be there
            account_names = [account.name for account in temp_customer_account_accounts.iter(history=True)]
            assert account.name.upper() in account_names

            account = create_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor)
            account_2 = create_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor)

            account_names = [account.name for account in temp_customer_account_accounts.iter()]
            assert len(account_names) == 3  # +1 for the orgadmin account from where we are executing these statements

            account_names = [account.name for account in temp_customer_account_accounts.iter(like="")]
            assert len(account_names) == 0

            account_names = [
                account.name for account in temp_customer_account_accounts.iter(like="TEST_CREATE_ACCOUNT_%")
            ]
            assert len(account_names) == 2

            # cleanup
            temp_customer_account_accounts[account.name].drop(grace_period_in_days=4)
            temp_customer_account_accounts[account_2.name].drop(grace_period_in_days=4)
        finally:
            cleanup_accounts_completely(sf_cursor)
