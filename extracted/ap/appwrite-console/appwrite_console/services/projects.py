from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..models.addon_list import AddonList
from ..models.addon import Addon
from ..models.addon_price import AddonPrice
from ..models.schedule_list import ScheduleList
from ..enums.schedule_resource_type import ScheduleResourceType
from ..models.schedule import Schedule
from ..models.stage_list import StageList
from ..models.stage import Stage
from ..enums.status import Status
from ..models.project import Project


class Projects(Service):

    def __init__(self, client) -> None:
        super(Projects, self).__init__(client)

    def list_addons(
        self,
        project_id: str,
    ) -> AddonList:
        """
        List all billing addons for a project.

        Parameters
        ----------
        project_id : str
            Project ID
        Returns
        -------
        AddonList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/addons'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=AddonList)

    def create_premium_geo_db_addon(
        self,
        project_id: str,
    ) -> Addon:
        """
        Create a Premium Geo DB addon for a project.

        Parameters
        ----------
        project_id : str
            Project ID
        Returns
        -------
        Addon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/addons/premium-geo-db'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Addon)

    def get_addon(
        self,
        project_id: str,
        addon_id: str,
    ) -> Addon:
        """
        Get the details of a billing addon for a project.

        Parameters
        ----------
        project_id : str
            Project ID
        addon_id : str
            Addon ID
        Returns
        -------
        Addon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/addons/{addonId}'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if addon_id is None or addon_id == '':
            raise AppwriteException('Missing required parameter: "addon_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_path = api_path.replace('{addonId}', self._encode_path(addon_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Addon)

    def delete_addon(
        self,
        project_id: str,
        addon_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a billing addon for a project.

        Parameters
        ----------
        project_id : str
            Project ID
        addon_id : str
            Addon ID
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/addons/{addonId}'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if addon_id is None or addon_id == '':
            raise AppwriteException('Missing required parameter: "addon_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_path = api_path.replace('{addonId}', self._encode_path(addon_id))

        response = self.client.call(
            'delete',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def confirm_addon_payment(
        self,
        project_id: str,
        addon_id: str,
    ) -> Addon:
        """
        Confirm payment for a billing addon for a project.

        Parameters
        ----------
        project_id : str
            Project ID
        addon_id : str
            Addon ID
        Returns
        -------
        Addon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/addons/{addonId}/confirmations'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if addon_id is None or addon_id == '':
            raise AppwriteException('Missing required parameter: "addon_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_path = api_path.replace('{addonId}', self._encode_path(addon_id))

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Addon)

    def get_addon_price(
        self,
        project_id: str,
        addon: str,
    ) -> AddonPrice:
        """
        Get the price details for a billing addon for a project, including the prorated amount for the remaining days in the current billing cycle.

        Parameters
        ----------
        project_id : str
            Project ID
        addon : str
            Addon key identifier (e.g. premiumGeoDB).
        Returns
        -------
        AddonPrice
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/addons/{addon}/price'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if addon is None or addon == '':
            raise AppwriteException('Missing required parameter: "addon"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_path = api_path.replace('{addon}', self._encode_path(addon))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=AddonPrice)

    def update_console_access(
        self,
        project_id: str,
    ) -> Dict[str, Any]:
        """
        Record console access to a project. This endpoint updates the last accessed timestamp for the project to track console activity.

        Parameters
        ----------
        project_id : str
            Project ID
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/console-access'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))

        response = self.client.call(
            'patch',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def list_schedules(
        self,
        project_id: str,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> ScheduleList:
        """
        Get a list of all the project's schedules. You can use the query params to filter your results.

        Parameters
        ----------
        project_id : str
            Project unique ID.
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: resourceType, resourceId, projectId, schedule, active, region
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        ScheduleList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/schedules'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ScheduleList)

    def create_schedule(
        self,
        project_id: str,
        resource_type: ScheduleResourceType,
        resource_id: str,
        schedule: Optional[str] = None,
        active: Optional[bool] = None,
        data: Optional[Dict[str, Any]] = None,
        interval: Optional[float] = None,
    ) -> Schedule:
        """
        Create a new schedule for a resource.

        Parameters
        ----------
        project_id : str
            Project unique ID.
        resource_type : ScheduleResourceType
            The resource type for the schedule. Possible values: function, execution, message, backup.
        resource_id : str
            The resource ID to associate with this schedule.
        schedule : Optional[str]
            Schedule CRON expression. Cannot be combined with interval.
        active : Optional[bool]
            Whether the schedule is active.
        data : Optional[Dict[str, Any]]
            Schedule data as a JSON string. Used to store resource-specific context needed for execution.
        interval : Optional[float]
            Minutes between runs, for function schedules only. Use 0 to disable. Cannot be combined with schedule.
        Returns
        -------
        Schedule
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/schedules'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if resource_type is None:
            raise AppwriteException('Missing required parameter: "resource_type"')
        if resource_id is None:
            raise AppwriteException('Missing required parameter: "resource_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_params['resourceType'] = self._normalize_value(resource_type)
        api_params['resourceId'] = self._normalize_value(resource_id)
        if schedule is not None:
            api_params['schedule'] = self._normalize_value(schedule)
        if active is not None:
            api_params['active'] = self._normalize_value(active)
        if data is not None:
            api_params['data'] = self._normalize_value(data)
        if interval is not None:
            api_params['interval'] = self._normalize_value(interval)

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Schedule)

    def get_schedule(
        self,
        project_id: str,
        schedule_id: str,
    ) -> Schedule:
        """
        Get a schedule by its unique ID.

        Parameters
        ----------
        project_id : str
            Project unique ID.
        schedule_id : str
            Schedule ID.
        Returns
        -------
        Schedule
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/schedules/{scheduleId}'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if schedule_id is None or schedule_id == '':
            raise AppwriteException('Missing required parameter: "schedule_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_path = api_path.replace('{scheduleId}', self._encode_path(schedule_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Schedule)

    def list_stages(
        self,
        project_id: str,
    ) -> StageList:
        """
        Get the onboarding stages for the current project, including each stage’s SDK method key and status (for example pending, completed, or skipped).

        Parameters
        ----------
        project_id : str
            Project unique ID.
        Returns
        -------
        StageList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/stages'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=StageList)

    def update_stage(
        self,
        project_id: str,
        stage_id: str,
        skip: Optional[bool] = None,
    ) -> Stage:
        """
        Update an onboarding stage for the current project. Use this endpoint to skip a stage or leave it unchanged without performing the related API action.

        Parameters
        ----------
        project_id : str
            Project unique ID.
        stage_id : str
            SDK method key (namespace.method).
        skip : Optional[bool]
            Mark the stage as skipped.
        Returns
        -------
        Stage
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/stages/{stageId}'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if stage_id is None or stage_id == '':
            raise AppwriteException('Missing required parameter: "stage_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_path = api_path.replace('{stageId}', self._encode_path(stage_id))
        if skip is not None:
            api_params['skip'] = self._normalize_value(skip)

        response = self.client.call(
            'patch',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Stage)

    def update_status(
        self,
        project_id: str,
        status: Status,
    ) -> Dict[str, Any]:
        """
        Update the status of a project. Can be used to archive/restore projects, and to restore paused projects. When restoring a paused project, the console fingerprint header must be provided and the project must not be blocked for any reason other than inactivity.

        Parameters
        ----------
        project_id : str
            Project ID
        status : Status
            New status for the project
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/status'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if status is None:
            raise AppwriteException('Missing required parameter: "status"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_params['status'] = self._normalize_value(status)

        response = self.client.call(
            'patch',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def update_team(
        self,
        project_id: str,
        team_id: str,
    ) -> Project:
        """
        Update the team ID of a project allowing for it to be transferred to another team.

        Parameters
        ----------
        project_id : str
            Project unique ID.
        team_id : str
            Team ID of the team to transfer project to.
        Returns
        -------
        Project
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/projects/{projectId}/team'
        api_params = {}
        if project_id is None or project_id == '':
            raise AppwriteException('Missing required parameter: "project_id"')
        if team_id is None:
            raise AppwriteException('Missing required parameter: "team_id"')
        api_path = api_path.replace('{projectId}', self._encode_path(project_id))
        api_params['teamId'] = self._normalize_value(team_id)

        response = self.client.call(
            'patch',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Project)
