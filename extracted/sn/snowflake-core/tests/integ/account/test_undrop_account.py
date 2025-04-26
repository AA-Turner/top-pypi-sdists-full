#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.exceptions import APIError, ConflictError
from tests.integ.account.utils import assert_account_existence, cleanup_accounts_completely, create_account

from ..utils import backup_role


pytestmark = [pytest.mark.internal_only, pytest.mark.skip_notebook]


def test_undrop_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor):
    with backup_role(temp_customer_account_cursor):
        try:
            temp_customer_account_cursor.execute("use role orgadmin;")
            # test happy path
            account = create_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor)

            # undrop existing account
            with pytest.raises(ConflictError):
                temp_customer_account_accounts[account.name].undrop()

            # account deleted
            temp_customer_account_accounts[account.name].drop(grace_period_in_days=4)
            assert_account_existence(temp_customer_account_accounts, account.name, should_exist=False)

            # undrop deleted account
            temp_customer_account_accounts[account.name].undrop()
            assert_account_existence(temp_customer_account_accounts, account.name)

            # account already restored account
            with pytest.raises(ConflictError):
                temp_customer_account_accounts[account.name].undrop()

            # undrop random account that does not exist
            with pytest.raises(APIError):
                temp_customer_account_accounts["RANDOM"].undrop()

            # cleanup
            temp_customer_account_accounts[account.name].drop(grace_period_in_days=4)
        finally:
            # cleanup
            cleanup_accounts_completely(sf_cursor)
