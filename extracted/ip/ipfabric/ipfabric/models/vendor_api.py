from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric.client import IPFClient

import json
from typing import Union, Literal, Annotated, Optional, Any

from pydantic import (
    field_validator,
    BaseModel,
    Field,
    AnyHttpUrl,
    model_serializer,
    AfterValidator,
    SerializationInfo,
    model_validator,
    RootModel,
)

from ipfabric.tools.shared import valid_slug, raise_for_status

AWS_REGIONS = [
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-southeast-5",
    "ap-southeast-7",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "mx-central-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-gov-east-1",
    "us-gov-west-1",
    "us-west-1",
    "us-west-2",
]

URL = Annotated[str, AfterValidator(lambda u: str(AnyHttpUrl(u)))]


def serialize_vendor(data: dict[str, Any], api_token: str) -> dict[str, Any]:
    token, username, password = data.get(api_token, None), data.get("username", None), data.get("password", None)
    if token and any([username, password]):
        raise ValueError(f"Cannot combine {api_token} with username and password.")
    [data.pop(_, None) for _ in ["username", "password", api_token] if not data.get(_, None)]
    return data


class BaseVendorAPI(BaseModel):
    """
    base Vendor API config
    """

    slug: str
    comment: str = ""
    isEnabled: bool = True
    vendor_id: Optional[str] = Field(None, alias="id")
    type: str
    respectSystemProxyConfiguration: bool = True

    @field_validator("slug")
    @classmethod
    def check_slug(cls, slug):
        return valid_slug(slug)

    @model_serializer
    def _ser_model(self, info: SerializationInfo) -> dict[str, Any]:
        _ = {self.model_fields[k].alias or k if info.by_alias else k: v for k, v in dict(self).items() if v is not None}
        return _

    def verify_connection(self, ipf: IPFClient) -> int:
        return raise_for_status(
            ipf.post(
                (
                    "/settings/vendor-api/verify-connection/reverify"
                    if self.vendor_id
                    else "/settings/vendor-api/verify-connection"
                ),
                json=self.model_dump(by_alias=True),
            )
        ).status_code


def check_input(x: BaseVendorAPI, attrs: list[str], token: list[str] = None):
    data, auth = [getattr(x, _) for _ in attrs], ([getattr(x, _) for _ in token] if token else [])
    if not x.vendor_id and token and any(data) and any(auth):
        raise ValueError(f"Cannot combine `{', '.join(attrs)}` with `{', '.join(token)}`.")
    elif not x.vendor_id and token and not (all(data) or all(auth)):
        raise ValueError(f"Required Fields: `{', '.join(attrs)}` or `{', '.join(token)}`.")
    elif not x.vendor_id and not all(data):
        raise ValueError(f"Required Fields: {', '.join(attrs)}")
    return x


class AssumeRole(BaseModel):
    role: str


class AWS(BaseVendorAPI):
    """
    AWS vendor api support
    """

    type: Literal["aws-ec2"] = "aws-ec2"
    apiKey: Optional[str] = None
    apiSecret: Optional[str] = None
    regions: list = Field(default_factory=list)
    assumeRoles: list[Union[str, dict, AssumeRole]] = Field(default_factory=list)

    maxCapacity: int = 50
    maxConcurrentRequests: int = 100000
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["apiKey", "apiSecret", "regions"])

    @field_validator("regions")
    @classmethod
    def check_region(cls, regions):
        for r in regions:
            if r.lower() not in AWS_REGIONS:
                raise ValueError(f"{r} is not a valid AWS Region")
        return [r.lower() for r in regions]

    @field_validator("assumeRoles")
    @classmethod
    def check_roles(cls, roles):
        validated_roles = list()
        for role in roles:
            if isinstance(role, str):
                validated_roles.append(AssumeRole(role=role))
            elif isinstance(role, dict):
                if "role" in role:
                    validated_roles.append(AssumeRole(**role))
                else:
                    raise SyntaxError(f'Role {role} not in \'{{"role": "<arn:aws:iam::*****:role/*****>"}}\' format.')
            elif isinstance(role, AssumeRole):
                validated_roles.append(role)
        return validated_roles


