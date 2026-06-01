"""AWS Config evaluations JSON parser.

Parses the output of `aws configservice get-compliance-details-by-config-rule`,
which produces a list of `EvaluationResults`. Each evaluation captures a
specific resource's compliance against a specific Config Rule.

Spec reference:
https://docs.aws.amazon.com/config/latest/APIReference/API_EvaluationResult.html

Example shape (one evaluation):

```json
{
  "EvaluationResultIdentifier": {
    "EvaluationResultQualifier": {
      "ConfigRuleName": "encrypted-volumes",
      "ResourceType": "AWS::EC2::Volume",
      "ResourceId": "vol-aaaaaaaa"
    },
    "OrderingTimestamp": "2026-05-15T00:00:00Z"
  },
  "ComplianceType": "NON_COMPLIANT",
  "ResultRecordedTime": "2026-05-15T01:00:00Z",
  "ConfigRuleInvokedTime": "2026-05-15T00:30:00Z",
  "Annotation": "Volume vol-aaaaaaaa is not encrypted"
}
```

Fields the parser does NOT consume at v0.1.114 (deferred):
- `ResultToken` — paginator metadata, not evidence-bearing.
- `ConfigRuleInvokedTime` — internal timing, not consumer-facing.
- Custom Config Rules (Lambda-backed) — same shape as managed rules,
  ingest works identically; mapping table just won't have an entry
  unless the customer adds one.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError

ConfigComplianceType = Literal["COMPLIANT", "NON_COMPLIANT", "NOT_APPLICABLE", "INSUFFICIENT_DATA"]
"""AWS Config ComplianceType field values per the AWS spec."""


class ConfigEvaluationQualifier(BaseModel):
    """The (ConfigRuleName, ResourceType, ResourceId) tuple that identifies an evaluation."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    ConfigRuleName: str
    ResourceType: str
    ResourceId: str


class ConfigEvaluationIdentifier(BaseModel):
    """Wrapper around the qualifier — Config nests it under `EvaluationResultIdentifier`."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    EvaluationResultQualifier: ConfigEvaluationQualifier
    OrderingTimestamp: str | None = None


class ConfigEvaluation(BaseModel):
    """One parsed Config evaluation. Strict on required fields."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    EvaluationResultIdentifier: ConfigEvaluationIdentifier
    ComplianceType: ConfigComplianceType
    ResultRecordedTime: str | None = None
    Annotation: str | None = None  # Human-readable explanation, optional

    @property
    def config_rule_name(self) -> str:
        return self.EvaluationResultIdentifier.EvaluationResultQualifier.ConfigRuleName

    @property
    def resource_type(self) -> str:
        return self.EvaluationResultIdentifier.EvaluationResultQualifier.ResourceType

    @property
    def resource_id(self) -> str:
        return self.EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId


class ConfigParseError(ValueError):
    """Raised when an AWS Config document is structurally invalid."""


def parse_config_document(path: Path) -> list[ConfigEvaluation]:
    """Parse an AWS Config evaluations JSON file.

    Accepts both shapes the AWS CLI produces:
    - Top-level `{"EvaluationResults": [...]}` (the
      `get-compliance-details-by-config-rule` shape)
    - A bare array `[...]` of evaluation objects (the export-via-S3
      / EventBridge shape)

    Soft schema drift handling (per parser pattern from v0.1.113
    Security Hub): findings that fail Pydantic validation are skipped
    silently rather than aborting the entire ingest.
    """
    if not path.is_file():
        raise FileNotFoundError(f"AWS Config input not found: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ConfigParseError(f"AWS Config input is not valid JSON: {e}") from e

    if isinstance(raw, dict) and "EvaluationResults" in raw:
        evaluations_raw = raw["EvaluationResults"]
    elif isinstance(raw, list):
        evaluations_raw = raw
    else:
        raise ConfigParseError(
            f"AWS Config input must be either a dict with `EvaluationResults` "
            f"key or a top-level array; got {type(raw).__name__}"
        )

    if not isinstance(evaluations_raw, list):
        raise ConfigParseError(
            f"`EvaluationResults` must be a list; got {type(evaluations_raw).__name__}"
        )

    out: list[ConfigEvaluation] = []
    for entry in evaluations_raw:
        if not isinstance(entry, dict):
            continue
        try:
            out.append(ConfigEvaluation.model_validate(entry))
        except ValidationError:
            continue
    return out
