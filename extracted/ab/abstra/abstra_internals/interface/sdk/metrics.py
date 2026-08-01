from typing import Optional

# Guardrails. Tags are for LOW-cardinality dimensions (e.g. {"route": "manual"});
# never put ids/emails there — high cardinality bloats storage and dashboards.
MAX_NAME_LEN = 128
MAX_TAG_KEYS = 5
MAX_TAG_KEY_LEN = 64
MAX_TAG_VALUE_LEN = 128


def count(name: str, value: float = 1.0, tags: Optional[dict] = None) -> None:
    """Record a business metric measurement.

    Emits one measurement of ``name`` — a low-frequency business event such as a
    routing decision ("was this document sent to AI or to manual review?") or a
    processed record. Measurements are pre-aggregated per execution and shipped
    to Abstra Cloud, where they power dashboards.

    Example::

        route = "ai" if fits_requirements(doc) else "manual"
        abstra.metrics.count("document_routing", tags={"route": route})

    Args:
        name: Metric name, e.g. ``"document_routing"``. Keep it stable.
        value: Magnitude of the event (defaults to ``1.0``). Use it to sum
            amounts, e.g. ``count("invoice_amount", value=1234.5)``.
        tags: Optional low-cardinality dimensions, e.g. ``{"route": "manual"}``.

    This call is best-effort: it NEVER raises and NEVER blocks your code. Called
    outside a running stage (e.g. a script imported locally) it is a no-op.
    """
    try:
        _count(name, value, tags)
    except Exception:
        # Instrumentation must never break the user's business logic.
        pass


def _count(name, value, tags) -> None:
    from abstra_internals.controllers.sdk.sdk_context import SDKContextStore
    from abstra_internals.interface.sdk.user_exceptions import ExecutionNotFound

    if not isinstance(name, str):
        return
    name = name.strip()[:MAX_NAME_LEN]
    if not name:
        return

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return

    normalized_tags = _normalize_tags(tags)

    try:
        context = SDKContextStore.get_by_thread()
    except ExecutionNotFound:
        return

    context.repositories.metrics.record(
        execution_id=context.execution.id,
        stage_id=context.execution.stage_id,
        name=name,
        value=numeric,
        tags=normalized_tags,
    )


def _normalize_tags(tags) -> dict:
    if not isinstance(tags, dict) or not tags:
        return {}
    normalized: dict = {}
    for raw_key, raw_value in tags.items():
        if len(normalized) >= MAX_TAG_KEYS:
            break
        if not isinstance(raw_key, str):
            continue
        key = raw_key.strip()[:MAX_TAG_KEY_LEN]
        if not key:
            continue
        normalized[key] = str(raw_value)[:MAX_TAG_VALUE_LEN]
    return normalized
