from enum import Enum, auto
from typing import List

from acceldata_sdk.constants import RuleExecutionStatus
from acceldata_sdk.models.asset import Asset
from acceldata_sdk.models.datasource import DataSource
from acceldata_sdk.models.threshold import RuleLevelThresholdConfiguration, parse_rule_threshold_configuration


class ExecutionPeriod(Enum):
    Last15minutes = auto()
    Last30minutes = auto()
    Last1hour = auto()
    Last3hours = auto()
    Last6hours = auto()
    Last12hours = auto()
    Last24hours = auto()
    Today = auto()
    Yesterday = auto()
    Last7days = auto()
    Thismonth = auto()
    Last1month = auto()
    Last3month = auto()


class RuleType(Enum):
    DATA_QUALITY = 'DATA-QUALITY'
    RECONCILIATION = 'RECONCILIATION'
    EQUALITY = 'EQUALITY'
    DATA_DRIFT = 'DATA-DRIFT'
    SCHEMA_DRIFT = 'SCHEMA_DRIFT'
    DATA_CADENCE = 'DATA_CADENCE'


class RuleExecutionMode(Enum):
    SCHEDULED = auto()
    MANUAL = auto()
    WEBHOOK = auto()
    API = auto()


class RuleResultStatus(Enum):
    STARTED = auto()
    RUNNING = auto()
    ERRORED = auto()
    WARNING = auto()
    SUCCESSFUL = auto()
    ABORTED = auto()
    WAITING = auto()


class PolicyExecutionType(Enum):
    SAMPLE = auto()
    FULL = auto()
    INCREMENTAL = auto()


class LivyExecutorConfig:
    def __init__(self, executorMemory=None, executorCores=None, numExecutors=None, driverCores=None, driverMemory=None,
                 *args, **kwargs):
        self.executorMemory = executorMemory
        self.executorCores = executorCores
        self.numExecutors = numExecutors
        self.driverCores = driverCores
        self.driverMemory = driverMemory

    def __repr__(self):
        return f"LivyExecutorConfig({self.__dict__})"


class DataprocSparkResourceConfig:
    def __init__(self, numWorkerNodes=None, numMasterNodes=None, clusterWorkerType=None, clusterMasterType=None, *args,
                 **kwargs):
        self.numWorkerNodes = numWorkerNodes
        self.numMasterNodes = numMasterNodes
        self.clusterWorkerType = clusterWorkerType
        self.clusterMasterType = clusterMasterType

    def __repr__(self):
        return f"DataprocSparkResourceConfig({self.__dict__})"


class YunikornSparkResourceConfig:
    def __init__(self, executorMemory=None, executorCores=None, maxExecutors=None, minExecutors=None,
                 executorMemoryOverhead=None, driverMemory=None,
                 driverCores=None, driverMemoryOverhead=None, driverMemoryOverheadFactor=None,
                 executorMemoryOverheadFactor=None, *args, **kwargs):
        self.executorMemory = executorMemory
        self.executorCores = executorCores
        self.maxExecutors = maxExecutors
        self.minExecutors = minExecutors
        self.executorMemoryOverhead = executorMemoryOverhead
        self.driverMemory = driverMemory
        self.driverCores = driverCores
        self.driverMemoryOverhead = driverMemoryOverhead
        self.driverMemoryOverheadFactor = driverMemoryOverheadFactor
        self.executorMemoryOverheadFactor = executorMemoryOverheadFactor


class DataBricksExecutorConfig:
    def __init__(self, minWorkers=None, maxWorkers=None, clusterWorkerType=None, clusterDriverType=None, *args,
                 **kwargs):
        self.minWorkers = minWorkers
        self.maxWorkers = maxWorkers
        self.clusterWorkerType = clusterWorkerType
        self.clusterDriverType = clusterDriverType

    def __repr__(self):
        return f"DataBricksExecutorConfig({self.__dict__})"


class ExecutorConfig:
    def __init__(self, livy=None, databricks=None, dataproc=None, yunikorn=None, additionalConfiguration=None, *args,
                 **kwargs):
        if isinstance(livy, dict):
            self.livy = LivyExecutorConfig(**livy)
        else:
            self.livy = livy
        if isinstance(databricks, dict):
            self.databricks = DataBricksExecutorConfig(**databricks)
        else:
            self.databricks = databricks
        if isinstance(dataproc, dict):
            self.dataproc = DataprocSparkResourceConfig(**databricks)
        else:
            self.dataproc = dataproc
        if isinstance(yunikorn, dict):
            self.yunikorn = YunikornSparkResourceConfig(**yunikorn)
        else:
            self.yunikorn = yunikorn
        self.additionalConfiguration = additionalConfiguration

    def __repr__(self):
        return f"ExecutorConfig({self.__dict__})"


