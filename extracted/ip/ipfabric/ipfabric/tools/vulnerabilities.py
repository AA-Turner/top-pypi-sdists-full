from collections import defaultdict
from copy import deepcopy
from typing import Optional

from httpx._types import ProxyTypes
from pydantic import BaseModel

from ipfabric.tools.nist import NIST, CVEs


class Version(BaseModel):
    vendor: str
    family: Optional[str] = None
    version: Optional[str] = None
    cves: list[CVEs]
    hostname: Optional[str] = None
    site: Optional[str] = None


class Vulnerabilities:
    def __init__(
        self, ipf, nvd_api_key: str, timeout: int = 60, proxies: Optional[ProxyTypes] = None, retries: int = 2
    ):
        """

        Args:
            ipf: IPFClient: IP Fabric client
            nvd_api_key: str: NVD API key
            timeout: Timeout value for requests
            proxies: Proxies for requests
            retries: int: Number of retries for requests, default 2
        """
        self.ipf = ipf
        self.nist = NIST(nvd_api_key=nvd_api_key, timeout=timeout, proxies=proxies, retries=retries)

    def __del__(self):
        try:
            self.nist.close()
        except AttributeError:
            return

    def _check_versions(self, versions) -> list[Version]:
        cves = list()
        for v in versions:
            cve = self.nist.check_cve(v["vendor"], v["family"], v["version"])
            cves.append(Version(vendor=v["vendor"], family=v["family"], version=v["version"], cves=cve))
        return cves

    def _check_devices(self, devices):
        versions = [
            {"vendor": v[0], "family": v[1], "version": v[2]}
            for v in {(d["vendor"], d["family"], d["version"]) for d in devices}
        ]
        cve_dict = defaultdict(dict)
        for c in self._check_versions(versions):
            if c.vendor not in cve_dict:
                cve_dict[c.vendor] = defaultdict(dict)
            cve_dict[c.vendor][c.family].update({c.version: c})
        cves = list()
        for d in devices:
            cve = deepcopy(cve_dict[d["vendor"]][d["family"]][d["version"]])
            cve.hostname = d["hostname"]
            cve.site = d["siteName"]
            cves.append(cve)
        return cves

    def check_versions(self, vendor=None) -> list[Version]:
        filters = {"vendor": ["like", vendor]} if vendor else None
        versions = self.ipf.fetch_all(
            "tables/inventory/os-version-consistency/platforms",
            columns=["vendor", "family", "version"],
            filters=filters,
        )
        return self._check_versions(versions)

    def check_device(self, device):
        devices = self.ipf.inventory.devices.all(
            columns=["hostname", "siteName", "vendor", "family", "version"],
            filters={"hostname": ["like", device]},
        )
        return self._check_devices(devices)

    def check_site(self, site):
        devices = self.ipf.inventory.devices.all(
            columns=["hostname", "siteName", "vendor", "family", "version"],
            filters={"siteName": ["like", site]},
        )
        return self._check_devices(devices)
