from unittest.mock import MagicMock

class BillingApiMock:

    def __init__(self):
        self.mock_add_billing_usage_record = MagicMock()
        self.mock_add_customer_balance_transaction = MagicMock()
        self.mock_add_org_to_billing_account = MagicMock()
        self.mock_add_org_to_billing_subscription = MagicMock()
        self.mock_add_subscription_balance_transaction = MagicMock()
        self.mock_create_billing_account = MagicMock()
        self.mock_create_feature = MagicMock()
        self.mock_create_product = MagicMock()
        self.mock_create_subscription = MagicMock()
        self.mock_delete_billing_account = MagicMock()
        self.mock_delete_feature = MagicMock()
        self.mock_delete_product = MagicMock()
        self.mock_delete_subscription = MagicMock()
        self.mock_get_billing_account = MagicMock()
        self.mock_get_billing_account_orgs = MagicMock()
        self.mock_get_billing_subscription_orgs = MagicMock()
        self.mock_get_customer_balance_transactions = MagicMock()
        self.mock_get_feature = MagicMock()
        self.mock_get_product = MagicMock()
        self.mock_get_subscription = MagicMock()
        self.mock_get_subscription_balance_transactions = MagicMock()
        self.mock_get_usage_records = MagicMock()
        self.mock_list_billing_accounts = MagicMock()
        self.mock_list_checkout_sessions = MagicMock()
        self.mock_list_features = MagicMock()
        self.mock_list_products = MagicMock()
        self.mock_list_subscription_features = MagicMock()
        self.mock_list_subscriptions = MagicMock()
        self.mock_list_subscriptions_with_feature = MagicMock()
        self.mock_new_subscription = MagicMock()
        self.mock_remove_org_from_billing_account = MagicMock()
        self.mock_remove_org_from_billing_subscription = MagicMock()
        self.mock_replace_billing_account = MagicMock()
        self.mock_replace_feature = MagicMock()
        self.mock_replace_product = MagicMock()
        self.mock_replace_subscription = MagicMock()
        self.mock_update_subscription_cancellation = MagicMock()

    def add_billing_usage_record(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.add_billing_usage_record with MagicMock.
        """
        return self.mock_add_billing_usage_record(self, *args, **kwargs)

    def add_customer_balance_transaction(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.add_customer_balance_transaction with MagicMock.
        """
        return self.mock_add_customer_balance_transaction(self, *args, **kwargs)

    def add_org_to_billing_account(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.add_org_to_billing_account with MagicMock.
        """
        return self.mock_add_org_to_billing_account(self, *args, **kwargs)

    def add_org_to_billing_subscription(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.add_org_to_billing_subscription with MagicMock.
        """
        return self.mock_add_org_to_billing_subscription(self, *args, **kwargs)

    def add_subscription_balance_transaction(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.add_subscription_balance_transaction with MagicMock.
        """
        return self.mock_add_subscription_balance_transaction(self, *args, **kwargs)

    def create_billing_account(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.create_billing_account with MagicMock.
        """
        return self.mock_create_billing_account(self, *args, **kwargs)

    def create_feature(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.create_feature with MagicMock.
        """
        return self.mock_create_feature(self, *args, **kwargs)

    def create_product(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.create_product with MagicMock.
        """
        return self.mock_create_product(self, *args, **kwargs)

    def create_subscription(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.create_subscription with MagicMock.
        """
        return self.mock_create_subscription(self, *args, **kwargs)

    def delete_billing_account(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.delete_billing_account with MagicMock.
        """
        return self.mock_delete_billing_account(self, *args, **kwargs)

    def delete_feature(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.delete_feature with MagicMock.
        """
        return self.mock_delete_feature(self, *args, **kwargs)

    def delete_product(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.delete_product with MagicMock.
        """
        return self.mock_delete_product(self, *args, **kwargs)

    def delete_subscription(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.delete_subscription with MagicMock.
        """
        return self.mock_delete_subscription(self, *args, **kwargs)

    def get_billing_account(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_billing_account with MagicMock.
        """
        return self.mock_get_billing_account(self, *args, **kwargs)

    def get_billing_account_orgs(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_billing_account_orgs with MagicMock.
        """
        return self.mock_get_billing_account_orgs(self, *args, **kwargs)

    def get_billing_subscription_orgs(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_billing_subscription_orgs with MagicMock.
        """
        return self.mock_get_billing_subscription_orgs(self, *args, **kwargs)

    def get_customer_balance_transactions(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_customer_balance_transactions with MagicMock.
        """
        return self.mock_get_customer_balance_transactions(self, *args, **kwargs)

    def get_feature(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_feature with MagicMock.
        """
        return self.mock_get_feature(self, *args, **kwargs)

    def get_product(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_product with MagicMock.
        """
        return self.mock_get_product(self, *args, **kwargs)

    def get_subscription(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_subscription with MagicMock.
        """
        return self.mock_get_subscription(self, *args, **kwargs)

    def get_subscription_balance_transactions(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_subscription_balance_transactions with MagicMock.
        """
        return self.mock_get_subscription_balance_transactions(self, *args, **kwargs)

    def get_usage_records(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.get_usage_records with MagicMock.
        """
        return self.mock_get_usage_records(self, *args, **kwargs)

    def list_billing_accounts(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.list_billing_accounts with MagicMock.
        """
        return self.mock_list_billing_accounts(self, *args, **kwargs)

    def list_checkout_sessions(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.list_checkout_sessions with MagicMock.
        """
        return self.mock_list_checkout_sessions(self, *args, **kwargs)

    def list_features(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.list_features with MagicMock.
        """
        return self.mock_list_features(self, *args, **kwargs)

    def list_products(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.list_products with MagicMock.
        """
        return self.mock_list_products(self, *args, **kwargs)

    def list_subscription_features(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.list_subscription_features with MagicMock.
        """
        return self.mock_list_subscription_features(self, *args, **kwargs)

    def list_subscriptions(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.list_subscriptions with MagicMock.
        """
        return self.mock_list_subscriptions(self, *args, **kwargs)

    def list_subscriptions_with_feature(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.list_subscriptions_with_feature with MagicMock.
        """
        return self.mock_list_subscriptions_with_feature(self, *args, **kwargs)

    def new_subscription(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.new_subscription with MagicMock.
        """
        return self.mock_new_subscription(self, *args, **kwargs)

    def remove_org_from_billing_account(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.remove_org_from_billing_account with MagicMock.
        """
        return self.mock_remove_org_from_billing_account(self, *args, **kwargs)

    def remove_org_from_billing_subscription(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.remove_org_from_billing_subscription with MagicMock.
        """
        return self.mock_remove_org_from_billing_subscription(self, *args, **kwargs)

    def replace_billing_account(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.replace_billing_account with MagicMock.
        """
        return self.mock_replace_billing_account(self, *args, **kwargs)

    def replace_feature(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.replace_feature with MagicMock.
        """
        return self.mock_replace_feature(self, *args, **kwargs)

    def replace_product(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.replace_product with MagicMock.
        """
        return self.mock_replace_product(self, *args, **kwargs)

    def replace_subscription(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.replace_subscription with MagicMock.
        """
        return self.mock_replace_subscription(self, *args, **kwargs)

    def update_subscription_cancellation(self, *args, **kwargs):
        """
        This method mocks the original api BillingApi.update_subscription_cancellation with MagicMock.
        """
        return self.mock_update_subscription_cancellation(self, *args, **kwargs)

