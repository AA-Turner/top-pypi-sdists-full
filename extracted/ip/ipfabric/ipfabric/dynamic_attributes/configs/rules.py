from functools import cached_property
from typing import Optional, Union, ForwardRef, Any

from pydantic import BaseModel, Field, model_validator, PrivateAttr, computed_field, ConfigDict

from ipfabric.dynamic_attributes.configs.filters import Filter, AttributeFilter, DeviceFilter
from ipfabric.dynamic_attributes.configs.values import TableValue, ConfigValue

REPORT_COLS = [
    "attribute",
    "global_value",
    "local_value",
    "no_config",
    "name",
    "api_endpoint",
    "no_start_config",
    "no_current_config",
    "new_value",
    "column_value",
    "static",
    "null_value",
    "regex_pattern",
    "regex_group",
    "regex_match",
    "mapping_match",
    "delete",
    "overwrite",
]

TableRule, ConfigRule = ForwardRef("TableRule"), ForwardRef("ConfigRule")
DefaultRule, DefaultConfigRule = ForwardRef("DefaultRule"), ForwardRef("DefaultConfigRule")


def merge_default(
    original: Union[TableRule, ConfigRule], default: Union[DefaultRule, DefaultConfigRule]
) -> Union[TableRule, ConfigRule]:
    if not default:
        original.overwrite = original.overwrite or False
        return original
    if default.overwrite is not None and original.overwrite is None:
        # Copy default overwrite to Rule:
        original.overwrite = default.overwrite
    # If Rule does not have overwrite set, set it to False:
    original.overwrite = original.overwrite or False
    # Copy Default Attribute Name to Rule:
    original.attribute = original.attribute or default.attribute
    if default.delete_attribute is not None and original.delete_attribute is None:
        # Copy Default Delete Attribute to Rule if Rule does not have delete_attribute set:
        original.delete_attribute = default.delete_attribute
    if original.merge_default_filters:
        if default.filter_string and not original.filters:
            # Copy Default Filter String to Rule if Rule does not have filters and merge_default_filters is True:
            original.filter_string = default.filter_string
        if default.filters and not original.filter_string:
            # Copy Default Filters to Rule if Rule does not have a filter_string and merge_default_filters is True:
            original.filters.extend(default.filters)
    return original


class FilterRule(BaseModel):
    filters: list[Filter] = Field(
        default_factory=list, description="List of filters to apply to table endpoint.", title="Table Filters"
    )
    filter_string: Optional[str] = Field(
        None,
        description="A string to use for the filter on table endpoint instead of the filters list.",
        title="Table Filter String",
        examples=['{"vendor":["like","cisco"]}'],
    )

    @model_validator(mode="after")
    def _validate(self):
        if self.filters and self.filter_string:
            raise ValueError("'rule[filter_string]' cannot be combined with 'rule[filters]'.")
        return self

    @property
    def filter_list(self) -> list[dict]:
        return [_.format for _ in self.filters]

    @property
    def calc_filter(self) -> Union[dict[str, list[dict]], str]:
        if self.filter_string:
            return self.filter_string
        return {"and": self.filter_list} if self.filter_list else {}

    @property
    def filter_hash(self) -> Union[int, None]:
        """Return a hash of the filter string or list."""
        if self.filter_string:
            return hash(self.filter_string)
        return hash(str(sorted(self.filter_list, key=lambda x: str(x)))) if self.filter_list else None


class BaseRule(FilterRule, BaseModel):
    attribute_filters: list[AttributeFilter] = Field(
        default_factory=list, description="Attribute Filters to apply to table endpoint.", title="Attribute Filters"
    )

    @model_validator(mode="after")
    def _validate(self):
        if (self.filters or self.attribute_filters) and self.filter_string:
            raise ValueError(
                "'rule[filter_string]' cannot be combined with 'rule[filters]' or 'rule[attribute_filters]'."
            )
        return self

    @property
    def filter_list(self) -> list[dict]:
        return [*super().filter_list, *[_.format for _ in self.attribute_filters]]


class InventoryRule(BaseRule, BaseModel):
    report_columns: list[str] = Field(
        default_factory=list,
        description="List of Inventory > Devices columns to also include in the Sync Report; "
        "the report will always return [hostname, sn, siteName].",
        title="Inventory Report Columns",
        examples=["model"],
    )

    @cached_property
    def calc_columns(self) -> list[str]:
        """Return the columns to use for the Inventory."""
        return [_ for _ in {"hostname", "sn", "siteName", *self.report_columns}]

    @cached_property
    def df_columns(self) -> list[str]:
        """Return the columns to use for the DataFrame."""
        return [*self.calc_columns, *REPORT_COLS]


class CommonDefaultRule(BaseModel):
    """Common Default Rule for Table and Config Rules."""

    attribute: Optional[str] = Field(
        None,
        description="The name of the Attribute to be updated or created.",
        title="Attribute Name",
        examples=["COUNTRY", "MGMT_IP", "ENVIRONMENT"],
    )
    delete_attribute: Optional[bool] = Field(
        None,
        description="Caution: If no match is found this will delete the Attribute from all devices in the filtered "
        "inventory list for this Attribute Name. After running each rule and no match is found, the "
        "attribute will be flagged for deletion in the remaining inventory list. If a later rule matches "
        "does find a match then the attribute will not be deleted and the new value will be assigned.",
        title="Delete Attribute (DANGEROUS - Read the Description)",
    )
    overwrite: Optional[bool] = Field(
        None,
        description="Overwrite existing Global Attribute values; default False.",
        title="Overwrite Global Attribute",
    )


