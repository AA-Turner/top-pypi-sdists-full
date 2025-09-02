from __future__ import annotations

import base64
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric.client import EXPORT_FORMAT

try:
    from pandas import DataFrame
except ImportError:
    DataFrame = None

import re
import logging
from datetime import timedelta, datetime
from ipfabric.settings.attributes import Attributes
from httpx import HTTPStatusError
from typing import Optional, Union, overload, Literal, Any
from ipaddress import IPv4Interface, IPv4Address, IPv6Address
from collections import defaultdict
from case_insensitive_dict import CaseInsensitiveDict
from ipfabric.models.technology import Technology
from ipfabric.tools.shared import create_filter, raise_for_status
from ipfabric.models.security import SecurityModel
from pytz import UTC

from pydantic import BaseModel, Field, PrivateAttr, field_validator, field_serializer

logger = logging.getLogger("ipfabric")


class DeviceConfig(BaseModel):
    status: str
    current: Optional[str] = Field(None, alias="currentConfig")
    start: Optional[str] = Field(None, alias="startupConfig")


class Device(BaseModel):
    client: Optional[Any] = Field(None, exclude=True)
    attributes: Optional[dict] = Field(default_factory=dict)
    global_attributes: Optional[dict] = Field(default_factory=dict)
    domain: Optional[str] = None
    family: Optional[str] = None
    fqdn: Optional[str] = None
    hostname: str
    image: Optional[str] = None
    model: Optional[str] = None
    platform: Optional[str] = None
    processor: Optional[str] = None
    reload: Optional[str] = None
    sn: str
    uptime: Optional[timedelta] = None
    vendor: str
    version: Optional[str] = None
    blob_key: Optional[str] = Field(None, alias="blobKey")
    config_reg: Optional[str] = Field(None, alias="configReg")
    dev_type: str = Field(None, alias="devType")
    stack: Optional[bool] = None
    hostname_original: Optional[str] = Field(None, alias="hostnameOriginal")
    hostname_processed: Optional[str] = Field(None, alias="hostnameProcessed")
    login_ip: Optional[IPv4Interface] = Field(None, alias="loginIp")  # TODO: 8.0 change to ipv4 or ipv6 property
    login_ipv4: Optional[IPv4Address] = Field(None, alias="loginIpv4")
    login_ipv6: Optional[IPv6Address] = Field(None, alias="loginIpv6")
    login_port: Optional[int] = Field(None, alias="loginPort")
    login_type: str = Field(None, alias="loginType")
    mem_total_bytes: Optional[float] = Field(None, alias="memoryTotalBytes")
    mem_used_bytes: Optional[float] = Field(None, alias="memoryUsedBytes")
    mem_utilization: Optional[float] = Field(None, alias="memoryUtilization")
    object_id: Optional[str] = Field(None, alias="objectId")
    routing_domain: Optional[int] = Field(None, alias="rd")
    site_name: str = Field(None, alias="siteName")
    sn_hw: str = Field(None, alias="snHw")
    stp_domain: Optional[int] = Field(None, alias="stpDomain")
    task_key: Optional[str] = Field(None, alias="taskKey")
    slug: Optional[str] = None
    ts_discovery_start: Optional[datetime] = Field(None, alias="tsDiscoveryStart")
    ts_discovery_end: Optional[datetime] = Field(None, alias="tsDiscoveryEnd")
    sec_discovery_duration: Optional[float] = Field(None, alias="secDiscoveryDuration")
    credentials_notes: Optional[str] = Field(None, alias="credentialsNotes")
    _filters: Optional[dict] = None
    _technology: Optional[Technology] = None

    def model_post_init(self, __context: Any) -> None:
        self._filters = {"sn": ["eq", self.sn]}

    @field_validator("ts_discovery_start", "ts_discovery_end")
    @classmethod
    def check_alphanumeric(cls, v: Union[int, datetime]) -> datetime:
        if isinstance(v, int):
            v = datetime.fromtimestamp(v / 1000, UTC)
        return v

    @field_serializer("login_ip", "login_ipv4", "login_ipv6")
    def serialize_login_ip(self, login_ip: IPv4Interface, _info):
        if isinstance(login_ip, IPv4Interface):
            return str(login_ip.ip)
        return str(login_ip) if login_ip else None

    def __repr__(self):
        return self.hostname

    def __str__(self):
        return self.hostname

    def __eq__(self, other):
        return self.sn == other.sn if isinstance(other, Device) else str(other)

    def __hash__(self):
        return hash(self.sn)

    @property
    def technology(self) -> Technology:
        if not hasattr(self, "_technology"):
            self._technology = Technology(client=self.client, sn=self.sn)
        return self._technology

    @property
    def site(self) -> str:
        return self.site_name

    @property
    def local_attributes(self) -> dict:
        return self.attributes

    @classmethod
    def check_attribute(cls, attribute) -> True:
        if attribute not in cls.model_fields:
            raise AttributeError(f"Attribute {attribute} not in Device class.")
        return True

    def get_log_file(self) -> str:
        return raise_for_status(self.client.get("/os/logs/task/" + self.task_key)).text

    def get_json(self, snapshot_id: str = None) -> dict:
        _ = snapshot_id if snapshot_id else self.client.snapshot_id
        encoded_sn = base64.urlsafe_b64encode(self.sn.encode("utf-8")).decode("utf-8").rstrip("=")
        return raise_for_status(self.client.get(f"/snapshots/{_}/devices/{encoded_sn}/json")).json()

    def get_security_model(self, snapshot_id: str = None) -> SecurityModel:
        _ = snapshot_id if snapshot_id else self.client.snapshot_id
        data = raise_for_status(self.client.get("security/", params=dict(sn=self.sn, snapshot=_))).json()
        return SecurityModel(**data)

    def get_config(self) -> Union[None, DeviceConfig]:
        if not self.blob_key:
            logger.warning("Device Config not in Snapshot File. Please try using ipfabric.tools.DeviceConfigs")
            return None
        res = raise_for_status(self.client.get("blobs/device-configuration/" + str(self.blob_key)))
        return DeviceConfig(**res.json())

    def interfaces(self) -> list:
        return self.fetch_all("tables/inventory/interfaces")

    def pn(self) -> list:
        return self.fetch_all("tables/inventory/pn")

    def switchport(self) -> list:
        return self.fetch_all("tables/interfaces/switchports")

    def managed_ip_ipv4(self) -> list:
        return self.fetch_all("tables/addressing/managed-devs")

    def managed_ip_ipv6(self) -> list:
        return self.fetch_all("tables/addressing/ipv6-managed-devs")

    def mac_table(self) -> list:
        return self.fetch_all("tables/addressing/mac")

    def arp_table(self) -> list:
        return self.fetch_all("tables/addressing/arp")

    def routes_ipv4(self) -> list:
        return self.fetch_all("tables/networks/routes")

    def routes_ipv6(self) -> list:
        return self.fetch_all("tables/networks/ipv6-routes")

    def neighbors_all(self) -> list:
        return self.fetch_all("tables/neighbors/all")

    def trigger_backup(self):
        return self.client.trigger_backup(sn=self.sn)

    @overload
    def fetch_all(
        self,
        url: str,
        export: Literal["csv"],
        columns: list[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
    ) -> list[dict]: ...

    @overload
    def fetch_all(
        self,
        url: str,
        export: Literal["csv"],
        columns: list[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        csv_tz: Optional[str] = None,
    ) -> bytes: ...

    @overload
    def fetch_all(
        self,
        url: str,
        export: Literal["df"],
        columns: list[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
    ) -> DataFrame: ...

    def fetch_all(
        self,
        url: str,
        export: EXPORT_FORMAT = "json",
        columns: list[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        csv_tz: Optional[str] = None,
    ):
        """Gets all data from IP Fabric for specified endpoint filtered on the `sn` of the device

        Args:
            url: Example tables/vlan/device-summary
            export: str: Export format to return [json, csv]; default is json.
            columns: Optional list of columns to return, None will return all
            filters: Optional dictionary of filters which will be merged with the sn filter
            snapshot_id: Optional snapshot_id to override default
            reports: String of frontend URL where the reports are displayed or a list of report IDs
            sort: Optional dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            csv_tz: str: Default None, set a timezone to return human-readable dates when using CSV;
                         see `ipfabric.tools.shared.TIMEZONES`
        Returns:
            Union[list[dict], bytes, pandas.DataFrame]: List of dict if json, bytes string if CSV, DataFrame is df
        """
        all_columns, f = create_filter(self.client, url, filters, self.sn)
        return self.client.fetch_all(
            url,
            filters=f,
            columns=columns or all_columns,
            export=export,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
            csv_tz=csv_tz,
        )


class DeviceDict(CaseInsensitiveDict):
    """CaseInsensitiveDict with functions to search or regex on dictionary keys."""

    def __init__(self, attribute, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute = attribute

    def __getitem__(self, key) -> Device:
        return super().__getitem__(key)

    @staticmethod
    def _new_dict(a):
        return DeviceDict[str, Device](attribute=a) if a == "sn" else DeviceDict[str, list[Device]](attribute=a)

    @overload
    def regex(self: DeviceDict[str, list[Device]], pattern: str, *flags: int) -> DeviceDict[str, list[Device]]: ...

    @overload
    def regex(self: DeviceDict[str, Device], pattern: str, *flags: int) -> DeviceDict[str, Device]: ...

    def regex(self, pattern: str, *flags: int) -> DeviceDict[str, Union[list[Device], Device]]:
        """
        Case-sensitive regex search on dictionary keys.
        Args:
            pattern: str: Regex string to search.
            *flags: int or re.RegexFlag: Regex flags to use.

        Returns:
            DeviceDict: New instance of DeviceDict (CaseInsensitiveDict)
        """
        regex = re.compile(pattern, flags=sum(flags))
        new_dict = self._new_dict(self.attribute)
        [new_dict.update({key: value}) for key, value in self._data.values() if key and regex.search(key)]
        return new_dict

    @overload
    def search(
        self: DeviceDict[str, list[Device]], pattern: Union[list[str], str]
    ) -> DeviceDict[str, list[Device]]: ...

    @overload
    def search(self: DeviceDict[str, Device], pattern: Union[list[str], str]) -> DeviceDict[str, Device]: ...

    def search(self, pattern: Union[list[str], str]) -> DeviceDict[str, Union[list[Device], Device]]:
        """
        Case-insensitive search on dictionary keys.
        Args:
            pattern: Union[list[str], str]: String or List of strings to match on.

        Returns:
            DeviceDict: New instance of DeviceDict (CaseInsensitiveDict)
        """
        pattern = [pattern.lower()] if isinstance(pattern, str) else [p.lower() for p in pattern]
        new_dict = self._new_dict(self.attribute)
        [new_dict.update({o_key: value}) for key, (o_key, value) in self._data.items() if key in pattern]
        return new_dict

    def _flatten_devs(self) -> list[Device]:
        devices = list()
        for value in self.values():
            if isinstance(value, list):
                devices.extend(value)
            else:
                devices.append(value)
        return devices

    def sub_search(self, attribute: str, pattern: Union[list[str], str]) -> DeviceDict[str, list[Device]]:
        """
        Case-insensitive sub search of another Device attribute.
        Args:
            attribute: str: Attribute of Device class.
            pattern: Union[list[str], str]: String or List of strings to match on.

        Returns:
             DeviceDict: New instance of DeviceDict (CaseInsensitiveDict) grouped by new attribute.
        """
        Device.check_attribute(attribute)
        return Devices.group_dev_by_attr(self._flatten_devs(), attribute).search(pattern)

    def sub_regex(self, attribute: str, pattern: Union[list[str], str], *flags: int) -> DeviceDict[str, list[Device]]:
        """
        Case-sensitive regex sub search of another Device attribute.
        Args:
            attribute: str: Attribute of Device class.
            pattern: str: Regex string to search.
            *flags: int or re.RegexFlag: Regex flags to use.

        Returns:
            DeviceDict: New instance of DeviceDict (CaseInsensitiveDict) grouped by new attribute.
        """
        Device.check_attribute(attribute)
        return Devices.group_dev_by_attr(self._flatten_devs(), attribute).regex(pattern, *flags)


class Devices(BaseModel):
    snapshot_id: str
    client: Any = Field(None, exclude=True)
    _attrs: Optional[defaultdict[str, set[str]]] = PrivateAttr()
    _global_attrs: Optional[defaultdict[str, set[str]]] = PrivateAttr()
    _all: list[Device] = PrivateAttr()

    def __init__(
        self,
        snapshot_id: str,
        client: Any,
        devices: Optional[list[dict]] = None,
        device_filters: Optional[dict] = None,
        device_attr_filters: Optional[dict] = None,
    ):
        super().__init__(snapshot_id=snapshot_id, client=client)
        self.update(devices, device_filters, device_attr_filters)

    def update(self, devices: list[dict] = None, device_filters: dict = None, device_attr_filters: dict = None):
        devices = devices if devices else self._load_devices(device_filters, device_attr_filters)
        if not devices:
            return None
        try:
            self._attrs, lcl_attr = self._parse_attrs(
                Attributes(client=self.client, snapshot_id=self.client.snapshot_id).all()
            )
        except HTTPStatusError:
            logger.warning(
                self.client._api_insuf_rights
                + 'on POST "/tables/snapshot-attributes". Cannot load Local (snapshot) Attributes in Devices.'
            )
            lcl_attr = dict()
        try:
            self._global_attrs, glb_attr = self._parse_attrs(Attributes(client=self.client).all())
        except HTTPStatusError:
            logger.warning(
                self.client._api_insuf_rights
                + 'on POST "/tables/global-attributes". Cannot load Global Attributes in Devices.'
            )
            glb_attr = dict()
        try:
            blob_keys = {
                b["sn"]: b["blobKey"]
                for b in self.client.fetch_all("/tables/management/configuration/saved", columns=["sn", "blobKey"])
            }
        except HTTPStatusError:
            logger.warning(
                self.client._api_insuf_rights + 'on POST "/tables/management/configuration/saved". '
                "You will not be able to pull device config from Device model."
            )
            blob_keys = dict()
        self._all = [
            Device(
                **d,
                attributes=lcl_attr.get(d["sn"], dict()),
                global_attributes=glb_attr.get(d["sn"], dict()),
                blobKey=blob_keys.get(d["sn"], None),
                client=self.client,
            )
            for d in devices
        ]

    def _load_devices(self, device_filters: dict = None, device_attr_filters: dict = None):
        if self.client._no_loaded_snapshots:
            logger.warning("No loaded snapshots, cannot load devices.")
            return list()
        if not device_attr_filters and self.client.attribute_filters:
            logger.warning(
                f"Global `attribute_filters` is set; only pulling devices matching:\n{self.client.attribute_filters}."
            )
        try:
            return self.client.inventory.devices.all(filters=device_filters, attr_filters=device_attr_filters)
        except HTTPStatusError:
            logger.warning(
                self.client._api_insuf_rights + 'on POST "/tables/inventory/devices". Will not load Devices.'
            )
        return list()

    @staticmethod
    def _parse_attrs(attributes: list[dict] = None):
        cls_attr, dev_attr = defaultdict(set), defaultdict(dict)
        for d in attributes or []:
            dev_attr[d["sn"]].update({d["name"]: d["value"]})
            cls_attr[d["name"]].add(d["value"])
        return cls_attr, dev_attr

    @property
    def all(self) -> list[Device]:
        """Returns list[Device]."""
        return self._all

    def _check_attr_name(self, name: str) -> bool:
        if self._attrs is None:
            logger.warning("Attributes were not loaded into devices.")
        elif name not in self._attrs:
            logger.warning(f'Attribute key "{name}" not found in snapshot "{self.snapshot_id}".')
        else:
            return True
        return False

    def _filter_attr(self, devs: set[Device], name: str, values: Union[list[str], str]) -> set[Device]:
        if not self._check_attr_name(name):
            return set()
        values = values if isinstance(values, list) else [values]
        for dev in devs.copy():
            dev_attr = dev.attributes.get(name, None)
            if not dev_attr or dev_attr not in values:
                devs.discard(dev)
        return devs

    def filter_by_attr(self, name: str, values: Union[list[str], str]) -> list[Device]:
        """
        Return list of devices with an attribute set to a value
        Args:
            name: str: Attribute name
            values: Union[list[str], str]: Single attribute value or list of values to match.
        Returns:
            list[Device]
        """
        return list(self._filter_attr(set(self.all.copy()), name, values))

    def filter_by_attrs(self, attr_filter: dict[str, Union[list[str], str]]) -> list[Device]:
        """
        Return list of devices matching multiple key/value attribute pairs
        Args:
            attr_filter: dict: {'ATTR_1': 'VALUE_1', 'ATTR_2': ['VALUE_2', 'VALUE_3']}
        Returns:
            list[Device]
        """
        devs = set(self.all.copy())
        for k, v in attr_filter.items():
            devs = self._filter_attr(devs, k, v)
        return list(devs)

    def has_attr(self, name: str) -> list[Device]:
        """
        Return list of devices that has an attribute set matching name.
        Args:
            name: str: Attribute name
        Returns:
            list[Device]
        """
        return [d for d in self.all if d.attributes.get(name, None)] if self._check_attr_name(name) else list()

    def does_not_have_attr(self, name: str) -> list[Device]:
        """
        Return list of devices that does not have an attribute set matching name.
        Args:
            name: str: Attribute name
        Returns:
            list[Device]
        """
        return [d for d in self.all if not d.attributes.get(name, None)] if self._check_attr_name(name) else list()

    def _group_dev_by_attr(self, attribute: str) -> DeviceDict[str, list[Device]]:
        return self.group_dev_by_attr(self._all, attribute)

    @classmethod
    def group_dev_by_attr(cls, devices: list[Device], attribute: str) -> DeviceDict[str, list[Device]]:
        devs = defaultdict(list)
        [devs[getattr(d, attribute)].append(d) for d in devices]
        return DeviceDict(attribute=attribute, data=devs)

    @property
    def by_sn(self) -> DeviceDict[str, Device]:
        """Returns Case-insensitive DeviceDict {'sn': Device}."""
        return DeviceDict(attribute="sn", data={d.sn: d for d in self._all})

    @property
    def by_hostname_original(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'hostname': [Device]}."""
        return self._group_dev_by_attr("hostname_original")

    @property
    def by_hostname(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'hostname': [Device]}."""
        return self._group_dev_by_attr("hostname")

    @property
    def by_sn_hw(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'sn_hw': [Device]}."""
        return self._group_dev_by_attr("sn_hw")

    @property
    def by_site(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'site': [Device]}."""
        return self._group_dev_by_attr("site")

    @property
    def by_vendor(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'vendor': [Device]}."""
        return self._group_dev_by_attr("vendor")

    @property
    def by_family(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'family': [Device]}."""
        return self._group_dev_by_attr("family")

    @property
    def by_platform(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'platform': [Device]}."""
        return self._group_dev_by_attr("platform")

    @property
    def by_model(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'model': [Device]}."""
        return self._group_dev_by_attr("model")

    @property
    def by_version(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        return self._group_dev_by_attr("version")

    @property
    def by_fqdn(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        return self._group_dev_by_attr("fqdn")

    @property
    def by_login_type(self) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        return self._group_dev_by_attr("login_type")

    def by_custom(self, attribute) -> DeviceDict[str, list[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        Device.check_attribute(attribute)
        return self._group_dev_by_attr(attribute)
