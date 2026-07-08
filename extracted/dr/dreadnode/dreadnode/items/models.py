"""Built-in item payload models.

Mirror of the platform validators in ``packages/api/app/items/schemas.py``. The
SDK validates here so the agent gets immediate feedback; the platform
re-validates on ingest (never trust the client).
"""

import typing as t

from pydantic import BaseModel, ConfigDict, Field

# Low-cardinality severity scale. Mirrors the platform's constrained enum. A
# finding's severity lives inside its ``data`` payload (not a promoted column).
ItemSeverity = t.Literal["critical", "high", "medium", "low", "info"]

# Built-in item type discriminators.
FINDING_TYPE = "finding"
ASSET_TYPE = "asset"


class Finding(BaseModel):
    """Something an agent discovered worth surfacing — a vuln, a risk, a result."""

    model_config = ConfigDict(extra="ignore")

    title: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description="Short, human-readable finding title.",
    )
    description: str | None = Field(
        None,
        description="What was observed, why it matters, and the affected behavior.",
    )
    severity: ItemSeverity = Field(
        "info",
        description="Impact level: critical, high, medium, low, or info.",
    )
    category: str | None = Field(
        None,
        description="Finding family, CWE/OWASP bucket, or domain-specific category.",
    )
    evidence: str | None = Field(
        None,
        description="Concrete proof: request, response, command output, file path, or trace note.",
    )
    metadata: dict[str, t.Any] = Field(
        default_factory=dict,
        description="Additional machine-readable context for filtering or reporting.",
    )


class Asset(BaseModel):
    """Something the agent identified or produced — a host, file, account, artifact."""

    model_config = ConfigDict(extra="ignore")

    title: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description="Short, human-readable asset label.",
    )
    asset_type: str | None = Field(
        None,
        description="Asset kind, such as host, service, file, account, endpoint, model, or artifact.",
    )
    identifier: str | None = Field(
        None,
        description="Stable identifier such as hostname, IP, URL, file path, account id, or artifact URI.",
    )
    description: str | None = Field(
        None,
        description="Useful context about where the asset came from or why it matters.",
    )
    metadata: dict[str, t.Any] = Field(
        default_factory=dict,
        description="Additional machine-readable context for filtering or reporting.",
    )
