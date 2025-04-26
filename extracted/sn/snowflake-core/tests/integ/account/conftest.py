import pytest

from snowflake.core.account import AccountCollection


@pytest.fixture(scope="session")
def temp_customer_account_accounts(temp_customer_account_root) -> AccountCollection:
    return temp_customer_account_root.accounts
