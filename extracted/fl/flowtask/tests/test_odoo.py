from pandas import DataFrame
import pytest
from flowtask.tests import BaseTestCase, PandasTestCase
from flowtask.exceptions import ComponentError


@pytest.fixture(autouse=True, scope="session")
def component():
    component = "Odoo"
    yield component


pytestmark = pytest.mark.asyncio


class TestOdooReadFSMOrders(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "HOST": "ODOO_HOST",
            "PORT": "ODOO_PORT",
            "DB": "ODOO_DB",
            "USERNAME": "ODOO_USERNAME",
            "PASSWORD": "ODOO_PASSWORD",
        },
        "model": "fsm.order",
        "method": "search_read",
        # "domain": [],
        "domain": [[("id", "in", [8, 9, 10])]],
        "fields": [
            "display_name",
            "person_id",
            "location_id",
            "stage_id",
        ],
    }

    expected_result_type = DataFrame


class TestOdooReadFSMOrdersPreviousDF(PandasTestCase):
    """Search records from a list of values provided in previous step DF.
    Set a field name to the 'use_filter_field' argument.
    """

    file_test = "odoo_fsm_locations.csv"

    arguments: dict = {
        "credentials": {
            "HOST": "ODOO_HOST",
            "PORT": "ODOO_PORT",
            "DB": "ODOO_DB",
            "USERNAME": "ODOO_USERNAME",
            "PASSWORD": "ODOO_PASSWORD",
        },
        "model": "fsm.order",
        "method": "search_read",
        "use_field_from_previous_step": "location_id",
        "fields": [
            "display_name",
            "person_id",
            "location_id",
            "stage_id",
        ],
    }

    expected_result_type = DataFrame


class TestOdooCreateFSMOrders(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "HOST": "ODOO_HOST",
            "PORT": "ODOO_PORT",
            "DB": "ODOO_DB",
            "USERNAME": "ODOO_USERNAME",
            "PASSWORD": "ODOO_PASSWORD",
        },
        "model": "fsm.order",
        "method": "create",
        "values": [[{"location_id": 2}, {"location_id": 2}]],
    }

    expected_result_type = DataFrame


class TestOdooCreateFSMOrdersPreviousDF(PandasTestCase):
    """Create records from a previous step DF"""

    file_test = "odoo_fsm_orders.csv"

    arguments: dict = {
        "credentials": {
            "HOST": "ODOO_HOST",
            "PORT": "ODOO_PORT",
            "DB": "ODOO_DB",
            "USERNAME": "ODOO_USERNAME",
            "PASSWORD": "ODOO_PASSWORD",
        },
        "model": "fsm.order",
        "method": "create",
    }

    expected_result_type = DataFrame


class TestOdooCreateFSMOrdersException(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "HOST": "ODOO_HOST",
            "PORT": "ODOO_PORT",
            "DB": "ODOO_DB",
            "USERNAME": "ODOO_USERNAME",
            "PASSWORD": "ODOO_PASSWORD",
        },
        "model": "fsm.order",
        "method": "create",
    }

    expected_exception_msg = '"values" required for "create" method'


class TestOdooReadStock(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "HOST": "ODOO_HOST",
            "PORT": "ODOO_PORT",
            "DB": "ODOO_DB",
            "USERNAME": "ODOO_USERNAME",
            "PASSWORD": "ODOO_PASSWORD",
        },
        "model": "stock.quant",
        "method": "search_read",
        # "domain": [],
        "fields": [
            "display_name",
            "product_id",
            "location_id",
            "quantity",
            "reserved_quantity",
            "available_quantity",
        ],
    }

    expected_result_type = DataFrame


class TestOdooCreateDeliveryOrders(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "HOST": "ODOO_HOST",
            "PORT": "ODOO_PORT",
            "DB": "ODOO_DB",
            "USERNAME": "ODOO_USERNAME",
            "PASSWORD": "ODOO_PASSWORD",
        },
        "model": "stock.picking",
        "method": "create",
        "values": [
            [
                {
                    "is_locked": True,
                    "immediate_transfer": True,
                    "priority": "0",
                    "partner_id": 9,
                    "picking_type_id": 2,
                    "location_id": 8,
                    "location_dest_id": 5,
                    "scheduled_date": "2024-05-24 22:10:45",
                    "origin": "FSM001",
                    "move_line_nosuggest_ids": [],
                    "move_line_ids_without_package": [
                        [
                            0,
                            "virtual_5",
                            {
                                "product_id": 1,
                                "move_id": False,
                                "picking_id": False,
                                "package_id": False,
                                "result_package_id": False,
                                "location_id": 8,
                                "location_dest_id": 5,
                                "qty_done": 10,
                            },
                        ],
                        [
                            0,
                            "virtual_6",
                            {
                                "product_id": 2,
                                "move_id": False,
                                "picking_id": False,
                                "package_id": False,
                                "result_package_id": False,
                                "location_id": 8,
                                "location_dest_id": 5,
                                "qty_done": 10,
                            },
                        ],
                    ],
                    "move_ids_without_package": [],
                    "package_level_ids": [],
                    "move_type": "direct",
                    "user_id": 8,
                    "note": "<p>Notes goes here<br></p>",
                }
            ]
        ],
    }

    expected_result_type = DataFrame


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
