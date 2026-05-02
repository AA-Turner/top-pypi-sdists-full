from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum, auto
from acceldata_sdk.constants import FailureStrategy
from acceldata_sdk.models.ruleExecutionResult import RuleExecutionSummary, RuleExecutionResult
from acceldata_sdk.models.common_types import PolicyExecutionRequest
from acceldata_sdk.models.threshold import RuleLevelThresholdConfiguration


class Rule:
    def __init__(self, id, name, description, createdAt, updatedAt, backingAssets, thresholdLevel, archivalReason=None,
                 archived=False, enabled=False, schedule=None, notificationChannels=None, *args, **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.backingAssets = backingAssets
        self.thresholdLevel = thresholdLevel
        self.archivalReason = archivalReason
        self.archived = archived
        self.enabled = enabled
        self.schedule = schedule
        self.notificationChannels = notificationChannels

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Rule({self.__dict__})"


class RuleCancelResponse:

    def __init__(self, message, status, *args, **kwargs):
        self.status = status
        self.message = message

    def __repr__(self):
        return f"Response({self.__dict__})"


class RuleExecution:

    def __init__(self, ruleId, ruleName, thresholdLevel, startedAt, resultStatus, executionStatus, executionMode
                 , ruleType=None, id=None, lastMarker=None, executionError=None, rightLastMarker=None,
                 leftLastMarker=None, finishedAt=None, ruleVersion=None, *args, **kwargs):
        self.ruleId = ruleId
        self.ruleName = ruleName
        self.ruleVersion = ruleVersion
        self.thresholdLevel = thresholdLevel
        self.startedAt = startedAt
        self.resultStatus = resultStatus
        self.executionStatus = executionStatus
        self.executionMode = executionMode
        self.ruleType = ruleType
        self.executionError = executionError
        self.rightLastMarker = rightLastMarker
        self.lastMarker = lastMarker
        self.leftLastMarker = leftLastMarker
        self.id = id
        self.finishedAt = finishedAt

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"RuleExecution({self.__dict__})"

class ExecutionResult:

    def __init__(self, execution, items, meta=None, result=None, *args, **kwargs):
        if isinstance(execution, dict):
            self.execution = RuleExecution(**execution)
        else:
            self.execution = execution
        if isinstance(result, dict):
            self.result = RuleExecutionResult(**result)
        else:
            self.result = result
        self.items = items
        self.meta = meta

    def __repr__(self):
        return f"ExecutionResult({self.__dict__})"


@dataclass
class ShortSegment:
    id = None
    name = None

    def __init__(self, id, name, *args, **kwargs):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"ShortSegment({self.__dict__})"


@dataclass
class Label:
    def __init__(self, key, value, *args, **kwargs):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"Label({self.__dict__})"


@dataclass
class BackingAsset:
    id = None
    ruleId = None
    tableAssetId = None
    customQuery = None
    customTableAssetIds = None
    tableAlias = None
    marker = None

    def __init__(self, id=None, ruleId=None, tableAssetId=None, customQuery=None, customTableAssetIds=None,
                 tableAlias=None, marker=None, *args, **kwargs):
        self.id = id
        self.ruleId = ruleId
        self.tableAssetId = tableAssetId
        self.customQuery = customQuery
        self.customTableAssetIds = customTableAssetIds
        self.tableAlias = tableAlias
        self.marker = marker

    def __repr__(self):
        return f"BackingAsset({self.__dict__})"


@dataclass
class RuleTag:
    id = None,
    tagId = None
    ruleId = None
    name = None

    def __init__(self, id, tagId, ruleId, name, *args, **kwargs):
        self.id = id
        self.tagId = tagId
        self.ruleId = ruleId
        self.name = name

    def __repr__(self):
        return f"RuleTag({self.__dict__})"


@dataclass
class PolicyGroup:
    id = None
    name = None
    description = None
    createdAt = None
    updatedAt = None
    tenantId = None

    def __init__(self, id, name, description, createdAt, updatedAt, tenantId, *args, **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.tenantId = tenantId

    def __repr__(self):
        return f"PolicyGroup({self.__dict__})"

class RuleResource:
    def __init__(self, rule, details, client=None, *args, **kwargs):
        self.rule = rule
        self.details = details
        self.client = client

    def execute(self, sync=True, incremental=False, failure_strategy: FailureStrategy = FailureStrategy.DoNotFail,
                policy_execution_request: PolicyExecutionRequest = None) -> RuleExecution:
        pass

    def get_executions(self, page=0, size=25, sortBy='finishedAt:DESC') -> List[RuleExecutionSummary]:
        pass