class Azure(BaseVendorAPI):
    """
    Azure vendor api support
    """

    type: Literal["azure"] = "azure"
    clientId: Optional[str] = None
    clientSecret: Optional[str] = None
    subscriptionIds: list[str] = Field(default_factory=list)
    tenantId: str

    maxConcurrentRequests: int = 1000
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["clientId", "clientSecret", "tenantId"])


class CheckPoint(BaseVendorAPI):
    domains: list[str] = Field(default_factory=list)
    type: Literal["checkpoint-mgmt-api"] = "checkpoint-mgmt-api"
    rejectUnauthorized: bool = True
    apiKey: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 1000
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"], ["apiKey"])

    @model_serializer
    def _ser_model(self, info: SerializationInfo) -> dict[str, Any]:
        return serialize_vendor(super()._ser_model(info), "apiKey")


class CiscoAPIC(BaseVendorAPI):
    """
    Cisco APIC vendor api support
    """

    type: Literal["ciscoapic"] = "ciscoapic"
    rejectUnauthorized: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 10
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"])


class CiscoFMC(BaseVendorAPI):
    type: Literal["ciscofmc"] = "ciscofmc"
    rejectUnauthorized: bool = True
    apiToken: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 9
    maxCapacity: int = 110
    refillRate: int = 110
    refillRateIntervalMs: int = 60000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"], ["apiToken"])

    @model_serializer
    def _ser_model(self, info: SerializationInfo) -> dict[str, Any]:
        return serialize_vendor(super()._ser_model(info), "apiToken")


class ForcePoint(BaseVendorAPI):
    """
    ForcePoint vendor api support
    """

    type: Literal["forcepoint"] = "forcepoint"
    rejectUnauthorized: bool = True
    authenticationKey: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 10
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["authenticationKey"])


class GCPCredentials(BaseModel):
    """
    GCP Credentials
    """

    auth_provider_x509_cert_url: str
    auth_uri: str
    client_email: str
    client_id: str
    client_x509_cert_url: str
    private_key: str
    private_key_id: str
    project_id: str
    token_uri: str
    type: str
    universe_domain: str


class GCP(BaseVendorAPI):
    """
    GCP vendor api support

    Args:
        credentialsJson: JSON File, Dictionary, or String of GCP Credentials
    """

    credentialsJson: Optional[Union[GCPCredentials, dict, str]] = None
    type: Literal["gcp"] = "gcp"

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["credentialsJson"])

    @field_validator("credentialsJson")
    @classmethod
    def validate_credentials(cls, credentials):
        if isinstance(credentials, dict):
            return GCPCredentials(**credentials)
        elif isinstance(credentials, str):
            try:
                with open(credentials, "r") as f:
                    return GCPCredentials(**json.load(f))
            except FileNotFoundError:
                try:
                    return GCPCredentials(**json.loads(credentials))
                except json.JSONDecodeError:
                    raise ValueError("credentialsJson must be a valid JSON file, JSON string or Python dictionary.")
        else:
            return credentials


class JuniperMist(BaseVendorAPI):
    """
    Juniper Mist vendor api support
    """

    type: Literal["juniper-mist"] = "juniper-mist"
    apiVer: Literal["v1"] = "v1"
    baseUrl: str = "https://api.mist.com"
    rejectUnauthorized: bool = True
    apiToken: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 250
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["apiToken"])


class Meraki(BaseVendorAPI):
    """
    Meraki v1 vendor api support
    """

    type: Literal["meraki"] = "meraki"
    organizations: list[str] = Field(default_factory=list)
    rejectUnauthorized: bool = True
    apiVer: Literal["v1"] = "v1"
    apiKey: Optional[str] = None
    baseUrl: URL

    maxCapacity: int = 10
    maxConcurrentRequests: int = 100000
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["apiKey"])


