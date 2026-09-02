"""Pydantic twin for `TokenUsage` (Phase 1b.2). Retirement Ledger row 8.

Shadowed, not swapped — and this one is deliberately a SEPARATE step from the
other siblings, because it is the only remaining contract type that is both
persisted and billing-relevant.

🚨 SCOPE OF THIS TWIN, STATED SO NOBODY MISTAKES IT FOR A DROP-IN.
It models the FIELDS, the construction-time derivation and `total_tokens`. It
does NOT port `calculate_cost`, `calculate_catalog_cost`,
`calculate_cost_breakdown`, the `from_<provider>` constructors, or
`aggregate_by_model`. Those read the pricing catalog (a DB-backed lookup that
warms itself on a miss) and porting them is mechanical but must happen before a
FLIP, not before a shadow. A shadow needs the shape to be right; a flip needs
the behaviour to move. Row 8 cannot reach S3 until they do.

WHAT THE CORPUS SAID — and half of it was unusable, which is itself the point.
`chat.request_snapshot.response_payload->'usage'` holds 3,460 rows as objects.
The other 2,049 (37.4%) are Python `repr` STRINGS, because `_json_safe` used
`dataclasses.asdict()` and one un-copyable leaf collapsed the whole record —
fixed 2026-08-24, but every row written before that is structurally unusable for
this field. So this twin rests on 3,460 rows, not 5,473, and that is stated
rather than rounded away.

Of those 3,460:

  * eight fields are present in ALL of them — input_tokens, output_tokens,
    cached_input_tokens, matrx_model_name, provider_model_name, api,
    response_id, metadata;
  * `raw_usage` is an object 2,502 times and an EXPLICIT NULL 888 times (absent
    in 70). Real nulls, so `dict[str, Any] | None` is right and the field must
    accept a null that is actually on the wire;
  * `offering_id`, `offering_route` and `billing_components` appear in 1,474 —
    the rows written after those fields were added;
  * `provider_charge` is EXPLICITLY NULL in every single row it appears in
    (1,474) and populated in NONE.

That last one is a coverage gap, not a curiosity. `provider_charge_from_usage`
only produces a value for a provider that reports an explicit charge — xAI's
integer tick field. Every mainstream provider returns None, verified directly.
So the derivation below is real, is reachable, and has NEVER been observed in
captured data — which means a corpus comparison cannot catch a subtle error in
it. It is pinned by direct unit assertions instead, including the exact firing
conditions (`provider_charge is None` AND `raw_usage` TRUTHY, so `{}` does not
fire and an already-set charge is preserved).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_ai.config.usage_config import provider_charge_from_usage


class TokenUsageModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=False,
        arbitrary_types_allowed=True,
    )

    input_tokens: int
    output_tokens: int
    cached_input_tokens: int = 0
    matrx_model_name: str = ""
    provider_model_name: str = ""
    api: str = ""
    response_id: str = ""
    offering_id: str = ""
    offering_route: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    raw_usage: dict[str, Any] | None = None
    billing_components: dict[str, int] = Field(default_factory=dict)
    # Staged `Any`: the derivation assigns a `ProviderCharge` DATACLASS, and
    # `ProviderChargeModel` is itself only at S0. Narrows when that row clears —
    # a separate, deliberate step, not a cleanup.
    provider_charge: Any = None

    @model_validator(mode="after")
    def _recover_provider_charge(self) -> TokenUsageModel:
        # `__post_init__`, verbatim. The `and self.raw_usage` is TRUTHINESS, not
        # `is not None`: an empty dict must NOT trigger a lookup, and an
        # already-set charge must survive untouched.
        if self.provider_charge is None and self.raw_usage:
            self.provider_charge = provider_charge_from_usage(self.raw_usage)
        return self

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.cached_input_tokens
