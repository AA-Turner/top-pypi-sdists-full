from enum import Enum, auto
from dataclasses import dataclass, asdict
from typing import List

from acceldata_sdk.models.ruleExecutionResult import RuleItemResult, RuleExecutionSummary, RuleResult
from acceldata_sdk.models.ruleExecutionResult import ExecutorConfig, SparkResourceConfig, RuleExecutionResult
from acceldata_sdk.models.threshold import RuleLevelThresholdConfiguration, parse_rule_threshold_configuration
from acceldata_sdk.models.rule import ShortSegment, Label, BackingAsset, RuleTag, PolicyGroup, \
    RuleResource, RuleExecution
from acceldata_sdk.models.common_types import PolicyExecutionRequest
from acceldata_sdk.constants import FailureStrategy, PolicyType

import logging

logger = logging.getLogger('reconciliationrule')
logger.setLevel(logging.INFO)

class ReconRuleExecutionSummary(RuleExecutionSummary):
    def __init__(self, ruleId, executionMode, executionStatus, resultStatus, startedAt, executionType,
                 isProtectedResource, thresholdLevel, ruleVersion, id=None, ruleName=None, ruleType=None,
                 lastMarker=None, leftLastMarker=None, rightLastMarker=None, executionError=None, finishedAt=None,
                 resetPoint=None, persistencePath=None, resultPersistencePath=None, executorConfig=None,
                 markerConfig=None, leftMarkerConfig=None, rightMarkerConfig=None, dataPersistenceEnabled=None,
                 sparkResourceConfig=None, *args, **kwargs):
        super().__init__(ruleId, executionMode, executionStatus, resultStatus, startedAt, executionType, thresholdLevel,
                         ruleVersion, id, ruleName, ruleType, lastMarker, leftLastMarker, rightLastMarker,
                         executionError, finishedAt, resetPoint, persistencePath, resultPersistencePath, executorConfig,
                         sparkResourceConfig, markerConfig, leftMarkerConfig, rightMarkerConfig, dataPersistenceEnabled,
                         isProtectedResource)

    def __repr__(self):
        return f"ReconRuleExecutionSummary({self.__dict__})"

class ReconciliationRuleExecutionResult(RuleExecutionResult):
    def __init__(
            self,
            status,
            description=None,
            successCount=None,
            failureCount=None,
            leftRows=None,
            rightRows=None,
            qualityScore=None,
            executionStatus=None,
            ruleExecutionType=None,
            *args,
            **kwargs
    ):
        # Call base class initializer once
        super().__init__(status=status, ruleExecutionType=ruleExecutionType)

        # Set reconciliation-specific fields
        self.description = description
        self.successCount = successCount
        self.failureCount = failureCount
        self.leftRows = leftRows
        self.rightRows = rightRows
        self.qualityScore = qualityScore
        self.executionStatus = executionStatus

    def __repr__(self):
        return f"ReconciliationRuleExecutionResult({self.__dict__})"



class MappingOperation(Enum):
    EQ = auto()
    NOT_EQ = auto()
    GTE = auto()
    GT = auto()
    LTE = auto()
    LT = auto()


class ColumnMapping:
    def __init__(self, leftColumnName, operation, rightColumnName, useForJoining, isJoinColumnUsedForMeasure,
                 ignoreNullValues, weightage, ruleVersion,isWarning, businessExplanation=None, id=None,
                 reconciliationRuleId=None, deletedAt=None, labels=None, *args, **kwargs):
        self.id = id
        self.leftColumnName = leftColumnName
        if isinstance(operation, dict):
            self.operation = MappingOperation(**operation)
        else:
            self.operation = operation
        self.rightColumnName = rightColumnName
        self.useForJoining = useForJoining
        self.isJoinColumnUsedForMeasure = isJoinColumnUsedForMeasure
        self.ignoreNullValues = ignoreNullValues
        self.weightage = weightage
        self.ruleVersion = ruleVersion
        self.isWarning = isWarning
        self.businessExplanation = businessExplanation
        self.reconciliationRuleId = reconciliationRuleId
        self.deletedAt = deletedAt
        self.labels = list()
        for obj in labels:
            if isinstance(obj, dict):
                self.labels.append(Label(**obj))
            else:
                self.labels.append(obj)

    def __repr__(self):
        return f"ColumnMapping({self.__dict__})"


class ReconciliationRuleItemResult(RuleItemResult):
    def __init__(self, id, ruleItemId, threshold, weightage, isRowMatchMeasure, isWarning, columnMapping=None,
                 resultPercent=None, success=None, error=None, *args, **kwargs):
        super().__init__(id, ruleItemId, threshold, weightage, isWarning, resultPercent, success, error)
        self.isRowMatchMeasure = isRowMatchMeasure
        if isinstance(columnMapping, dict):
            self.columnMapping = ColumnMapping(**columnMapping)
        else:
            self.columnMapping = columnMapping

    def __repr__(self):
        return f"ReconciliationRuleItemResult({self.__dict__})"


