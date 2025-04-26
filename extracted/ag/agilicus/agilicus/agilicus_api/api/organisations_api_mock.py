from unittest.mock import MagicMock

class OrganisationsApiMock:

    def __init__(self):
        self.mock_cancel_subscription = MagicMock()
        self.mock_create_billing_portal_link = MagicMock()
        self.mock_create_blocking_upgrade_orgs_task = MagicMock()
        self.mock_create_checkout_session = MagicMock()
        self.mock_create_org = MagicMock()
        self.mock_create_reconcile_org_default_policy = MagicMock()
        self.mock_create_sub_org = MagicMock()
        self.mock_delete_sub_org = MagicMock()
        self.mock_get_inherent_capabilities = MagicMock()
        self.mock_get_org = MagicMock()
        self.mock_get_org_billing_account = MagicMock()
        self.mock_get_org_features = MagicMock()
        self.mock_get_org_status = MagicMock()
        self.mock_get_system_options = MagicMock()
        self.mock_get_usage_metrics = MagicMock()
        self.mock_list_email_domains = MagicMock()
        self.mock_list_org_guid_mapping = MagicMock()
        self.mock_list_orgs = MagicMock()
        self.mock_list_sub_orgs = MagicMock()
        self.mock_reconcile_sub_org_issuer = MagicMock()
        self.mock_replace_org = MagicMock()
        self.mock_replace_system_options = MagicMock()
        self.mock_set_inherent_capabilities = MagicMock()
        self.mock_validate_new_org = MagicMock()

    def cancel_subscription(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.cancel_subscription with MagicMock.
        """
        return self.mock_cancel_subscription(self, *args, **kwargs)

    def create_billing_portal_link(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.create_billing_portal_link with MagicMock.
        """
        return self.mock_create_billing_portal_link(self, *args, **kwargs)

    def create_blocking_upgrade_orgs_task(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.create_blocking_upgrade_orgs_task with MagicMock.
        """
        return self.mock_create_blocking_upgrade_orgs_task(self, *args, **kwargs)

    def create_checkout_session(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.create_checkout_session with MagicMock.
        """
        return self.mock_create_checkout_session(self, *args, **kwargs)

    def create_org(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.create_org with MagicMock.
        """
        return self.mock_create_org(self, *args, **kwargs)

    def create_reconcile_org_default_policy(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.create_reconcile_org_default_policy with MagicMock.
        """
        return self.mock_create_reconcile_org_default_policy(self, *args, **kwargs)

    def create_sub_org(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.create_sub_org with MagicMock.
        """
        return self.mock_create_sub_org(self, *args, **kwargs)

    def delete_sub_org(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.delete_sub_org with MagicMock.
        """
        return self.mock_delete_sub_org(self, *args, **kwargs)

    def get_inherent_capabilities(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.get_inherent_capabilities with MagicMock.
        """
        return self.mock_get_inherent_capabilities(self, *args, **kwargs)

    def get_org(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.get_org with MagicMock.
        """
        return self.mock_get_org(self, *args, **kwargs)

    def get_org_billing_account(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.get_org_billing_account with MagicMock.
        """
        return self.mock_get_org_billing_account(self, *args, **kwargs)

    def get_org_features(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.get_org_features with MagicMock.
        """
        return self.mock_get_org_features(self, *args, **kwargs)

    def get_org_status(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.get_org_status with MagicMock.
        """
        return self.mock_get_org_status(self, *args, **kwargs)

    def get_system_options(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.get_system_options with MagicMock.
        """
        return self.mock_get_system_options(self, *args, **kwargs)

    def get_usage_metrics(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.get_usage_metrics with MagicMock.
        """
        return self.mock_get_usage_metrics(self, *args, **kwargs)

    def list_email_domains(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.list_email_domains with MagicMock.
        """
        return self.mock_list_email_domains(self, *args, **kwargs)

    def list_org_guid_mapping(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.list_org_guid_mapping with MagicMock.
        """
        return self.mock_list_org_guid_mapping(self, *args, **kwargs)

    def list_orgs(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.list_orgs with MagicMock.
        """
        return self.mock_list_orgs(self, *args, **kwargs)

    def list_sub_orgs(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.list_sub_orgs with MagicMock.
        """
        return self.mock_list_sub_orgs(self, *args, **kwargs)

    def reconcile_sub_org_issuer(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.reconcile_sub_org_issuer with MagicMock.
        """
        return self.mock_reconcile_sub_org_issuer(self, *args, **kwargs)

    def replace_org(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.replace_org with MagicMock.
        """
        return self.mock_replace_org(self, *args, **kwargs)

    def replace_system_options(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.replace_system_options with MagicMock.
        """
        return self.mock_replace_system_options(self, *args, **kwargs)

    def set_inherent_capabilities(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.set_inherent_capabilities with MagicMock.
        """
        return self.mock_set_inherent_capabilities(self, *args, **kwargs)

    def validate_new_org(self, *args, **kwargs):
        """
        This method mocks the original api OrganisationsApi.validate_new_org with MagicMock.
        """
        return self.mock_validate_new_org(self, *args, **kwargs)

