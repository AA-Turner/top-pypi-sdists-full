import logging
from copy import deepcopy
from typing import Any, Literal, Optional

from pydantic import Field, BaseModel

from ipfabric.tools.shared import raise_for_status

logger = logging.getLogger("ipfabric")


class SiteSeparation(BaseModel):
    client: Any = Field(None, exclude=True)

    def get_separation_rules(self):
        return self.client.get("settings/site-separation").json()

    def _post_rule(self, data):
        return raise_for_status(self.client.post("settings/site-separation/test-regex", json=data)).json()

    def get_rule_matches(self, rule):
        rule = deepcopy(rule)
        [rule.pop(key, None) for key in ["id", "note"]]
        return self._post_rule(rule)

    def _get_matches(
        self, regex: str, transformation, type: str, site_name: Optional[str] = None, cloud: Optional[bool] = None
    ):
        transformation = transformation.lower()
        if transformation not in ["uppercase", "lowercase", "none"]:
            raise SyntaxError('Transformation type is not in ["uppercase", "lowercase", "none"].')
        rule = {"regex": regex, "transformation": transformation, "siteName": site_name, "type": type}
        if isinstance(cloud, bool):
            rule["applyToCloudInstances"] = cloud
        return self._post_rule(rule)

    def get_hostname_matches(
        self, regex: str, transformation: Literal["uppercase", "lowercase", "none"], site_name: Optional[str] = None
    ):
        return self._get_matches(regex, transformation, "regexHostname", site_name)

    def get_snmp_matches(
        self, regex: str, transformation: Literal["uppercase", "lowercase", "none"], site_name: Optional[str] = None
    ):
        return self._get_matches(regex, transformation, "regexSnmpLocation", site_name)

    def get_cloud_id_matches(
        self,
        regex: str,
        transformation: Literal["uppercase", "lowercase", "none"],
        site_name: Optional[str] = None,
        apply_to_cloud: bool = False,
    ):
        return self._get_matches(regex, transformation, "regexCloudResourceId", site_name, apply_to_cloud)
