from acceldata_sdk.models.ruleExecutionResult import RuleItemResult, RuleResult, RuleExecutionSummary
from enum import Enum
from dataclasses import dataclass
from typing import List
from acceldata_sdk.models.rule import (ShortSegment, Label, BackingAsset, RuleTag, PolicyGroup, RuleResource, RuleExecution, RuleExecutionResult)
from acceldata_sdk.models.common_types import PolicyExecutionRequest
from acceldata_sdk.models.threshold import parse_rule_threshold_configuration

from acceldata_sdk.models.ruleExecutionResult import SparkResourceConfig, RuleExecutionResult
from acceldata_sdk.constants import FailureStrategy, PolicyType


import logging

logger = logging.getLogger('dqrule')
logger.setLevel(logging.INFO)

class RootCauseAnalysis:
    def __init__(self, key, bad, good, badFraction, goodFraction, *args, **kwargs):
        self.key = key
        self.bad = bad
        self.good = good
        self.badFraction = badFraction
        self.goodFraction = goodFraction

    def __repr__(self):
        return f"RootCauseAnalysis({self.__dict__})"


class DataQualityRuleExecutionResult(RuleExecutionResult):
    def __init__(
            self,
            status,
            description=None,
            successCount=None,
            failureCount=None,
            rows=None,
            failedRows=None,
            warningRows=None,
            qualityScore=None,
            rca=None,
            executionStatus=None,
            leftRowsScanned=None,
            rightRowsScanned=None,
            ruleExecutionType=None,
            *args,
            **kwargs
    ):
        # Initialize base class
        super().__init__(status=status, ruleExecutionType=ruleExecutionType)

        # DQ-specific fields
        self.description = description
        self.successCount = successCount
        self.failureCount = failureCount
        self.rows = rows
        self.failedRows = failedRows
        self.warningRows = warningRows
        self.qualityScore = qualityScore
        self.executionStatus = executionStatus
        self.leftRowsScanned = leftRowsScanned
        self.rightRowsScanned = rightRowsScanned

        # Handle RCA details (could be list or single object)
        if isinstance(rca, list):
            self.rca = [
                RootCauseAnalysis(**item) if isinstance(item, dict) else item
                for item in rca
            ]
        elif isinstance(rca, dict):
            self.rca = [RootCauseAnalysis(**rca)]
        else:
            self.rca = rca

    def __repr__(self):
        return f"DataQualityRuleExecutionResult({self.__dict__})"


class DataQualityRuleItemResult(RuleItemResult):
    def __init__(self, id, ruleItemId, threshold, weightage, isWarning=None, resultPercent=None, businessItemId=None,
                 success=None, error=None, *args, **kwargs):
        super().__init__(id, ruleItemId, threshold, weightage, isWarning, resultPercent, success, error)
        self.businessItemId = businessItemId

    def __repr__(self):
        return f"DataQualityRuleItemResult({self.__dict__})"


class DataQualityExecutionResult(RuleResult):
    def __init__(self, execution, items, meta=None, result=None, *args, **kwargs):
        if isinstance(execution, dict):
            self.execution = RuleExecutionSummary(**execution)
        else:
            self.execution = execution
        if isinstance(result, dict):
            self.result = DataQualityRuleExecutionResult(**result)
        else:
            self.result = result
        self.items = list()
        for obj in items:
            if isinstance(obj, dict):
                self.items.append(DataQualityRuleItemResult(**obj))
            else:
                self.items.append(obj)
        self.meta = meta
        self.executionId = self.execution.id

    def __repr__(self):
        return f"DataQualityExecutionResult({self.__dict__})"


