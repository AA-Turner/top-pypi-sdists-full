from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .aggregation_breakdown import AggregationBreakdown
from .usage_resources import UsageResources


class AggregationTeam(AppwriteModel):
    """
    Team

    Attributes
    ----------
    id : str
        Aggregation ID.
    createdat : str
        Aggregation creation time in ISO 8601 format.
    updatedat : str
        Aggregation update date in ISO 8601 format.
    permissions : List[Any]
        Aggregation permissions. [Learn more about permissions](/docs/permissions).
    xfrom : str
        Beginning date of the invoice
    to : str
        End date of the invoice
    usagestorage : float
        Total storage usage
    usagetotalstorage : float
        Total storage usage with builds storage
    usagefilesstorage : float
        Total files storage usage
    usagedeploymentsstorage : float
        Total deployments storage usage
    usagebuildsstorage : float
        Total builds storage usage
    usagedatabasesstorage : float
        Total databases storage usage
    usagefunctionsstorage : float
        Total functions storage usage, deployments and builds together. Supersedes usageDeploymentsStorage and usageBuildsStorage.
    usagesitesstorage : float
        Total sites storage usage, deployments and builds together. Supersedes usageDeploymentsStorage and usageBuildsStorage.
    usageusers : float
        Total active users for the billing period
    usageexecutions : float
        Total number of executions for the billing period
    usagebandwidth : float
        Total bandwidth usage for the billing period
    usagerealtime : float
        Peak concurrent realtime connections for the billing period
    usagerealtimemessages : float
        Total realtime messages sent for the billing period
    usagerealtimebandwidth : float
        Total realtime bandwidth usage for the billing period
    additionalmembers : float
        Additional members
    additionalmemberamount : float
        Additional members cost
    additionalstorageamount : float
        Additional storage usage cost
    additionalusersamount : float
        Additional users usage cost.
    additionalexecutionsamount : float
        Additional executions usage cost
    additionalbandwidthamount : float
        Additional bandwidth usage cost
    additionalrealtimeamount : float
        Additional realtime usage cost
    plan : str
        Billing plan
    amount : float
        Aggregated amount
    breakdown : List[AggregationBreakdown]
        Aggregation project breakdown
    resources : List[UsageResources]
        Usage resources
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    permissions: List[Any] = Field(..., alias='$permissions')
    xfrom: str = Field(..., alias='from')
    to: str = Field(..., alias='to')
    usagestorage: float = Field(..., alias='usageStorage')
    usagetotalstorage: float = Field(..., alias='usageTotalStorage')
    usagefilesstorage: float = Field(..., alias='usageFilesStorage')
    usagedeploymentsstorage: float = Field(..., alias='usageDeploymentsStorage')
    usagebuildsstorage: float = Field(..., alias='usageBuildsStorage')
    usagedatabasesstorage: float = Field(..., alias='usageDatabasesStorage')
    usagefunctionsstorage: float = Field(..., alias='usageFunctionsStorage')
    usagesitesstorage: float = Field(..., alias='usageSitesStorage')
    usageusers: float = Field(..., alias='usageUsers')
    usageexecutions: float = Field(..., alias='usageExecutions')
    usagebandwidth: float = Field(..., alias='usageBandwidth')
    usagerealtime: float = Field(..., alias='usageRealtime')
    usagerealtimemessages: float = Field(..., alias='usageRealtimeMessages')
    usagerealtimebandwidth: float = Field(..., alias='usageRealtimeBandwidth')
    additionalmembers: float = Field(..., alias='additionalMembers')
    additionalmemberamount: float = Field(..., alias='additionalMemberAmount')
    additionalstorageamount: float = Field(..., alias='additionalStorageAmount')
    additionalusersamount: float = Field(..., alias='additionalUsersAmount')
    additionalexecutionsamount: float = Field(..., alias='additionalExecutionsAmount')
    additionalbandwidthamount: float = Field(..., alias='additionalBandwidthAmount')
    additionalrealtimeamount: float = Field(..., alias='additionalRealtimeAmount')
    plan: str = Field(..., alias='plan')
    amount: float = Field(..., alias='amount')
    breakdown: List[AggregationBreakdown] = Field(..., alias='breakdown')
    resources: List[UsageResources] = Field(..., alias='resources')

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
        if '$permissions' not in data and 'permissions' not in data:
            data['$permissions'] = []
        if 'from' not in data and 'xfrom' not in data:
            data['from'] = ''
        if 'to' not in data:
            data['to'] = ''
        if 'usageStorage' not in data and 'usagestorage' not in data:
            data['usageStorage'] = 0
        if 'usageTotalStorage' not in data and 'usagetotalstorage' not in data:
            data['usageTotalStorage'] = 0
        if 'usageFilesStorage' not in data and 'usagefilesstorage' not in data:
            data['usageFilesStorage'] = 0
        if 'usageDeploymentsStorage' not in data and 'usagedeploymentsstorage' not in data:
            data['usageDeploymentsStorage'] = 0
        if 'usageBuildsStorage' not in data and 'usagebuildsstorage' not in data:
            data['usageBuildsStorage'] = 0
        if 'usageDatabasesStorage' not in data and 'usagedatabasesstorage' not in data:
            data['usageDatabasesStorage'] = 0
        if 'usageFunctionsStorage' not in data and 'usagefunctionsstorage' not in data:
            data['usageFunctionsStorage'] = 0
        if 'usageSitesStorage' not in data and 'usagesitesstorage' not in data:
            data['usageSitesStorage'] = 0
        if 'usageUsers' not in data and 'usageusers' not in data:
            data['usageUsers'] = 0
        if 'usageExecutions' not in data and 'usageexecutions' not in data:
            data['usageExecutions'] = 0
        if 'usageBandwidth' not in data and 'usagebandwidth' not in data:
            data['usageBandwidth'] = 0
        if 'usageRealtime' not in data and 'usagerealtime' not in data:
            data['usageRealtime'] = 0
        if 'usageRealtimeMessages' not in data and 'usagerealtimemessages' not in data:
            data['usageRealtimeMessages'] = 0
        if 'usageRealtimeBandwidth' not in data and 'usagerealtimebandwidth' not in data:
            data['usageRealtimeBandwidth'] = 0
        if 'additionalMembers' not in data and 'additionalmembers' not in data:
            data['additionalMembers'] = 0
        if 'additionalMemberAmount' not in data and 'additionalmemberamount' not in data:
            data['additionalMemberAmount'] = 0
        if 'additionalStorageAmount' not in data and 'additionalstorageamount' not in data:
            data['additionalStorageAmount'] = 0
        if 'additionalUsersAmount' not in data and 'additionalusersamount' not in data:
            data['additionalUsersAmount'] = 0
        if 'additionalExecutionsAmount' not in data and 'additionalexecutionsamount' not in data:
            data['additionalExecutionsAmount'] = 0
        if 'additionalBandwidthAmount' not in data and 'additionalbandwidthamount' not in data:
            data['additionalBandwidthAmount'] = 0
        if 'additionalRealtimeAmount' not in data and 'additionalrealtimeamount' not in data:
            data['additionalRealtimeAmount'] = 0
        if 'plan' not in data:
            data['plan'] = ''
        if 'amount' not in data:
            data['amount'] = 0
        if 'breakdown' not in data:
            data['breakdown'] = []
        if 'resources' not in data:
            data['resources'] = []
        return data
