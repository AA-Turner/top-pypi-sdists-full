"""Helpers for classifying session environments."""

from __future__ import annotations

# Matches the backend's app/proctor_constants.py PROCTOR_SERVICE_NAME: the proctor
# job's `service` (surfaced to the SDK as the env's `simulator` and default `alias`).
PROCTOR_SERVICE_NAME = "proctor"


def is_proctor_env(env: object) -> bool:
    """True if this session env is the proctor scoring service.

    Sessions made from a PEX test case include a proctor env (the scoring
    service). It has a real ``artifact_id`` but no login flow and must stay
    invisible to the agent, so login loops skip it.

    Duck-typed: callers pass ``plato.v2.{sync,async_}`` ``Environment`` actors,
    generated ``EnvironmentContext`` models, or v1 env objects — the attribute
    set isn't known at author time, hence ``getattr``. Checks ``simulator``
    (the job's service name) with ``alias`` as a fallback for contexts that
    don't carry ``simulator`` (e.g. async ``create(wait=False)``).
    """
    return PROCTOR_SERVICE_NAME in (
        getattr(env, "simulator", None),
        getattr(env, "alias", None),
    )
