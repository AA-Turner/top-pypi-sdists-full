"""Network helpers — assertion evaluation and HAR-based network query.

evaluate_network_assertion: sync, deterministic, no smart gate.
network_query: async — polls HAR endpoint resolved via _config.get_har_url().
"""
import json as _json
import logging
import os
import re

from testmu._helpers._errors import AssertionFailureError

_log = logging.getLogger("testmu")

# Operand values are captured HAR responses and can run to hundreds of
# kilobytes; keep the failure message readable.
_OPERAND_PREVIEW_CHARS = 200


def _preview(value: str) -> str:
    """Render an operand for a failure message: quoted, length-tagged, truncated."""
    if len(value) <= _OPERAND_PREVIEW_CHARS:
        return repr(value)
    return f"{value[:_OPERAND_PREVIEW_CHARS]!r}… ({len(value)} chars)"


def _format_failed_leaves(failed_leaves: list) -> str:
    """Describe each failing comparison by its *resolved* operands."""
    if not failed_leaves:
        return "no leaf comparison recorded"
    return "; ".join(
        f"{_preview(left)} {op} {_preview(right)}"
        for op, left, right in failed_leaves
    )


def evaluate_network_assertion(assertion_tree: dict) -> dict:
    """Evaluate a network assertion tree against the current variable store.

    Resolves {{var.path}} placeholders from testmu._vars._variable_store,
    then walks the operator tree (and/or/leaf) to produce a verdict.

    Returns a dict shaped like verify_assertion: {"status": "passed"|"failed",
    "tree": <the input tree>}. On `status==failed`, honors
    TESTMU_SKIP_ASSERTION_FAILURE env: truthy → log [ASSERTION WARN] + return
    dict; unset → raise AssertionFailureError so the step honors authored
    on_failure.

    Args:
        assertion_tree: Dict with operator, operands (for and/or nodes) or
            left_operand/right_operand (for leaf comparison nodes).

    Returns:
        Dict with "status" and "tree" keys.

    Raises:
        AssertionFailureError: If the assertion evaluates to False and the
            TESTMU_SKIP_ASSERTION_FAILURE env var is unset.
    """
    from testmu._vars import _variable_store

    _log.info("    [network_assertion] evaluating operator=%s operands=%d",
              assertion_tree.get('operator', '?'),
              len(assertion_tree.get('operands', [])))

    def _resolve_operand(operand, variables):
        if isinstance(operand, dict):
            operand = next(iter(operand.keys()), '')
        match = re.match(r'^\{\{(.+?)\}\}$', str(operand).strip())
        if not match:
            return operand
        path = match.group(1)
        parts = path.split('.', 1)
        var_name = parts[0]
        if var_name not in variables:
            # info, not debug: an operand that silently stays a template is the
            # single most misleading state this evaluator can be in.
            _log.info("    [network_assertion] var '%s' not found — operand stays unresolved", var_name)
            return operand
        value = variables[var_name]
        if len(parts) > 1:
            for key in parts[1].split('.'):
                if isinstance(value, dict):
                    value = value.get(key, '')
                else:
                    # A None here means network_query found nothing and set_var
                    # stored None, so the operand collapses to ''. Say so at info
                    # level rather than letting it look like a resolution bug.
                    _log.info(
                        "    [network_assertion] path '%s' — %s at key '%s', resolving to ''",
                        path, "value is None" if value is None else "non-dict", key,
                    )
                    return ''
        return value

    def _evaluate_node(node, variables):
        op = node.get('operator', '').lower()
        if op in ('and', 'or'):
            results = [_evaluate_node(operand, variables) for operand in node.get('operands', [])]
            combined = all(results) if op == 'and' else any(results)
            return combined
        left = _resolve_operand(node.get('left_operand', ''), variables)
        right = _resolve_operand(node.get('right_operand', ''), variables)
        left_str, right_str = str(left), str(right)
        if op == 'equals':
            result = left_str == right_str
        elif op == 'not_equals':
            result = left_str != right_str
        elif op == 'contains':
            result = right_str in left_str
        elif op == 'not_contains':
            result = right_str not in left_str
        elif op in ('greater_than', 'greater_than_or_equal'):
            try:
                result = float(left) > float(right) if op == 'greater_than' else float(left) >= float(right)
            except (ValueError, TypeError):
                result = False
        elif op in ('less_than', 'less_than_or_equal'):
            try:
                result = float(left) < float(right) if op == 'less_than' else float(left) <= float(right)
            except (ValueError, TypeError):
                result = False
        elif op == 'start_with':
            result = left_str.startswith(right_str)
        elif op == 'end_with':
            result = left_str.endswith(right_str)
        else:
            _log.warning("    [network_assertion] unknown operator '%s'", op)
            result = False
        if not result:
            failed_leaves.append((op, left_str, right_str))
        return result

    failed_leaves = []
    passed = _evaluate_node(assertion_tree, _variable_store)
    _log.info("    [network_assertion] result=%s", "PASS" if passed else "FAIL")
    result = {"status": "passed" if passed else "failed", "tree": assertion_tree}

    if not passed:
        # Report what the comparison actually compared. The tree still holds the
        # unresolved {{var}} templates, so a tree-only message reads as though the
        # operand never resolved when in fact it resolved to '' — which is how an
        # unreachable HAR service used to present itself (TE-27434).
        detail = _format_failed_leaves(failed_leaves)
        if os.environ.get("TESTMU_SKIP_ASSERTION_FAILURE"):
            _log.warning(
                "[ASSERTION WARN] Network assertion failed: %s | %s", detail, assertion_tree,
            )
            return result
        raise AssertionFailureError(
            f"Network assertion failed: {detail}", result=result,
        )
    return result


