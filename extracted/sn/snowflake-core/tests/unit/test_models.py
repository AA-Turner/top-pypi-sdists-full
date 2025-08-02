import pytest

from snowflake.core.account import Account
from snowflake.core.account._generated.models import Account as BaseAccount
from snowflake.core.compute_pool import ComputePool
from snowflake.core.compute_pool._generated.models import ComputePool as BaseComputePool
from snowflake.core.database import Database
from snowflake.core.database._generated.models.database import Database as BaseDatabase
from snowflake.core.image_repository import ImageRepository
from snowflake.core.image_repository._generated.models import ImageRepository as BaseImageRepository
from snowflake.core.managed_account import ManagedAccount
from snowflake.core.managed_account._generated.models import ManagedAccount as BaseManagedAccount
from snowflake.core.role import Role
from snowflake.core.role._generated.models import Role as BaseRole
from snowflake.core.schema import Schema
from snowflake.core.schema._generated.models import Schema as BaseSchema
from snowflake.core.task import Task
from snowflake.core.task._generated.models import Task as BaseTask
from snowflake.core.user import User
from snowflake.core.user._generated.models import User as BaseUser
from snowflake.core.warehouse import Warehouse
from snowflake.core.warehouse._generated.models import Warehouse as BaseWarehouse


@pytest.mark.parametrize(
    "base_obj, obj",
    [
        (
            BaseAccount(name="admin", edition="STANDARD", admin_name="admin", email="admin@localhost"),
            Account("admin", "STANDARD", "admin", "admin@localhost"),
        ),
        (
            BaseComputePool(name="cp", min_nodes=1, max_nodes=1, instance_family="fake"),
            ComputePool(name="cp", min_nodes=1, max_nodes=1, instance_family="fake"),
        ),
        (BaseDatabase(name="db"), Database("db")),
        (
            BaseManagedAccount(name="admin", admin_name="admin", admin_password="test123", account_type=""),
            ManagedAccount("admin", "admin", "test123", ""),
        ),
        (BaseRole(name="role"), Role("role")),
        (BaseImageRepository(name="rep"), ImageRepository("rep")),
        (BaseSchema(name="public"), Schema("public")),
        (BaseTask(name="task", definition="select 1"), Task("task", "select 1")),
        (BaseUser(name="user"), User("user")),
        (BaseWarehouse(name="wh"), Warehouse("wh")),
    ],
    ids=lambda t: type(t).__name__,
)
def test_repr(base_obj, obj):
    assert repr(base_obj) == repr(obj)
