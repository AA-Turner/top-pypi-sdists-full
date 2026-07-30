"""Network helpers — HAR polling and assertion evaluation against the variable store.

network_query: sync HAR poller — mirrors playwright's async networkQuery,
    stripped of asyncio. Uses requests + time.sleep instead of aiohttp +
    asyncio.sleep.

evaluate_network_assertion: sync, deterministic, no smart gate.
"""
import logging
import re

from testmu_selenium.condition import _normalize_bool_str

_log = logging.getLogger("testmu_selenium")


def network_query(method, url, index, network_log_id=None, polling_interval=2, max_polling_time=10) -> dict:
    """Sync HAR poller for NETWORK assertions / DRIVER_QUERY ops.
    Mirrors the async networkQuery implementation in the code generator."""
    import requests
    import time

    har_base = "http://127.0.0.1:8181"

    _log.info("    [network_query] starting — method=%s, url=%s, index=%s, network_log_id=%s",
              method, url[:80], index, network_log_id)

    if network_log_id:
        try:
            resp = requests.get(f"{har_base}/logs/entry?id={network_log_id}", timeout=30)
            data = resp.json()
            entry = data.get("entry", {})
            if entry:
                _log.info("    [network_query] found entry by network_log_id=%s", network_log_id)
                return _decode_har_entry(entry)
            _log.info("    [network_query] entry not found by network_log_id, falling back to polling")
        except Exception as e:
            _log.info("    [network_query] network_log_id lookup failed: %s, falling back to polling", e)

    num_tries = 0
    max_tries = int(max_polling_time / polling_interval)

    while num_tries < max_tries:
        num_tries += 1
        _log.info("    [network_query] polling attempt %d/%d", num_tries, max_tries)
        try:
            resp = requests.get(f"{har_base}/logs", timeout=30)
            data = resp.json()
            entries = data.get("log", {}).get("entries", [])
            _log.info("    [network_query] HAR has %d entries, matching method=%s url=%s",
                      len(entries), method, url[:60])
            match_index = 0
            for entry in entries:
                if entry["request"]["method"] == method and entry["request"]["url"] == url:
                    match_index += 1
                    if match_index == int(index):
                        entry_id = entry.get("_id", "")
                        _log.info("    [network_query] matched at match_index=%d, entry_id=%s",
                                  match_index, entry_id)
                        if entry_id:
                            resp2 = requests.get(f"{har_base}/logs/entry?id={entry_id}", timeout=30)
                            full_data = resp2.json()
                            full_entry = full_data.get("entry", {})
                            if full_entry:
                                _log.info("    [network_query] fetched full entry for id=%s", entry_id)
                                return _decode_har_entry(full_entry)
                        return _decode_har_entry(entry)
        except Exception as e:
            _log.info("    [network_query] polling error: %s", e)
        time.sleep(polling_interval)

    _log.info("    [network_query] no match found after %d attempts", max_tries)
    return {}


def _decode_har_entry(entry):
    """Decode base64/JSON bodies in HAR entry IN-PLACE, preserving full HAR nesting."""
    import base64 as _b64
    import json as _json

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


def evaluate_network_assertion(assertion_tree: dict) -> bool:
    """Evaluate a network assertion tree against the current variable store.

    Resolves {{var.path}} placeholders from testmu_selenium._vars._variable_store,
    then walks the operator tree (and/or/leaf) to produce a boolean result.

    Args:
        assertion_tree: Dict with operator, operands (for and/or nodes) or
            left_operand/right_operand (for leaf comparison nodes).

    Returns:
        True if the assertion passes.

    Raises:
        AssertionError: If the assertion evaluates to False.
    """
    from testmu_selenium._vars import _variable_store

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
            _log.debug("    [network_assertion] var '%s' not found", var_name)
            return operand
        value = variables[var_name]
        if len(parts) > 1:
            for key in parts[1].split('.'):
                if isinstance(value, dict):
                    value = value.get(key, '')
                else:
                    _log.debug("    [network_assertion] path '%s' — non-dict at key '%s'", path, key)
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
            # Normalize a bool-vs-string pair (True == 'true') before comparing,
            # matching the primary Assertion evaluator; str() otherwise.
            l, r = _normalize_bool_str(left, right)
            result = str(l) == str(r)
        elif op == 'not_equals':
            l, r = _normalize_bool_str(left, right)
            result = str(l) != str(r)
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
        return result

    result = _evaluate_node(assertion_tree, _variable_store)
    _log.info("    [network_assertion] result=%s", "PASS" if result else "FAIL")
    assert result, f"Network assertion failed: {assertion_tree}"
    return result