class DataQualityMeasurementType(Enum):
    MISSING_VALUES = 'MISSING_VALUES'
    DATATYPE_MATCH = 'DATATYPE_MATCH'
    REGEX_MATCH = 'REGEX_MATCH'
    VALUES_IN_LIST = 'VALUES_IN_LIST'
    DISTINCTNESS_CHECK = 'DISTINCTNESS_CHECK'
    DUPLICATE_ROWS_CHECK = 'DUPLICATE_ROWS_CHECK'
    PRECISION_SCALE_CHECK = 'PRECISION_SCALE_CHECK'
    BUSINESS_MEASURE = 'BUSINESS_MEASURE'
    TAG_MATCH = 'TAG_MATCH'
    RANGE_MATCH = 'RANGE_MATCH'
    SIZE_CHECK = 'SIZE_CHECK'
    CUSTOM = 'CUSTOM'
    UDF_PREDICATE = 'UDF_PREDICATE'


@dataclass
class Item:
    id = None
    ruleId = None
    measurementType = None
    executionOrder = None
    columnName = None
    value = None
    ruleExpression = None
    resultThreshold = None
    weightage = None
    ruleVersion = None
    businessExplanation = None
    labels = None
    isWarning = None

    def __init__(self,
                 id=None,
                 ruleId=None,
                 measurementType=None,
                 executionOrder=None,
                 columnName=None,
                 value=None,
                 ruleExpression=None,
                 resultThreshold=None,
                 weightage=None,
                 ruleVersion=None,
                 businessExplanation=None,
                 labels=None,
                 isWarning=None,
                 *args, **kwargs):
        self.ruleId = ruleId
        self.id = id
        if isinstance(measurementType, dict):
            self.measurementType = DataQualityMeasurementType(**measurementType)
        else:
            self.measurementType = measurementType
        self.executionOrder = executionOrder
        self.columnName = columnName
        self.value = value
        self.ruleExpression = ruleExpression
        self.resultThreshold = resultThreshold
        self.weightage = weightage
        self.ruleVersion = ruleVersion
        self.businessExplanation = businessExplanation
        self.labels = list()
        for obj in labels:
            if isinstance(obj, dict):
                self.labels.append(Label(**obj))
            else:
                self.labels.append(obj)
        self.isWarning = isWarning

    def __repr__(self):
        return f"Item({self.__dict__})"


class DataQualityRuleDetails:
    def __init__(self, ruleId, backingAssetId, items, isSegmented, segments=None, id=None,
                 transformUDFs=None, parentId=None, isCompositeRule=False, filter=None,
                 executionSequence=1, continueExecutionOnFailure=False, engineType=None,
                 customSqlConfig=None, tenantId=None, subType=None, jobSchedule=None,
                 policyScoreStrategy=None, *args, **kwargs):

        self.id = id
        self.ruleId = ruleId
        self.backingAssetId = backingAssetId
        self.items = [Item(**obj) if isinstance(obj, dict) else obj for obj in items]
        self.isSegmented = isSegmented
        self.segments = [ShortSegment(**obj) if isinstance(obj, dict) else obj for obj in (segments or [])]
        self.transformUDFs = transformUDFs or []
        self.parentId = parentId
        self.isCompositeRule = isCompositeRule
        self.filter = filter
        self.executionSequence = executionSequence
        self.continueExecutionOnFailure = continueExecutionOnFailure
        self.engineType = engineType
        self.customSqlConfig = customSqlConfig
        self.tenantId = tenantId
        self.subType = subType
        self.jobSchedule = jobSchedule
        self.policyScoreStrategy = policyScoreStrategy
        self.columnMappings = []

    def __repr__(self):
        return f"DataQualityRuleDetails({self.__dict__})"



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


