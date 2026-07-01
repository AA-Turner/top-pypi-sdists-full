"""Assertion and branch evaluation helpers.

Two helpers:
    verify_assertion(page, claim, assertion_tree) → dict
    evaluate_branch(sub_checks, composite_operator) → bool

Each has two internal paths:
- Deterministic (store_key present in sub_checks, or evaluate_branch): resolves
  variables from _variable_store and calls POST /api/v1/evaluate.
- Visual (no store_key, verify_assertion only): takes a screenshot and calls
  POST /api/v1/assertions/verify — only runs when smart mode is ON.

When smart is OFF verify_assertion always takes the deterministic path even if
there are no store_keys (skips the visual fallback).
"""
import base64
import logging
import os

import aiohttp

from testmu._helpers._errors import AssertionFailureError
from testmu._helpers._http import create_session
from testmu._helpers._screenshot import take_screenshot

_AI_API_HOST = os.getenv("TESTMU_AI_API_HOST", "https://kaneai-api.lambdatest.com/v16-server")

from testmu import _config
from testmu._vars import _variable_store, var
from testmu_helper.evaluation import evaluate_sub_checks

_log = logging.getLogger("testmu")


async def _resolve(text):
    """Resolve {{...}} / ${...} placeholders via testmu.var()."""
    if isinstance(text, str) and ("{{" in text or "${" in text):
        try:
            resolved = var(text)
            if resolved is None:
                return text
            return str(resolved)
        except Exception:
            return text
    return text if text is not None else ""


def _build_eval_sub_checks(sub_checks):
    """Return a coroutine that resolves sub_checks fields (helper for reuse)."""
    return sub_checks  # actual resolution is async — see _resolve_sub_checks


async def _resolve_sub_checks(sub_checks):
    """Resolve variable placeholders in each sub_check dict."""
    result = []
    for sc in sub_checks:
        # V16 SubCheckResult uses "expected"; legacy uses "expected_value"
        # Coerce None → "" since /api/v1/evaluate requires non-null strings
        raw_expected = sc.get("expected_value") or sc.get("expected") or ""
        raw_description = sc.get("description") or ""
        raw_extracted = sc.get("extracted_value") or ""
        result.append({
            "description": await _resolve(raw_description),
            "expected_value": await _resolve(raw_expected),
            "extracted_value": await _resolve(raw_extracted),
            "operator": sc.get("operator") or "contains",
            "transforms": sc.get("transforms") or ["strip"],
        })
    return result


async def _evaluate_deterministic(claim, composite_op, sub_checks):
    """Deterministic path: resolve variables then evaluate locally (no network)."""
    _log.info("    [assertion] deterministic claim=%s", claim[:80])
    eval_sub_checks = await _resolve_sub_checks(sub_checks)
    result = evaluate_sub_checks(claim, composite_op, eval_sub_checks)
    _log.info("    [assertion] result status=%s", result.get("status", "unknown"))
    return result


