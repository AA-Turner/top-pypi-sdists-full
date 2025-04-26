#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.exceptions import UnauthorizedError
from tests.integ.account.utils import cleanup_accounts_completely, create_account

from ..utils import backup_role, random_string


pytestmark = [pytest.mark.internal_only, pytest.mark.skip_notebook]


def test_create_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor):
    with backup_role(temp_customer_account_cursor):
        try:
            temp_customer_account_cursor.execute("use role orgadmin;")
            # test happy path
            account = create_account(temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor)

            # account already exists
            create_account(
                temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor, account, UnauthorizedError
            )

            # account deleted
            temp_customer_account_accounts[account.name].drop(grace_period_in_days=4)

            # account does not exist but is not available to create as it is still yet to be dropped
            create_account(
                temp_customer_account_accounts, sf_cursor, temp_customer_account_cursor, account, UnauthorizedError
            )

            # create account endpoint for rsa public key but since it is fake it will be rejected
            account.name = random_string(5, "test_create_account_")
            account.admin_rsa_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlmNyi9mEc18wdZw0lCeOxD3pwiLO9BzDIU84dqAws3hge4E2sgYaepcE3CUtC147jiWgD7atzKTHy0Ov88xh"  # pragma: allowlist secret  # noqa: E501
            create_account(
                temp_customer_account_accounts,
                sf_cursor,
                temp_customer_account_cursor,
                account,
                UnauthorizedError,
                ".*new public key rejected by current policy. reason: 'invalid public key'.*",
            )
        finally:
            # cleanup
            cleanup_accounts_completely(sf_cursor)