class ReconciliationExecutionResult(RuleResult):
    def __init__(self, execution, items, meta=None, result=None, *args, **kwargs):
        if isinstance(execution, dict):
            self.execution = ReconRuleExecutionSummary(**execution)
        else:
            self.execution = execution
        if isinstance(result, dict):
            self.result = ReconciliationRuleExecutionResult(**result)
        else:
            self.result = result
        self.items = list()
        for obj in items:
            if isinstance(obj, dict):
                self.items.append(ReconciliationRuleItemResult(**obj))
            else:
                self.items.append(obj)
        self.meta = meta
        self.executionId = self.execution.id

    def __repr__(self):
        return f"ReconciliationExecutionResult({self.__dict__})"


class ReconciliationMeasurementType(Enum):
    EQUALITY = 'EQUALITY'
    COUNT = 'COUNT'
    PROFILE_EQUALITY = 'PROFILE_EQUALITY'
    HASHED_EQUALITY = 'HASHED_EQUALITY'
    TIMELINESS = 'TIMELINESS'
    CUSTOM = 'CUSTOM'


@dataclass
class Item:
    id = None
    ruleId = None
    measurementType = None
    executionOrder = None
    version = None

    def __init__(self,
                 id=None,
                 ruleId=None,
                 measurementType = None,
                 executionOrder = None,
                 version = None, *args, **kwargs
                 ):
        self.ruleId = ruleId
        self.id = id
        self.executionOrder = executionOrder
        self.version = version
        if isinstance(measurementType, dict):
            self.measurementType = ReconciliationMeasurementType(**measurementType)
        else:
            self.measurementType = measurementType


class ReconciliationRuleDetails:
    def __init__(self, ruleId, leftBackingAssetId, rightBackingAssetId, columnMappings, timeSecondsOffset,
                 items, isSegmented, segments, delayInMinutes=None, ruleVersion=None,
                 leftFilter=None, rightFilter=None, leftEngineType=None, rightEngineType=None,
                 isCompositeRule=False, continueExecutionOnFailure=False,
                 leftSparkSQLFilterType="STATIC", leftSparkSQLDynamicFilterVariableMapping=None,
                 leftSparkFilterSelectedColumns=None, rightSparkSQLFilterType="STATIC",
                 rightSparkSQLDynamicFilterVariableMapping=None, rightSparkFilterSelectedColumns=None,
                 id=None, *args, **kwargs):
        self.id = id
        self.ruleId = ruleId
        self.leftBackingAssetId = leftBackingAssetId
        self.rightBackingAssetId = rightBackingAssetId
        self.timeSecondsOffset = timeSecondsOffset
        self.delayInMinutes = delayInMinutes
        self.ruleVersion = ruleVersion
        self.leftFilter = leftFilter
        self.rightFilter = rightFilter
        self.leftEngineType = leftEngineType
        self.rightEngineType = rightEngineType
        self.isCompositeRule = isCompositeRule
        self.continueExecutionOnFailure = continueExecutionOnFailure
        self.leftSparkSQLFilterType = leftSparkSQLFilterType
        self.leftSparkSQLDynamicFilterVariableMapping = leftSparkSQLDynamicFilterVariableMapping
        self.leftSparkFilterSelectedColumns = leftSparkFilterSelectedColumns or []
        self.rightSparkSQLFilterType = rightSparkSQLFilterType
        self.rightSparkSQLDynamicFilterVariableMapping = rightSparkSQLDynamicFilterVariableMapping
        self.rightSparkFilterSelectedColumns = rightSparkFilterSelectedColumns or []
        self.items = [Item(**obj) if isinstance(obj, dict) else obj for obj in items]
        self.isSegmented = isSegmented
        self.segments = [ShortSegment(**obj) if isinstance(obj, dict) else obj for obj in (segments or [])]
        self.columnMappings = []
        if columnMappings is not None:
            for obj in columnMappings:
                if isinstance(obj, dict):
                    self.columnMappings.append(ColumnMapping(**obj))
                else:
                    self.columnMappings.append(obj)

    def __repr__(self):
        return f"ReconciliationRuleDetails({self.__dict__})"



class ChannelType(Enum):
    JIRA = 'JIRA'
    EMAIL = 'EMAIL'
    SLACK = 'SLACK'
    HANGOUT = 'HANGOUT'
    WEBHOOK = 'WEBHOOK'