async def _verify_visual(page, claim, composite_op, sub_checks, assertion_tree):
    """Visual path: screenshot + LLM-based assertion via /api/v1/assertions/verify."""
    _log.info("    [assertion] visual claim=%s", claim[:80])

    screenshot_bytes = await take_screenshot(page)
    screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")
    current_url = page.url

    verification = (assertion_tree or {}).get("verification")
    request_body = {
        "screenshot_b64": screenshot_b64,
        "claim": claim,
        "current_url": current_url,
        "composite_operator": composite_op,
        "sub_checks": sub_checks,
        "step": 0,
    }
    if verification:
        request_body["verification"] = verification

    async with create_session() as session:
        async with session.post(
            f"{_AI_API_HOST}/api/v1/assertions/verify",
            json=request_body,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Assertion API error {response.status}: {text}")
            result = await response.json()

    _log.info("    [assertion] result status=%s", result.get("status", "unknown"))
    return result


def _evaluate_v3(claim: str, assertion_tree: dict) -> dict:
    """Code-side assertion evaluator (no network call).

    Evaluates assertion_tree in pure Python via the Assertion class. The tree
    uses the left_operand/right_operand/operator schema emitted by the code
    generator, with optionally nested operands for AND/OR groups.

    Args:
        claim: Assertion description (used for logging only).
        assertion_tree: Dict with operator, left_operand, right_operand (and
            optionally nested operands for AND/OR groups).

    Returns:
        dict with status ("passed" or "failed").
    """
    from testmu._helpers._assertion_v3_eval import Assertion
    from testmu._vars import _variable_store, var as _var

    def _get_variable_value(template, variables, *args, **kwargs):
        """Adapter: resolve {{...}} / ${...} templates via testmu.var()."""
        return _var(template)

    _log.info("    [assertion] evaluating claim=%s", (claim or "")[:80])
    node = Assertion.from_json(assertion_tree or {})
    passed, _ = node.evaluate(_variable_store, _get_variable_value)
    status = "passed" if passed else "failed"
    _log.info("    [assertion] result status=%s", status)
    return {"status": status}


async def verify_assertion(page, claim: str, assertion_tree: dict = None) -> dict:
    """Verify an assertion.

    When kane_version is "v3": evaluate the assertion_tree code-side in pure
    Python (no network call). The tree uses the left_operand/right_operand
    schema emitted by the code generator.

    Otherwise, two paths:
    1. Deterministic (store_key present in sub_checks OR smart mode is OFF):
       Resolves variables from _variable_store, calls POST /api/v1/evaluate.
    2. Visual (no store_key AND smart mode is ON): Takes screenshot, calls
       POST /api/v1/assertions/verify (LLM-based).

    Args:
        page: Playwright page object. Ignored in the code-side path.
        claim: Assertion description.
        assertion_tree: Code-side path — dict with operator/left_operand/
                        right_operand. Otherwise — dict with sub_checks, claim,
                        composite_operator.

    Returns:
        dict with status ("passed"/"failed") and sub_results.
    """
    from testmu import _configure

    if _configure.get("kane_version") == "v3":
        result = _evaluate_v3(claim, assertion_tree)
        if (result or {}).get("status") == "failed":
            if os.environ.get("TESTMU_SKIP_ASSERTION_FAILURE"):
                _log.warning(
                    "[ASSERTION WARN] %s — Ignoring assertion failure: %s",
                    claim, result,
                )
                return result
            raise AssertionFailureError(
                f"Assertion failed: {claim}", result=result,
            )
        return result

    sub_checks = (assertion_tree or {}).get("sub_checks", [])
    composite_op = (assertion_tree or {}).get("composite_operator", "and")
    assertion_claim = (assertion_tree or {}).get("claim", claim)

    has_store_keys = any(sc.get("store_key") for sc in sub_checks)

    # Deterministic path: store_keys present, or smart is OFF (no vision available)
    if has_store_keys or not _config.smart:
        result = await _evaluate_deterministic(assertion_claim, composite_op, sub_checks)
    else:
        # Visual path: smart mode ON, no store_keys → screenshot-based verification
        result = await _verify_visual(page, assertion_claim, composite_op, sub_checks, assertion_tree)

    if (result or {}).get("status") == "failed":
        if os.environ.get("TESTMU_SKIP_ASSERTION_FAILURE"):
            _log.warning(
                "[ASSERTION WARN] %s — Ignoring assertion failure: %s",
                assertion_claim, result,
            )
            return result
        raise AssertionFailureError(
            f"Assertion failed: {assertion_claim}", result=result,
        )
    return result


async def evaluate_branch(sub_checks: list, composite_operator: str = "and") -> bool:
    """Evaluate a conditional branch's sub_checks via /api/v1/evaluate.

    Resolves {{var}} and ${param} references in description, expected_value,
    and extracted_value from testmu._vars._variable_store, then calls
    POST /api/v1/evaluate.

    Args:
        sub_checks: List of dicts with description, expected_value,
            extracted_value, operator, transforms.
        composite_operator: "and" or "or" for combining sub_check results.

    Returns:
        True if the branch condition is satisfied, False otherwise.
    """
    _log.info("[if/else] evaluating %s of %d sub-check(s)",
              composite_operator, len(sub_checks))

    eval_sub_checks = await _resolve_sub_checks(sub_checks)

    if not eval_sub_checks:
        _log.info("[if/else] result=False (no valid sub-checks) → taking false branch")
        return False

    result = evaluate_sub_checks(
        f"Branch condition ({composite_operator})",
        composite_operator,
        eval_sub_checks,
    )

    passed = result.get("status") == "passed"
    _log.info("[if/else] result=%s → taking %s branch",
              passed, "true" if passed else "false")
    return passed
