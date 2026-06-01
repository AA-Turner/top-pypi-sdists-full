"""Typed representation of source material detectors consume.

At v0 the only source type is Terraform/OpenTofu. `TerraformResource` wraps one
HCL block — either a `resource "TYPE" "NAME" { ... }` (the historical name
of the model) or a `data "TYPE" "NAME" { ... }` block (added in v0.1.10).
The `kind` field disambiguates; defaults to `"resource"` for backwards
compat. Detectors that only care about resources can filter
`r.kind == "resource"`; detectors that walk references between resources
and data sources (e.g. `aws_iam_policy_document` indirection) use both.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from efterlev.models.source_ref import SourceRef

TerraformBlockKind = Literal["resource", "data"]


class TerraformResource(BaseModel):
    """A single HCL block from a Terraform file — resource or data source."""

    model_config = ConfigDict(frozen=True)

    type: str
    name: str
    body: dict[str, Any] = Field(default_factory=dict)
    source_ref: SourceRef
    # v0.1.10: distinguishes `resource` blocks (the v0 default) from `data`
    # source blocks. The model name stays `TerraformResource` for callsite
    # stability; the kind tag is the structural truth. Default "resource"
    # means existing detectors and tests need no migration — they receive
    # only resources unless the parser emits data sources, and they can
    # opt into seeing data sources by reading `r.kind`.
    kind: TerraformBlockKind = "resource"

    def get_nested(self, *keys: str) -> Any:
        """Walk the body dict by key path, returning None on any missing step.

        Terraform nested blocks are represented by python-hcl2 as lists of dicts
        (one entry per block instance). We unwrap single-element lists so
        detectors can chain `.get_nested("foo", "bar")` without manual index
        gymnastics for the common single-block case.
        """
        cur: Any = self.body
        for key in keys:
            if isinstance(cur, list) and len(cur) == 1:
                cur = cur[0]
            if not isinstance(cur, dict):
                return None
            cur = cur.get(key)
            if cur is None:
                return None
        if isinstance(cur, list) and len(cur) == 1:
            cur = cur[0]
        return cur
