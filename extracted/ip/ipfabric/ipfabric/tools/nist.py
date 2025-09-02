from time import sleep
from typing import Optional, Union

from httpx import Client, ReadTimeout, HTTPStatusError
from pydantic import BaseModel, ConfigDict, field_validator

from ipfabric.tools.shared import ProxyTypes, TimeoutTypes

UNSUPPORTED_VENDORS = [
    "azure",
    "aws",
    "gcp",
    "brocade",
    "dell",
    "extreme",  # TODO: Verify
    "fs",
    "huawei",
    "nokia",
    "riverbed",
    "ruckus",
]
UNSUPPORTED_FAMILIES = [
    "meraki",
    "mist",
    "encs",
    "sg",
    "viptela",
    "lap",
    "prisma",
    "comware",
    "comware-lap",
    "3com",
    "velocloud",
]


class CveMetricV2(BaseModel):
    model_config = ConfigDict(extra="ignore")
    version: str
    accessVector: str
    accessComplexity: str
    confidentialityImpact: str
    integrityImpact: str
    availabilityImpact: str
    baseScore: float
    baseSeverity: str
    exploitabilityScore: float
    impactScore: float
    acInsufInfo: bool
    obtainAllPrivilege: bool
    obtainUserPrivilege: bool
    obtainOtherPrivilege: bool
    userInteractionRequired: Optional[bool] = None


class CveMetricV3(BaseModel):
    model_config = ConfigDict(extra="ignore")
    version: str
    attackVector: str
    attackComplexity: str
    privilegesRequired: str
    userInteraction: str
    scope: str
    confidentialityImpact: str
    integrityImpact: str
    availabilityImpact: str
    baseScore: float
    baseSeverity: str
    exploitabilityScore: float
    impactScore: float


class CPE(BaseModel):
    cpeName: str
    cpeNameId: str
    deprecated: bool
    created: str
    lastModified: str
    error: Optional[str] = None


class CVE(BaseModel):
    cve_id: str
    description: str
    url: str
    metric_v2: Optional[Union[CveMetricV2, dict]] = None
    metric_v3: Optional[Union[CveMetricV3, dict]] = None

    @field_validator("metric_v3")
    @classmethod
    def create_metric_v3(cls, metric: Union[dict, CveMetricV3]) -> Union[None, CveMetricV3]:
        if isinstance(metric, CveMetricV3):
            return metric
        elif not metric:
            return None
        metrics = sorted([_ for _ in metric.keys() if "cvssMetricV3" in _], reverse=True)
        if not metrics:
            return None
        return CveMetricV3(**metric[metrics[0]][0], **metric[metrics[0]][0]["cvssData"])

    @field_validator("metric_v2")
    @classmethod
    def create_metric_v2(cls, metric: Union[dict, CveMetricV2]) -> Union[None, CveMetricV2]:
        if isinstance(metric, CveMetricV2):
            return metric
        elif not metric:
            return None
        metrics = sorted([_ for _ in metric.keys() if "cvssMetricV2" in _], reverse=True)
        if not metrics:
            return None
        return CveMetricV2(**metric[metrics[0]][0], **metric[metrics[0]][0]["cvssData"])

    @property
    def base_score(self) -> Union[float, None]:
        if self.metric_v3:
            return self.metric_v3.baseScore
        elif self.metric_v2:
            return self.metric_v2.baseScore
        return None

    def __repr__(self):
        return self.cve_id

    def __hash__(self):
        return hash(self.cve_id)


class CVEs(BaseModel):
    cpe: Optional[CPE] = None
    total_results: int
    cves: list[CVE]
    error: Optional[str] = None


