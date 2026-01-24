import re
from functools import cached_property
from typing import Optional, Literal, Any, Union

from pydantic import BaseModel, Field, model_validator

RE_FLAGS = list[
    Literal[
        "IGNORECASE", "MULTILINE", "DOTALL", "VERBOSE", "UNICODE", "ASCII", "LOCALE", "I", "M", "S", "X", "A", "U", "L"
    ]
]


class RegexValue(BaseModel):
    pattern: str = Field(
        description="The regex pattern to use for the Attribute Value.", title="Regex Pattern", examples=["^(\\w\\w)-"]
    )
    group: int = Field(0, description="The group number to extract from the regex match.", title="Regex Group", ge=0)
    flags: Optional[RE_FLAGS] = Field(
        default_factory=list,
        description="Regex flags to use for the regex pattern.",
        title="Regex Flags",
        examples=["IGNORECASE", "MULTILINE", "DOTALL", "VERBOSE", "UNICODE", "ASCII", "LOCALE"],
    )

    @cached_property
    def compiled(self):
        """Compile the regex pattern for use in matching."""
        flags = 0
        for _ in self.flags:
            flags |= getattr(re, _)
        return re.compile(self.pattern, flags=flags)


class BaseValue(BaseModel):
    static: Optional[Any] = Field(
        None,
        description="A static value to assign to the Attribute.",
        title="Static Value",
        examples=["PROD", "TEST", "LAB"],
    )
    regex: Optional[RegexValue] = Field(
        None, description="A regex pattern to extract a value from the returned data.", title="Regex Value"
    )
    transform: Optional[Literal["upper", "lower"]] = Field(
        None,
        description="Transform the value to upper or lower case (not used for static values).",
        title="Transformation",
        examples=["upper", "lower"],
    )
    mapping: dict[str, Any] = Field(
        default_factory=dict,
        description="A dictionary mapping the returned data or regex group to a static value to assign to the "
        "Attribute. Any transformations is applied prior to lookup.",
        title="Attribute Value Mapping",
        examples=[{"US": "United States", "usnyc": "New York City"}],
    )
    null_value: Optional[Any] = Field(
        None,
        description="Value to assign if the column is null or no regex match.",
        title="Null Value",
        examples=["unknown", "N/A"],
    )
    default_mapping_value: Optional[Any] = Field(
        None,
        description="Default Value to assign in conjunction with mapping if no key/value pair is found.",
        title="Default Mapping Value",
        examples=["unknown", "N/A"],
    )

    def calc_mapped_value(self, value: str) -> tuple[Union[str, None], str, Union[dict[str, str], None]]:
        regex_match = value if self.regex else None
        if not self.mapping:
            return value, regex_match, None
        if value in self.mapping:
            # If a mapping is set, we want to look up the value in the mapping.
            mapped = str(self.mapping.get(value))
            return mapped, regex_match, {value: mapped}
        if self.default_mapping_value:
            # If the value is not in the mapping, we want to return the default mapping value if set.
            mapped = str(self.default_mapping_value)
            return mapped, regex_match, {value: mapped}
        # If the value is not in the mapping and no default mapping value is set, we return None.
        return None, regex_match, None


class ConfigValue(BaseValue, BaseModel):
    config: Literal["current", "startup", "log"] = Field(
        "current",
        description="The configuration to use for the Attribute Value. Not all vendors and families support snapshot "
        "configuration tasks and some do not startup configs.",
        title="Configuration Type",
        examples=["current", "startup"],
    )
    static: Optional[Any] = Field(
        None,
        description="A static value to assign to the Attribute if a regex match is found in the configuration.",
        title="Static Value",
        examples=["PROD", "TEST", "LAB"],
    )
    regex: RegexValue = Field(
        description="A regex pattern to search the config; if a static value is used then the group is ignored.",
        title="Regex Value",
    )
    no_config_value: Optional[str] = Field(
        None,
        description="Value to assign if the config is not found or supported.",
        title="No Config Value",
        examples=["unknown", "N/A"],
    )
    no_log_value: Optional[str] = Field(
        None,
        description="Value to assign if the log file is not found or supported.",
        title="No Log Value",
        examples=["unknown", "N/A"],
    )

    @model_validator(mode="after")
    def _validate(self):
        if self.default_mapping_value and not self.mapping:
            raise ValueError("'default_mapping_value' must be used with 'mapping'.")
        if self.mapping and self.static:
            raise ValueError("Mapping cannot be used with a Static Value.")
        return self

    def calc_value(self, data: str) -> tuple[Union[str, None], Union[str, None], Union[dict[str, str], None]]:
        if self.transform:
            # If a transform is set, we want to apply it to the value.
            data = data.upper() if self.transform == "upper" else data.lower()
        match = self.regex.compiled.search(data)
        if match and self.static:
            # If the static value is set, we want to return it directly on the matched config.
            return str(self.static), match.group(0), None
        if not match or self.regex.group > len(match.groups()):
            return self.null_value, None, None
        value = match.group(self.regex.group)
        return self.calc_mapped_value(value)


