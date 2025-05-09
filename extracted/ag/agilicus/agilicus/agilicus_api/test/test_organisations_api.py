"""
    Agilicus API

    Agilicus is API-first. Modern software is controlled by other software, is open, is available for you to use the way you want, securely, simply.  The OpenAPI Specification in YAML format is available on [www](https://www.agilicus.com/www/api/agilicus-openapi.yaml) for importing to other tools.  A rendered, online viewable and usable version of this specification is available at [api](https://www.agilicus.com/api). You may try the API inline directly in the web page. To do so, first obtain an Authentication Token (the simplest way is to install the Python SDK, and then run `agilicus-cli --issuer https://MYISSUER get-token`). You will need an org-id for most calls (and can obtain from `agilicus-cli --issuer https://MYISSUER list-orgs`). The `MYISSUER` will typically be `auth.MYDOMAIN`, and you will see it as you sign-in to the administrative UI.  This API releases on Bearer-Token authentication. To obtain a valid bearer token you will need to Authenticate to an Issuer with OpenID Connect (a superset of OAUTH2).  Your \"issuer\" will look like https://auth.MYDOMAIN. For example, when you signed-up, if you said \"use my own domain name\" and assigned a CNAME of cloud.example.com, then your issuer would be https://auth.cloud.example.com.  If you selected \"use an Agilicus supplied domain name\", your issuer would look like https://auth.myorg.agilicus.cloud.  For test purposes you can use our [Python SDK](https://pypi.org/project/agilicus/) and run `agilicus-cli --issuer https://auth.MYDOMAIN get-token`.  This API may be used in any language runtime that supports OpenAPI 3.0, or, you may use our [Python SDK](https://pypi.org/project/agilicus/), our [Typescript SDK](https://www.npmjs.com/package/@agilicus/angular), or our [Golang SDK](https://git.agilicus.com/pub/sdk-go).  100% of the activities in our system our API-driven, from our web-admin, through our progressive web applications, to all internals: there is nothing that is not accessible.  For more information, see [developer resources](https://www.agilicus.com/developer).   # noqa: E501

    The version of the OpenAPI document: 2025.05.07
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import agilicus_api
from agilicus_api.api.organisations_api import OrganisationsApi  # noqa: E501


class TestOrganisationsApi(unittest.TestCase):
    """OrganisationsApi unit test stubs"""

    def setUp(self):
        self.api = OrganisationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_cancel_subscription(self):
        """Test case for cancel_subscription

        Cancel the billing subscription for this organisation  # noqa: E501
        """
        pass

    def test_create_billing_portal_link(self):
        """Test case for create_billing_portal_link

        Create a link to the billing portal  # noqa: E501
        """
        pass

    def test_create_blocking_upgrade_orgs_task(self):
        """Test case for create_blocking_upgrade_orgs_task

        utility to upgrade organisations  # noqa: E501
        """
        pass

    def test_create_checkout_session(self):
        """Test case for create_checkout_session

        Create a session checkout  # noqa: E501
        """
        pass

    def test_create_org(self):
        """Test case for create_org

        Create an organisation  # noqa: E501
        """
        pass

    def test_create_reconcile_org_default_policy(self):
        """Test case for create_reconcile_org_default_policy

        Reconciles one or more org's default policies  # noqa: E501
        """
        pass

    def test_create_sub_org(self):
        """Test case for create_sub_org

        Create a sub organisation  # noqa: E501
        """
        pass

    def test_delete_sub_org(self):
        """Test case for delete_sub_org

        Delete a sub organisation  # noqa: E501
        """
        pass

    def test_get_inherent_capabilities(self):
        """Test case for get_inherent_capabilities

        Get the inherent capabilities for an org  # noqa: E501
        """
        pass

    def test_get_org(self):
        """Test case for get_org

        Get a single organisation  # noqa: E501
        """
        pass

    def test_get_org_billing_account(self):
        """Test case for get_org_billing_account

        Get the billing account associated with the organisation  # noqa: E501
        """
        pass

    def test_get_org_features(self):
        """Test case for get_org_features

        all features associated with organisation  # noqa: E501
        """
        pass

    def test_get_org_status(self):
        """Test case for get_org_status

        Get the status of an organisation  # noqa: E501
        """
        pass

    def test_get_system_options(self):
        """Test case for get_system_options

        Get organisation system options  # noqa: E501
        """
        pass

    def test_get_usage_metrics(self):
        """Test case for get_usage_metrics

        Get all usage metrics for an organisation  # noqa: E501
        """
        pass

    def test_list_email_domains(self):
        """Test case for list_email_domains

        List all unique email domains for users that are inside an organisation  # noqa: E501
        """
        pass

    def test_list_org_guid_mapping(self):
        """Test case for list_org_guid_mapping

        Get all org guids and a unique name mapping  # noqa: E501
        """
        pass

    def test_list_orgs(self):
        """Test case for list_orgs

        Get all organisations  # noqa: E501
        """
        pass

    def test_list_sub_orgs(self):
        """Test case for list_sub_orgs

        Get all sub organisations  # noqa: E501
        """
        pass

    def test_reconcile_sub_org_issuer(self):
        """Test case for reconcile_sub_org_issuer

        Creates an issuer for the sub org  # noqa: E501
        """
        pass

    def test_replace_org(self):
        """Test case for replace_org

        Create or update an organisation  # noqa: E501
        """
        pass

    def test_replace_system_options(self):
        """Test case for replace_system_options

        Update organisation system options  # noqa: E501
        """
        pass

    def test_set_inherent_capabilities(self):
        """Test case for set_inherent_capabilities

        Set the inherent capabilities for an org  # noqa: E501
        """
        pass

    def test_validate_new_org(self):
        """Test case for validate_new_org

        Validate that the requested org is available  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
