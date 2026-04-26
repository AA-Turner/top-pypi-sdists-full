"""Plato v2 — synchronous DatagenSession."""

from __future__ import annotations

import logging
import time

import httpx

from plato._generated.api.v2.artifacts import get_artifact
from plato._generated.api.v2.sessions import close as sessions_close
from plato._generated.api.v2.sessions import wait_for_ready as sessions_wait_for_ready
from plato.chronos.sdk import Chronos
from plato.v2._datagen_launch import (
    REST_PORT,
    RUNTIME_ENV_ALIAS,
    DatagenResponse,
    build_launch_config,
)
from plato.v2._wait_for_ready import poll_until_ready_sync
from plato.v2.sync.session import Session
from plato.v2.types import EnvFromArtifact, EnvFromResource, EnvFromSimulator

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Built-in agent system instructions.
#
# These are shipped with the SDK so customers can see/extend what the agent is
# told (vs. it being buried in a cloud experiment). Import and pass via
# ``instruction=`` to ``plato.datagen_sessions.create(...)``:
#
#     from plato.v2 import DATA_LOAD_INSTRUCTION
#     session = plato.datagen_sessions.create(
#         envs=[Env.artifact(artifact_id)],
#         experiment="agent-data-load",
#         instruction=DATA_LOAD_INSTRUCTION,
#     )
#
# Extend by concatenation: ``instruction=DATA_LOAD_INSTRUCTION + "\n\n..."``.
# ---------------------------------------------------------------------------

DATA_LOAD_INSTRUCTION = """\
You are a data-loading agent. Your job is to insert user-provided records into a live application's database. The user has already produced the data — you are NOT generating it. Your job is to land it correctly.

== TOOL PRIORITY ==

1. db MCP (preferred for inserts):
   - db.get_table_schemas first to confirm columns, types, and constraints.
   - db.insert_rows for bulk inserts (single call per ~100-row batch).
   - db.select_context to verify counts and sample rows.
   ~10x faster and more reliable than the UI.

2. vm MCP (for source files and shell verification):
   - vm.exec to read source files, run psql/mysql/mongo commands, etc.
   - vm.make_file is for creating helper files; the user has already uploaded the source if the prompt references a file path.

3. browser MCP (only when required):
   - Use only for UI-only flows (file uploads with thumbnails, multi-step forms with computed fields). Skip for plain DB inserts.

== FIELD MAPPING ==

If source keys don't match column names exactly:
- Match by semantic meaning (full_name → name, email_address → email).
- For dropdown/enum columns, look up valid values via db.get_table_schemas and map source values to the nearest valid option.
- For foreign keys, resolve referenced entities by name or external_id via db.select_context. If the referenced row doesn't exist, FLAG the source row (do not silently null the FK; do not create a placeholder).

For required columns the source doesn't provide:
- Use sensible defaults (created_at = now, status = the table's default enum value, etc.).
- NEVER fabricate critical fields like name, email, amount — flag the row instead.

== HARD RULES ==

- PRESERVE user-provided values EXACTLY. Do not 'improve', 'diversify', or vary names, emails, dates, amounts, IDs, or any other value the user supplied.
- NEVER modify schema (no ALTER TABLE, no migrations, no new columns).
- NEVER restart services or change Docker/env files.
- NEVER skip a row silently. Every failure must appear in the final report with its row index and the underlying error.
- If the schema doesn't match the source data shape, STOP and report rather than mangling the data to fit.

== EXECUTION ==

1. Identify the target table from the user's prompt + the data.
2. db.get_table_schemas on the target table.
3. db.select_context 'SELECT COUNT(*) ...' → record before_count.
4. db.insert_rows in batches of ~100. On per-row failure, log the index + error and continue with the rest of the batch.
5. db.select_context COUNT(*) again → record after_count.
6. db.select_context first 2-3 inserted rows → include in report sample.

== FINAL REPORT ==

Your last message MUST be a single JSON object on its own line, like:

{"table": "<name>", "before_count": <int>, "after_count": <int>, "rows_inserted": <int>, "rows_failed": <int>, "failures": [{"row_index": int, "error": str, "row_keys": [str]}, ...], "sample": [<2-3 inserted records>]}

No prose around the JSON. The caller parses this directly."""


