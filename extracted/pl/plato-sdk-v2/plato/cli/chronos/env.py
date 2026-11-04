"""Chronos org-secret resolution for local dev and test runs.

Resolves the ``${VAR}`` placeholders in a world config by asking Chronos for
each referenced secret **by name** (``GET /api/secrets/{name}``), which
resolves it the way a launch does: org-wide values overlaid by the caller's
own.

This replaces reading the whole ``chronos:analyzer-env`` table. That read is
masked now that org secrets are encrypted at rest — it answers with every
secret's name and ``********`` in place of its value — so it cannot serve a
caller that needs a usable value, and pulling every credential the org has to
reach one of them was a bad deal even before that. Substituting the mask is
how a missing credential used to surface three layers downstream as
``401 Invalid bearer token``, reading like a rotated key rather than an
absent one.
"""

from __future__ import annotations

import logging
import re
from typing import Any, NamedTuple
from urllib.parse import quote

import httpx

from plato.cli.chronos.settings import get_settings

logger = logging.getLogger(__name__)

_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


class UnresolvedSecretError(RuntimeError):
    """A config still references ``${VAR}`` names that nothing supplied."""


def substitute_env_vars(obj: Any, values: dict[str, str]) -> Any:
    """Replace ``${VAR}`` placeholders in all string values of a nested object.

    Returns a new object — does not mutate the input.
    """
    if isinstance(obj, str):
        return _ENV_VAR_PATTERN.sub(lambda m: values.get(m.group(1), m.group(0)), obj)
    if isinstance(obj, list):
        return [substitute_env_vars(item, values) for item in obj]
    if isinstance(obj, dict):
        return {k: substitute_env_vars(v, values) for k, v in obj.items()}
    return obj


def placeholder_names(obj: Any) -> set[str]:
    """Every ``${VAR}`` name still standing in a nested object."""
    if isinstance(obj, str):
        return set(_ENV_VAR_PATTERN.findall(obj))
    if isinstance(obj, list):
        return {name for item in obj for name in placeholder_names(item)}
    if isinstance(obj, dict):
        return {name for value in obj.values() for name in placeholder_names(value)}
    return set()


class SecretLookup(NamedTuple):
    """What Chronos said about the names we asked for.

    ``problems`` never holds a name Chronos answered 404 for — that is a
    definite "not set", not a failed lookup.
    """

    values: dict[str, str]
    problems: dict[str, str]


async def fetch_secrets(names: set[str], api_key: str | None = None) -> SecretLookup:
    """Ask Chronos for each named secret, one request per name.

    A 404 is an answer: Chronos does not have that secret. Anything else —
    an unreachable host, a rejected API key, a 500 — is a *failure to ask*,
    and is kept apart from the 404s so the caller can say which one happened
    instead of telling someone to go set a secret that is already there.
    """
    if not names:
        return SecretLookup(values={}, problems={})

    settings = get_settings()
    values: dict[str, str] = {}
    problems: dict[str, str] = {}

    async with httpx.AsyncClient(
        base_url=settings.chronos_url.rstrip("/"),
        timeout=30.0,
        headers={"X-API-Key": api_key} if api_key else {},
    ) as client:
        for name in sorted(names):
            try:
                resp = await client.get(f"/api/secrets/{quote(name, safe='')}")
            except httpx.RequestError as exc:
                problems[name] = f"could not reach Chronos ({type(exc).__name__})"
                logger.warning("Could not reach Chronos for secret %s: %r", name, exc)
                continue
            if resp.status_code == 404:
                logger.debug("Chronos has no secret named %s", name)
                continue
            if resp.status_code != 200:
                problems[name] = f"Chronos answered HTTP {resp.status_code}"
                logger.warning("Secret %s came back HTTP %d", name, resp.status_code)
                continue
            value = resp.json().get("value")
            if isinstance(value, str):
                values[name] = value
            else:
                problems[name] = "Chronos answered without a string value"
                logger.warning("Secret %s came back without a string value", name)

    return SecretLookup(values=values, problems=problems)


async def resolve_config_env_vars(config: dict[str, Any], api_key: str | None = None) -> None:
    """Resolve the config's ``${VAR}`` placeholders from Chronos, in place.

    Raises :class:`UnresolvedSecretError` if any placeholder is left over. A
    ``${VAR}`` that reaches an agent verbatim is always a bug, and failing
    here names it instead of letting it surface as a downstream auth error.
    """
    wanted = placeholder_names(config)
    if not wanted:
        return

    lookup = await fetch_secrets(wanted, api_key)
    if lookup.values:
        logger.info(
            "Resolved %d secrets from Chronos: %s",
            len(lookup.values),
            ", ".join(sorted(lookup.values)),
        )

    substituted = substitute_env_vars(config, lookup.values)
    if isinstance(substituted, dict):
        config.clear()
        config.update(substituted)

    missing = sorted(placeholder_names(config))
    if not missing:
        return

    names = ", ".join(missing)
    # Chronos never got to answer for some of these, so "go set the secret"
    # would be the wrong advice — it may well be set already.
    blocked = {name: lookup.problems[name] for name in missing if name in lookup.problems}
    if blocked:
        detail = "; ".join(f"{name} — {why}" for name, why in sorted(blocked.items()))
        raise UnresolvedSecretError(
            f"Could not resolve {names}: Chronos could not be asked ({detail}). "
            "That is a connection or credential problem on this side, not a missing "
            "secret — check PLATO_API_KEY and that Chronos is reachable."
        )

    it = "them" if len(missing) > 1 else "it"
    raise UnresolvedSecretError(
        f"Nothing supplied {names}. Set {it} in the org's Chronos environment, or export "
        f"{it} in your shell and list the name{'s' if len(missing) > 1 else ''} in this "
        f'config\'s `test.pass_env` (e.g. "pass_env": ["PLATO_API_KEY", "{missing[0]}"]), '
        "which substitutes before Chronos is asked."
    )
