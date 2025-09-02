"""Location handler for Crownstone cloud data."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from crownstone_cloud.cloud import CrownstoneCloud


class Locations:
    """Handler for the locations of a sphere."""

    def __init__(self, cloud: CrownstoneCloud, sphere_id: str) -> None:
        """Initialization."""
        self.cloud = cloud
        self.sphere_id = sphere_id
        self.data: dict[str, Location] = {}

    def __iter__(self) -> Iterator[Location]:
        """Iterate over locations."""
        return iter(self.data.values())

    async def async_update_location_data(self) -> None:
        """
        Get the locations and presence from the cloud.

        This method is a coroutine.
        """
        cloud_data: list[dict[str, Any]] = await self.cloud.request_handler.get(
            "Spheres", "ownedLocations", model_id=self.sphere_id
        )
        # process items
        removed_items: list[str] = []
        new_items: list[str] = []
        for location in cloud_data:
            location_id: str = location["id"]
            exists = self.data.get(location_id)
            # check if the location already exists
            # it is important that we don't throw away existing objects,
            # as they need to remain functional
            if exists:
                # update data
                self.data[location_id].data = location
            else:
                # add new Location
                self.data[location_id] = Location(location)

            # generate list with new id's to check with the existing id's
            new_items.append(location_id)

        # check for removed items
        for location_id in self.data:
            if location_id not in new_items:
                removed_items.append(location_id)

        # remove items from dict
        for location_id in removed_items:
            del self.data[location_id]

    async def async_update_location_presence(self) -> None:
        """
        Get the presentPeople for this Sphere, and get the users in this Location.

        This method is a coroutine.
        """
        presence_data: list[dict[str, Any]] = await self.cloud.request_handler.get(
            "Spheres", "presentPeople", model_id=self.sphere_id
        )
        # reset the presence
        for location in self.data.values():
            location.present_people = []
        # add new presence
        for presence in presence_data:
            for present_location in presence["locations"]:
                for location in self.data.values():
                    if present_location == location.cloud_id:
                        location.present_people.append(presence["userId"])

    def find(self, location_name: str) -> Location | None:
        """Search for a sphere by name and return sphere object if found."""
        for location in self.data.values():
            if location_name == location.name:
                return location

        return None

    def find_by_id(self, location_id: str) -> Location | None:
        """Search for a sphere by id and return sphere object if found."""
        return self.data.get(location_id)


class Location:
    """Represents a Location."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialization."""
        self.data = data
        self.present_people: list[str] = []

    @property
    def name(self) -> str:
        """Return the name of this Location."""
        return str(self.data["name"])

    @property
    def cloud_id(self) -> str:
        """Return the cloud id of this Location."""
        return str(self.data["id"])

    @property
    def unique_id(self) -> int:
        """Return the unique id of this Location."""
        return int(self.data["uid"])
