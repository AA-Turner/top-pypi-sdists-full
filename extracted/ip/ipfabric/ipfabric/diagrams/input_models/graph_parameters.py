from __future__ import annotations as _annotations

import os
import re
from ipaddress import IPv4Interface
from typing import Optional, Union, Any, Annotated

from pydantic import field_validator, BaseModel, Field, AliasChoices, model_serializer, StringConstraints
from pydantic.functional_validators import BeforeValidator, AfterValidator

from ipfabric.tools.shared import validate_ip_network_str, VALID_IP
from .constants import VALID_LAYOUTS

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")
PORT_REGEX = re.compile(r"^\d*$|^\d*-\d*$")
ALL_NETWORK = "$main"

IPv4 = Annotated[Union[str, VALID_IP], BeforeValidator(validate_ip_network_str)]


class Instance(BaseModel, extra=PYDANTIC_EXTRAS):
    rootId: str
    vlanId: int
    visible: bool = True
    grouped: bool = True


class STPInstances(BaseModel, extra=PYDANTIC_EXTRAS):
    isolate: bool = False
    instances: list[Instance] = Field(default_factory=list)


class Technologies(BaseModel, extra=PYDANTIC_EXTRAS):
    expandDeviceGroups: Optional[list[str]] = Field(default_factory=list)
    stpInstances: Optional[STPInstances] = Field(default_factory=STPInstances)


class ICMP(BaseModel, extra=PYDANTIC_EXTRAS):
    type: int
    code: int


class OtherOptions(BaseModel, extra=PYDANTIC_EXTRAS):
    applications: str = ".*"
    tracked: bool = False
    category: str = ""
    url: str = ""


class EntryPoint(BaseModel, extra=PYDANTIC_EXTRAS):
    sn: str = Field(title="Serial Number", description="IP Fabric Unique Device Serial Number API column sn")
    iface: str = Field(
        title="Interface", description="Interface to use as entry point. This is the intName not nameOriginal."
    )
    hostname: str = Field(title="Hostname", description="Hostname of the Device")


class Algorithm(BaseModel):
    """Default is automatic. Adding entryPoints will change to userDefined."""

    vrf: Optional[str] = None
    entryPoints: Optional[list[EntryPoint]] = None

    @property
    def type(self):
        return "userDefined" if self.entryPoints else "automatic"

    @model_serializer
    def _serialize_algorithm(self) -> dict[str, Any]:
        if self.entryPoints:
            return dict(type=self.type, entryPoints=[_.model_dump() for _ in self.entryPoints])
        else:
            return dict(type=self.type, vrf=self.vrf) if self.vrf else dict(type=self.type)


class PathLookup(BaseModel, extra=PYDANTIC_EXTRAS):
    protocol: Annotated[str, AfterValidator(lambda s: s.lower()), StringConstraints(pattern=r"tcp|udp|icmp")] = Field(
        "tcp", title="Protocol", description="Valid protocols are tcp, udp, or icmp."
    )
    srcPorts: Union[str, int] = Field(
        "1024-65535",
        title="Source Ports",
        description="Source ports if protocol is tcp or udp. "
        "Can be comma separated, a range using -, or any combination.",
    )
    dstPorts: Union[str, int] = Field(
        "80,443",
        title="Destination Ports",
        description="Destination ports if protocol is tcp or udp. "
        "Can be comma separated, a range using -, or any combination.",
    )
    tcpFlags: list[
        Annotated[str, AfterValidator(lambda s: s.lower()), StringConstraints(pattern=r"ack|fin|psh|rst|syn|urg")]
    ] = Field(
        default_factory=list,
        title="TCP Flags",
        description="Optional additional flags if protocol = TCP. "
        "Valid flags are ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']",
        validation_alias=AliasChoices("tcpFlags", "flags"),
    )
    icmp: ICMP = Field(
        ICMP(type=0, code=0),
        title="ICMP Packet",
        description="Default is Echo Reply (type=0, code=0). You can pass in an ICMP model from ipfabric.diagrams.icmp "
        "or specify your own values like {'type': 1, 'code': 2}.",
    )
    ttl: int = Field(128, title="Time To Live", description="TTL value, default is 128.")
    fragmentOffset: int = Field(0, title="Fragment Offset", description="Fragment Offset value, default is 0.")
    securedPath: bool = True
    enableRegions: bool = False
    srcRegions: str = ".*"
    dstRegions: str = ".*"
    otherOptions: OtherOptions = Field(default_factory=OtherOptions)
    firstHopAlgorithm: Algorithm = Field(default_factory=Algorithm)

    @field_validator("srcPorts", "dstPorts")
    @classmethod
    def _check_ports(cls, v):
        ports = str(v).replace(" ", "").split(",")
        for p in ports:
            if not PORT_REGEX.match(p):
                raise ValueError(
                    f'Ports "{v}" is not in the valid syntax, examples: ["80", "80,443", "0-1024", "80,8000-8100,8443"]'
                )
            if "-" in p:
                pn = p.split("-")
                if int(pn[0]) >= int(pn[1]):
                    raise ValueError(f'Ports "{p}" is invalid. {pn[0]} must be smaller than {pn[1]}.')
        return str(",".join(ports))

    @property
    def l4_options(self) -> dict[str, Any]:
        if self.protocol == "icmp":
            return dict(type=self.icmp.type, code=self.icmp.code)
        elif self.protocol == "udp":
            return dict(srcPorts=self.srcPorts, dstPorts=self.dstPorts)
        else:
            return dict(srcPorts=self.srcPorts, dstPorts=self.dstPorts, flags=self.tcpFlags)

    @model_serializer
    def _serializer(self) -> dict[str, Any]:
        return dict(
            type="pathLookup",
            groupBy="siteName",
            protocol=self.protocol,
            ttl=self.ttl,
            fragmentOffset=self.fragmentOffset,
            securedPath=self.securedPath,
            enableRegions=self.enableRegions,
            srcRegions=self.srcRegions,
            dstRegions=self.dstRegions,
            l4Options=self.l4_options,
            otherOptions=vars(self.otherOptions),
            firstHopAlgorithm=self.firstHopAlgorithm.model_dump(),
        )


