"""Redaction of secret-bearing tool arguments before telemetry emission.

Redaction != truncation. We preserve the full structure/content of every event
in the durable store; we only mask *secret values*. The secret-bearing tools are
`create_secret` / `update_secret`, whose args carry raw secret material.

Response bodies are opaque strings we don't parse, so response "redaction" is
best-effort: we scrub any *known* secret value (captured from the args) out of
the response text. Handlers are not expected to echo secrets back, so this is a
defense-in-depth backstop, not the primary control.
"""

from __future__ import annotations

import json

from typing import Any

REDACTED = "***REDACTED***"

# Arg keys whose values are secret material, regardless of tool. Kept as a set so
# it is trivial to extend when a new secret-bearing tool/arg lands.
SENSITIVE_ARG_KEYS: frozenset[str] = frozenset(
    {"secret_value", "secret_keys", "secret_key_value", "contact_email"}
)
# `contact_email` is not a credential. It is here because it is the ONLY path by
# which a cleartext user address can enter tool args: `send_feedback` resolves
# the reporter server-side from the API key and accepts this fallback only for a
# bot/CLI key with no address on file. Issue #231 keeps cleartext email out of the
# archive (domain + hash only); masking it here means taking the fallback does not
# quietly widen what the archive holds.

# Args whose value is a JSON BLOB that may contain secrets under some keys but not
# others. Masking the whole thing would lose the diagnostic value of `apps` and the
# rest, so it is masked per-key using the same name test the tool output uses —
# `modules._is_secret_variable`.
#
# Why this exists: `expose`/`unexpose` mint a Teleport join token server-side, so it
# never appears in their args. But `install_module`/`update_module_variables` take it
# from the CALLER — the documented Teleport-agent install flow passes
# `variables={"authToken": "<live join token>"}` — and masking the tool RESPONSE left
# that leg untouched, so the token still reached the S3 archive and the OTLP span.
STRUCTURED_ARG_KEYS: frozenset[str] = frozenset({"variables"})


def redact_args(args: Any) -> Any:
    """Return a deep copy of `args` with sensitive values masked.

    Recurses into nested dicts/lists so a secret nested under a sensitive key is
    masked wholesale.
    """
    if isinstance(args, dict):
        out: dict[str, Any] = {}
        for key, value in args.items():
            if key in SENSITIVE_ARG_KEYS:
                out[key] = REDACTED
            elif key in STRUCTURED_ARG_KEYS:
                out[key] = _redact_structured(value)
            else:
                out[key] = redact_args(value)
        return out
    if isinstance(args, list):
        return [redact_args(v) for v in args]
    return args


def collect_secret_values(args: Any) -> list[str]:
    """Collect the raw secret values present in `args`, stringified.

    Used to scrub these exact substrings out of response text as a backstop.
    """
    found: list[str] = []

    def _walk(node: Any, under_secret_key: bool) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                _walk(value, under_secret_key or key in SENSITIVE_ARG_KEYS)
        elif isinstance(node, list):
            for value in node:
                _walk(value, under_secret_key)
        elif under_secret_key and node is not None:
            text = str(node)
            if text:
                found.append(text)

    _walk(args, False)
    return found


def scrub_secrets(text: str | None, secret_values: list[str]) -> str | None:
    """Replace any known secret value substring in `text` with the redaction
    marker. Best-effort backstop for responses that unexpectedly echo a secret.
    """
    if not text or not secret_values:
        return text
    scrubbed = text
    # Longest-first so an overlapping shorter secret can't partially unmask.
    for value in sorted(set(secret_values), key=len, reverse=True):
        if value and value in scrubbed:
            scrubbed = scrubbed.replace(value, REDACTED)
    return scrubbed


def _redact_structured(value: Any) -> Any:
    """Mask secret-named entries inside a JSON-string (or dict) arg.

    Returns the value unchanged if it is not parseable as an object — better to keep
    an odd shape visible than to silently drop a diagnostic, and the only values that
    reach here are ones a caller passed as `variables`.
    """
    from cube_cloud.tools.modules import _is_secret_variable, _value_is_sensitive

    raw = value
    if isinstance(value, str):
        try:
            raw = json.loads(value)
        except (ValueError, TypeError):
            return REDACTED  # unparseable: cannot tell what is in it, so mask it all
    if not isinstance(raw, dict):
        return REDACTED
    masked = {
        k: (REDACTED if (_is_secret_variable(str(k)) or _value_is_sensitive(v)) else v)
        for k, v in raw.items()
    }
    return json.dumps(masked) if isinstance(value, str) else masked
