from typing import Union

from ..extensions import UnknownType
from ..models.array_element_app_config_item import ArrayElementAppConfigItem
from ..models.boolean_app_config_item import BooleanAppConfigItem
from ..models.date_app_config_item import DateAppConfigItem
from ..models.datetime_app_config_item import DatetimeAppConfigItem
from ..models.entity_schema_app_config_item import EntitySchemaAppConfigItem
from ..models.field_app_config_item import FieldAppConfigItem
from ..models.float_app_config_item import FloatAppConfigItem
from ..models.generic_api_identified_app_config_item import GenericApiIdentifiedAppConfigItem
from ..models.integer_app_config_item import IntegerAppConfigItem
from ..models.json_app_config_item import JsonAppConfigItem
from ..models.secure_text_app_config_item import SecureTextAppConfigItem
from ..models.text_app_config_item import TextAppConfigItem

AppConfigItem = Union[
    ArrayElementAppConfigItem,
    DateAppConfigItem,
    DatetimeAppConfigItem,
    JsonAppConfigItem,
    EntitySchemaAppConfigItem,
    FieldAppConfigItem,
    BooleanAppConfigItem,
    IntegerAppConfigItem,
    FloatAppConfigItem,
    TextAppConfigItem,
    GenericApiIdentifiedAppConfigItem,
    SecureTextAppConfigItem,
    UnknownType,
]
