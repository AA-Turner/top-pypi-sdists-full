import asyncio
from pandas import DataFrame
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope="session")
def component():
    component = "AutoTask"
    yield component


pytestmark = pytest.mark.asyncio


class TestAutoTaskTickets(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "API_INTEGRATION_CODE": "AUTOTASK_API_INTEGRATION_CODE",
            "USERNAME": "AUTOTASK_USERNAME",
            "SECRET": "AUTOTASK_SECRET",
        },
        "entity": "Tickets",
        "zone": "webservices14",
        "id_column_name": "ticket_id",
        "picklist_fields": ["status"],
        "ids": [], # Will override Filter below
        "query_json": { # For syntax, check autotask documentation
            "IncludeFields": [
                "id",
                "ticketNumber",
                "title",
                "companyID",
                "contractID",
                "contactID",
                "status",
                "configurationItemID",
                "createDate",
                "resolvedDateTime",
                "completedDate",
                "lastActivityDate",
                "lastTrackedModificationDateTime",
            ],
            "Filter": [
                # {"op": "gte", "field": "id", "value": 320000},
                {"op": "gte", "field": "createDate", "value": "2024-07-06"},
                # #     # {"op": "eq", "field": "CompanyID", "value": 999},
                # #     # {"op": "in", "field": "status", "value": [1, 5, 31]},
                # {"op": "in", "field": "ticketNumber", "value":[
                #     "T20990129.0001"
                #         # "20990129.0002",
                #         # "20990129.0003",
                #         # "20990129.0004",
            ],
        },
    }

    expected_result_type = DataFrame

#TODO Test that IDs can be extracted from previous step

class TestAutoTaskTicketsNotes(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "API_INTEGRATION_CODE": "AUTOTASK_API_INTEGRATION_CODE",
            "USERNAME": "AUTOTASK_USERNAME",
            "SECRET": "AUTOTASK_SECRET",
        },
        "entity": "TicketNotes",
        "zone": "webservices14",
        "id_column_name": "ticket_note_id",
        "picklist_fields": ["noteType", "publish"],
        "ids": [], # Will override Filter below
        "query_json": { # For syntax, check autotask documentation
            "IncludeFields": [
                "id",
                "createDateTime",
                "createdByContactID",
                "creatorResourceID",
                "description",
                "impersonatorCreatorResourceID",
                "impersonatorUpdaterResourceID",
                "lastActivityDate",
                "noteType",
                "publish",
                "ticketID",
                "title"
            ],
            "Filter": [
                {"op":"gte","field":"createDateTime","value":"2024-07-06"},
            ],
        },
    }

    expected_result_type = DataFrame


class TestAutoTaskAssets(BaseTestCase):
    arguments: dict = {
        "skipError": "skip",
        "credentials": {
          "API_INTEGRATION_CODE": "AUTOTASK_API_INTEGRATION_CODE",
          "USERNAME": "AUTOTASK_USERNAME",
          "SECRET": "AUTOTASK_SECRET"
        },
        "entity": "ConfigurationItems",
        "zone": "webservices14",
        "id_column_name": "configuration_item_id",
        "picklist_fields": [
          "configurationItemType",
          "rmmDeviceAuditManufacturerID",
          "rmmDeviceAuditModelID",
        ],
        "ids": [],
        "query_json": {
          "IncludeFields": [
            "id",
            "productID",
            "companyID",
            "configurationItemCategoryID",
            "configurationItemType",
            "installDate",
            "warrantyExpirationDate",
            "serialNumber",
            "referenceNumber",
            "referenceTitle",
            "contactID",
            "contractServiceID",
            "serviceID",
            "vendorID",
            "isActive",
            "rmmDeviceAuditManufacturerID",
            "rmmDeviceAuditModelID",
            
            # UDFs
            "Asset Status",
            "Asset Tag",
            "Date Purchased",
            "Purchase Price",
            "Finance"
          ],
          "Filter": [
            {
              "op": "gte",
              "field": "id",
              "value": 12000
            }
          ]
        }
      }
    
    expected_result_type = DataFrame


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
