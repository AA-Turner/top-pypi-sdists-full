"""Main class for the Crownstone cloud cloud."""
from __future__ import annotations

import asyncio
import logging

import aiohttp

from crownstone_cloud.cloud_models.crownstones import Crownstone
from crownstone_cloud.cloud_models.spheres import Spheres
from crownstone_cloud.exceptions import CrownstoneNotFoundError
from crownstone_cloud.helpers.conversion import password_to_hash
from crownstone_cloud.helpers.requests import RequestHandler

_LOGGER = logging.getLogger(__name__)


class CrownstoneCloud:
    """Create a Crownstone cloud instance."""

    cloud_data: Spheres
    access_token: str

    def __init__(
        self,
        email: str,
        password: str,
        clientsession: aiohttp.ClientSession | None = None,
    ) -> None:
        self.request_handler = RequestHandler(self, clientsession)
        self.login_data = {"email": email, "password": password_to_hash(password)}

    async def async_initialize(self) -> None:
        """
        Login to Crownstone API & synchronize all cloud data.

        This method is a coroutine.
        """
        # Login
        login_response = await self.request_handler.request_login(self.login_data)

        # Save access token & create cloud data object
        self.access_token = login_response["id"]
        self.cloud_data = Spheres(self, login_response["userId"])
        _LOGGER.debug("Login to Crownstone Cloud successful")

        # Synchronize data
        await self.async_synchronize()

    async def async_synchronize(self) -> None:
        """
        Sync all data from cloud.

        This method is a coroutine.
        """
        _LOGGER.debug("Initiating all cloud data")
        # get the sphere data for this user_id
        await self.cloud_data.async_update_sphere_data()

        # get the data from the sphere attributes
        for sphere in self.cloud_data:
            await asyncio.gather(
                sphere.async_update_sphere_presence(),
                sphere.crownstones.async_update_crownstone_data(),
                sphere.locations.async_update_location_data(),
                sphere.locations.async_update_location_presence(),
                sphere.users.async_update_user_data(),
            )
        _LOGGER.debug("Cloud data successfully initialized")

    def get_crownstone(
        self, crownstone_name: str, sphere_id: str | None = None
    ) -> Crownstone:
        """
        Get a Crownstone object by providing the name and optionally a sphere id.

        :param crownstone_name: Name of the Crownstone.
        :param sphere_id: Sphere id that should match.
        :return: Crownstone object.
        """
        for sphere in self.cloud_data:
            if sphere_id is not None:
                if sphere.cloud_id != sphere_id:
                    continue

            for crownstone in sphere.crownstones:
                if crownstone.name == crownstone_name:
                    return crownstone

        raise CrownstoneNotFoundError from None

    def get_crownstone_by_id(
        self, crownstone_id: str, sphere_id: str | None = None
    ) -> Crownstone:
        """
        Get a Crownstone object by providing the id and optionally a sphere id.

        :param crownstone_id: The cloud id of the Crownstone.
        :param sphere_id: Sphere id that should match.
        :return: Crownstone object.
        """
        for sphere in self.cloud_data:
            if sphere_id is not None:
                if sphere.cloud_id != sphere_id:
                    continue

            for crownstone in sphere.crownstones:
                if crownstone.cloud_id == crownstone_id:
                    return crownstone

        raise CrownstoneNotFoundError from None

    def get_crownstone_by_uid(
        self, crownstone_uid: int, sphere_id: str | None = None
    ) -> Crownstone:
        """
        Get a Crownstone object by providing the uid and optionally a sphere id.

        :param crownstone_uid: The unique id of the Crownstone.
        :param sphere_id: Sphere id that should match.
        :return: Crownstone object.
        """
        for sphere in self.cloud_data:
            if sphere_id is not None:
                if sphere.cloud_id != sphere_id:
                    continue

            for crownstone in sphere.crownstones:
                if crownstone.unique_id == crownstone_uid:
                    return crownstone

        raise CrownstoneNotFoundError from None

    async def async_close_session(self) -> None:
        """
        Close the aiohttp clientsession after all requests are done.

        The session should always be closed when the program ends.
        When there's an external clientsession in use, DON'T use this method.

        This method is a coroutine.
        """
        await self.request_handler.client_session.close()
