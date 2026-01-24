from functools import cached_property
from typing import Union

from pydantic import BaseModel, Field


class BaseFilter(BaseModel):
    value: Union[str, bool, int, float] = Field(description="The value to use for the filter.", title="Filter Value")
    operator: str = Field(
        "eq",
        description="The IP Fabric operator to use for the filter (see API documentation).",
        title="Filter Operator",
        examples=[
            "eq",
            "neq",
            "ieq",
            "nieq",
            "lt",
            "lte",
            "gt",
            "gte",
            "like",
            "notlike",
            "reg",
            "nreg",
            "ireg",
            "nireg",
        ],
    )


class AttributeFilter(BaseFilter, BaseModel):
    key: str = Field(
        description="The Attribute Name to filter on.", title="Attribute Name", examples=["MGMT_IP", "COUNTRY"]
    )

    @cached_property
    def format(self) -> dict[str, list]:
        """Format the filter for use in the API request."""
        return {"device.attributes": [self.key, self.operator, self.value]}


class Filter(BaseFilter, BaseModel):
    column: str = Field(
        description="The name of the column to use for the filter.",
        title="API Column Name",
        examples=["primaryIp", "hostname"],
    )

    @cached_property
    def format(self) -> dict[str, list]:
        """Format the filter for use in the API request."""
        return {self.column: [self.operator, self.value]}


class DeviceFilter(Filter, BaseModel):
    @cached_property
    def format(self) -> dict[str, list]:
        """Format the filter for use in the API request."""
        return {f"device.{self.column}": [self.operator, self.value]}
