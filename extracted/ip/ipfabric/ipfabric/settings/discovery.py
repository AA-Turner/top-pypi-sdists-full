import logging
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_serializer

from ipfabric.models.discovery import (
    Community,
    Networks,
    CliRetryLimit,
    CliSessionsLimit,
    SeedList,
    DiscoveryHistorySeeds,
    DiscoveryTask,
    BGPLimit,
    LimitDiscoveryTasks,
    ManualLink,
    ResolveNames,
    Scanner,
    Timeouts,
    Traceroute,
    Ports,
)
from ipfabric.models.site_separation import SiteSeparation
from ipfabric.settings.authentication import Authentication
from ipfabric.settings.vendor_api import VendorAPI
from ipfabric.tools.shared import raise_for_status

logger = logging.getLogger("ipfabric")


class Discovery(BaseModel):
    client: Any = Field(exclude=True)
    snapshot_id: Optional[str] = Field(None, exclude=True)
    allowTelnet: bool
    authentication: Authentication
    bgps: list[Community] = Field(default_factory=list)
    cliRetryLimit: CliRetryLimit
    cliSessionsLimit: CliSessionsLimit
    disabledPostDiscoveryActions: list[Literal["graphCache", "historicalData", "intentVerification"]] = Field(
        default_factory=list,
    )
    discoveryHistorySeeds: DiscoveryHistorySeeds
    discoveryTasks: list[DiscoveryTask] = Field(default_factory=list)
    fullBgpIpv6Limit: BGPLimit
    fullBgpLimit: BGPLimit
    limitDiscoveryTasks: LimitDiscoveryTasks
    manualLinks: list[ManualLink] = Field(default_factory=list)
    networks: Networks
    ports: list[Ports] = Field(default_factory=list)
    resolveNames: ResolveNames
    scanner: Scanner
    seedList: list[str] = Field(default_factory=list)
    siteSeparation: SiteSeparation
    timeouts: Timeouts
    traceroute: Traceroute
    vendorApi: VendorAPI

    @property
    def _endpoint(self) -> str:
        return f"snapshots/{self.snapshot_id}/settings" if self.snapshot_id else "settings"

    @field_validator("seedList")
    @classmethod
    def _verify_seed_list(cls, v: list[str]) -> list[str]:
        return SeedList(seeds=v).model_dump()

    @model_serializer
    def _ser_model(self) -> dict[str, Any]:
        ser = dict()
        for k, v in self.model_fields.items():
            if v.exclude:
                continue
            if k == "authentication":
                ser.update(self.authentication.model_dump(by_alias=True))
            elif k in ["allowTelnet", "disabledPostDiscoveryActions", "seedList"]:
                ser.update({k: getattr(self, k)})
            elif k in ["bgps", "discoveryTasks", "ports", "manualLinks"]:
                ser.update({k: [_.model_dump(by_alias=True) for _ in getattr(self, k)]})
            else:
                ser.update({k: getattr(self, k).model_dump(by_alias=True)})
        return ser

    def update_discovery_networks(self, subnets: list, include: bool = False):
        payload = dict()
        payload["networks"] = dict()
        if include:
            payload["networks"]["include"] = subnets
            payload["networks"]["exclude"] = self.networks.exclude
        else:
            payload["networks"]["exclude"] = subnets
            payload["networks"]["include"] = self.networks.include
        res = raise_for_status(self.client.patch(self._endpoint, json=payload))
        return Networks(**res.json()["networks"])
