"""Keep identifiers on the exception while unit/span/context blocks unwind.

No I/O, frame locals, prompt text, tensors, or global last-sample state. A
handled exception cannot leave context behind for a later unrelated failure.
"""

from __future__ import annotations

from typing import Any

from .redaction import scrub_text

_ATTRIBUTE = "_probe_failure_context"
_ALIASES = {
    "model": ("model", "model_name"),
    "dataset": ("dataset", "dataset_name", "dataset_id"),
    "sample_id": ("sample_id", "sample", "example_id", "row_id"),
    "prompt_id": ("prompt_id",),
    "batch_id": ("batch_id",),
    "task_id": ("task_id",),
    "split": ("split",),
    "phase": ("phase",),
    # An identifier like the rest (int or string, carried as text), NOT a
    # second step axis: `step` below stays the only integer-typed key.
    "epoch": ("epoch",),
}


def _clean(values: dict[str, Any], run_id: str) -> dict[str, Any]:
    context: dict[str, Any] = {"run_id": run_id}
    for key, aliases in _ALIASES.items():
        for alias in aliases:
            value = values.get(alias)
            if key == "epoch" and isinstance(value, float) and value.is_integer():
                # Hugging Face's `state.epoch` is a float (2.0 at an epoch
                # boundary); a whole one is an epoch, so keep it as one.
                value = int(value)
            if isinstance(value, bool) or not isinstance(value, (str, int)):
                continue
            text = " ".join(str(value).split())
            if text and "\x00" not in text:
                context[key] = scrub_text(text, max_chars=160)[:160]
                break
    step = values.get("step")
    if isinstance(step, int) and not isinstance(step, bool) and step >= 0:
        context["step"] = step
    return context


def identifiers(values: dict[str, Any]) -> dict[str, Any]:
    """Canonicalize each scope before merging, so inner aliases override outer IDs."""
    try:
        result = _clean(values, "")
        result.pop("run_id")
        return result
    except BaseException:  # noqa: BLE001 -- optional context cannot break application code
        return {}


def remember(exc: BaseException | None, run_id: str | None, values: dict[str, Any]) -> None:
    """Innermost values win; enclosing spans can add their phase and step."""
    if exc is None or not run_id:
        return
    try:
        existing = getattr(exc, _ATTRIBUTE, None)
        if existing is not None and (
            not isinstance(existing, dict) or existing.get("run_id") != run_id
        ):
            return
        context = _clean(existing or {}, run_id)
        for key, value in _clean(values, run_id).items():
            context.setdefault(key, value)
        if len(context) > 1:
            setattr(exc, _ATTRIBUTE, context)
    except BaseException:  # noqa: BLE001 -- diagnostic capture cannot alter unwinding
        pass


def read(exc: BaseException | None, run_id: str | None) -> dict[str, Any] | None:
    """Follow wrapped causes too, restricted to the run sending this report."""
    if not run_id:
        return None
    seen: set[int] = set()
    result: dict[str, Any] = {}
    try:
        while exc is not None and id(exc) not in seen and len(seen) < 5:
            seen.add(id(exc))
            context = getattr(exc, _ATTRIBUTE, None)
            if isinstance(context, dict) and context.get("run_id") == run_id:
                # A deeper cause's input is more specific than its wrapper's.
                result.update(_clean(context, run_id))
            exc = exc.__cause__ or exc.__context__
    except BaseException:  # noqa: BLE001
        pass
    return result or None
