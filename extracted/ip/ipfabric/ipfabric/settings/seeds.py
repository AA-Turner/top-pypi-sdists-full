import logging
from ipaddress import IPv4Interface, AddressValueError
from typing import Any

from pydantic import Field, BaseModel

from ipfabric.tools.shared import raise_for_status

logger = logging.getLogger("ipfabric")


class Seeds(BaseModel):
    client: Any = Field(exclude=True)

    @property
    def seeds(self):
        return raise_for_status(self.client.get("settings/seed")).json()

    @staticmethod
    def _check_seeds(seeds):
        valid = True
        for seed in seeds:
            try:
                IPv4Interface(seed)
            except AddressValueError:
                valid = False
                logger.error(f"Seed {seed} is not a valid IP address or network.")
        return valid

    def set_seeds(self, seeds):
        """
        Sets the seeds with supplied list, will override current configuration.
        :param seeds: list: List of IP addresses or networks
        :return: list: Updated list of configured seeds
        """
        if not isinstance(seeds, list):
            raise SyntaxError("Seeds must be a list of IP Addresses or networks")
        return raise_for_status(self.client.put("settings/seed", json=self._check_seeds(seeds))).json()

    def add_seeds(self, seeds):
        """
        Adds a single seed or list of seeds to the current configuration
        :param seeds: list: List of IP addresses or networks
        :return: list: Updated list of configured seeds
        """
        if isinstance(seeds, str):
            seeds = [seeds]
        updated = list(set.union(set(self.seeds), set(seeds)))
        return self.set_seeds(updated)

    def delete_seeds(self, seeds):
        """
        Deletes a seed or a list of seeds from what is configured.
        :param seeds: list: List of IP addresses or networks
        :return: list: Updated list of configured seeds
        """
        if isinstance(seeds, str):
            seeds = [seeds]
        updated = list(set(self.seeds) - set(seeds))
        return self.set_seeds(updated)
