from abc import ABC
import asyncio
import googlemaps
from typing import Tuple, Union, Dict, List
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError


class GoogleMapsGeocodingClient(GoogleClient, ABC):
    """
    Google Maps Geocoding Client for location-based tasks including geocoding, 
    reverse geocoding, distance calculation, and place details.
    """

    def __init__(self, *args, api_key: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self._client = None

    async def get_client(self):
        """Get the Google Maps client, with caching."""
        if not self._client:
            self._client = await asyncio.to_thread(googlemaps.Client, self.api_key)
        return self._client

    async def geocode_address(self, address: str) -> Dict:
        """
        Geocode an address to retrieve latitude and longitude.

        Args:
            address (str): The address to geocode.

        Returns:
            dict: Geocoded location with latitude and longitude.
        """
        client = await self.get_client()
        result = await asyncio.to_thread(client.geocode, address)
        if result:
            location = result[0]['geometry']['location']
            return {"lat": location['lat'], "lng": location['lng']}
        else:
            raise ComponentError("Address could not be geocoded.")

    async def reverse_geocode(self, lat: float, lng: float) -> List[Dict]:
        """
        Reverse geocode coordinates to retrieve address information.

        Args:
            lat (float): Latitude of the location.
            lng (float): Longitude of the location.

        Returns:
            list: List of addresses for the location.
        """
        client = await self.get_client()
        result = await asyncio.to_thread(client.reverse_geocode, (lat, lng))
        return result

    async def calculate_distance(self, origin: str, destination: str) -> Dict:
        """
        Calculate the distance between two locations.

        Args:
            origin (str): Starting location (address or coordinates).
            destination (str): Ending location (address or coordinates).

        Returns:
            dict: Distance and duration between the origin and destination.
        """
        client = await self.get_client()
        result = await asyncio.to_thread(client.distance_matrix, origin, destination)
        if result['rows']:
            distance_info = result['rows'][0]['elements'][0]
            return {
                "distance": distance_info['distance']['text'],
                "duration": distance_info['duration']['text']
            }
        else:
            raise ComponentError("Could not calculate distance between locations.")

    async def get_place_details(self, place_id: str) -> Dict:
        """
        Get detailed information about a place by its place ID.

        Args:
            place_id (str): The place ID of the location.

        Returns:
            dict: Detailed information about the place.
        """
        client = await self.get_client()
        result = await asyncio.to_thread(client.place, place_id)
        return result['result'] if 'result' in result else {}
