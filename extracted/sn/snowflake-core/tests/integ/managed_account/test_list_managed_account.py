#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from tests.integ.managed_account.utils import cleanup_managed_accounts_completely, create_managed_account

from ..utils import backup_role


pytestmark = [pytest.mark.internal_only, pytest.mark.skip_notebook]


def test_list_managed_account(temp_customer_account_managed_accounts, sf_cursor, temp_customer_account_cursor):
    with backup_role(temp_customer_account_cursor):
        try:
            temp_customer_account_cursor.execute("use role accountadmin;")
            # test happy path
            managed_account = create_managed_account(
                temp_customer_account_managed_accounts, sf_cursor, temp_customer_account_cursor
            )

            temp_customer_account_managed_accounts[managed_account.name].drop()

            managed_account = create_managed_account(
                temp_customer_account_managed_accounts, sf_cursor, temp_customer_account_cursor
            )
            managed_account_2 = create_managed_account(
                temp_customer_account_managed_accounts, sf_cursor, temp_customer_account_cursor
            )

            managed_account_names = [
                managed_account.name for managed_account in temp_customer_account_managed_accounts.iter()
            ]
            assert len(managed_account_names) == 2

            assert ['This is my managed account@$W%*#$()%', 'This is my managed account@$W%*#$()%'] == [
                managed_account.comment for managed_account in temp_customer_account_managed_accounts.iter()
            ]

            managed_account_names = [
                managed_account.name for managed_account in temp_customer_account_managed_accounts.iter(like="")
            ]
            assert len(managed_account_names) == 0

            managed_account_names = [
                managed_account.name
                for managed_account in temp_customer_account_managed_accounts.iter(like="TEST_CREATE_MANAGED_ACCOUNT_%")
            ]
            assert len(managed_account_names) == 2

            # cleanup
            temp_customer_account_managed_accounts[managed_account.name].drop()
            temp_customer_account_managed_accounts[managed_account_2.name].drop()
        finally:
            # cleanup
            cleanup_managed_accounts_completely(temp_customer_account_cursor)
