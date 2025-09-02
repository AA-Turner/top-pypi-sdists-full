import logging
from copy import deepcopy
from typing import Optional

from pydantic.dataclasses import dataclass

from ipfabric.settings.attributes import Attributes
from ipfabric.settings.site_separation import SiteSeparation

logger = logging.getLogger("ipfabric")


@dataclass
class Matches:
    hostname: str
    sn: str
    old_site_name: str
    rule_type: str
    slug: Optional[str] = None
    cloud_resource_id: Optional[str] = None
    new_site_name: Optional[str] = None
    rule_number: Optional[int] = None
    rule_note: Optional[str] = None
    regex: Optional[str] = None
    transformation: Optional[str] = None


def check_attributes(ipf, devices):
    matches = list()
    attributes = {a["sn"]: a for a in Attributes(client=ipf).all(filters={"name": ["eq", "siteName"]})}
    for sn, dev in deepcopy(devices).items():
        if sn in attributes:
            matches.append(
                Matches(
                    hostname=dev["hostname"],
                    sn=sn,
                    slug=dev["slug"],
                    old_site_name=attributes[sn]["value"],
                    rule_type="attributes",
                    rule_number=-1,
                )
            )
            devices.pop(sn)
    return matches


def _create_device_match(rule, device, idx):
    transformation = rule["transformation"] if rule["transformation"] != "none" else None
    return Matches(
        hostname=device["hostname"],
        slug=device["slug"],
        cloud_resource_id=device["resourceId"],
        old_site_name=device["sn"],
        sn=device["sn"],
        new_site_name=rule["siteName"],
        rule_type=rule["type"],
        rule_number=idx,
        rule_note=rule["note"],
        regex=rule.get("regex", None),
        transformation=transformation,
    )


def _get_cloud_inventory(ipf) -> dict:
    cloud = dict()
    for k, v in {"aws": "arn", "azure": "resourceId", "gcp": "resourceName"}.items():
        columns = {"sn"}
        columns.add(v)
        cloud.update(
            {_["sn"]: _[v] for _ in ipf.fetch_all(f"tables/cloud/vendors/{k}/inventory", columns=list(columns))}
        )
    return cloud


def map_devices_to_rules(ipf, snapshot_id: str = "$last"):  # NOSONAR
    ss = SiteSeparation(client=ipf)
    devices = {
        d["sn"]: d
        for d in ipf.inventory.devices.all(
            columns=["hostname", "sn", "siteName", "slug", "vendor"], snapshot_id=snapshot_id
        )
    }
    cloud = _get_cloud_inventory(ipf)
    {devices[_].update({"resourceId": cloud.get(_, None)}) for _ in devices}
    rules = ss.get_separation_rules()

    matches = check_attributes(ipf, devices) if rules["manualEnabled"] else list()

    for idx, rule in enumerate(rules["rules"]):
        if rule["type"] != "slug":
            data = ss.get_rule_matches(rule)
            for match in data["matched"]:
                if match["sn"] in devices:
                    matches.append(_create_device_match(rule, devices[match["sn"]], idx))
                    devices.pop(match["sn"], None)
        else:
            for device in devices.copy().values():
                if device["vendor"] in rule["enabledVendors"]:
                    # TODO: Include also cloud devices discovered via SSH or Vendor API
                    rule["siteName"] = device["siteName"]
                    matches.append(_create_device_match(rule, device, idx))
                    devices.pop(device["sn"], None)

    for sn, dev in devices.items():
        matches.append(
            Matches(
                hostname=dev["hostname"],
                sn=sn,
                slug=dev["slug"],
                cloud_resource_id=dev["resourceId"],
                old_site_name=dev["siteName"],
                rule_type="noMatchingRule",
            )
        )
    return [vars(m) for m in matches]