class Sort(BaseModel):
    column: str = Field(
        description="The name of the column to sort by.",
        title="API Column Name",
        examples=["primaryIp", "hostname"],
    )
    order: Literal["asc", "desc"] = Field(
        "asc",
        description="The order to sort the results in.",
        title="Table Sort",
        examples=["asc", "desc"],
    )


class TableValue(BaseValue, BaseModel):
    api_endpoint: str = Field(
        description="The IP Fabric API table endpoint to fetch data from.",
        title="API Table Endpoint",
        examples=["tables/inventory/interfaces", "tables/vrf/detail"],
    )
    column: Optional[str] = Field(
        None,
        description="The name of the column to use for the Attribute Value.",
        title="API Column Name",
        examples=["primaryIp", "hostname"],
    )
    sn_column: Optional[str] = Field(
        None,
        description="The name of the column to use for the device serial number, defaults to 'sn'. "
        "Some tables have a different column name for the device serial number such as 'localSn'.",
        title="Device Serial Number Column",
        examples=["sn", "localSn"],
    )
    sort: Optional[Sort] = Field(None, description="Sort the results by the specified column.", title="Table Sorting")

    @model_validator(mode="after")
    def _validate(self):
        if not self.column and not self.static:
            raise ValueError("Either 'column' or 'static' must be provided.")
        if self.column and self.static and not self.regex:
            raise ValueError("Only 'static' can only be used with 'column' and 'regex' or by itself.")
        if self.default_mapping_value and not self.mapping:
            raise ValueError("'default_mapping_value' must be used with 'mapping'.")
        if self.mapping and self.static:
            raise ValueError("Mapping cannot be used with a Static Value.")
        if self.null_value and self.static and not self.column:
            raise ValueError("'null_value' must be used with 'column'.")
        if self.regex and not self.column:
            raise ValueError("'regex' can only be used with a column.")
        return self

    @cached_property
    def sn(self) -> str:
        """Return the serial number column name to use for the API request."""
        return self.sn_column or "sn"

    def calc_value(self, data) -> tuple[Union[str, None], Union[str, None], Union[dict[str, str], None]]:
        """Calculate the value for the attribute based on the data from the API response.

        Args:
            data (dict): The data from the API response.

        Returns:
            tuple: A tuple containing the value to assign to the attribute, the regex match, and the mapping match.
        """
        if self.static and not self.column:
            # If the static value is set, we want to return it directly.
            return str(self.static), None, None
        value = data.get(self.column)
        if isinstance(value, dict) and ["data", "severity"] == list(value.keys()):
            # If the value is a dict with keys "data" and "severity", we want to extract the "data" part.
            value = value["data"]
        if value is None:
            # If the value is None, we want to return the null_value if set.
            return self.null_value, None, None

        value = str(value)
        if self.transform:
            # If a transform is set, we want to apply it to the value.
            value = value.upper() if self.transform == "upper" else value.lower()
        if self.regex:
            match = self.regex.compiled.match(value)
            if match and self.static:
                # If the static value is set, we want to return it directly on the matched value.
                return str(self.static), match.group(0), None
            if match and self.regex.group <= len(match.groups()):
                # If the regex pattern matches, we want to extract the group specified and set it as the value.
                value = match.group(self.regex.group)
            else:
                # If the regex pattern does not match, we want to return the null_value if set.
                return self.null_value, None, None
        return self.calc_mapped_value(value)