class NIST(Client):
    def __init__(
        self, nvd_api_key: str, timeout: TimeoutTypes = 60, proxies: Optional[ProxyTypes] = None, retries: int = 2
    ):
        """
        NIST updated to API v2.0.  You must request and pass an API Key which can be obtained at
        https://nvd.nist.gov/developers/request-an-api-key

        Args:
            nvd_api_key: str: https://nvd.nist.gov/developers/request-an-api-key
            timeout: Timeout value for requests
            proxies: Proxies for requests
            retries: int: Number of retries for requests, default 2
        """
        super().__init__(
            base_url="https://services.nvd.nist.gov/rest/json/",
            timeout=timeout,
            headers={"apiKey": nvd_api_key},
            proxy=proxies,
        )
        self.retries = retries

    def _check_cisco(self, family, version):
        safe_version = version.replace("(", "\\(").replace(")", "\\)")
        family_map = {
            "viptela": f"cisco:sd-wan:{safe_version}",
            # "asa": f"cisco:asa:{version.replace('(', '.').replace(')', '.')}",  # Not Supported requires Model
            "ftd": f"cisco:firepower_threat_defense:{version.split(' ')[0]}",
            "wlc-air": f"cisco:wireless_lan_controller_software:{version}",
            "apic": f"cisco:application_policy_infrastructure_controller:{safe_version}",
            "nx-os": f"cisco:nx-os:{safe_version}",
            "aci": f"cisco:nx-os:{safe_version}",
            "ios-xe": f"cisco:ios_xe:{self._normalize_ios_version(version, family, safe_version)}",
            "ios-xr": f"cisco:ios_xr:{safe_version}",
            "ios": f"cisco:ios:{self._normalize_ios_version(version, family, safe_version)}",
        }
        return family_map.get(family, False)

    @staticmethod
    def _normalize_ios_version(version, family, safe_version):
        if family == "ios-xe":
            parts = [part.lstrip("0") for part in version.split(".")]
            if "" in parts:
                parts.remove("")
            return ".".join(parts[:-1]) + parts[-1] if parts[-1].isalpha() else ".".join(parts)
        elif family == "ios" and ("CML" in version or len(version.split(":")) > 1):
            return version.split("(")[0]
        elif family == "ios" and version.count("(") == 2:
            _ = safe_version.find("\\(", safe_version.find(")"))
            return safe_version[:_] + version.split("(")[-1].rstrip(")")
        return safe_version

    @staticmethod
    def _check_hp(family, version):
        if family in ["arubacx", "arubasw"]:  # Verified
            _ = version.split(".", maxsplit=1)
            version = version if len(_) < 2 else _[1]
            family = "arubaos-cx" if family == "arubacx" else "arubaos-switch"
            return "hpe:" + family + ":" + version
        elif family == "aruba":  # Verified
            return "arubanetworks:arubaos:" + version
        elif family in ["aruba-iap", "aruba-lap"]:  # Verified
            return "arubanetworks:instant:" + version
        return False

    @staticmethod
    def _check_juniper(family, version):
        if "R" in version:
            _ = version.split("R")
            version = _[0] + ":r" + _[1].split(".")[0]
        elif "-D" in version:
            _ = version.split("-D")
            version = _[0] + ":d" + _[1].split(".")[0]
        return "juniper:" + family + ":" + version

    @staticmethod
    def _trim_version(version: str, max_len: int = 3) -> str:
        parts = version.split(".")
        return ".".join(parts[:max_len]) if len(parts) > max_len else version

    def get_cpe(self, vendor: str, family: str, version: str) -> list[CPE]:  # noqa: C901
        """returns CVE data about a specific product line

        Args:
        vendor: Vendor for the device to be checked
        family: Family of the device to be checked
        version: Software version of the device to be checked
        Returns:
            a list of CVEs
        """
        match_str = "cpe:2.3:*:"
        unsupported = [
            CPE(cpeName="", cpeNameId="", deprecated=False, created="", lastModified="", error="Unsupported")
        ]
        if vendor in UNSUPPORTED_VENDORS or family in UNSUPPORTED_FAMILIES:
            return unsupported

        vendor_family_map = {
            "pan-os": f"paloaltonetworks:pan-os:{':'.join(version.split('-'))}",
            "alcatel": f"alcatel:{family}:{version.split('.R')[0]}",
            "adc": f"citrix:application_delivery_controller:{version}",
            "big-ip": f"f5:big-ip_local_traffic_manager:{version}",
            "fortigate": f"fortinet:fortios:{version.split(',')[0]}",
            "fortiswitch": f"fortinet:fortiswitch:{version.split(',')[0]}",
            "forcepoint": f"forcepoint:next_generation_firewall:{self._trim_version(version, 3)}",
            "frr": f"frrouting:frrouting:{version}",
            "checkpoint": f"checkpoint:gaia_os:{version}",
            "mikrotik": f"mikrotik:{family}:{version}",
            "opengear": f"opengear:opengear:{version}",
            "quagga": f"quagga:quagga:{version}",
            "arista": f"arista:{family}:{version.split('-')[0]}",
            "versa": f"versa-networks:versa_operating_system:{version.split('-')[0]}",
            "silverpeak": f"arubanetworks:edgeconnect_enterprise:{version.split('_')[0]}",
            "stormshield": f"stormshield:stormshield_network_security:{version}",
            "nsx-t": f"vmware:nsx-t_data_center:{self._trim_version(version, 5)}",
        }

        if vendor in ["cisco", "hp"]:
            _ = self._check_cisco(family, version) if vendor == "cisco" else self._check_hp(family, version)
            if not _:
                return unsupported
            match_str += _
        elif vendor == "juniper":
            match_str += self._check_juniper(family, version)
        elif vendor in vendor_family_map:
            match_str += vendor_family_map[vendor]
        elif family in vendor_family_map:
            match_str += vendor_family_map[family]
        else:
            return unsupported
        return self._query_cpe({"cpeMatchString": match_str + ":", "startIndex": 0})

    def check_cve(self, vendor: str, family: str, version: str) -> list[CVEs]:
        cpes = self.get_cpe(vendor, family, version)
        if not cpes:
            return [CVEs(total_results=0, cves=[], error="No CPEs Found.")]
        cves = list()
        for cpe in cpes:
            if cpe.error:
                cves.append(CVEs(total_results=0, cves=[], error=cpe.error, cpe=cpe))
            else:
                cves.append(self._query_cve(cpe))
        return cves

    def _query_cve(self, cpe: CPE, attempt: int = 0) -> CVEs:
        try:
            sleep(0.3 + attempt)  # NIST Rate Limit: 50 requests/30 seconds
            res = self.get("cves/2.0", params={"cpeName": cpe.cpeName, "startIndex": 0})
            res.raise_for_status()
            data = res.json()

            cves = CVEs(
                total_results=data["totalResults"],
                cves=[
                    CVE(
                        cve_id=i["cve"]["id"],
                        description=i["cve"]["descriptions"][0]["value"],
                        url=i["cve"]["references"][0]["url"],
                        metric_v2=i["cve"].get("metrics", {}),
                        metric_v3=i["cve"].get("metrics", {}),
                    )
                    for i in data["vulnerabilities"]
                ],
                cpe=cpe,
            )
            return cves
        except ReadTimeout:
            return CVEs(total_results=0, cves=[], error="Timeout", cpe=cpe)
        except HTTPStatusError as e:
            if attempt > self.retries:
                return CVEs(total_results=0, cves=[], error=f"HTTP Error {e.response.status_code}", cpe=cpe)
            else:
                return self._query_cve(cpe, attempt + 1)

    def _query_cpe(self, params, attempt: int = 0) -> list[CPE]:
        try:
            sleep(0.3 + attempt)  # NIST Rate Limit: 50 requests/30 seconds
            res = self.get("cpes/2.0", params=params)
            res.raise_for_status()
            data = res.json()
            return [CPE(**_["cpe"]) for _ in data["products"] if "cpe" in _]
        except ReadTimeout:
            return [CPE(cpeName="", cpeNameId="", deprecated=False, created="", lastModified="", error="Timeout")]
        except HTTPStatusError as e:
            if attempt > self.retries:
                return [
                    CPE(
                        cpeName="",
                        cpeNameId="",
                        deprecated=False,
                        created="",
                        lastModified="",
                        error=f"HTTP Error {e.response.status_code}",
                    )
                ]
            else:
                return self._query_cpe(params, attempt + 1)