class SparkResourceConfig:
    def __init__(self, livy=None, databricks=None, dataproc=None, yunikorn=None, additionalConfiguration=None, *args,
                 **kwargs):
        if isinstance(livy, dict):
            self.livy = LivyExecutorConfig(**livy)
        else:
            self.livy = livy
        if isinstance(databricks, dict):
            self.databricks = DataBricksExecutorConfig(**databricks)
        else:
            self.databricks = databricks
        if isinstance(dataproc, dict):
            self.dataproc = DataprocSparkResourceConfig(**databricks)
        else:
            self.dataproc = dataproc
        if isinstance(yunikorn, dict):
            self.yunikorn = YunikornSparkResourceConfig(**yunikorn)
        else:
            self.yunikorn = yunikorn
        self.additionalConfiguration = additionalConfiguration

    def __repr__(self):
        return f"ExecutorConfig({self.__dict__})"


class RuleExecutionSummary:
    def __init__(self, ruleId=None, executionMode=None, executionStatus=None, resultStatus=None, startedAt=None,
                 executionType=None, thresholdLevel=None, ruleVersion=None, id=None, ruleName=None, ruleType=None,
                 lastMarker=None, leftLastMarker=None, rightLastMarker=None, executionError=None, finishedAt=None,
                 resetPoint=None, persistencePath=None, resultPersistencePath=None, executorConfig=None,
                 markerConfig=None, leftMarkerConfig=None, rightMarkerConfig=None, dataPersistenceEnabled=None,
                 isProtectedResource=None, sparkResourceConfig=None, *args, **kwargs):

        self.ruleId = ruleId
        self.id = id
        self.ruleName = ruleName
        if isinstance(ruleType, dict):
            self.ruleType = RuleType(**ruleType)
        else:
            self.ruleType = ruleType
        if isinstance(executionMode, dict):
            self.executionMode = RuleExecutionMode(**executionMode)
        else:
            self.executionMode = executionMode
        if isinstance(executionStatus, dict):
            self.executionStatus = RuleExecutionStatus(**executionStatus)
        else:
            self.executionStatus = executionStatus
        if isinstance(resultStatus, dict):
            self.resultStatus = RuleResultStatus(**resultStatus)
        else:
            self.resultStatus = resultStatus

        self.lastMarker = lastMarker
        self.leftLastMarker = leftLastMarker
        self.rightLastMarker = rightLastMarker
        self.executionError = executionError
        self.startedAt = startedAt
        self.finishedAt = finishedAt
        self.thresholdLevel = (
            parse_rule_threshold_configuration(thresholdLevel)
            if isinstance(thresholdLevel, dict)
            else thresholdLevel
        )
        self.resetPoint = resetPoint
        self.persistencePath = persistencePath
        self.resultPersistencePath = resultPersistencePath
        self.ruleVersion = ruleVersion
        if isinstance(executorConfig, dict):
            self.executorConfig = ExecutorConfig(**executorConfig)
        else:
            self.executorConfig = executorConfig

        if isinstance(sparkResourceConfig, dict):
            self.sparkResourceConfig = SparkResourceConfig(**sparkResourceConfig)
        elif sparkResourceConfig is not None:
            self.sparkResourceConfig = sparkResourceConfig
        else:
            self.sparkResourceConfig = None

        self.markerConfig = markerConfig
        self.leftMarkerConfig = leftMarkerConfig
        self.rightMarkerConfig = rightMarkerConfig
        if isinstance(executionType, dict):
            self.executionType = PolicyExecutionType(**executionType)
        else:
            self.executionType = executionType
        self.dataPersistenceEnabled = dataPersistenceEnabled
        self.isProtectedResource = isProtectedResource

    def __repr__(self):
        return f"RuleExecutionSummary({self.__dict__})"


class RuleExecutionResult:
    def __init__(self, status, description=None, successCount=None, failureCount=None, qualityScore=None, *args,
                 **kwargs):
        if isinstance(status, dict):
            self.status = status
        else:
            self.status = status
        self.description = description
        self.successCount = successCount
        self.failureCount = failureCount
        self.qualityScore = qualityScore


class RuleItemResult:
    def __init__(self, id, ruleItemId, threshold, weightage, isWarning, resultPercent=None, success=None, error=None,
                 *args, **kwargs):
        self.id = id
        self.ruleItemId = ruleItemId
        self.threshold = threshold
        self.resultPercent = resultPercent
        self.success = success
        self.error = error
        self.weightage = weightage
        self.isWarning = isWarning

    def __repr__(self):
        return f"RuleItemResult({self.__dict__})"


class RuleResult:
    def __init__(self, execution: RuleExecutionSummary = None, items: [RuleItemResult] = None, meta=None,
                 result: RuleExecutionResult = None, *args, **kwargs):
        self.execution = execution
        self.items = items
        self.meta = meta
        self.result = result

    def __repr__(self):
        return f"RuleResult({self.__dict__})"


class PolicyFilter:
    def __init__(self, period: ExecutionPeriod = None, tags: str = None, lastExecutionResult: RuleResultStatus = None,
                 asset: List[Asset] = None, policyType: RuleType = None, enable: bool = None, active: bool = None,
                 data_source: List[DataSource] = None, *args, **kwargs):
        self.period = period
        self.tags = tags
        self.lastExecutionResult = lastExecutionResult
        self.assets = asset
        self.data_sources = data_source
        self.policyType = policyType
        self.enable = enable
        self.active = active

    def __repr__(self):
        return f"PolicyFilter({self.__dict__})"