class DefaultRule(CommonDefaultRule, BaseRule, BaseModel):
    value: Optional[TableValue] = Field(
        None,
        description="The value to assign to the Attribute, "
        "either configured in the Default Table rules or per Table rule.",
        title="Attribute Value",
    )
    device_filters: list[DeviceFilter] = Field(
        default_factory=list,
        description="Device filter to apply to the table endpoint (i.e. vendor, family, etc.).",
        title="Device Filters",
    )

    @model_validator(mode="after")
    def _validate(self):
        if (self.filters or self.attribute_filters or self.device_filters) and self.filter_string:
            raise ValueError(
                "'rule[filter_string]' cannot be combined with 'rule[filters]', "
                "'rule[attribute_filters]', or 'rule[device_filters]'."
            )
        return self

    @property
    def filter_list(self) -> list[dict]:
        return [*super().filter_list, *[_.format for _ in self.device_filters]]


class CommonRule(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str = Field(
        description="A unique name of the rule for reporting purposes.",
        title="Rule Name",
        examples=["Rule 1", "Loopback0 Rule"],
    )
    _inventory: Optional[InventoryRule] = PrivateAttr(None)

    def model_post_init(self, context: Any, /) -> None:
        self._inventory = InventoryRule(**self.model_extra["inventory"]) if "inventory" in self.model_extra else None

    @computed_field(
        title="Internal Inventory Rule",
        description="Internal Inventory Rule used for filtering devices when joining multiple configuration files.",
    )
    @property
    def inventory(self) -> Union[InventoryRule, None]:
        return self._inventory

    @inventory.setter
    def inventory(self, value: Union[InventoryRule, None]):
        self._inventory = value


class TableRule(CommonRule, DefaultRule, BaseModel):
    merge_default_filters: bool = Field(
        True,
        description="Merge 'default[filters]' with Table TableRule filters or "
        "'default[filter_string]' to Table TableRule filter_string.",
        title="Merge Default Filters",
    )
    merge_default_device_filters: bool = Field(
        True,
        description="Merge 'default[device_filters]' with Table TableRule device_filters.",
        title="Merge Default Device Filters",
    )
    merge_default_attribute_filters: bool = Field(
        True,
        description="Merge 'default[attribute_filters]' with Table TableRule attribute_filters.",
        title="Merge Default Attribute Filters",
    )

    def merge_default(self, default: DefaultRule) -> "TableRule":
        if not isinstance(default, DefaultRule):
            return self
        rule = merge_default(self.model_copy(deep=True), default)
        # Copy Default Value Config to TableRule:
        rule.value = rule.value or default.value
        # Copy Default SN Column to TableRule:
        rule.value.sn_column = rule.value.sn_column or (default.value.sn_column if default.value else "sn")
        if not rule.filter_string:
            if default.device_filters and rule.merge_default_device_filters:
                # Copy Default Device Filters to TableRule if merge_default_filters is True and filter_string is not set:
                rule.device_filters.extend(default.device_filters)
            if default.attribute_filters and rule.merge_default_attribute_filters:
                # Copy Default Attribute Filters to TableRule if merge_default_attribute_filters is True:
                rule.attribute_filters.extend(default.attribute_filters)
        return rule


class DefaultConfigRule(CommonDefaultRule, FilterRule, BaseModel):
    filters: list[Filter] = Field(
        default_factory=list,
        description="Additional Inventory Filters to apply to limit devices for configuration matching.",
        title="Additional Inventory Filters",
    )
    filter_string: Optional[str] = Field(
        None,
        description="A string to use for additional Inventory Filtering instead of the filters list.",
        title="Additional Inventory Filter String",
        examples=['{"vendor":["like","cisco"]}'],
    )
    overwrite_unsupported: Optional[bool] = Field(
        None,
        description="If a device does not support configuration tasks and a custom Attribute is set then the default"
        " (false) is to ignore overwriting the manual Attribute with the 'no_config_value' in the value "
        "config. This provides more flexibility than the 'overwrite' setting which is only used for "
        "supported devices. If this is set to 'true' then the 'no_config_value' will be used to "
        "overwrite the manual Attribute value.",
        title="Overwrite Unsupported Devices' Attributes",
    )

    @model_validator(mode="after")
    def _validate(self):
        if self.filters and self.filter_string:
            raise ValueError("'rule[filter_string]' cannot be combined with 'rule[filters]'.")
        return self


class ConfigRule(CommonRule, DefaultConfigRule, BaseModel):
    value: ConfigValue = Field(
        description="The value to assign to the Attribute based on a configuration search.",
        title="Attribute Value",
    )
    merge_default_filters: bool = Field(
        True,
        description="Merge 'default[config_filters]' with Configuration TableRule filters.",
        title="Merge Default Configuration Filters",
    )

    def merge_default(self, default: DefaultConfigRule) -> "ConfigRule":
        """Merge Default Config TableRule with Config TableRule"""
        if isinstance(default, DefaultConfigRule):
            rule = merge_default(self.model_copy(deep=True), default)
            if default.overwrite_unsupported is not None and rule.overwrite_unsupported is None:
                # Copy default overwrite_unsupported to Rule:
                rule.overwrite_unsupported = default.overwrite_unsupported
        else:
            rule = self.model_copy(deep=True)
        rule.overwrite_unsupported = rule.overwrite_unsupported or False
        return rule


TableRule.model_rebuild()
ConfigRule.model_rebuild()
DefaultRule.model_rebuild()
DefaultConfigRule.model_rebuild()
