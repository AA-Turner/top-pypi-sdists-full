"""Build the Chronos launch config for DatagenSession.

Fetches an experiment (cloud-managed config bundle) via the Chronos SDK,
stamps in the customer's envs with per-env db credentials fetched from
Plato's artifact API, and applies optional instruction/overrides.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

import httpx
from pydantic import BaseModel

from plato._generated.models import (
    EnvFromArtifact,
    EnvFromResource,
    EnvFromSimulator,
)
from plato.chronos.sdk import Chronos

logger = logging.getLogger(__name__)

REST_PORT = 8002
RUNTIME_ENV_ALIAS = "runtime"

EnvAny = EnvFromSimulator | EnvFromArtifact | EnvFromResource


class DatagenResponse(BaseModel):
    """Latest snapshot of the session's user-message state.

    Returned by :meth:`DatagenSession.poll_message`. ``status`` values:

    - ``idle``    — no message has ever been sent on this session
    - ``running`` — an agent run is in flight; ``text`` is empty
    - ``done``    — last run completed; ``text`` contains the agent's reply
    - ``error``   — last run failed; ``error`` describes what went wrong
    """

    status: str = "idle"
    text: str = ""
    error: str | None = None
    chronos_session_id: str = ""
    iteration: int = 0


def build_launch_config(
    envs: list[EnvAny],
    *,
    experiment: str,
    http_client: httpx.Client,
    api_key: str,
    base_url: str,
    instruction: str,
) -> dict[str, Any]:
    """Fetch an experiment + stamp customer envs and instruction.

    Experiments carry infrastructure only (world version, agent model, step
    shape). The agent's system instruction is passed in by the caller
    (typically a constant from :mod:`plato.v2`, e.g. ``DATA_LOAD_INSTRUCTION``).
    Pass ``""`` to run the agent with only its built-in default system prompt.

    Credentials (``${ANTHROPIC_API_KEY}`` etc.) live as placeholders in the
    experiment; Chronos resolves them from ``org_settings`` at launch time.
    The SDK never touches Claude/Anthropic keys.
    """
    # Fetch experiment template via the Chronos SDK.
    with Chronos(api_key=api_key) as chronos:
        files = chronos.experiments.list_files()
    match = next((f for f in files if f.name == experiment), None)
    if match is None or match.latest_version is None or match.latest_version.config_json is None:
        raise RuntimeError(
            f"Experiment {experiment!r} not found or has no published version. "
            f"Push it with: plato pm experiment agent <variant> push"
        )
    template = match.latest_version.config_json.model_dump(mode="json", exclude_none=True)
    world = template.get("world") or {}
    config = world.get("config")
    if not isinstance(config, dict):
        raise RuntimeError(f"Experiment {experiment!r} has invalid shape (missing world.config)")

    # Stamp per-env entries: alias + db MCP (from artifact) + vm + functions.
    seen: set[str] = set()
    env_entries: list[dict[str, Any]] = []
    for i, env in enumerate(envs):
        alias = env.alias or f"env-{uuid.uuid4().hex[:8]}"
        if alias == RUNTIME_ENV_ALIAS:
            raise ValueError(f"env.alias {RUNTIME_ENV_ALIAS!r} is reserved.")
        if alias in seen:
            raise ValueError(f"Duplicate env alias: {alias!r}")
        env.alias = alias
        seen.add(alias)

        artifact_id = getattr(env, "artifact_id", None)
        db_rows: list[dict[str, Any]] = []
        if artifact_id:
            try:
                resp = http_client.get(
                    f"{base_url}/api/v1/simulator/{artifact_id}/db_config",
                    headers={"X-API-Key": api_key},
                    timeout=30.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    db_rows = data if isinstance(data, list) else [data]
                else:
                    logger.warning("db_config %s for %s", resp.status_code, artifact_id)
            except Exception as exc:
                logger.warning("db_config fetch failed for %s: %s", artifact_id, exc)
        else:
            logger.warning("env %r has no artifact_id; db MCP will be skipped", alias)

        service = getattr(env, "simulator", None) or alias
        mcps: list[dict[str, Any]] = []
        for idx, db in enumerate(db_rows):
            raw = db.get("db_database") or f"db{idx}"
            name = "".join(c if (c.isalnum() or c == "_") else "_" for c in raw)
            name = name.lstrip("0123456789_") or "db"
            mcps.append(
                {
                    "type": "db",
                    "name": name,
                    "db_type": db.get("db_type") or "mysql",
                    "db_port": db.get("db_port") or 3306,
                    "db_user": db.get("db_user") or "",
                    "db_password": db.get("db_password") or "",
                    "db_database": db.get("db_database") or "",
                    "service": service,
                }
            )
        mcps.append({"type": "vm", "name": "vm"})
        mcps.append({"type": "functions", "name": "functions", "service": service})

        env_entries.append(
            {
                "env": env.model_dump(exclude_none=True, mode="json"),
                "mcps": mcps,
                "default": i == 0,
            }
        )

    config["envs"] = env_entries
    config["plato_api_key"] = api_key

    # Stamp the caller's instruction onto the first user_input step. ``""``
    # clears it (agent runs with the framework's built-in system prompt).
    for step in config.get("steps") or []:
        if step.get("source") == "user_input":
            step["instruction"] = instruction or None
            break
    else:
        raise ValueError(f"Experiment {experiment!r} has no user_input step to attach the instruction to.")

    return template


__all__ = [
    "DatagenResponse",
    "REST_PORT",
    "RUNTIME_ENV_ALIAS",
    "build_launch_config",
]
