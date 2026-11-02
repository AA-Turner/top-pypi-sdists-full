from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .metric import Metric
from .usage_organization_project import UsageOrganizationProject


class UsageOrganization(AppwriteModel):
    """
    Organization

    Attributes
    ----------
    bandwidth : List[Metric]
        Aggregated stats for number of requests.
    users : List[Metric]
        Aggregated stats for consumed bandwidth.
    executions : List[Metric]
        Aggregated stats for function executions.
    databasesreads : List[Metric]
        Aggregated stats for database reads.
    databaseswrites : List[Metric]
        Aggregated stats for database writes.
    imagetransformations : List[Metric]
        Aggregated stats for file transformations.
    imagetransformationstotal : float
        Aggregated stats for total file transformations.
    screenshotsgenerated : List[Metric]
        Aggregated stats for file transformations.
    screenshotsgeneratedtotal : float
        Aggregated stats for total file transformations.
    userstotal : float
        Aggregated stats for total users.
    executionstotal : float
        Aggregated stats for total executions.
    executionsmbsecondstotal : float
        Aggregated stats for function executions in mb seconds.
    buildsmbsecondstotal : float
        Aggregated stats for function builds in mb seconds.
    filesstoragetotal : float
        Aggregated stats for total file storage.
    buildsstoragetotal : float
        Aggregated stats for total builds storage.
    deploymentsstoragetotal : float
        Aggregated stats for total deployments storage.
    databasesstoragetotal : float
        Aggregated stats for total databases storage.
    databasesreadstotal : float
        Aggregated stats for total databases  reads.
    databaseswritestotal : float
        Aggregated stats for total databases  writes.
    backupsstoragetotal : float
        Aggregated stats for total backups storage.
    avatarsstoragetotal : float
        Aggregated stats for total custom user photos storage.
    storagetotal : float
        Aggregated stats for total storage.
    authphonetotal : float
        Aggregated stats for total auth phone.
    authphoneestimate : float
        Aggregated stats for total auth phone estimation.
    projects : List[UsageOrganizationProject]
        Aggregated stats for each projects.
    realtimeconnections : List[Metric]
        Aggregated stats for realtime connections.
    realtimeconnectionstotal : float
        Aggregated stats for total realtime connections.
    realtimemessages : List[Metric]
        Aggregated stats for realtime messages.
    realtimemessagestotal : float
        Aggregated stats for total realtime messages.
    realtimebandwidth : List[Metric]
        Aggregated stats for realtime bandwidth.
    realtimebandwidthtotal : float
        Aggregated stats for total realtime bandwidth.
    """

    bandwidth: List[Metric] = Field(..., alias='bandwidth')
    users: List[Metric] = Field(..., alias='users')
    executions: List[Metric] = Field(..., alias='executions')
    databasesreads: List[Metric] = Field(..., alias='databasesReads')
    databaseswrites: List[Metric] = Field(..., alias='databasesWrites')
    imagetransformations: List[Metric] = Field(..., alias='imageTransformations')
    imagetransformationstotal: float = Field(..., alias='imageTransformationsTotal')
    screenshotsgenerated: List[Metric] = Field(..., alias='screenshotsGenerated')
    screenshotsgeneratedtotal: float = Field(..., alias='screenshotsGeneratedTotal')
    userstotal: float = Field(..., alias='usersTotal')
    executionstotal: float = Field(..., alias='executionsTotal')
    executionsmbsecondstotal: float = Field(..., alias='executionsMBSecondsTotal')
    buildsmbsecondstotal: float = Field(..., alias='buildsMBSecondsTotal')
    filesstoragetotal: float = Field(..., alias='filesStorageTotal')
    buildsstoragetotal: float = Field(..., alias='buildsStorageTotal')
    deploymentsstoragetotal: float = Field(..., alias='deploymentsStorageTotal')
    databasesstoragetotal: float = Field(..., alias='databasesStorageTotal')
    databasesreadstotal: float = Field(..., alias='databasesReadsTotal')
    databaseswritestotal: float = Field(..., alias='databasesWritesTotal')
    backupsstoragetotal: float = Field(..., alias='backupsStorageTotal')
    avatarsstoragetotal: float = Field(..., alias='avatarsStorageTotal')
    storagetotal: float = Field(..., alias='storageTotal')
    authphonetotal: float = Field(..., alias='authPhoneTotal')
    authphoneestimate: float = Field(..., alias='authPhoneEstimate')
    projects: List[UsageOrganizationProject] = Field(..., alias='projects')
    realtimeconnections: List[Metric] = Field(..., alias='realtimeConnections')
    realtimeconnectionstotal: float = Field(..., alias='realtimeConnectionsTotal')
    realtimemessages: List[Metric] = Field(..., alias='realtimeMessages')
    realtimemessagestotal: float = Field(..., alias='realtimeMessagesTotal')
    realtimebandwidth: List[Metric] = Field(..., alias='realtimeBandwidth')
    realtimebandwidthtotal: float = Field(..., alias='realtimeBandwidthTotal')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'bandwidth' not in data:
            data['bandwidth'] = []
        if 'users' not in data:
            data['users'] = []
        if 'executions' not in data:
            data['executions'] = []
        if 'databasesReads' not in data and 'databasesreads' not in data:
            data['databasesReads'] = []
        if 'databasesWrites' not in data and 'databaseswrites' not in data:
            data['databasesWrites'] = []
        if 'imageTransformations' not in data and 'imagetransformations' not in data:
            data['imageTransformations'] = []
        if 'imageTransformationsTotal' not in data and 'imagetransformationstotal' not in data:
            data['imageTransformationsTotal'] = 0
        if 'screenshotsGenerated' not in data and 'screenshotsgenerated' not in data:
            data['screenshotsGenerated'] = []
        if 'screenshotsGeneratedTotal' not in data and 'screenshotsgeneratedtotal' not in data:
            data['screenshotsGeneratedTotal'] = 0
        if 'usersTotal' not in data and 'userstotal' not in data:
            data['usersTotal'] = 0
        if 'executionsTotal' not in data and 'executionstotal' not in data:
            data['executionsTotal'] = 0
        if 'executionsMBSecondsTotal' not in data and 'executionsmbsecondstotal' not in data:
            data['executionsMBSecondsTotal'] = 0
        if 'buildsMBSecondsTotal' not in data and 'buildsmbsecondstotal' not in data:
            data['buildsMBSecondsTotal'] = 0
        if 'filesStorageTotal' not in data and 'filesstoragetotal' not in data:
            data['filesStorageTotal'] = 0
        if 'buildsStorageTotal' not in data and 'buildsstoragetotal' not in data:
            data['buildsStorageTotal'] = 0
        if 'deploymentsStorageTotal' not in data and 'deploymentsstoragetotal' not in data:
            data['deploymentsStorageTotal'] = 0
        if 'databasesStorageTotal' not in data and 'databasesstoragetotal' not in data:
            data['databasesStorageTotal'] = 0
        if 'databasesReadsTotal' not in data and 'databasesreadstotal' not in data:
            data['databasesReadsTotal'] = 0
        if 'databasesWritesTotal' not in data and 'databaseswritestotal' not in data:
            data['databasesWritesTotal'] = 0
        if 'backupsStorageTotal' not in data and 'backupsstoragetotal' not in data:
            data['backupsStorageTotal'] = 0
        if 'avatarsStorageTotal' not in data and 'avatarsstoragetotal' not in data:
            data['avatarsStorageTotal'] = 0
        if 'storageTotal' not in data and 'storagetotal' not in data:
            data['storageTotal'] = 0
        if 'authPhoneTotal' not in data and 'authphonetotal' not in data:
            data['authPhoneTotal'] = 0
        if 'authPhoneEstimate' not in data and 'authphoneestimate' not in data:
            data['authPhoneEstimate'] = 0
        if 'projects' not in data:
            data['projects'] = []
        if 'realtimeConnections' not in data and 'realtimeconnections' not in data:
            data['realtimeConnections'] = []
        if 'realtimeConnectionsTotal' not in data and 'realtimeconnectionstotal' not in data:
            data['realtimeConnectionsTotal'] = 0
        if 'realtimeMessages' not in data and 'realtimemessages' not in data:
            data['realtimeMessages'] = []
        if 'realtimeMessagesTotal' not in data and 'realtimemessagestotal' not in data:
            data['realtimeMessagesTotal'] = 0
        if 'realtimeBandwidth' not in data and 'realtimebandwidth' not in data:
            data['realtimeBandwidth'] = []
        if 'realtimeBandwidthTotal' not in data and 'realtimebandwidthtotal' not in data:
            data['realtimeBandwidthTotal'] = 0
        return data
