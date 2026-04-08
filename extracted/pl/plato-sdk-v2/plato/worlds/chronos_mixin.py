"""Chronos session reporting and state persistence mixin for Plato worlds.

Handles OTel tracing setup, Chronos session lifecycle (completion reporting),
and world state persistence (save/load/resume).
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime

from plato.otel import init_tracing, shutdown_tracing
from plato.vm_metrics import shutdown_metrics
from plato.worlds.config import WorkspaceSourceSpec
from plato.worlds.models import StateHistoryEntry, WorkspaceSnapshot

logger = logging.getLogger(__name__)

_WORLD_DEV_MODE_ENV = "PLATO_WORLD_DEV_MODE"
_WORLD_TEST_MODE_ENV = "PLATO_WORLD_TEST_MODE"


class ChronosSessionMixin:
    """Mixin providing Chronos session reporting and state persistence for BaseWorld.

    All methods assume ``self`` is a :class:`BaseWorld` instance with the
    expected attributes (config, session, _workspaces, etc.).
    """

    # -- Chronos session reporting -----------------------------------------

    async def _complete_chronos_session(
        self,
        status: str,
        exit_code: int = 0,
        error_message: str | None = None,
        result: dict | None = None,
    ) -> None:
        """Report session completion to Chronos."""
        if not self.chronos.otel_url or not self.chronos.session_id:
            return

        try:
            self.logger.info("Completing Chronos session %s as %s", self.chronos.session_id, status)
            async with self._chronos_client() as client:
                await client.complete(
                    self.chronos.session_id,
                    status=status,
                    result=result,
                    error_message=error_message,
                )
            self.logger.info(f"Reported session {status} to Chronos")
        except Exception as e:
            self.logger.warning(f"Failed to report session completion to Chronos: {e}")

    def _get_chronos_base_url(self) -> str:
        """Get the Chronos API base URL from session config."""
        if self.chronos.chronos_url:
            return self.chronos.chronos_url.rstrip("/")
        if self.chronos.otel_url:
            return self.chronos.otel_url.removesuffix("/api/otel")
        return ""

    def _chronos_client(self):
        """Create an AsyncChronos client for the current session."""
        from plato.chronos.sdk import AsyncChronos

        return AsyncChronos(
            base_url=self._get_chronos_base_url(),
            api_key=self.chronos.api_key,
        )

    # -- OTel / session setup ----------------------------------------------

    def _setup_session(self) -> None:
        """Initialize OTel tracing and session info."""
        if not self.chronos.session_id:
            return

        self._session_id = self.chronos.session_id
        os.environ["SESSION_ID"] = self.chronos.session_id

        if self.chronos.otel_url:
            agent_otel_url = self.chronos.otel_url
            if "localhost" in agent_otel_url or "127.0.0.1" in agent_otel_url:
                agent_otel_url = agent_otel_url.replace("localhost", "host.docker.internal")
                agent_otel_url = agent_otel_url.replace("127.0.0.1", "host.docker.internal")
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = agent_otel_url
            os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"

        if self.chronos.otel_url:
            parent_trace_id = (
                getattr(self.chronos, "parent_trace_id", None)
                or (self.config.model_extra or {}).get("parent_trace_id")
                or os.environ.get("OTEL_TRACE_ID")
            )
            parent_span_id = (
                getattr(self.chronos, "parent_span_id", None)
                or (self.config.model_extra or {}).get("parent_span_id")
                or os.environ.get("OTEL_PARENT_SPAN_ID")
            )

            if parent_trace_id and parent_span_id:
                logger.debug(f"Linking to parent trace: trace_id={parent_trace_id}, span_id={parent_span_id}")

            logger.debug(f"Initializing OTel tracing with endpoint: {self.chronos.otel_url}")
            init_tracing(
                service_name=f"world-{self.name}",
                session_id=self.chronos.session_id,
                otlp_endpoint=self.chronos.otel_url,
                parent_trace_id=parent_trace_id,
                parent_span_id=parent_span_id,
            )
        else:
            logger.debug("No otel_url in session - OTel tracing disabled")

    # -- Finalize ----------------------------------------------------------

    async def _finalize(self, run_error: Exception | None) -> None:
        """Report completion/failure to Chronos and shutdown tracing."""
        await shutdown_metrics()

        is_dev = os.environ.get(_WORLD_DEV_MODE_ENV) == "1"
        is_test = os.environ.get(_WORLD_TEST_MODE_ENV) == "1"
        final_result = getattr(self, "_final_result", None)
        if is_dev or is_test:
            mode = "dev" if is_dev else "test"
            self.logger.info(
                "Skipping Chronos completion in %s mode (run_error=%s)",
                mode,
                type(run_error).__name__ if run_error else "None",
            )
        else:
            if run_error:
                error_msg = f"{type(run_error).__name__}: {run_error}"
                await self._complete_chronos_session(
                    "failed",
                    exit_code=1,
                    error_message=error_msg,
                    result=final_result,
                )
            else:
                await self._complete_chronos_session("completed", exit_code=0, result=final_result)

        self._chronos_completed = True

        shutdown_tracing()
        self._session_id = None

        if run_error:
            raise run_error

        self.logger.info(f"World '{self.name}' completed after {self._step_count} steps")

    # -- State persistence -------------------------------------------------

    async def save_state(self) -> None:
        """Persist world state to Chronos DB."""
        if not self.config.state.enabled or self._state is None:
            return

        ws_snapshots: dict[str, WorkspaceSnapshot] = {}
        if self._workspaces:
            for name, ws in self._workspaces.items():
                ws_dict = await ws.to_state_dict()
                ws_snapshots[name] = WorkspaceSnapshot(**ws_dict)
            self._state.workspaces = ws_snapshots

        self._state.state_history.append(
            StateHistoryEntry(
                step=self._step_count,
                timestamp=datetime.now(UTC).isoformat(),
                workspaces=ws_snapshots,
            )
        )

        await self._upload_state(self._state.model_dump())

    async def load_state(self, session_id: str | None = None) -> bool:
        """Load world state from Chronos DB and restore tracked workspaces."""
        if not self.config.state.enabled:
            return False

        raw_workspace_specs = self.config.state.workspaces
        repo_to_field: dict[str, str] = {}
        for field_name in self._workspaces:
            repo_to_field[self.workspace_repo_name(field_name)] = field_name

        workspace_specs: dict[str, tuple[str | None, str]] = {}
        for key, val in raw_workspace_specs.items():
            if isinstance(val, (dict, WorkspaceSourceSpec)):
                spec = val if isinstance(val, WorkspaceSourceSpec) else WorkspaceSourceSpec(**val)
                if key not in self._workspaces:
                    self.logger.warning(
                        "Unknown workspace field '%s' in state.workspaces",
                        key,
                    )
                    continue
                workspace_specs[key] = (spec.repo, spec.ref)
            elif isinstance(val, str):
                field = repo_to_field.get(key) or (key if key in self._workspaces else None)
                if field is None:
                    self.logger.warning(
                        "Ignoring unknown workspace key '%s' in state.workspaces. Expected one of: %s",
                        key,
                        list(repo_to_field.keys()) + list(self._workspaces.keys()),
                    )
                    continue
                workspace_specs[field] = (None, val)
        use_workspace_specs_mode = bool(workspace_specs)
        sid = session_id or self.chronos.session_id
        if not sid and not use_workspace_specs_mode:
            return False

        state_applied = False
        if sid:
            data = await self._download_state(sid)
            if data is None:
                if not use_workspace_specs_mode:
                    return False
            elif not data:
                self.logger.info("State payload for session %s is empty; starting fresh", sid)
                if not use_workspace_specs_mode:
                    return False
            else:
                if not self._apply_state(data):
                    return False
                state_applied = True

        resume_repos = self.config.state.resume_workspaces
        saved_snapshots = self._state.workspaces if self._state else {}
        restored_any = False
        for name, workspace in self._workspaces.items():
            if workspace.tracked:
                snap = saved_snapshots.get(name)
                if use_workspace_specs_mode:
                    ws_entry = workspace_specs.get(name)
                    if ws_entry is None:
                        self.logger.info(
                            "State workspaces has no entry for tracked workspace '%s'; treating as empty workspace",
                            name,
                        )
                        continue
                    override_repo_from_spec, ref_spec = ws_entry
                    ref_spec = ref_spec.strip()
                    if not ref_spec:
                        self.logger.info(
                            "State workspaces has no entry for tracked workspace '%s'; treating as empty workspace",
                            name,
                        )
                        continue
                    if ":" in ref_spec:
                        source_session_id, exact_step = ref_spec.split(":", 1)
                        source_session_id = source_session_id.strip()
                        exact_step = exact_step.strip()
                    else:
                        source_session_id = (session_id or self.config.state.resume_from or "").strip()
                        exact_step = ref_spec
                    if not source_session_id:
                        raise RuntimeError(
                            f"Workspace resume spec for '{name}' must include session_id:step (got '{ref_spec}')"
                        )
                    if not exact_step:
                        raise RuntimeError(
                            f"Workspace resume spec for '{name}' is missing step name (got '{ref_spec}')"
                        )
                    should_record_resume_input = source_session_id != (self.chronos.session_id or "")
                else:
                    override_repo_from_spec = None
                    if not snap:
                        self.logger.info(
                            "State has no snapshot for tracked workspace '%s'; treating as empty workspace",
                            name,
                        )
                        continue
                    if not snap.steps:
                        self.logger.info(
                            "State snapshot for tracked workspace '%s' has no saved step; treating as empty workspace",
                            name,
                        )
                        continue
                    exact_step = snap.steps[-1]
                    source_session_id = (session_id or "").strip()
                    should_record_resume_input = bool(session_id)

                original = {
                    "session_id": workspace.session_id,
                    "repo_name": workspace.repo_name,
                    "repo_id": workspace.repo_id,
                    "s3_bucket": workspace.s3_bucket,
                    "s3_prefix": workspace.s3_prefix,
                }
                source_session_public_id: str | None = None
                source_repo_name: str | None = None
                source_ref_public_id: str | None = None
                try:
                    if source_session_id:
                        workspace.session_id = source_session_id

                    override_repo = (override_repo_from_spec if use_workspace_specs_mode else None) or resume_repos.get(
                        name
                    )
                    if (
                        not override_repo
                        and not use_workspace_specs_mode
                        and source_session_id
                        and snap
                        and snap.repo_name
                    ):
                        override_repo = snap.repo_name
                    if override_repo and source_session_id:
                        resolved = await self._resolve_workspace_repo_by_name(override_repo)
                        workspace.repo_name = override_repo
                        workspace.repo_id = resolved.repo_id
                        workspace.s3_bucket = resolved.s3_bucket
                        workspace.s3_prefix = resolved.s3_prefix
                        workspace._sts_credentials = {}
                        workspace._sts_expires_at = 0

                    self.logger.info(
                        f"Restoring workspace '{name}' from session '{workspace.session_id}' "
                        f"(repo={workspace.repo_name}, step={exact_step})"
                    )
                    restored = await workspace.restore(exact_step)
                    if not restored:
                        raise RuntimeError(
                            f"Workspace '{name}' step '{exact_step}' has no DVC files "
                            f"(session={workspace.session_id}, repo={workspace.repo_name})"
                        )
                    # For git workspaces, re-checkout repo/ from restored bare repo
                    from plato.transports.git import GitTransport

                    if isinstance(workspace.transport, GitTransport):
                        bare = workspace.transport.bare_repo_path
                        repo = workspace.transport.repo_path
                        from plato.git_ops.repo import checkout_main_from_bare, trust_git_directory

                        trust_git_directory(bare)
                        trust_git_directory(repo)
                        checkout_main_from_bare(bare_repo_path=bare, worktree_path=repo)
                        self.logger.info(f"Re-checked out repo/ from restored bare repo for workspace '{name}'")
                    self.logger.info(f"Restored workspace '{name}' from step '{exact_step}'")
                    restored_any = True
                    if self._state and name in self._state.workspaces:
                        self._state.workspaces[name].steps = [exact_step]
                    source_session_public_id = workspace.session_id
                    source_repo_name = workspace.repo_name
                    source_ref_public_id = getattr(workspace, "_last_restored_source_ref_public_id", "") or None
                except Exception as e:
                    self.logger.exception(
                        "Failed to restore workspace '%s' from session '%s' (repo=%s, step=%s)",
                        name,
                        workspace.session_id,
                        workspace.repo_name,
                        exact_step,
                    )
                    raise RuntimeError(
                        f"Failed to restore workspace '{name}' from session '{workspace.session_id}' "
                        f"(repo={workspace.repo_name}, step={exact_step}): {e}"
                    ) from e
                finally:
                    workspace.session_id = original["session_id"]
                    workspace.repo_name = original["repo_name"]
                    workspace.repo_id = original["repo_id"]
                    workspace.s3_bucket = original["s3_bucket"]
                    workspace.s3_prefix = original["s3_prefix"]
                    workspace._sts_credentials = {}
                    workspace._sts_expires_at = 0

                if should_record_resume_input:
                    restored_dvc_files = getattr(workspace, "_last_restored_dvc_files", None) or {}
                    if source_ref_public_id:
                        await workspace._record_workspace_ref(
                            exact_step,
                            "input",
                            restored_dvc_files,
                            source_ref_public_id=source_ref_public_id,
                        )
                    elif source_session_public_id and source_repo_name:
                        await workspace._record_workspace_ref(
                            exact_step,
                            "input",
                            restored_dvc_files,
                            source_session_public_id=source_session_public_id,
                            source_repo_name=source_repo_name,
                            source_step_name=exact_step,
                        )
                    else:
                        raise RuntimeError(
                            f"Failed to record resume lineage for workspace '{name}' "
                            f"(repo={workspace.repo_name}, step={exact_step}): missing source metadata"
                        )

        return restored_any or state_applied

    def _apply_state(self, data: dict) -> bool:
        """Apply a state dict to the world's in-memory state."""
        if not self._state_class:
            return False
        self._state = self._state_class.model_validate(data)
        return True

    async def _try_resume(self) -> bool:
        """Try to resume from saved state. Returns True if resumed."""
        if not self.config.state.enabled:
            return False

        resume_sid = self.config.state.resume_from or None
        if not resume_sid and not self.config.state.workspaces:
            return False
        restored = await self.load_state(session_id=resume_sid)
        return restored

    async def _upload_state(self, state_data: dict) -> bool:
        """Upload world state dict to Chronos DB."""
        session_id = self.chronos.session_id
        if not session_id:
            self.logger.warning("Cannot upload state: no session_id")
            return False

        if not self._get_chronos_base_url():
            self.logger.warning("Cannot upload state: no chronos_url")
            return False

        try:
            async with self._chronos_client() as client:
                return await client.save_state(session_id, state_data)
        except Exception as e:
            self.logger.warning(f"Failed to upload state: {e}")
            return False

    async def _download_state(self, session_id: str) -> dict | None:
        """Download world state dict from Chronos DB. Returns None if not found."""
        if not self._get_chronos_base_url():
            self.logger.warning("Cannot download state: no chronos_url")
            return None

        try:
            async with self._chronos_client() as client:
                data = await client.get_state(session_id)
            if data is None:
                self.logger.info(f"No state found for session {session_id}")
            else:
                self.logger.info(f"Downloaded state from session {session_id}")
            return data
        except Exception as e:
            self.logger.warning(f"Failed to download state: {e}")
            return None
