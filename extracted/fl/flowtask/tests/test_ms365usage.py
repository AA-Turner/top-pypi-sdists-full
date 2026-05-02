from pandas import DataFrame
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope="session")
def component():
    component = "MS365Usage"
    yield component


pytestmark = pytest.mark.asyncio


class TestMS365UsageUserDetail(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "client_id": "OFFICE_365_REPORT_ID",
            "secret_id": "OFFICE_365_REPORT_SECRET",
            "tenant_id": "AZURE_ADFS_TENANT_ID",
        },
        "period": "D7",
        "report_type": "M365",
        "usage_method": "UserDetail",
    }

    expected_result_type = DataFrame


class TestMS365UsageUserCounts(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "client_id": "OFFICE_365_REPORT_ID",
            "secret_id": "OFFICE_365_REPORT_SECRET",
            "tenant_id": "AZURE_ADFS_TENANT_ID",
        },
        "period": "D180",
        "report_type": "M365",
        "usage_method": "UserCounts",
    }

    expected_result_type = DataFrame


class TestMS365UsageUserPlatformUserCounts(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "client_id": "OFFICE_365_REPORT_ID",
            "secret_id": "OFFICE_365_REPORT_SECRET",
            "tenant_id": "AZURE_ADFS_TENANT_ID",
        },
        "period": "D7",
        "report_type": "M365",
        "usage_method": "PlatformUserCounts",
    }


class TestMS365UsageYammerDeviceUsersDetail(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "client_id": "OFFICE_365_REPORT_ID",
            "secret_id": "OFFICE_365_REPORT_SECRET",
            "tenant_id": "AZURE_ADFS_TENANT_ID",
        },
        "period": "D7",
        "report_type": "Yammer",
        "usage_method": "DeviceUserDetails",
    }

    expected_result_type = DataFrame


class TestMS365UsageYammerUserCounts(BaseTestCase):
    arguments: dict = {
        "period": "D7",
        "report_type": "Yammer",
        "usage_method": "UserCounts",
        "credentials": {
            "client_id": "OFFICE_365_REPORT_ID",
            "secret_id": "OFFICE_365_REPORT_SECRET",
            "tenant_id": "AZURE_ADFS_TENANT_ID",
        },
    }

    expected_result_type = DataFrame


class TestMS365UsageYammerActivityCounts(BaseTestCase):
    arguments: dict = {
        "period": "D7",
        "report_type": "Yammer",
        "usage_method": "Counts",
        "credentials": {
            "client_id": "OFFICE_365_REPORT_ID",
            "secret_id": "OFFICE_365_REPORT_SECRET",
            "tenant_id": "AZURE_ADFS_TENANT_ID",
        },
    }

    expected_result_type = DataFrame


class TestMS365UsageYammerUserDetails(BaseTestCase):
    arguments: dict = {
        "period": "D7",
        "report_type": "Yammer",
        "usage_method": "UserDetail",
        "credentials": {
            "client_id": "OFFICE_365_REPORT_ID",
            "secret_id": "OFFICE_365_REPORT_SECRET",
            "tenant_id": "AZURE_ADFS_TENANT_ID",
        },
    }

    expected_result_type = DataFrame