# ---------------------------------------------------------------------------
# network_query — polls a HAR-format endpoint (configurable via env vars)
# ---------------------------------------------------------------------------

async def network_query(method, url, index, network_log_id="", polling_interval=2, max_polling_time=10):
    """Poll a HAR-format endpoint for a matching network entry.

    HAR endpoint is resolved at call time via _config.get_har_url():
      - TESTMU_HAR_HOST / TESTMU_HAR_PORT env vars if PORT is set, else
      - http://127.0.0.1:8181 if TESTMU_RUN_TARGET=cloud, else None (skipped).

    Args:
        method: HTTP method to match (e.g. "GET", "POST").
        url: Full URL to match.
        index: 1-based occurrence index for duplicate URLs.
        network_log_id: Optional direct entry ID — skips polling when provided.
        polling_interval: Seconds between polling attempts.
        max_polling_time: Total seconds before giving up.

    Returns:
        Decoded HAR entry dict, or None when HAR endpoint is unconfigured /
        no match found.
    """
    from testmu import _config

    _har_base = _config.get_har_url()
    if _har_base is None:
        _log.info("    [network_query] HAR endpoint not configured (no port env, not cloud) — skipping")
        return None

    import asyncio
    import aiohttp
    from testmu._helpers._http import create_session

    _log.info("    [network_query] %s %s (index=%s)", method, url[:80], index)

    if network_log_id:
        try:
            async with create_session() as session:
                async with session.get(
                    f"{_har_base}/logs/entry?id={network_log_id}",
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status == 200:
                        try:
                            data = await resp.json(content_type=None)
                            entry = data.get("entry", {}) if isinstance(data, dict) else {}
                            if entry:
                                _log.info("    [network_query] found by log_id=%s", network_log_id)
                                return _decode_har_entry(entry)
                        except (aiohttp.ContentTypeError, ValueError):
                            pass
                    _log.debug(
                        "    [network_query] log_id %s not in HAR (status=%d), falling back to polling",
                        network_log_id, resp.status,
                    )
        except Exception as e:
            _log.debug("    [network_query] log_id lookup error: %s (falling back)", e)

    num_tries = 0
    max_tries = int(max_polling_time / polling_interval)
    poll_failures = 0
    last_error = None

    while num_tries < max_tries:
        num_tries += 1
        try:
            async with create_session() as session:
                async with session.get(
                    f"{_har_base}/logs",
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status != 200:
                        _log.debug("    [network_query] /logs returned %d", resp.status)
                        await asyncio.sleep(polling_interval)
                        continue
                    data = await resp.json(content_type=None)

            entries = data.get("log", {}).get("entries", [])
            _log.info("    [network_query] attempt %d/%d — %d HAR entries",
                      num_tries, max_tries, len(entries))

            match_index = 0
            for entry in entries:
                req = entry.get("request", {})
                if req.get("method") == method and req.get("url") == url:
                    match_index += 1
                    if match_index == int(index):
                        entry_id = entry.get("_id", "")
                        _log.info("    [network_query] matched at occurrence %d, entry_id=%r",
                                  match_index, entry_id)
                        if entry_id:
                            # Best-effort enrichment via /logs/entry; fall through to listing entry on failure.
                            try:
                                async with create_session() as s2:
                                    async with s2.get(
                                        f"{_har_base}/logs/entry?id={entry_id}",
                                        timeout=aiohttp.ClientTimeout(total=30),
                                    ) as resp2:
                                        if resp2.status == 200:
                                            try:
                                                full_data = await resp2.json(content_type=None)
                                                full_entry = full_data.get("entry", {}) if isinstance(full_data, dict) else {}
                                                if full_entry:
                                                    return _decode_har_entry(full_entry)
                                            except (aiohttp.ContentTypeError, ValueError):
                                                pass
                                        else:
                                            _log.debug(
                                                "    [network_query] entry-detail %s returned %d, using listing entry",
                                                entry_id, resp2.status,
                                            )
                            except Exception as e:
                                _log.debug(
                                    "    [network_query] entry-detail fetch failed: %s, using listing entry",
                                    e,
                                )
                        return _decode_har_entry(entry)
        except Exception as e:
            poll_failures += 1
            last_error = e
            _log.info("    [network_query] polling error: %s", e)

        await asyncio.sleep(polling_interval)

    if poll_failures == num_tries and num_tries > 0:
        # Every attempt raised, so the HAR service was never reached. That is a
        # different failure from "the service answered and had no such request",
        # and it used to be indistinguishable downstream: both ended as
        # set_var(name, None) and an operand resolving to '' (TE-27434).
        _log.error(
            "    [network_query] HAR service unreachable at %s — all %d attempt(s) failed, "
            "last error: %s. Network capture is probably not enabled for this run "
            "(LT:Options.network / NETWORK=true).",
            _har_base, num_tries, last_error,
        )
    else:
        _log.info("    [network_query] no match found after %d attempts", max_tries)
    return None


def _decode_har_entry(entry):
    """Decode base64/JSON bodies in a HAR entry in-place."""
    import base64 as _b64

    resp_content = entry.get("response", {}).get("content", {})
    if "application/json" in resp_content.get("mimeType", ""):
        resp_text = resp_content.get("text", "")
        if resp_content.get("encoding") == "base64" and resp_text:
            try:
                resp_text = _b64.b64decode(resp_text).decode("utf-8")
            except Exception:
                pass
        if resp_text:
            try:
                entry["response"]["content"]["text"] = _json.loads(resp_text)
            except (_json.JSONDecodeError, TypeError):
                pass
        else:
            entry["response"]["content"]["text"] = {}

    req_post = entry.get("request", {}).get("postData", {})
    if "application/json" in req_post.get("mimeType", ""):
        req_text = req_post.get("text", "")
        if req_post.get("encoding") == "base64" and req_text:
            try:
                req_text = _b64.b64decode(req_text).decode("utf-8")
            except Exception:
                pass
        if req_text:
            try:
                entry["request"]["postData"]["text"] = _json.loads(req_text)
            except (_json.JSONDecodeError, TypeError):
                pass
        else:
            entry["request"]["postData"]["text"] = {}

    return entry
