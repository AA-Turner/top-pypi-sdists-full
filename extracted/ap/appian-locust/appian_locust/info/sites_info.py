from typing import Dict

from .._sites import _Sites
from ..objects import Site


class SitesInfo:
    """
    Class which provides metadata about available Sites
    """

    def __init__(self, sites: _Sites):
        self.__sites = sites

    def get_all_available_sites(self) -> Dict[str, Site]:
        """
        Retrieves all the available "sites" and associated metadata

        Returns (dict): List of sites and associated metadata

        Examples:

            >>> sites_info.get_all_available_sites()

        """
        return self.__sites.get_all()

    def get_site_info(self, site_name: str, exact_match: bool = True) -> Site:
        """
        Get the information about specific site by name.

        Args:
            site_name (str): Name of the action

        Returns (Site): Specific site's info

        Raises: In case of site is not found in the system, it throws an "Exception"

        Example:
            If full name of site is known:

            >>> site_info.get_site_info("site_name", exact_match=True)

            If only the display name is known, or part of the display name:

            >>> site_info.get_site_info("site")

        """
        return self.__sites.get_site_data_by_site_name(site_name=site_name)
