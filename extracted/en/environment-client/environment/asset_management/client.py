"""
An async client for the UK Environment Agency's Asset Management API.
"""

import httpx
from .models import (
    Asset,
    MaintenanceActivity,
    MaintenanceTask,
    MaintenancePlan,
    CapitalScheme,
)


async def log_request(request):
    print(f">>> Request: {request.method} {request.url}")


async def log_response(response):
    # Avoid pre-reading body so VCR can capture content
    print(f"<<< Response: {response.status_code}")


class AssetManagementClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Asset Management API.
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
            base_url="https://environment.data.gov.uk/asset-management",
            timeout=timeout,
            follow_redirects=True,
            **kwargs,
        )
        if verbose:
            self.event_hooks["request"].append(log_request)
            self.event_hooks["response"].append(log_response)

    async def get_assets(self, **params) -> list[Asset]:
        """
        Returns a list of assets.

        Returns:
            list[Asset]: A list of assets.
        """
        response = await self.get("/id/asset.json", params=params)
        response.raise_for_status()
        return [Asset(**item) for item in response.json()["items"]]

    async def get_asset_by_id(self, asset_id: str) -> Asset:
        """
        Returns details of a single asset by ID.

        Args:
            asset_id (str): The ID of the asset.

        Returns:
            Asset: Details of the asset.
        """
        response = await self.get(f"/id/asset/{asset_id}.json")
        response.raise_for_status()
        return Asset(**response.json()["items"][0])

    async def get_maintenance_activities(self, **params) -> list[MaintenanceActivity]:
        """
        Returns a list of maintenance activities.

        Returns:
            list[MaintenanceActivity]: A list of maintenance activities.
        """
        response = await self.get("/id/maintenance-activity.json", params=params)
        response.raise_for_status()
        return [MaintenanceActivity(**item) for item in response.json()["items"]]

    async def get_maintenance_activity_by_id(
        self, activity_id: str
    ) -> MaintenanceActivity:
        """
        Returns details of a single maintenance activity by ID.

        Args:
            activity_id (str): The ID of the maintenance activity.

        Returns:
            MaintenanceActivity: Details of the maintenance activity.
        """
        response = await self.get(f"/id/maintenance-activity/{activity_id}.json")
        response.raise_for_status()
        return MaintenanceActivity(**response.json()["items"][0])

    async def get_maintenance_tasks(self, **params) -> list[MaintenanceTask]:
        """
        Returns a list of maintenance tasks.

        Returns:
            list[MaintenanceTask]: A list of maintenance tasks.
        """
        response = await self.get("/id/maintenance-task.json", params=params)
        response.raise_for_status()
        return [MaintenanceTask(**item) for item in response.json()["items"]]

    async def get_maintenance_task_by_id(self, task_id: str) -> MaintenanceTask:
        """
        Returns details of a single maintenance task by ID.

        Args:
            task_id (str): The ID of the maintenance task.

        Returns:
            MaintenanceTask: Details of the maintenance task.
        """
        response = await self.get(f"/id/maintenance-task/{task_id}.json")
        response.raise_for_status()
        return MaintenanceTask(**response.json()["items"][0])

    async def get_maintenance_plans(self, **params) -> list[MaintenancePlan]:
        """
        Returns a list of maintenance plans.

        Returns:
            list[MaintenancePlan]: A list of maintenance plans.
        """
        response = await self.get("/id/maintenance-plan.json", params=params)
        response.raise_for_status()
        return [MaintenancePlan(**item) for item in response.json()["items"]]

    async def get_maintenance_plan_by_id(self, plan_id: str) -> MaintenancePlan:
        """
        Returns details of a single maintenance plan by ID.

        Args:
            plan_id (str): The ID of the maintenance plan.

        Returns:
            MaintenancePlan: Details of the maintenance plan.
        """
        response = await self.get(f"/id/maintenance-plan/{plan_id}.json")
        response.raise_for_status()
        return MaintenancePlan(**response.json()["items"][0])

    async def get_capital_schemes(self, **params) -> list[CapitalScheme]:
        """
        Returns a list of capital schemes.

        Returns:
            list[CapitalScheme]: A list of capital schemes.
        """
        response = await self.get("/id/capital-scheme.json", params=params)
        response.raise_for_status()
        return [CapitalScheme(**item) for item in response.json()["items"]]

    async def get_capital_scheme_by_id(self, scheme_id: str) -> CapitalScheme:
        """
        Returns details of a single capital scheme by ID.

        Args:
            scheme_id (str): The ID of the capital scheme.

        Returns:
            CapitalScheme: Details of the capital scheme.
        """
        response = await self.get(f"/id/capital-scheme/{scheme_id}.json")
        response.raise_for_status()
        return CapitalScheme(**response.json()["items"][0])
