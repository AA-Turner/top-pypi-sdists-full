from typing import Literal, cast

ConfigItemDefinitionTypeType0 = Literal["BOOLEAN", "JSON", "NUMBER", "STRING"]

CONFIG_ITEM_DEFINITION_TYPE_TYPE_0_VALUES: set[ConfigItemDefinitionTypeType0] = {
    "BOOLEAN",
    "JSON",
    "NUMBER",
    "STRING",
}


def check_config_item_definition_type_type_0(value: str) -> ConfigItemDefinitionTypeType0:
    if value in CONFIG_ITEM_DEFINITION_TYPE_TYPE_0_VALUES:
        return cast(ConfigItemDefinitionTypeType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONFIG_ITEM_DEFINITION_TYPE_TYPE_0_VALUES!r}")
