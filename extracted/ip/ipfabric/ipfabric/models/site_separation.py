from typing import Optional, Literal, Annotated, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseRule(BaseModel):
    rule_type: Literal["regexHostname", "regexSnmpLocation", "regexCloudResourceId", "slug", "routingSwitching"] = (
        Field(alias="type")
    )
    rule_id: str = Field(alias="id", default_factory=lambda x: str(x or uuid4()))
    note: str = ""
    transformation: Literal["none", "uppercase", "lowercase"]


class SiteRule(BaseRule, BaseModel):
    siteName: Optional[str] = None
    regex: str


class HostnameRule(SiteRule, BaseModel):
    rule_type: Literal["regexHostname"] = Field(alias="type")


class SNMPRule(SiteRule, BaseModel):
    rule_type: Literal["regexSnmpLocation"] = Field(alias="type")


class RouteSwitchRule(BaseRule, BaseModel):
    rule_type: Literal["routingSwitching"] = Field(alias="type")
    firewall: bool
    minimumSiteSize: int = Field(ge=1)
    wan: list[Literal["serial", "tunnel"]] = Field(default_factory=list)


class SlugRule(BaseRule, BaseModel):
    rule_type: Literal["slug"] = Field(alias="type")
    applyToCloudInstances: bool


class CloudIDRule(SiteRule, BaseModel):
    rule_type: Literal["regexCloudResourceId"] = Field(alias="type")
    applyToCloudInstances: bool


SeparationRule = Annotated[
    Union[
        HostnameRule,
        SNMPRule,
        RouteSwitchRule,
        SlugRule,
        CloudIDRule,
    ],
    Field(discriminator="rule_type"),
]


class SiteSeparation(BaseModel):
    rules: list[SeparationRule] = Field(default_factory=list)
    manualEnabled: bool
    neighborshipFallbackEnabled: bool
