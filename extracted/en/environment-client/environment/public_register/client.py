from __future__ import annotations

import httpx
from typing import Any, Dict, List, Optional, Union

from .models import (
    RegistrationSearchResponse,
    RegistrationSummary,
    RegistrationDetail,
)


class PublicRegisterClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Public Register API.
    
    This client provides access to various public registers including:
    - Waste Operations
    - End of Life Vehicles
    - Industrial Installations
    - Water Discharges
    - Radioactive Substances
    - Waste Carriers and Brokers
    - Waste Exemptions
    - Water Discharge Exemptions
    - Scrap Metal Dealers
    - Enforcement Actions
    - Flood Risk Exemptions
    """

    def __init__(self, timeout=30.0, verbose=False, **kwargs):
        """
        Initializes the client.

        Args:
            timeout (float, optional): The timeout for requests in seconds. Defaults to 30.0.
            verbose (bool, optional): If True, logs requests and responses. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the httpx.AsyncClient constructor.
        """
        super().__init__(
            base_url="https://environment.data.gov.uk/public-register",
            timeout=timeout,
            **kwargs,
        )
        if verbose:
            self.event_hooks["request"].append(self._log_request)
            self.event_hooks["response"].append(self._log_response)

    def _log_request(self, request: httpx.Request) -> None:
        """Log the request details."""
        print(f"Request: {request.method} {request.url}")

    def _log_response(self, response: httpx.Response) -> None:
        """Log the response details."""
        print(f"Response: {response.status_code} {response.url}")

    async def search_all_registers(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search across all registers for registrations matching the criteria.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/api/search.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_completion(
        self,
        query: str,
        limit: Optional[int] = None,
        **params
    ) -> List[str]:
        """
        Get text completion suggestions for names or registration numbers.

        Args:
            query: Partial text to complete
            limit: Maximum number of suggestions to return
            **params: Additional query parameters

        Returns:
            List[str]: List of completion suggestions
        """
        completion_params = {
            "q": query,
            "_limit": limit,
        }
        completion_params.update(params)
        
        response = await self.get("/api/completion.json", params=completion_params)
        response.raise_for_status()
        return response.json()

    async def get_waste_operations(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Environmental Permitting Regulations - Waste Operations.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/waste-operations/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_waste_operation_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific waste operation registration.

        Args:
            registration_id: The ID of the waste operation registration

        Returns:
            RegistrationDetail: Details of the waste operation registration
        """
        response = await self.get(f"/waste-operations/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_end_of_life_vehicles(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of End of Life Vehicle Authorised Treatment Facilities.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/end-of-life-vehicles/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_end_of_life_vehicle_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific end of life vehicle registration.

        Args:
            registration_id: The ID of the end of life vehicle registration

        Returns:
            RegistrationDetail: Details of the end of life vehicle registration
        """
        response = await self.get(f"/end-of-life-vehicles/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_industrial_installations(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Industrial Installations.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/industrial-installations/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_industrial_installation_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific industrial installation registration.

        Args:
            registration_id: The ID of the industrial installation registration

        Returns:
            RegistrationDetail: Details of the industrial installation registration
        """
        response = await self.get(f"/industrial-installations/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_water_discharges(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Water Discharges.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/water-discharges/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_water_discharge_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific water discharge registration.

        Args:
            registration_id: The ID of the water discharge registration

        Returns:
            RegistrationDetail: Details of the water discharge registration
        """
        response = await self.get(f"/water-discharges/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_radioactive_substances(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Radioactive Substances.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/radioactive-substance/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_radioactive_substance_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific radioactive substance registration.

        Args:
            registration_id: The ID of the radioactive substance registration

        Returns:
            RegistrationDetail: Details of the radioactive substance registration
        """
        response = await self.get(f"/radioactive-substance/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_waste_carriers_brokers(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Waste Carriers and Brokers.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/waste-carriers-brokers/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_waste_carrier_broker_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific waste carrier or broker registration.

        Args:
            registration_id: The ID of the waste carrier or broker registration

        Returns:
            RegistrationDetail: Details of the waste carrier or broker registration
        """
        response = await self.get(f"/waste-carriers-brokers/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_waste_exemptions(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Waste Exemptions.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/waste-exemptions/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_waste_exemption_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific waste exemption registration.

        Args:
            registration_id: The ID of the waste exemption registration

        Returns:
            RegistrationDetail: Details of the waste exemption registration
        """
        response = await self.get(f"/waste-exemptions/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_water_discharge_exemptions(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Water Discharge Exemptions.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/water-discharge-exemptions/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_water_discharge_exemption_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific water discharge exemption registration.

        Args:
            registration_id: The ID of the water discharge exemption registration

        Returns:
            RegistrationDetail: Details of the water discharge exemption registration
        """
        response = await self.get(f"/water-discharge-exemptions/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_scrap_metal_dealers(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Scrap Metal Dealers.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/scrap-metal-dealers/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_scrap_metal_dealer_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific scrap metal dealer registration.

        Args:
            registration_id: The ID of the scrap metal dealer registration

        Returns:
            RegistrationDetail: Details of the scrap metal dealer registration
        """
        response = await self.get(f"/scrap-metal-dealers/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_enforcement_actions(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Enforcement Actions.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/enforcement-action/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_enforcement_action_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific enforcement action registration.

        Args:
            registration_id: The ID of the enforcement action registration

        Returns:
            RegistrationDetail: Details of the enforcement action registration
        """
        response = await self.get(f"/enforcement-action/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    async def get_flood_risk_exemptions(
        self,
        name_search: Optional[str] = None,
        number_search: Optional[str] = None,
        name_number_search: Optional[str] = None,
        address_search: Optional[str] = None,
        easting: Optional[float] = None,
        northing: Optional[float] = None,
        dist: Optional[float] = None,
        local_authority: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        exact_name: Optional[str] = None,
        registration_number: Optional[str] = None,
        **params
    ) -> RegistrationSearchResponse:
        """
        Search the register of Flood Risk Exemptions.

        Args:
            name_search: Full or partial name of the business or individual registered
            number_search: The full or partial ID of a registration or permit
            name_number_search: Search for records where either name or registration number matches
            address_search: Full or partial address of the business or individual registered
            easting: Easting coordinate for location-based search
            northing: Northing coordinate for location-based search
            dist: Distance in kilometers from the specified coordinates
            local_authority: Local authority name for filtering
            limit: Maximum number of results to return
            offset: Number of results to skip
            exact_name: Exact name match
            registration_number: Specific registration number
            **params: Additional query parameters

        Returns:
            RegistrationSearchResponse: Search results with metadata
        """
        search_params = {
            "name-search": name_search,
            "number-search": number_search,
            "name-number-search": name_number_search,
            "address-search": address_search,
            "easting": easting,
            "northing": northing,
            "dist": dist,
            "local-authority": local_authority,
            "_limit": limit,
            "_offset": offset,
            "name": exact_name,
            "registration-number": registration_number,
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        search_params.update(params)
        
        response = await self.get("/flood-risk-exemptions/registration.json", params=search_params)
        response.raise_for_status()
        return RegistrationSearchResponse(**response.json())

    async def get_flood_risk_exemption_by_id(self, registration_id: str) -> RegistrationDetail:
        """
        Get details of a specific flood risk exemption registration.

        Args:
            registration_id: The ID of the flood risk exemption registration

        Returns:
            RegistrationDetail: Details of the flood risk exemption registration
        """
        response = await self.get(f"/flood-risk-exemptions/registration/{registration_id}.json")
        response.raise_for_status()
        data = response.json()
        return RegistrationDetail(**data["items"][0])

    # Download methods for each register type
    async def download_waste_operations(self, **params) -> bytes:
        """
        Download waste operations data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/waste-operations", params=params)
        response.raise_for_status()
        return response.content

    async def download_end_of_life_vehicles(self, **params) -> bytes:
        """
        Download end of life vehicles data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/end-of-life-vehicles", params=params)
        response.raise_for_status()
        return response.content

    async def download_industrial_installations(self, **params) -> bytes:
        """
        Download industrial installations data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/industrial-installations", params=params)
        response.raise_for_status()
        return response.content

    async def download_water_discharges(self, **params) -> bytes:
        """
        Download water discharges data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/water-discharges", params=params)
        response.raise_for_status()
        return response.content

    async def download_radioactive_substances(self, **params) -> bytes:
        """
        Download radioactive substances data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/radioactive-substance", params=params)
        response.raise_for_status()
        return response.content

    async def download_waste_carriers_brokers(self, **params) -> bytes:
        """
        Download waste carriers and brokers data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/waste-carriers-brokers", params=params)
        response.raise_for_status()
        return response.content

    async def download_water_discharge_exemptions(self, **params) -> bytes:
        """
        Download water discharge exemptions data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/water-discharge-exemptions", params=params)
        response.raise_for_status()
        return response.content

    async def download_waste_exemptions(self, **params) -> bytes:
        """
        Download waste exemptions data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/waste-exemptions", params=params)
        response.raise_for_status()
        return response.content

    async def download_scrap_metal_dealers(self, **params) -> bytes:
        """
        Download scrap metal dealers data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/scrap-metal-dealers", params=params)
        response.raise_for_status()
        return response.content

    async def download_enforcement_actions(self, **params) -> bytes:
        """
        Download enforcement actions data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/enforcement-action", params=params)
        response.raise_for_status()
        return response.content

    async def download_flood_risk_exemptions(self, **params) -> bytes:
        """
        Download flood risk exemptions data in CSV format.

        Args:
            **params: Additional query parameters

        Returns:
            bytes: CSV data
        """
        response = await self.get("/downloads/flood-risk-exemptions", params=params)
        response.raise_for_status()
        return response.content