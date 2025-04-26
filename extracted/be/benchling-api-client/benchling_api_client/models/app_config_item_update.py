from typing import Union

from ..extensions import UnknownType
from ..models.app_config_item_boolean_update import AppConfigItemBooleanUpdate
from ..models.app_config_item_date_update import AppConfigItemDateUpdate
from ..models.app_config_item_datetime_update import AppConfigItemDatetimeUpdate
from ..models.app_config_item_float_update import AppConfigItemFloatUpdate
from ..models.app_config_item_generic_update import AppConfigItemGenericUpdate
from ..models.app_config_item_integer_update import AppConfigItemIntegerUpdate
from ..models.app_config_item_json_update import AppConfigItemJsonUpdate

AppConfigItemUpdate = Union[
    AppConfigItemGenericUpdate,
    AppConfigItemBooleanUpdate,
    AppConfigItemIntegerUpdate,
    AppConfigItemFloatUpdate,
    AppConfigItemDateUpdate,
    AppConfigItemDatetimeUpdate,
    AppConfigItemJsonUpdate,
    UnknownType,
]
