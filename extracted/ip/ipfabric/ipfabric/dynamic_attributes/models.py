import json
from functools import cached_property
from typing import Optional, Any, Union

import numpy as np
from ipfabric.models import Device
from pydantic import BaseModel, Field

from ipfabric.dynamic_attributes.configs import TableValue, ConfigValue
from ipfabric.dynamic_attributes.configs.rules import ConfigRule


CONFIG_MAP = {
    "current": {
        "no": "no_current_config",
        "config": "current_config",
        "name": "current",
    },
    "startup": {
        "no": "no_start_config",
        "config": "start_config",
        "name": "startup",
    },
    "log": {
        "no": "no_log_file",
        "config": "log_file",
        "name": "log_file",
    },
}


class BaseMatch(BaseModel):
    name: str = Field(description="The name of the rule that matched this device.")
    attribute: str = Field(description="The name of the attribute to assign.")
    current_value: Optional[str] = Field(None, description="The current global value of the attribute.")
    new_value: Optional[str] = Field(None, description="The new value to assign to the attribute.")
    mapping_match: Optional[dict] = Field(None, description="The mapping match from the mapping file.")
    regex_match: Optional[str] = Field(None, description="The original regex match.")
    delete: bool = Field(False, description="Whether to delete the attribute.")
    overwrite: bool = Field(False, description="Whether to overwrite existing attribute values.")

    @property
    def marked_for_deletion(self) -> bool:
        if self.delete and not self.new_value and self.current_value:
            return True
        return False

    def export(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "new_value": self.new_value,
            "null_value": self.null_value,
            "regex_pattern": self.regex.pattern if self.regex else np.nan,
            "regex_group": self.regex.group if self.regex else np.nan,
            "regex_match": self.regex_match,
            "mapping_match": (json.dumps(self.mapping_match) if self.mapping_match else np.nan),
            "delete": self.delete,
            "overwrite": self.overwrite,
        }


class MatchedRule(BaseMatch, TableValue, BaseModel):
    column_value: Optional[str] = Field(None, description="The value of the column from the API response.")

    def export(self) -> dict[str, Any]:
        return {
            "api_endpoint": self.api_endpoint,
            "column_value": self.column_value if self.column else np.nan,
            "static": self.static if self.static else np.nan,
            **super().export(),
        }


class MatchedConfig(BaseMatch, ConfigValue, BaseModel):
    no_config_match: bool = Field(False, description="Whether the config was not found or supported.")

    def export(self) -> dict[str, Any]:
        return {
            "config": self.config,
            **super().export(),
        }


class Attribute(BaseModel):
    device: Device = Field(description="IP Fabric Device object.")
    matched_rule: dict[str, Union[MatchedRule, None]] = Field(
        default_factory=dict, description="Dictionary of Attributes mapped to the Matched TableRule."
    )
    no_start_config: Optional[bool] = Field(None, description="Whether the startup config is not supported.")
    no_current_config: Optional[bool] = Field(None, description="Whether the current config is not supported.")
    no_log_file: Optional[bool] = Field(None, description="Whether the log file is not supported.")
    start_config: Optional[str] = Field(None, description="Cached Startup Configuration.")
    current_config: Optional[str] = Field(None, description="Cached Current Configuration.")
    log_file: Optional[str] = Field(None, description="Cached Current Configuration.")

    @cached_property
    def sn(self) -> str:
        return self.device.sn

    def config_skip(self, rule: ConfigRule) -> bool:
        attribute = self.matched_rule.get(rule.attribute)
        if attribute and (not attribute.no_config_match or attribute.marked_for_deletion):
            # If an Attribute was set or no match was found, skip the device
            return True
        if getattr(self, CONFIG_MAP[rule.value.config]["no"]):
            # If the config is not supported, skip the device
            return True
        return False

    def global_attribute(self, name) -> Union[str, None]:
        return self.device.global_attributes.get(name)

    def local_attribute(self, name) -> Union[str, None]:
        return self.device.local_attributes.get(name)

    def export(self, report_columns: Union[None, list[str]] = None) -> list[dict[str, Any]]:
        matches = []
        for attribute, match in self.matched_rule.items():
            data = {
                **{_: self.device.model_dump(by_alias=True).get(_) for _ in report_columns},
                "attribute": attribute,
                "global_value": self.global_attribute(attribute),
                "local_value": self.local_attribute(attribute),
                "no_start_config": self.no_start_config,
                "no_current_config": self.no_current_config,
                "no_log_file": self.no_log_file,
            }
            if match:
                data.update(match.export())
            matches.append(data)
        return matches