class Prisma(BaseVendorAPI):
    """
    Prisma vendor api support
    """

    type: Literal["prisma"] = "prisma"
    rejectUnauthorized: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    tsgid: Optional[str] = None

    maxConcurrentRequests: int = 4
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password", "tsgid"])


class RuckusVirtualSmartZone(BaseVendorAPI):
    """
    Ruckus Virtual SmartZone vendor api support
    """

    apiVersion: Literal["v9_1"] = "v9_1"
    type: Literal["ruckus-vsz"] = "ruckus-vsz"
    rejectUnauthorized: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 10
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"])


class SilverPeak(BaseVendorAPI):
    """
    SilverPeak vendor api support
    """

    type: Literal["silverpeak"] = "silverpeak"
    rejectUnauthorized: bool = True
    apiKey: Optional[str] = None
    loginType: Optional[Literal["Local", "RADIUS", "TACACS+"]] = None
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 5
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password", "loginType"], ["apiKey"])

    @model_serializer
    def _ser_model(self, info: SerializationInfo) -> dict[str, Any]:
        _ = serialize_vendor(super()._ser_model(info), "apiKey")
        if self.apiKey or not self.loginType:
            del _["loginType"]
        elif self.vendor_id and not self.loginType and not self.apiKey:
            raise ValueError("loginType must be specified with username and password.")
        return _


class VeloCloud(BaseVendorAPI):
    """
    VeloCloud vendor api support
    """

    type: Literal["velocloud"] = "velocloud"
    rejectUnauthorized: bool = True
    apiToken: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 1000
    maxCapacity: int = 1000
    refillRate: int = 1000
    refillRateIntervalMs: int = 5000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"], ["apiToken"])

    @model_serializer
    def _ser_model(self, info: SerializationInfo) -> dict[str, Any]:
        return serialize_vendor(super()._ser_model(info), "apiToken")


class Versa(BaseVendorAPI):
    """
    Versa vendor api support
    """

    type: Literal["versa"] = "versa"
    combinedDiscovery: bool = True
    rejectUnauthorized: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 10
    maxCapacity: int = 100
    refillRate: int = 2
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"])


class Viptela(BaseVendorAPI):
    """
    Viptela vendor api support
    """

    type: Literal["viptela"] = "viptela"
    combinedDiscovery: bool = True
    rejectUnauthorized: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 25
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"])


class NSXT(BaseVendorAPI):
    """
    NSXT vendor api support
    """

    type: Literal["nsxT"] = "nsxT"
    username: Optional[str] = None
    password: Optional[str] = None
    baseUrl: URL

    maxConcurrentRequests: int = 40
    maxCapacity: int = 100
    refillRate: int = 50
    refillRateIntervalMs: int = 1000
    rejectUnauthorized: bool = True

    @model_validator(mode="after")
    def _check_model(self):
        return check_input(self, ["username", "password"])


VENDOR_API = Annotated[
    Union[
        AWS,
        Azure,
        CheckPoint,
        CiscoAPIC,
        CiscoFMC,
        ForcePoint,
        GCP,
        JuniperMist,
        Meraki,
        Prisma,
        RuckusVirtualSmartZone,
        SilverPeak,
        VeloCloud,
        Versa,
        Viptela,
        NSXT,
    ],
    Field(discriminator="type"),
]

VENDOR_API_MODELS = (
    AWS,
    Azure,
    CheckPoint,
    CiscoAPIC,
    CiscoFMC,
    ForcePoint,
    GCP,
    JuniperMist,
    Meraki,
    Prisma,
    RuckusVirtualSmartZone,
    SilverPeak,
    VeloCloud,
    Versa,
    Viptela,
    NSXT,
)

TYPE_TO_MODEL = {c.model_fields["type"].default: c for c in VENDOR_API_MODELS}


class VendorAPIModel(RootModel):
    root: VENDOR_API

    def __getattr__(self, name: str) -> Any:
        return getattr(self.root, name)
