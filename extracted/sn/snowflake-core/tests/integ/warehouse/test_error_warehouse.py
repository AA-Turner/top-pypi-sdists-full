import pytest

from snowflake.core.exceptions import APIError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse_fixture")


def test_api_error(warehouses, root):
    test_warehouse_name = random_string(3, "test_wh_123")
    new_wh_def = Warehouse(name=test_warehouse_name, warehouse_size="f")
    with pytest.raises(APIError) as exc_info:
        warehouses.create(new_wh_def)
    assert "Error Message: invalid type of property 'f' for 'warehouse_size'" in str(exc_info.value)
