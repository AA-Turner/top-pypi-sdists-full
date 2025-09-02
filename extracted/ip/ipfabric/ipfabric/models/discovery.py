from typing import Any, Optional, Literal, Annotated

from pydantic import BaseModel, Field, field_validator, model_validator, model_serializer, AfterValidator

from ipfabric.tools.shared import validate_ip_network_str


def valid_networks(v: list[str]) -> list[str]:
    return [validate_ip_network_str(_, ipv6=True) for _ in v]


VALID_NETWORKS = Annotated[list[str], AfterValidator(valid_networks)]


class BaseSetting(BaseModel):
    @model_serializer
    def _ser_model(self) -> dict[str, Any]:
        if not (_ := {v.alias or k: getattr(self, k) for k, v in self.model_fields.items()})["id"]:
            del _["id"]
        return _


class BaseEnableSetting(BaseModel):
    enabled: bool

    @model_serializer
    def _ser_model(self) -> dict:
        return dict(self) if self.enabled else {"enabled": self.enabled}


class Community(BaseSetting, BaseModel):
    communityList: list[str]
    isVrfStd: bool
    protocol: Literal["IPv4", "IPv6"]
    sn: str
    vrf: Optional[str] = None
    community_id: Optional[str] = Field(None, alias="id")

    @model_validator(mode="after")
    def _verify_vrf(self):
        if self.vrf and self.isVrfStd:
            raise ValueError("Cannot provide both custom VRF and set `isVrfStd` to True.")
        if not self.vrf and not self.isVrfStd:
            raise ValueError("You must provide a custom VRF or set `isVrfStd` to True.")
        return self


class ManualLink(BaseSetting, BaseModel):
    dstDeviceSn: str
    dstInterface: str
    type: Literal["L1", "L2"]
    srcDeviceSn: str
    srcInterface: str
    link_id: Optional[str] = Field(None, alias="id")


class Networks(BaseModel):
    exclude: VALID_NETWORKS = Field(default_factory=list)
    include: VALID_NETWORKS = Field(default_factory=list)
    whitelist: VALID_NETWORKS = Field(default_factory=list)

    @model_validator(mode="after")
    def _verify_include_not_empty(self):
        if not self.include:
            raise ValueError("Discovery Settings Network Include list cannot be empty.")
        return self


class SeedList(BaseModel):
    seeds: list[str] = Field(default_factory=list)

    @field_validator("seeds")
    @classmethod
    def _verify_valid_networks(cls, v: list[str]) -> list[str]:
        return [validate_ip_network_str(_, max_size=24, max_v6_size=119, ipv6=True) for _ in v]

    @model_serializer
    def _ser_model(self) -> list[str]:
        return self.seeds


class Tacacs(BaseModel):
    retry: int
    delay: int


class CliRetryLimit(BaseModel):
    authFail: int
    default: int
    tacacs: Tacacs


class CliSessionsLimit(BaseEnableSetting, BaseModel):
    limit: int


class DiscoveryTask(BaseSetting, BaseModel):
    disabled_task_id: Optional[str] = Field(None, alias="id")
    vendor: Optional[str] = None
    family: Optional[str] = None
    platform: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None
    sn: Optional[str] = None
    taskId: str


class BGPLimit(BaseModel):
    enabled: bool
    threshold: int


class LimitDiscoveryTasks(BaseModel):
    alreadyDiscovered: bool
    sourceOfTasks: list[Literal["aciEndpoint", "arp", "routes", "trace", "xdp"]]


class ResolveNames(BaseModel):
    discoveryDevices: bool


class Scanner(BaseEnableSetting, BaseModel):
    shortestMask: int

    @field_validator("shortestMask")
    @classmethod
    def _verify_shortest_mask(cls, v: int) -> int:
        if v > 32 or v < 16:
            raise ValueError("Shortest mask must be number from 16 to 32.")
        return v


class Timeouts(BaseModel):
    authentication: int
    command: int
    login: int
    session: int


class Traceroute(BaseModel):
    port: Optional[int] = None
    protocol: Literal["tcp", "udp", "icmp"]
    scope: VALID_NETWORKS

    @model_validator(mode="after")
    def _verify_port(self):
        if self.protocol == "icmp" and self.port:
            self.port = None
        elif self.protocol != "icmp" and not self.port:
            raise ValueError("Port must be provided if protocol is not icmp.")
        return self


class Ports(BaseModel):
    excludeSubnets: VALID_NETWORKS = Field(default_factory=list)
    subnets: VALID_NETWORKS = Field(default_factory=list)
    label: str = ""
    protocol: Literal["ssh", "telnet"]
    port: int

    @model_validator(mode="after")
    def _verify_subnets_not_empty(self):
        if not self.subnets:
            raise ValueError("Custom Port Network Include list cannot be empty.")
        return self


class DiscoveryHistorySeeds(BaseModel):
    afterDate: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    daysLimit: Optional[int] = Field(None, ge=0, le=365)
    enabled: bool = False

    @model_validator(mode="after")
    def _verify_limit(self):
        if not self.enabled and self.afterDate and self.daysLimit:
            raise ValueError("Either daysLimit or afterDate must be defined, but not both.")
        return self
