#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.account.utils import assert_account_existence, cleanup_accounts_completely, create_account

from ..utils import backup_role


pytestmark = [pytest.mark.internal_only, pytest.mark.skip_notebook]


def test_drop_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor):
    with backup_role(temp_customer_account_cursor):
        try:
            temp_customer_account_cursor.execute("use role orgadmin;")
            # test happy path
            account = create_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor)

            # account deleted
            temp_customer_account_accounts[account.name].drop(grace_period_in_days=4)
            assert_account_existence(temp_customer_account_accounts, account.name, should_exist=False)

            # account already deleted account
            temp_customer_account_accounts[account.name].drop(grace_period_in_days=4)

            # delete account that does not exist
            with pytest.raises(NotFoundError):
                temp_customer_account_accounts["RANDOM"].drop(grace_period_in_days=4)

            # delete account that does not exist with if exists flag
            temp_customer_account_accounts["RANDOM"].drop(grace_period_in_days=4, if_exists=True)
        finally:
            # cleanup
            cleanup_accounts_completely(sf_cursor)
