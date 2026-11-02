from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class UsageOrganizationProject(AppwriteModel):
    """
    OrganizationProject

    Attributes
    ----------
    projectid : str
        projectId
    bandwidth : float
        Aggregated stats for number of requests.
    users : float
        Aggregated stats for consumed bandwidth.
    executions : float
        Aggregated stats for function executions.
    databasesreads : float
        Aggregated stats for database reads.
    databaseswrites : float
        Aggregated stats for database writes.
    executionsmbseconds : float
        Aggregated stats for function executions in mb seconds.
    buildsmbseconds : float
        Aggregated stats for function builds in mb seconds.
    storage : float
        Aggregated stats for number of documents.
    authphonetotal : float
        Aggregated stats for phone authentication.
    authphoneestimate : float
        Aggregated stats for phone authentication estimated cost.
    databasesreadstotal : float
        Aggregated stats for total databases reads.
    databaseswritestotal : float
        Aggregated stats for total databases writes.
    imagetransformations : float
        Aggregated stats for file transformations.
    imagetransformationstotal : float
        Aggregated stats for total file transformations.
    screenshotsgenerated : float
        Aggregated stats for file transformations.
    screenshotsgeneratedtotal : float
        Aggregated stats for total file transformations.
    realtimeconnections : float
        Aggregated stats for realtime connections.
    realtimemessages : float
        Aggregated stats for realtime messages.
    realtimebandwidth : float
        Aggregated stats for realtime bandwidth.
    """

    projectid: str = Field(..., alias='projectId')
    bandwidth: float = Field(..., alias='bandwidth')
    users: float = Field(..., alias='users')
    executions: float = Field(..., alias='executions')
    databasesreads: float = Field(..., alias='databasesReads')
    databaseswrites: float = Field(..., alias='databasesWrites')
    executionsmbseconds: float = Field(..., alias='executionsMBSeconds')
    buildsmbseconds: float = Field(..., alias='buildsMBSeconds')
    storage: float = Field(..., alias='storage')
    authphonetotal: float = Field(..., alias='authPhoneTotal')
    authphoneestimate: float = Field(..., alias='authPhoneEstimate')
    databasesreadstotal: float = Field(..., alias='databasesReadsTotal')
    databaseswritestotal: float = Field(..., alias='databasesWritesTotal')
    imagetransformations: float = Field(..., alias='imageTransformations')
    imagetransformationstotal: float = Field(..., alias='imageTransformationsTotal')
    screenshotsgenerated: float = Field(..., alias='screenshotsGenerated')
    screenshotsgeneratedtotal: float = Field(..., alias='screenshotsGeneratedTotal')
    realtimeconnections: float = Field(..., alias='realtimeConnections')
    realtimemessages: float = Field(..., alias='realtimeMessages')
    realtimebandwidth: float = Field(..., alias='realtimeBandwidth')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'projectId' not in data and 'projectid' not in data:
            data['projectId'] = ''
        if 'bandwidth' not in data:
            data['bandwidth'] = 0
        if 'users' not in data:
            data['users'] = 0
        if 'databasesReads' not in data and 'databasesreads' not in data:
            data['databasesReads'] = 0
        if 'databasesWrites' not in data and 'databaseswrites' not in data:
            data['databasesWrites'] = 0
        if 'executionsMBSeconds' not in data and 'executionsmbseconds' not in data:
            data['executionsMBSeconds'] = 0
        if 'buildsMBSeconds' not in data and 'buildsmbseconds' not in data:
            data['buildsMBSeconds'] = 0
        if 'databasesReadsTotal' not in data and 'databasesreadstotal' not in data:
            data['databasesReadsTotal'] = 0
        if 'databasesWritesTotal' not in data and 'databaseswritestotal' not in data:
            data['databasesWritesTotal'] = 0
        if 'imageTransformations' not in data and 'imagetransformations' not in data:
            data['imageTransformations'] = 0
        if 'imageTransformationsTotal' not in data and 'imagetransformationstotal' not in data:
            data['imageTransformationsTotal'] = 0
        if 'screenshotsGenerated' not in data and 'screenshotsgenerated' not in data:
            data['screenshotsGenerated'] = 0
        if 'screenshotsGeneratedTotal' not in data and 'screenshotsgeneratedtotal' not in data:
            data['screenshotsGeneratedTotal'] = 0
        if 'realtimeConnections' not in data and 'realtimeconnections' not in data:
            data['realtimeConnections'] = 0
        if 'realtimeMessages' not in data and 'realtimemessages' not in data:
            data['realtimeMessages'] = 0
        if 'realtimeBandwidth' not in data and 'realtimebandwidth' not in data:
            data['realtimeBandwidth'] = 0
        return data