class NotifyOn(Enum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    SUCCESS = 'SUCCESS'
    ALL = 'ALL'


@dataclass
class NotificationPayload:
    configuredList: List
    notifyOn: List[NotifyOn]
    tags: List[str] = None


class ReconciliationRule:
    def __init__(self, name=None, description=None, type=None, enabled=None, schedule=None, scheduled=None,
                 notificationChannels=None, leftBackingAsset=None, rightBackingAsset=None, timeSecondsOffset=None,
                 createdAt=None, updatedAt=None, thresholdLevel=None, archived=None, archivalReason=None,
                 tenantId=None, createdBy=None, lastUpdatedBy=None, tags=None, version=None, executorConfig=None,
                 labels=None, isProtectedResource=None, policyGroups=None, id=None, sparkResourceConfig=None,
                 timeZone="GMT", executionTimeoutInMinutes=None, totalExecutionTimeoutInMinutes=None,
                 analyticsPipelineId=None, autoCreated=False, delayInMinutes=None, leftFilter=None,
                 leftSparkSQLFilterType="STATIC", leftSparkSQLDynamicFilterVariableMapping=None,
                 leftSparkFilterSelectedColumns=None, rightFilter=None, rightSparkSQLFilterType="STATIC",
                 rightSparkSQLDynamicFilterVariableMapping=None, rightSparkFilterSelectedColumns=None,
                 engineType=None, rightEngineType=None, resourceStrategyType=None, autoRetryEnabled=False,
                 selectedResourceInventory=None, *args, **kwargs):

        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.enabled = enabled
        self.schedule = schedule
        self.scheduled = scheduled
        self.notificationChannels = notificationChannels
        self.leftBackingAsset = BackingAsset(**leftBackingAsset) if isinstance(leftBackingAsset, dict) else leftBackingAsset
        self.rightBackingAsset = BackingAsset(**rightBackingAsset) if isinstance(rightBackingAsset, dict) else rightBackingAsset
        self.timeSecondsOffset = timeSecondsOffset
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.thresholdLevel = (
            parse_rule_threshold_configuration(thresholdLevel)
            if isinstance(thresholdLevel, dict)
            else thresholdLevel
        )
        self.archived = archived
        self.archivalReason = archivalReason
        self.tenantId = tenantId
        self.createdBy = createdBy
        self.lastUpdatedBy = lastUpdatedBy
        self.tags = [RuleTag(**obj) if isinstance(obj, dict) else obj for obj in (tags or [])]
        self.version = version
        self.executorConfig = ExecutorConfig(**executorConfig) if isinstance(executorConfig, dict) else executorConfig
        self.sparkResourceConfig = SparkResourceConfig(**sparkResourceConfig) if isinstance(sparkResourceConfig, dict) else sparkResourceConfig
        self.labels = [Label(**obj) if isinstance(obj, dict) else obj for obj in (labels or [])]
        self.isProtectedResource = isProtectedResource
        self.policyGroups = [PolicyGroup(**obj) if isinstance(obj, dict) else obj for obj in (policyGroups or [])]
        self.timeZone = timeZone
        self.executionTimeoutInMinutes = executionTimeoutInMinutes
        self.totalExecutionTimeoutInMinutes = totalExecutionTimeoutInMinutes
        self.analyticsPipelineId = analyticsPipelineId
        self.autoCreated = autoCreated
        self.delayInMinutes = delayInMinutes
        self.leftFilter = leftFilter
        self.leftSparkSQLFilterType = leftSparkSQLFilterType
        self.leftSparkSQLDynamicFilterVariableMapping = leftSparkSQLDynamicFilterVariableMapping
        self.leftSparkFilterSelectedColumns = leftSparkFilterSelectedColumns or []
        self.rightFilter = rightFilter
        self.rightSparkSQLFilterType = rightSparkSQLFilterType
        self.rightSparkSQLDynamicFilterVariableMapping = rightSparkSQLDynamicFilterVariableMapping
        self.rightSparkFilterSelectedColumns = rightSparkFilterSelectedColumns or []
        self.engineType = engineType
        self.rightEngineType = rightEngineType
        self.resourceStrategyType = resourceStrategyType
        self.autoRetryEnabled = autoRetryEnabled
        self.selectedResourceInventory = selectedResourceInventory

    def __repr__(self):
        return f"ReconciliationRule({self.__dict__})"


class ReconciliationRuleResource(RuleResource):
    def __init__(self, rule, details, client=None, *args, **kwargs):
        if isinstance(rule, dict):
            self.rule = ReconciliationRule(**rule)
        else:
            self.rule = rule
        if isinstance(details, dict):
            self.details = ReconciliationRuleDetails(**details)
        else:
            self.details = details
        self.client = client

    def execute(self, sync=True, incremental=False, failure_strategy: FailureStrategy = FailureStrategy.DoNotFail,
                policy_execution_request: PolicyExecutionRequest = None) -> RuleExecution:
        logger.info(f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}")
        return self.client.execute_rule(PolicyType.RECONCILIATION, self.rule.id, sync, incremental, failure_strategy,
                                        policy_execution_request)

    def get_executions(self, page=0, size=25, sortBy='finishedAt:DESC'):
        return self.client.policy_executions(self.rule.id, PolicyType.RECONCILIATION, page, size, sortBy)

    def __repr__(self):
        return f"ReconciliationRuleResource({self.__dict__})"