class DatagenSession(Session):
    """Session that launches via a Chronos experiment and drives an in-VM agent loop.

    Adds :meth:`send_message` and :meth:`stop_conversation`.
    """

    _runtime_connect_url: str | None = None

    # -- Construction ---------------------------------------------------

    @classmethod
    def from_envs(  # type: ignore[override]
        cls,
        http_client: httpx.Client,
        api_key: str,
        envs: list[EnvFromSimulator | EnvFromArtifact | EnvFromResource],
        *,
        experiment: str,
        instruction: str,
        allow_prerelease: bool = True,
        timeout: int = 1800,
    ) -> DatagenSession:
        """Launch a DatagenSession from a Chronos experiment.

        ``instruction`` is the agent's system prompt — pass one of the
        SDK-shipped constants (e.g. ``DATA_LOAD_INSTRUCTION`` — importable
        from :mod:`plato.v2`) or your own string. ``""`` runs the agent with
        only its built-in default prompt. Credentials (``ANTHROPIC_API_KEY``
        etc.) are resolved by Chronos from ``org_settings`` at launch — never
        via the SDK.
        """
        base_url = str(http_client.base_url).rstrip("/")
        template = build_launch_config(
            envs,
            experiment=experiment,
            http_client=http_client,
            api_key=api_key,
            base_url=base_url,
            instruction=instruction,
        )
        world = template["world"]

        with Chronos(api_key=api_key) as chronos:
            launch = chronos.launch(
                package=world["package"],
                config=world["config"],
                runtime=world.get("runtime"),
                tags=(template.get("tags") or []) + ["datagen-session"],
                allow_prerelease=allow_prerelease,
            )
        session_id = launch.session_id
        logger.info(f"[DatagenSession] Chronos launched session={session_id}")

        try:
            session = cls._hydrate_from_session_id(http_client, api_key, session_id, timeout=timeout)
        except Exception:
            try:
                with Chronos(api_key=api_key) as cleanup:
                    cleanup.stop(session_id)
            except Exception as stop_err:
                logger.warning(f"[DatagenSession] stop after hydrate-fail: {stop_err}")
            raise

        runtime_env = session.get_env(RUNTIME_ENV_ALIAS)
        if runtime_env is None:
            raise RuntimeError(
                f"No {RUNTIME_ENV_ALIAS!r} env in session after Chronos launch (got {[e.alias for e in session.envs]})"
            )
        session._runtime_connect_url = f"https://{runtime_env.job_id}--{REST_PORT}.connect.plato.so"
        session._wait_for_rest_ready(timeout=timeout)

        # The world's reset() adds customer envs AFTER our first wait_for_ready
        # returned (only `runtime` was present then). Re-poll so session.envs
        # reflects the full set.
        try:
            session.wait_until_ready(timeout=30.0)
        except Exception as exc:
            logger.warning(f"[DatagenSession] post-launch env refresh failed: {exc}")
        return session

    @classmethod
    def _hydrate_from_session_id(
        cls,
        http_client: httpx.Client,
        api_key: str,
        session_id: str,
        timeout: int = 1800,
    ) -> DatagenSession:
        """Adopt an already-created Plato session (Chronos just launched one)."""
        try:
            ready_response = poll_until_ready_sync(
                lambda per_call: sessions_wait_for_ready.sync(
                    client=http_client,
                    session_id=session_id,
                    timeout=per_call,
                    x_api_key=api_key,
                ),
                timeout=int(timeout),
            )
            context = cls._check_ready_response(ready_response, timeout)
        except (TimeoutError, RuntimeError):
            try:
                sessions_close.sync(client=http_client, session_id=session_id, x_api_key=api_key)
            except Exception as close_err:
                logger.warning(f"close after hydrate-fail: {close_err}")
            raise

        for env_ctx in context.envs or []:
            if not env_ctx.simulator and env_ctx.artifact_id:
                try:
                    env_ctx.simulator = get_artifact.sync(
                        client=http_client,
                        artifact_id=env_ctx.artifact_id,
                        x_api_key=api_key,
                    ).simulator_name
                except Exception:
                    pass

        session = cls(http_client=http_client, api_key=api_key, context=context)
        session.start_heartbeat()
        return session

    # -- REST calls -----------------------------------------------------

    def _wait_for_rest_ready(self, timeout: float = 300.0) -> None:
        # /api/health (not /health) — connect.plato.so's nginx intercepts /health
        # with its own response and would false-pass before the app is up.
        assert self._runtime_connect_url is not None
        deadline = time.monotonic() + timeout
        last_error: str | None = None
        while time.monotonic() < deadline:
            try:
                resp = self._http.get(
                    f"{self._runtime_connect_url}/api/health",
                    timeout=10.0,
                )
                if resp.status_code == 200 and "structured-execution-rest" in resp.text:
                    logger.info("[DatagenSession] REST server ready")
                    return
                last_error = f"status={resp.status_code} body={resp.text[:120]!r}"
            except Exception as exc:
                last_error = str(exc)
            time.sleep(2.0)
        raise TimeoutError(
            f"REST server on {self._runtime_connect_url} not ready within {timeout}s (last: {last_error})"
        )

    def _require_runtime(self, op: str) -> str:
        self._check_closed()
        if self._runtime_connect_url is None:
            raise RuntimeError(f"DatagenSession.{op} requires a DatagenSession created via DatagenSession.from_envs().")
        return self._runtime_connect_url

    def send_message(self, prompt: str, *, env: str | None = None) -> None:
        """Queue a prompt for the active user_input step.

        Returns immediately. The agent run starts on the world's next step
        loop iteration; call :meth:`poll_message` to retrieve the result.
        Raises if another message is already in flight (one at a time).
        """
        url = self._require_runtime("send_message")
        resp = self._http.post(
            f"{url}/send_message",
            json={"prompt": prompt, "env_alias": env},
            timeout=30.0,
        )
        if resp.status_code == 409:
            raise RuntimeError(resp.json().get("detail", "send_message rejected"))
        resp.raise_for_status()

    def poll_message(self) -> DatagenResponse:
        """Snapshot the latest message state.

        Returns immediately with current state — caller writes their own
        polling loop. ``status`` is one of ``idle | running | done | error``.
        """
        url = self._require_runtime("poll_message")
        resp = self._http.post(f"{url}/poll_message", timeout=30.0)
        resp.raise_for_status()
        return DatagenResponse.model_validate(resp.json())

    def stop_conversation(self, *, timeout: float = 60.0) -> None:
        """Gracefully end the active user_input loop step (runs end-of-loop verifiers)."""
        url = self._require_runtime("stop_conversation")
        resp = self._http.post(f"{url}/terminate_step", timeout=timeout)
        if resp.status_code == 409:
            return  # already ended — no-op
        resp.raise_for_status()

    # -- Session methods that don't apply ------------------------------

    def reset(self, *a, **kw):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.reset() — would tear down the runtime VM the agent loop "
            "is attached to. Open a new DatagenSession instead."
        )

    def add_env(self, *a, **kw):  # type: ignore[override]
        raise NotImplementedError("DatagenSession.add_env() — envs are fixed at launch.")

    def remove_env(self, *a, **kw):
        raise NotImplementedError("DatagenSession.remove_env() — envs are fixed at launch.")

    def evaluate(self, *a, **kw):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.evaluate() — evaluation is tied to testcase scoring; "
            "DatagenSession isn't created from a testcase."
        )

    def link_testcase(self, *a, **kw):  # type: ignore[override]
        raise NotImplementedError("DatagenSession.link_testcase() — DatagenSession isn't created from a testcase.")

    def setup_sandbox(self, *a, **kw):  # type: ignore[override]
        raise NotImplementedError("DatagenSession.setup_sandbox() — sandbox setup runs at world-launch time.")

    @classmethod
    def from_testcase(cls, *a, **kw):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.from_testcase() — use plato.datagen_sessions.create(envs=..., experiment=...)."
        )

    @classmethod
    def from_artifacts(cls, *a, **kw):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.from_artifacts() — use "
            "plato.datagen_sessions.create(envs=[Env.artifact(...)], experiment=...)."
        )

    def login(self, *args, **kwargs):  # type: ignore[override]
        # The runtime env hosts world/REST servers and has no artifact login;
        # Session.login would 400 with "Job has no artifact_id". Hide it for
        # the duration of the call.
        original = self._envs
        sim_envs = [e for e in (original if original is not None else self.envs) if e.alias != RUNTIME_ENV_ALIAS]
        self._envs = sim_envs
        try:
            return super().login(*args, **kwargs)
        finally:
            self._envs = original

    def __repr__(self) -> str:
        env_count = len(self._context.envs) if self._context.envs else 0
        return f"DatagenSession(session_id={self.session_id!r}, envs={env_count})"
