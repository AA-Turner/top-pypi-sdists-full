"""`generated_by(...)`: which model wrote a sample, as compact JSON text an adapter can carry where only
scalars fit (an ART trajectory's metadata), and `parse_generated_by` reading it back (RL plan §3.3)."""

from __future__ import annotations

import json
from typing import Any


def generated_by(
    run: Any = None,
    *,
    version: int | None = None,
    step: int | None = None,
    external: str | None = None,
    revision: str | None = None,
    provider: str | None = None,
    policy_id: str | None = None,
) -> str:
    """A `ModelRef` as text: another Probe run's weights (``run`` = a Run or its id, with exactly one of
    ``version`` or ``step``), or an outside model (``external`` = its name). Raises on a ref the contract
    refuses: this runs in the researcher's own code, never inside a hook."""
    from ....generated.samples import ExternalRef, RunRef

    if (run is None) == (external is None):
        raise ValueError("generated_by() names exactly one of run= or external=")
    if external is not None:
        model = ExternalRef(name=external, revision=revision, provider=provider)
    else:
        run_id = getattr(run, "id", run)
        fields: dict[str, Any] = {"run_id": str(run_id), "version": version, "step": step}
        if policy_id is not None:
            fields["policy_id"] = policy_id
        model = RunRef(**fields)
    return json.dumps(model.model_dump(mode="json", exclude_none=True), separators=(",", ":"), sort_keys=True)


def parse_generated_by(text: Any) -> dict | None:
    """What `generated_by` wrote, as the ref's dict; None for anything else (the part's contract check
    decides whether the ref itself is valid)."""
    if not isinstance(text, str) or not text.startswith("{"):
        return None
    try:
        value = json.loads(text)
    except ValueError:
        return None
    return value if isinstance(value, dict) and isinstance(value.get("kind"), str) else None
