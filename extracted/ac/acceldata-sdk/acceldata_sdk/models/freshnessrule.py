import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


from acceldata_sdk.constants import FailureStrategy, PolicyType
from acceldata_sdk.models.common_types import PolicyExecutionRequest
from acceldata_sdk.models.threshold import parse_rule_threshold_configuration
from acceldata_sdk.models.rule import (
    ShortSegment,
    BackingAsset,
    RuleTag,
    PolicyGroup,
    RuleResource,
    RuleExecution,
)
from acceldata_sdk.models.ruleExecutionResult import (
    RuleExecutionResult,
    RuleItemResult,
    RuleExecutionSummary,
    RuleResult,
    ExecutorConfig,
    SparkResourceConfig,
    RuleExecutionResult
)

logger = logging.getLogger("freshnessrule")
logger.setLevel(logging.INFO)


# --------------------------------------------------------------------
# Item (aligned to details.items[])
# --------------------------------------------------------------------
@dataclass
class Item:
    id: Optional[int] = None
    ruleItemId: Optional[int] = None
    threshold: Optional[float] = None
    resultPercent: Optional[float] = None
    success: Optional[bool] = None
    error: Optional[str] = None
    weightage: Optional[float] = None
    isWarning: Optional[bool] = None
    dimension: Optional[str] = None
    includeInQualityScore: Optional[bool] = None
    anomalyDetected: Optional[bool] = None
    anomalyDetails: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    thresholdBreached: Optional[bool] = None
    thresholdBreachDetails: Optional[Dict[str, Any]] = field(default_factory=dict)

    def __init__(
            self,
            id=None,
            ruleItemId=None,
            threshold=None,
            resultPercent=None,
            success=None,
            error=None,
            weightage=None,
            isWarning=None,
            dimension=None,
            includeInQualityScore=None,
            anomalyDetected=None,
            anomalyDetails=None,
            thresholdBreached=None,
            thresholdBreachDetails=None,
            *args,
            **kwargs,
    ):
        self.id = id
        self.ruleItemId = ruleItemId
        self.threshold = threshold
        self.resultPercent = resultPercent
        self.success = success
        self.error = error
        self.weightage = weightage
        self.isWarning = isWarning
        self.dimension = dimension
        self.includeInQualityScore = includeInQualityScore
        self.anomalyDetected = anomalyDetected
        self.anomalyDetails = anomalyDetails or []
        self.thresholdBreached = thresholdBreached
        self.thresholdBreachDetails = thresholdBreachDetails or {}

    def __repr__(self):
        return f"Item({self.__dict__})"


class FreshnessRuleExecutionSummary(RuleExecutionSummary):
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
        return f"FreshnessRuleExecutionSummary({self.__dict__})"


class FreshnessRuleExecutionResult(RuleExecutionResult):
    def __init__(
            self,
            status,
            description=None,
            successCount=None,
            failureCount=None,
            qualityScore=None,
            anomalyCount=None,
            slaBreachCount=None,
            executionStatus=None,
            ruleExecutionType=None,
            *args,
            **kwargs
    ):
        # Initialize base class
        super().__init__(status=status, ruleExecutionType=ruleExecutionType)

        # Freshness-specific fields
        self.description = description
        self.successCount = successCount
        self.failureCount = failureCount
        self.qualityScore = qualityScore
        self.anomalyCount = anomalyCount
        self.slaBreachCount = slaBreachCount
        self.executionStatus = executionStatus

    def __repr__(self):
        return f"FreshnessRuleExecutionResult({self.__dict__})"

