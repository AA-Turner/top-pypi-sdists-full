#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.exceptions import ConflictError
from tests.integ.managed_account.utils import cleanup_managed_accounts_completely, create_managed_account

from ..utils import backup_role


pytestmark = [pytest.mark.internal_only, pytest.mark.skip_notebook]


def test_create_managed_account(temp_customer_account_managed_accounts, sf_cursor, temp_customer_account_cursor):
    with backup_role(temp_customer_account_cursor):
        try:
            temp_customer_account_cursor.execute("use role accountadmin;")
            # test happy path
            managed_account = create_managed_account(
                temp_customer_account_managed_accounts, sf_cursor, temp_customer_account_cursor
            )

            # managed_account already exists
            create_managed_account(
                temp_customer_account_managed_accounts,
                sf_cursor,
                temp_customer_account_cursor,
                managed_account,
                ConflictError,
            )

            # managed_account deleted
            temp_customer_account_managed_accounts[managed_account.name].drop()

            # recreate the account with the same name
            create_managed_account(
                temp_customer_account_managed_accounts,
                sf_cursor,
                temp_customer_account_cursor,
                managed_account,
            )

            # managed_account deleted
            temp_customer_account_managed_accounts[managed_account.name].drop()
        finally:
            # cleanup
            cleanup_managed_accounts_completely(temp_customer_account_cursor)
