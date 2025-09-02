import logging
import re
from datetime import datetime
from typing import Optional, Any

from pydantic import Field, BaseModel

from ipfabric.tools.shared import raise_for_status

logger = logging.getLogger("ipfabric")

ATTR_REGEX = re.compile(r"^[a-zA-Z]\w*[a-zA-Z0-9]+$")


class Attributes(BaseModel):
    """
    Class to retrieve Global and Local (Snapshot specific) Attributes.  You must specify snapshot_id to use local.
    """

    client: Any = Field(description="IPFClient", exclude=True)
    snapshot_id: Optional[str] = Field(default=None, description="Snapshot ID to switch to Local Attributes")

    def model_post_init(self, __context: Any) -> None:
        if isinstance(self.snapshot_id, str):
            self.snapshot_id = self.client.get_snapshot(self.snapshot_id).snapshot_id

    @property
    def endpoint(self):
        return "attributes/local" if self.snapshot_id else "attributes/global"

    @property
    def post_endpoint(self):
        return "tables/snapshot-attributes" if self.snapshot_id else "tables/global-attributes"

    @staticmethod
    def check_attribute_name(attributes: set):
        invalid = list()
        for attribute in attributes:
            if not ATTR_REGEX.match(attribute):
                invalid.append(attribute)
        if invalid:
            raise NameError(
                f"The following Attribute Names are invalid and do match regex rule "
                f'"^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]+$":\n{invalid}'
            )
        return True

    def all(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        sort: Optional[dict] = None,
    ):
        """Gets all data from corresponding endpoint

        Args:
            columns: Optional columns to return, default is all
            filters: Optional filters
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}

        Returns:
            list: List of Dictionaries
        """
        return self.client.fetch_all(
            self.post_endpoint,
            columns=columns,
            filters=filters,
            sort=sort,
            snapshot=True if self.snapshot_id else False,
            snapshot_id=self.snapshot_id,
        )

    def set_attribute_by_sn(self, serial_number, name, value):
        """
        Set a single Attribute by serial number.
        If Global will Error if already set.
        If Local will not error and either Add or Update
        :param serial_number: str: IP Fabric Unique Serial Number
        :param name: str: Attribute name (case sensitive)
        :param value: str: Attribute value (case sensitive)
        :return:
        """
        self.check_attribute_name({name})
        attribute = dict(name=name, sn=serial_number, value=value)
        if self.snapshot_id:
            return self.set_attributes_by_sn([attribute])
        resp = raise_for_status(self.client.post(self.endpoint, json=attribute))
        return resp.json()

    def set_attributes_by_sn(self, attributes: list[dict]):
        """
        Sets a list of Attributes for devices based on serial numbers.
        Will Add or Update Attributes.
        :param attributes: list: [{'sn': 'IPF SERIAL NUMBER', 'name': 'attributeName', 'value': 'SITE NAME'}]
        :return:
        """
        self.check_attribute_name({v["name"] for v in attributes})
        payload = dict(attributes=attributes)
        if self.snapshot_id:
            payload["snapshot"] = self.snapshot_id
        resp = raise_for_status(self.client.put(self.endpoint, json=payload))
        return resp.json()

    def set_site_by_sn(self, serial_number, site_name):
        """
        Set a single site by serial number
        If Global will Error if already set.
        If Local will not error and either Add or Update
        :param serial_number: str: IP Fabric Unique Serial Number
        :param site_name: str: Site name for device.
        :return:
        """
        return self.set_attribute_by_sn(serial_number, "siteName", site_name)

    def set_sites_by_sn(self, sites: list[dict]):
        """Sets a list of sites for devices based on serial numbers.

        Args:
            sites: [{'sn': 'IPF SERIAL NUMBER', 'value': 'SITE NAME'}]
        """
        [a.update(dict(name="siteName")) for a in sites]
        return self.set_attributes_by_sn(sites)

    def delete_attribute_by_sn(self, *serial_numbers):
        """Deletes attributes by Unique IP Fabric Serial Number(s)

        Args:
            serial_numbers: Serial Numbers
        """
        payload = dict(attributes=dict(sn=[str(i) for i in serial_numbers]))
        if self.snapshot_id:
            payload["snapshot"] = self.snapshot_id
        raise_for_status(self.client.request("DELETE", self.endpoint, json=payload))
        return True

    def delete_attribute_by_id(self, *attribute_ids):
        """Deletes attributes by Attribute ID(s)

        Args:
            attribute_ids: Attribute IDs
        """
        payload = dict(attributes=dict(id=[str(i) for i in attribute_ids]))
        if self.snapshot_id:
            payload["snapshot"] = self.snapshot_id
        raise_for_status(self.client.request("DELETE", self.endpoint, json=payload))
        return True

    def delete_attribute(self, *attributes):
        """
        Deletes attributes by Attribute
        :param attributes: dict: Attribute dictionaries
        :return:
        """
        return self.delete_attribute_by_id(*[str(i["id"]) for i in attributes])

    def update_local_attr_from_global(
        self,
        wait_for_load: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> bool:
        """
        Updates Snapshot Local Attributes based on Global.
        Returns True is successfully completed, False if the snapshot load did not complete if required.
        """
        if not self.snapshot_id:
            raise ImportError("Please initialize Attributes class with a snapshot_id.")
        recalc = self.check_sites_recalculation()
        ts = int(datetime.now().timestamp() * 1000)
        raise_for_status(self.client.post("/attributes/local/update-from-global", json={"snapshot": self.snapshot_id}))

        if (
            recalc
            and (wait_for_load or wait_for_assurance)
            and not self.client.snapshots[self.snapshot_id]._check_load_status(
                ts, wait_for_assurance, timeout, retry, "recalculate"
            )
        ):
            return False
        self.client.snapshots[self.snapshot_id]._refresh_status()
        if self.client.snapshots[self.snapshot_id].loaded and self.client.snapshot_id == self.snapshot_id:
            self.client.devices.update()
        return True

    def check_sites_recalculation(self) -> bool:
        """Checks if updating local attributes requires recalculation."""
        if not self.snapshot_id:
            raise ImportError("Please initialize Attributes class with a snapshot_id.")
        resp = raise_for_status(
            self.client.post(
                "/attributes/local/update-from-global/check-sites-recalculation", json={"snapshot": self.snapshot_id}
            )
        )
        return resp.json()["needsRecalculation"]
