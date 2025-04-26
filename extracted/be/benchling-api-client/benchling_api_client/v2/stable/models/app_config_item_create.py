from typing import Union

from ..extensions import UnknownType
from ..models.app_config_item_boolean_create import AppConfigItemBooleanCreate
from ..models.app_config_item_date_create import AppConfigItemDateCreate
from ..models.app_config_item_datetime_create import AppConfigItemDatetimeCreate
from ..models.app_config_item_float_create import AppConfigItemFloatCreate
from ..models.app_config_item_generic_create import AppConfigItemGenericCreate
from ..models.app_config_item_integer_create import AppConfigItemIntegerCreate
from ..models.app_config_item_json_create import AppConfigItemJsonCreate

AppConfigItemCreate = Union[
    AppConfigItemGenericCreate,
    AppConfigItemBooleanCreate,
    AppConfigItemIntegerCreate,
    AppConfigItemFloatCreate,
    AppConfigItemDateCreate,
    AppConfigItemDatetimeCreate,
    AppConfigItemJsonCreate,
    UnknownType,
]
