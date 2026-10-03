"""Schema assertion helper — validate a captured API response against a JSON Schema (Draft 2020-12)."""
import json
import logging

_log = logging.getLogger("testmu_selenium")


def _fold_header_list(entries):
    folded = {}
    for item in entries:
        if isinstance(item, dict):
            pairs = [(k, v) for k, v in item.items() if isinstance(k, str)]
        elif isinstance(item, str) and "=" in item:
            name, _, value = item.split(";", 1)[0].partition("=")
            pairs = [(name.strip(), value.strip())]
        else:
            continue
        for k, v in pairs:
            key = k.lower()
            folded[key] = f"{folded[key]}, {v}" if key in folded else v
    return folded


def _normalize_envelope_for_schema(instance):
    if not isinstance(instance, dict) or "status" not in instance or "headers" not in instance:
        return instance
    out = dict(instance)
    changed = False
    for key in ("headers", "cookies"):
        if isinstance(out.get(key), list):
            out[key] = _fold_header_list(out[key])
            changed = True
    if "response_body" in out and out.get("response_body") is not None \
            and out.get("body") != out.get("response_body"):
        out["body"] = out["response_body"]
        changed = True
    return out if changed else instance


def verify_schema_assertion(
    schema_id: str = "",
    source_variable: str = "",
    failure_condition: str = "hard_fail",
    description: str = "",
) -> dict:
    from testmu_selenium._vars import _variable_store, _atms_get_schema, var

    _log.info(
        "    [schema_assertion] %s schema_id=%s source=%s failure=%s",
        (description or "")[:80], schema_id, source_variable, failure_condition,
    )

    if source_variable and ("{{" in source_variable or "${" in source_variable):
        instance = var(source_variable)
    elif source_variable in _variable_store:
        instance = _variable_store[source_variable]
    else:
        instance = var("{{" + source_variable + "}}")

    if isinstance(instance, str):
        try:
            instance = json.loads(instance)
        except (ValueError, TypeError):
            pass

    instance = _normalize_envelope_for_schema(instance)
    if isinstance(instance, dict) and "status" in instance and "headers" in instance \
            and ("response_body" in instance or "body" in instance):
        instance = instance.get("response_body", instance.get("body"))

    schema = _atms_get_schema(schema_id)

    from jsonschema import Draft202012Validator

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if not errors:
        _log.info("    [schema_assertion] result status=passed")
        return {"status": "passed"}

    reason = "; ".join(
        f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
        for err in errors
    )
    _log.info("    [schema_assertion] result status=failed reason=%s", reason[:200])

    raise AssertionError(f"Schema assertion failed: {description} — {reason}")
