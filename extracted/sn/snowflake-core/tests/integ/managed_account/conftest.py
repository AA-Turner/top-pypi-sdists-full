import pytest

from snowflake.core.managed_account import ManagedAccountCollection


@pytest.fixture(scope="session")
def temp_customer_account_managed_accounts(temp_customer_account_root) -> ManagedAccountCollection:
    return temp_customer_account_root.managed_accounts
