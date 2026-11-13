from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from ..enums.alert_status import AlertStatus
from ..enums.alert_metric import AlertMetric
from ..enums.alert_comparator import AlertComparator
from ..enums.monitor_type import MonitorType
from ..enums.monitor_resource_type import MonitorResourceType


class Alert(AppwriteModel):
    """
    Alert

    Attributes
    ----------
    id : str
        Alert ID.
    createdat : str
        Date the alert started firing, in ISO 8601 format.
    updatedat : str
        Alert update date in ISO 8601 format.
    monitorid : str
        ID of the monitor that raised the alert.
    name : str
        Name of the monitor when the alert fired.
    status : AlertStatus
        Whether the alert is still firing or has resolved.
    resolvedat : Optional[str]
        Date the alert resolved, in ISO 8601 format. Empty while it fires.
    acknowledgedat : Optional[str]
        Date a member acknowledged the alert, in ISO 8601 format. Empty while nobody has.
    acknowledgedby : str
        ID of the user who acknowledged the alert. Empty while nobody has, or when it was acknowledged with an API key.
    acknowledgedbyname : str
        Name of the user who acknowledged the alert, when they did.
    rules : List[Any]
        The monitor&#039;s rules when the alert fired, as query strings.
    critical : bool
        Whether the monitor was critical when the alert fired.
    metric : AlertMetric
        Metric the alert fired on.
    comparator : AlertComparator
        How the metric was compared with the threshold.
    threshold : float
        Threshold the metric crossed, in the metric&#039;s unit.
    value : float
        Latest reading while the alert fired.
    peak : float
        Reading furthest past the threshold while the alert fired.
    type : MonitorType
        Type of the monitor that raised the alert.
    resourcetype : MonitorResourceType
        Type of the resource the alert fired on: the project, or one database, bucket, function or site.
    resourceid : str
        ID of the resource the alert fired on. The project ID for a project-wide monitor.
    notifications : float
        How many times the alert was announced as firing: once when it fired, and again after each cooldown while it kept firing.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    monitorid: str = Field(..., alias='monitorId')
    name: str = Field(..., alias='name')
    status: AlertStatus = Field(..., alias='status')
    resolvedat: Optional[str] = Field(default=None, alias='resolvedAt')
    acknowledgedat: Optional[str] = Field(default=None, alias='acknowledgedAt')
    acknowledgedby: str = Field(..., alias='acknowledgedBy')
    acknowledgedbyname: str = Field(..., alias='acknowledgedByName')
    rules: List[Any] = Field(..., alias='rules')
    critical: bool = Field(..., alias='critical')
    metric: AlertMetric = Field(..., alias='metric')
    comparator: AlertComparator = Field(..., alias='comparator')
    threshold: float = Field(..., alias='threshold')
    value: float = Field(..., alias='value')
    peak: float = Field(..., alias='peak')
    type: MonitorType = Field(..., alias='type')
    resourcetype: MonitorResourceType = Field(..., alias='resourceType')
    resourceid: str = Field(..., alias='resourceId')
    notifications: float = Field(..., alias='notifications')

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
        if 'monitorId' not in data and 'monitorid' not in data:
            data['monitorId'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'status' not in data:
            data['status'] = 'firing'
        if 'acknowledgedBy' not in data and 'acknowledgedby' not in data:
            data['acknowledgedBy'] = ''
        if 'acknowledgedByName' not in data and 'acknowledgedbyname' not in data:
            data['acknowledgedByName'] = ''
        if 'rules' not in data:
            data['rules'] = []
        if 'critical' not in data:
            data['critical'] = False
        if 'metric' not in data:
            data['metric'] = 'network.requests'
        if 'comparator' not in data:
            data['comparator'] = 'greaterThan'
        if 'threshold' not in data:
            data['threshold'] = 0
        if 'value' not in data:
            data['value'] = 0
        if 'peak' not in data:
            data['peak'] = 0
        if 'type' not in data:
            data['type'] = 'usage'
        if 'resourceType' not in data and 'resourcetype' not in data:
            data['resourceType'] = 'project'
        if 'resourceId' not in data and 'resourceid' not in data:
            data['resourceId'] = ''
        if 'notifications' not in data:
            data['notifications'] = 0
        return data