class DataQualityRule:
    def __init__(self, name=None, description=None, type=None, enabled=None, schedule=None, scheduled=None,
                 timeZone="GMT", notificationChannels=None, backingAsset=None, createdAt=None, updatedAt=None,
                 thresholdLevel=None, archived=None, archivalReason=None, tenantId=None, createdBy=None,
                 lastUpdatedBy=None, tags=None, segments=None, version=0, sparkResourceConfig=None,
                 additionalPersistedColumns=None, labels=None, isProtectedResource=False, policyGroups=None,
                 ruleSetId=None, executionTimeoutInMinutes=None, totalExecutionTimeoutInMinutes=None,
                 isCompositeRule=False, executionSequence=1, filter=None, parentId=None,
                 continueExecutionOnFailure=False, sparkSQLFilterType=None,
                 sparkSQLDynamicFilterVariableMapping=None, sparkFilterSelectedColumns=None, autoCreated=False,
                 engineType=None, subType=None, jobSchedule=None, resourceStrategyType=None,
                 autoRetryEnabled=False, selectedResourceInventory=None, customSqlConfig=None,
                 policyScoreStrategy=None, id=None, *args, **kwargs):

        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.enabled = enabled
        self.schedule = schedule
        self.scheduled = scheduled
        self.timeZone = timeZone
        self.notificationChannels = notificationChannels
        self.backingAsset = BackingAsset(**backingAsset) if isinstance(backingAsset, dict) else backingAsset
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
        self.segments = [ShortSegment(**obj) if isinstance(obj, dict) else obj for obj in (segments or [])]
        self.version = version
        self.sparkResourceConfig = SparkResourceConfig(**sparkResourceConfig) if isinstance(sparkResourceConfig, dict) else sparkResourceConfig
        self.additionalPersistedColumns = additionalPersistedColumns or []
        self.labels = [Label(**obj) if isinstance(obj, dict) else obj for obj in (labels or [])]
        self.isProtectedResource = isProtectedResource
        self.policyGroups = [PolicyGroup(**obj) if isinstance(obj, dict) else obj for obj in (policyGroups or [])]
        self.ruleSetId = ruleSetId
        self.executionTimeoutInMinutes = executionTimeoutInMinutes
        self.totalExecutionTimeoutInMinutes = totalExecutionTimeoutInMinutes
        self.isCompositeRule = isCompositeRule
        self.executionSequence = executionSequence
        self.filter = filter
        self.parentId = parentId
        self.continueExecutionOnFailure = continueExecutionOnFailure
        self.sparkSQLFilterType = sparkSQLFilterType
        self.sparkSQLDynamicFilterVariableMapping = sparkSQLDynamicFilterVariableMapping
        self.sparkFilterSelectedColumns = sparkFilterSelectedColumns or []
        self.autoCreated = autoCreated
        self.engineType = engineType
        self.subType = subType
        self.jobSchedule = jobSchedule
        self.resourceStrategyType = resourceStrategyType
        self.autoRetryEnabled = autoRetryEnabled
        self.selectedResourceInventory = selectedResourceInventory
        self.customSqlConfig = customSqlConfig
        self.policyScoreStrategy = policyScoreStrategy

    def __repr__(self):
        return f"DataQualityRule({self.__dict__})"



class DataQualityRuleResource(RuleResource):
    def __init__(self, rule, details, client=None, *args, **kwargs):
        if isinstance(rule, dict):
            self.rule = DataQualityRule(**rule)
        else:
            self.rule = rule
        if isinstance(details, dict):
            self.details = DataQualityRuleDetails(**details)
        else:
            self.details = details
        self.client = client

    def execute(self, sync=True, incremental=False, failure_strategy: FailureStrategy = FailureStrategy.DoNotFail,
                policy_execution_request: PolicyExecutionRequest = None) -> RuleExecution:
        logger.info(
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}")
        return self.client.execute_rule(PolicyType.DATA_QUALITY, self.rule.id, sync, incremental, failure_strategy,
                                        policy_execution_request)

    def get_executions(self, page=0, size=25, sortBy='finishedAt:DESC'):
        return self.client.policy_executions(self.rule.id, PolicyType.DATA_QUALITY, page, size, sortBy)

    def __repr__(self):
        return f"DataQualityRuleResource({self.__dict__})"