class Multicast(PathLookup, BaseModel, extra=PYDANTIC_EXTRAS):
    group: IPv4
    source: IPv4
    receiver: Optional[IPv4] = None

    @field_validator("group")
    @classmethod
    def _valid_group(cls, v):
        ip = IPv4Interface(v)
        if not ip.network.is_multicast:
            raise ValueError(f'Group IP "{v}" is not a valid Multicast Address.')
        return v

    @model_serializer
    def _serializer(self) -> dict[str, Any]:
        parameters = super()._serializer()
        if self.receiver:
            parameters["receiver"] = str(self.receiver)
        return dict(
            pathLookupType="multicast",
            group=str(self.group),
            source=str(self.source),
            **parameters,
        )


class Unicast(PathLookup, BaseModel, extra=PYDANTIC_EXTRAS):
    startingPoint: IPv4 = Field(title="Source IP Address or Subnet")
    destinationPoint: IPv4 = Field(title="Destination IP Address or Subnet")

    @model_serializer
    def _serializer(self) -> dict[str, Any]:
        parameters = super()._serializer()
        return dict(
            pathLookupType="unicast",
            networkMode=self._check_subnets(),
            startingPoint=self.startingPoint,
            destinationPoint=self.destinationPoint,
            **parameters,
        )

    def _check_subnets(self) -> bool:
        """Checks for valid IP Addresses or Subnet.

        :return: True if a subnet is found to set to networkMode, False if only hosts
        """
        masks = {IPv4Interface(ip).network.prefixlen for ip in [self.startingPoint, self.destinationPoint]}
        return True if masks != {32} else False

    @property
    def swap_src_dst(self) -> Unicast:
        return self.model_copy(
            update={
                "startingPoint": self.destinationPoint,
                "destinationPoint": self.startingPoint,
                "srcPorts": self.dstPorts,
                "dstPorts": self.srcPorts,
                "srcRegions": self.dstRegions,
                "dstRegions": self.srcRegions,
            }
        )


class Host2GW(BaseModel, extra=PYDANTIC_EXTRAS):
    startingPoint: IPv4
    vrf: Optional[str] = None

    @model_serializer
    def _serializer(self) -> dict[str, Any]:
        parameters = dict(
            pathLookupType="hostToDefaultGW",
            type="pathLookup",
            groupBy="siteName",
            startingPoint=self.startingPoint,
        )
        if self.vrf:
            parameters["vrf"] = self.vrf
        return parameters


class Layout(BaseModel, extra=PYDANTIC_EXTRAS):
    path: str
    layout: str

    @field_validator("layout")
    @classmethod
    def _valid_layout(cls, v):
        if v and v not in VALID_LAYOUTS:
            raise ValueError(f'Layout "{v}" is not in the valid layouts of {VALID_LAYOUTS}')
        return v


class Network(BaseModel, extra=PYDANTIC_EXTRAS):
    sites: Optional[Union[str, list[str]]] = Field(default_factory=list)
    all_network: bool = Field(True, description="Show all sites as clouds, UI option 'All Network'")
    layouts: Optional[list[Layout]] = None
    technologies: Optional[Technologies] = None

    @field_validator("sites")
    @classmethod
    def _format_paths(cls, v):
        if isinstance(v, str):
            return [v]
        return v

    @model_serializer
    def _serializer(self) -> dict[str, Any]:
        parameters = dict(type="topology", groupBy="siteName", paths=self.sites.copy())
        if self.all_network and ALL_NETWORK not in parameters["paths"]:
            parameters["paths"].append(ALL_NETWORK)
        if self.layouts:
            parameters["layouts"] = [_.model_dump() for _ in self.layouts]
        if self.technologies:
            parameters["technologies"] = self.technologies.model_dump()
        return parameters
