from typing import Union

from ..extensions import UnknownType
from ..models.app_config_item_boolean_bulk_update import AppConfigItemBooleanBulkUpdate
from ..models.app_config_item_date_bulk_update import AppConfigItemDateBulkUpdate
from ..models.app_config_item_datetime_bulk_update import AppConfigItemDatetimeBulkUpdate
from ..models.app_config_item_float_bulk_update import AppConfigItemFloatBulkUpdate
from ..models.app_config_item_generic_bulk_update import AppConfigItemGenericBulkUpdate
from ..models.app_config_item_integer_bulk_update import AppConfigItemIntegerBulkUpdate
from ..models.app_config_item_json_bulk_update import AppConfigItemJsonBulkUpdate

AppConfigItemBulkUpdate = Union[
    AppConfigItemGenericBulkUpdate,
    AppConfigItemBooleanBulkUpdate,
    AppConfigItemIntegerBulkUpdate,
    AppConfigItemFloatBulkUpdate,
    AppConfigItemDateBulkUpdate,
    AppConfigItemDatetimeBulkUpdate,
    AppConfigItemJsonBulkUpdate,
    UnknownType,
]
