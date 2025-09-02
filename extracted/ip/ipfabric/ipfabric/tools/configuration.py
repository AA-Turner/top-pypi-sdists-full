import logging
from collections import defaultdict
from datetime import datetime
from ipaddress import IPv4Address, AddressValueError
from typing import Any, Union, Optional

from pydantic import BaseModel, Field

from ipfabric.tools.shared import date_parser, raise_for_status

logger = logging.getLogger("ipfabric")
DEFAULT_SNAPSHOT = "$last"
NAMED_SNAPSHOTS = [DEFAULT_SNAPSHOT, "$prev", "$first"]


def trigger_backup(ipf, sn: str = None, ip: str = None):
    if sn:
        payload = {"sn": sn}
    else:
        try:
            ip = str(IPv4Address(ip))
        except AddressValueError:
            raise ValueError(f"Invalid IP Address, CIDR is not allowed: {ip}")
        payload = {"ip": ip}
    return raise_for_status(ipf.post("/discovery/trigger-config-backup", json=payload)).status_code


class Config(BaseModel):
    config_id: str = Field(None, alias="id")
    sn: str
    hostname: str
    config_hash: str = Field(None, alias="hash")
    status: str
    last_change: datetime = Field(None, alias="lastChangeAt")
    last_check: datetime = Field(None, alias="lastCheckAt")
    text: Optional[str] = None

    def get_text_config(self, client: Any, sanitized: bool = True) -> str:
        """gets a device config
        Args:
            client: IPF Client
            sanitized: bool to determine to return sensitive data

        Returns:
            string containing config of a device
        """
        res = raise_for_status(
            client.get(
                "/tables/management/configuration/download",
                params=dict(hash=self.config_hash, sanitized=sanitized),
            )
        )
        self.text = res.text
        return res.text


class DeviceConfigs(BaseModel):
    client: Any = Field(exclude=True)

    def get_all_configurations(self, device: Optional[str] = None, sn: Optional[str] = None) -> Union[dict, None]:
        """Get all configurations in IP Fabric

        Args:
            device: Hostname (case insensitive) filter
            sn: Serial number of device
        Returns:
            results: dict: {sn: [Config, Config]}
        """
        if device or sn:
            filters = dict(sn=["eq", sn]) if sn else dict(hostname=["ieq", device])
            res = self.client.fetch_all(
                "tables/management/configuration",
                sort={"order": "desc", "column": "lastChangeAt"},
                columns=[
                    "id",
                    "sn",
                    "hostname",
                    "lastChangeAt",
                    "lastCheckAt",
                    "status",
                    "hash",
                ],
                filters=filters,
                snapshot=False,
            )
            if len(res) == 0:
                logger.warning(f"Could not find any configurations for device '{device}'.")
                return None
        else:
            res = self.client.fetch_all(
                "tables/management/configuration",
                sort={"order": "desc", "column": "lastChangeAt"},
                columns=[
                    "id",
                    "sn",
                    "hostname",
                    "lastChangeAt",
                    "lastCheckAt",
                    "status",
                    "hash",
                ],
                snapshot=False,
            )
        results = defaultdict(list)
        [results[cfg["sn"]].append(Config(**cfg)) for cfg in res]
        return results

    def _search_ip(self, ip: str, snapshot_id: str = None, log: bool = False) -> dict:
        res = self.client.fetch_all(
            "tables/addressing/managed-devs",
            columns=["ip", "hostname", "sn"],
            reports="/technology/addressing/managed-ip",
            filters=dict(ip=["eq", ip]),
        )
        if len(res) == 1 and not log:
            return {"hostname": res[0]["hostname"], "sn": res[0]["sn"]}
        if len(res) == 1 and log:
            res = self.client.inventory.devices.all(
                columns=["hostname", "taskKey", "sn"],
                snapshot_id=snapshot_id,
                filters=dict(sn=["eq", res[0]["sn"]]),
            )
            return {"hostname": res[0]["hostname"], "taskKey": res[0]["taskKey"], "sn": res[0]["sn"]}
        elif len(res) > 1:
            logger.warning(f"Found multiple entries for IP '{ip}'.")
        elif len(res) == 0:
            logger.warning(f"Could not find a matching IP for '{ip}'.")
        return {"hostname": None, "sn": None}

    def get_configuration(
        self, device: str = None, sn: str = None, sanitized: bool = True, date: Union[str, tuple] = DEFAULT_SNAPSHOT
    ) -> Union[Config, None]:
        """Gets last configuration of a device based on hostname or IP or IPF Unique Serial Number

        Args:
        device: Hostname or IP
        sn: Serial Number
        sanitized: Default True to mask passwords
        date: Defaults to latest config. Values in [$last, $prev, $first] or can be a
            tuple of a date range to get the latest snapshot in that range.
            Date can be string or int in seconds ("11/22/ 1:30", 1637629200)
        Returns:
            Returns a result or None
        """
        if not isinstance(date, tuple) and date not in NAMED_SNAPSHOTS:
            raise SyntaxError(f"Date must be in {NAMED_SNAPSHOTS} or tuple ('startDate', 'endDate')")
        if not sn:
            sn = self._validate_device(device)["sn"]
            if not sn:
                return None
        cfgs = self.get_all_configurations(sn=sn)
        if not cfgs:
            return None
        cfg = self._get_hash(cfgs[sn], date)
        if cfg:
            return self.get_text_config(cfg, sanitized)
        else:
            logger.error(f"Could not find a configuration with date {date}")
            return None

    def get_text_config(self, cfg: Config, sanitized: bool = True) -> Config:
        """gets a devices config
        Args:
            cfg: Config from get_configuration method
            sanitized: bool to determine to return sensitive data

        Returns:
            string containing config of a device
        """
        res = raise_for_status(
            self.client.get(
                "/tables/management/configuration/download",
                params=dict(hash=cfg.config_hash, sanitized=sanitized),
            )
        )
        cfg.text = res.text
        return cfg

    @staticmethod
    def _get_hash(configs, date):
        if isinstance(date, tuple):
            start = date_parser(date[0])
            end = date_parser(date[1])
            for cfg in configs:
                if start < cfg.last_change < end:
                    return cfg
        elif date == DEFAULT_SNAPSHOT:
            return configs[0]
        elif date == "$prev" and len(configs) > 1:
            return configs[1]
        elif date == "$first":
            return configs[-1]
        return None

    def _validate_device(self, device: str, snapshot_id: str = None, log: bool = False) -> dict:
        try:
            ip = IPv4Address(device)
            return self._search_ip(str(ip), snapshot_id=snapshot_id, log=log)
        except AddressValueError:
            res = self.client.inventory.devices.all(
                columns=["hostname", "taskKey", "sn"],
                filters=dict(hostname=["ieq", device]),
                snapshot_id=snapshot_id,
            )
            if len(res) == 1:
                return {"hostname": res[0]["hostname"], "taskKey": res[0]["taskKey"], "sn": res[0]["sn"]}
            elif len(res) == 0:
                logger.warning(f"Could not find a matching device for '{device}'")
            elif len(res) > 1:
                logger.warning(f"Found multiple devices matching '{device}'.")
        return {"hostname": None, "sn": None}

    def get_log(self, device: str, snapshot_id: str = None):
        device = self._validate_device(device, snapshot_id=snapshot_id, log=True)
        if not device["sn"]:
            return None
        return self.get_text_log(device)

    def get_text_log(self, device: dict):
        return raise_for_status(self.client.get("/os/logs/task/" + device["taskKey"])).text