# --------------------------------------------------------------------
# FreshnessRule (aligned to root['rule'])
# --------------------------------------------------------------------
class FreshnessRule:
    def __init__(
            self,
            id=None,
            name=None,
            description=None,
            notificationChannels=None,
            enabled=None,
            backingAsset=None,
            createdAt=None,
            updatedAt=None,
            thresholdLevel=None,
            archived=None,
            archivalReason=None,
            tenantId=None,
            createdBy=None,
            lastUpdatedBy=None,
            tags=None,
            sparkResourceConfig=None,
            policyGroups=None,
            version=None,
            type=None,
            autoCreated=False,
            anomalyStrengthThreshold=None,
            resourceStrategyType=None,
            autoRetryEnabled=False,
            selectedResourceInventory=None,
            includeInQualityScore=None,
            schedule=None,
            scheduled=None,
            timeZone="GMT",
            timeSecondsOffset=None,
            jobSchedule=None,
            *args,
            **kwargs,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.notificationChannels = notificationChannels
        self.enabled = enabled

        self.backingAsset = (
            BackingAsset(**backingAsset)
            if isinstance(backingAsset, dict)
            else backingAsset
        )

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

        self.tags = [
            RuleTag(**obj) if isinstance(obj, dict) else obj
            for obj in (tags or [])
        ]

        self.sparkResourceConfig = (
            SparkResourceConfig(**sparkResourceConfig)
            if isinstance(sparkResourceConfig, dict)
            else sparkResourceConfig
        )

        self.policyGroups = [
            PolicyGroup(**obj) if isinstance(obj, dict) else obj
            for obj in (policyGroups or [])
        ]

        self.version = version
        self.type = type
        self.autoCreated = autoCreated
        self.anomalyStrengthThreshold = anomalyStrengthThreshold
        self.resourceStrategyType = resourceStrategyType
        self.autoRetryEnabled = autoRetryEnabled
        self.selectedResourceInventory = selectedResourceInventory
        self.includeInQualityScore = includeInQualityScore
        self.schedule = schedule
        self.scheduled = scheduled
        self.timeZone = timeZone
        self.timeSecondsOffset = timeSecondsOffset
        self.jobSchedule = jobSchedule

    def __repr__(self):
        return f"FreshnessRule({self.__dict__})"


# --------------------------------------------------------------------
# FreshnessRuleDetails (aligned to root['details'])
# --------------------------------------------------------------------
class FreshnessRuleDetails:
    def __init__(
            self,
            id=None,
            ruleId=None,
            backingAssetId=None,
            items=None,
            isSegmented=False,
            segments=None,
            isCompositeRule=False,
            continueExecutionOnFailure=False,
            version=None,
            *args,
            **kwargs,
    ):
        self.id = id
        self.ruleId = ruleId
        self.backingAssetId = backingAssetId
        self.isSegmented = isSegmented
        self.isCompositeRule = isCompositeRule
        self.continueExecutionOnFailure = continueExecutionOnFailure
        self.version = version

        # Items list — dict → Item conversion
        self.items = [Item(**obj) if isinstance(obj, dict) else obj for obj in (items or [])]

        # Segments list
        self.segments = [
            ShortSegment(**obj) if isinstance(obj, dict) else obj
            for obj in (segments or [])
        ]

    def __repr__(self):
        return f"FreshnessRuleDetails({self.__dict__})"


# --------------------------------------------------------------------
# FreshnessRuleResource (wrapper + executor)
# --------------------------------------------------------------------
class FreshnessRuleResource(RuleResource):
    def __init__(self, rule, details, client=None, *args, **kwargs):
        self.rule = FreshnessRule(**rule) if isinstance(rule, dict) else rule
        self.details = FreshnessRuleDetails(**details) if isinstance(details, dict) else details
        self.client = client

    def get_executions(self, page=0, size=25, sortBy='finishedAt:DESC'):
        return self.client.policy_executions(self.rule.id, PolicyType.DATA_CADENCE, page, size, sortBy)

    def execute(
            self,
            sync=True,
            incremental=False,
            failure_strategy: FailureStrategy = FailureStrategy.DoNotFail,
            policy_execution_request: Optional[PolicyExecutionRequest] = None,
    ) -> RuleExecution:
        logger.info(
            f"Policy Execution Request: "
            f"{policy_execution_request.to_dict() if policy_execution_request else 'None'}"
        )
        return self.client.execute_rule(
            PolicyType.DATA_CADENCE,
            self.rule.id,
            sync,
            incremental,
            failure_strategy,
            policy_execution_request,
        )

    def __repr__(self):
        return f"FreshnessRuleResource({self.__dict__})"
