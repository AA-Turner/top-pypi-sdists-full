from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Schedule(AppwriteModel):
    """
    Schedule

    Attributes
    ----------
    id : str
        Schedule ID.
    createdat : str
        Schedule creation date in ISO 8601 format.
    updatedat : str
        Schedule update date in ISO 8601 format.
    resourcetype : str
        The resource type associated with this schedule.
    resourceid : str
        The resource ID associated with this schedule.
    resourceupdatedat : str
        Change-tracking timestamp used by the scheduler to detect resource changes in ISO 8601 format.
    projectid : str
        The project ID associated with this schedule.
    schedule : str
        The CRON schedule expression.
    interval : Optional[float]
        Minutes between runs. 0 when the schedule has no interval.
    data : Dict[str, Any]
        Schedule data used to store resource-specific context needed for execution.
    active : bool
        Whether the schedule is active.
    region : str
        The region where the schedule is deployed.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    resourcetype: str = Field(..., alias='resourceType')
    resourceid: str = Field(..., alias='resourceId')
    resourceupdatedat: str = Field(..., alias='resourceUpdatedAt')
    projectid: str = Field(..., alias='projectId')
    schedule: str = Field(..., alias='schedule')
    interval: Optional[float] = Field(default=None, alias='interval')
    data: Dict[str, Any] = Field(..., alias='data')
    active: bool = Field(..., alias='active')
    region: str = Field(..., alias='region')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if '$createdAt' not in data and 'createdat' not in data:
            data['$createdAt'] = ''
        if '$updatedAt' not in data and 'updatedat' not in data:
            data['$updatedAt'] = ''
        if 'resourceType' not in data and 'resourcetype' not in data:
            data['resourceType'] = ''
        if 'resourceId' not in data and 'resourceid' not in data:
            data['resourceId'] = ''
        if 'resourceUpdatedAt' not in data and 'resourceupdatedat' not in data:
            data['resourceUpdatedAt'] = ''
        if 'projectId' not in data and 'projectid' not in data:
            data['projectId'] = ''
        if 'schedule' not in data:
            data['schedule'] = ''
        if 'data' not in data:
            data['data'] = {}
        if 'active' not in data:
            data['active'] = False
        if 'region' not in data:
            data['region'] = ''
        return data
