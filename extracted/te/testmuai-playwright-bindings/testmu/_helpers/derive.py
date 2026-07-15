"""testmu.derive / testmu.condition_compute — derivation recompute.

Recorded tests capture derived extractions as a RAW observation plus a
`code_js` derivation. Exported tests
re-extract the raw value at replay time and RECOMPUTE the derivation with
these helpers instead of asserting against a stale recorded literal:

    raw = await testmu.textual_analyzer(page, ...)          # fresh raw value
    computed = await testmu.derive(page, code_js, raw)       # recompute
    testmu_helper.evaluation.evaluate(...)                   # assert

- ``derive(page, code_js, value)``: wraps the recorded code body with a
  ``const value = <json>;`` binding (the same injection the agent performs)
  and executes it via ``page.evaluate``. The code computes FROM ``value``.
- ``condition_compute(page, expression, variables)``: the condition-leg
  variant — resolves ``{{var}}`` tokens into the expression, then evaluates
  the self-contained arithmetic (no ``value`` binding on this leg).

Both return the computed operand as a string (JS booleans coerce to
'true'/'false', matching the agent's comparison convention) and fail LOUD on
execution errors or a null result — a derivation must produce an operand;
comparing an underived/empty value is never correct.
"""
from __future__ import annotations

import json
import logging
import re

_log = logging.getLogger("testmu")

_VAR_TOKEN = re.compile(r"\{\{\s*([^}]+?)\s*\}\}")


def _coerce(value) -> str:
    """JS booleans -> lowercase 'true'/'false'; everything else stringified.

    Mirrors the agent's convention so recomputed operands compare identically.
    """
    return ("true" if value else "false") if isinstance(value, bool) else str(value)


def _wrap_body(body: str) -> str:
    """Wrap a JS function body in an IIFE for page.evaluate."""
    return f"() => {{ {body}\n }}"


async def derive(page, code_js: str, value: str) -> str:
    """Recompute a recorded derivation over a fresh raw value.

    Args:
        page: Playwright page instance.
        code_js: The recorded JavaScript function body. A constant named
            ``value`` holding the raw extraction is in scope.
        value: The freshly re-extracted RAW observation (e.g. '$1,100.00').

    Returns:
        The computed operand as a string.

    Raises:
        RuntimeError: On JS execution failure or a null/undefined result.
    """
    preview = code_js[:80] + ("..." if len(code_js) > 80 else "")
    _log.info("    [derive] value=%r code=%s", value, preview)
    wrapped = _wrap_body(f"const value = {json.dumps(value)};\n{code_js}")
    try:
        result = await page.evaluate(wrapped)
    except Exception as e:  # noqa: BLE001 — surface as a step failure
        raise RuntimeError(f"derive: code_js execution failed: {e}") from e
    if result is None:
        raise RuntimeError(
            "derive: code_js returned null/undefined — a derivation must "
            "produce the computed operand"
        )
    return _coerce(result)


async def condition_compute(page, expression: str, variables: dict) -> str:
    """Compute a condition-leg arithmetic expression over resolved variables.

    Args:
        page: Playwright page instance.
        expression: The recorded LEFT-operand expression, possibly containing
            ``{{var}}`` tokens (e.g. '{{rack_count}} - {{shelf_count}}').
        variables: Mapping of variable name -> value used to resolve tokens.

    Returns:
        The computed operand as a string.

    Raises:
        KeyError: When a ``{{var}}`` token has no entry in ``variables``.
        RuntimeError: On JS execution failure or a null/undefined result.
    """
    def _sub(m: re.Match) -> str:
        name = m.group(1).strip()
        if name not in variables:
            raise KeyError(
                f"condition_compute: variable {name!r} not found in variables"
            )
        return str(variables[name])

    resolved = _VAR_TOKEN.sub(_sub, expression)
    _log.info("    [condition_compute] %r -> %r", expression, resolved)
    wrapped = _wrap_body(f"return ({resolved});")
    try:
        result = await page.evaluate(wrapped)
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(
            f"condition_compute: expression evaluation failed: {e}"
        ) from e
    if result is None:
        raise RuntimeError(
            "condition_compute: expression evaluated to null/undefined"
        )
    return _coerce(result)
