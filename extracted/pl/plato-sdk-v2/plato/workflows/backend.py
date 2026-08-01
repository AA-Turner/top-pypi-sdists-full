"""Agent-call backend: bridges workflow ``agent()`` calls to ``world.agent()``.

The runtime hands this module an :class:`AgentCallRequest` (already keyed and
deduplicated against the journal) and gets back an :class:`AgentCallOutcome`.
``run_call`` NEVER raises — every failure mode (agent crash, git push conflict,
timeout, schema-invalid output) is folded into the outcome's ``status`` so the
workflow's ``agent()`` primitive can soft-fail to ``None``.

Sync-mode landmines this module is responsible for (see execution.py/mounts.py):

- ``sync="publish_ref"``: the published ref must survive the run un-merged.
  ``GitSyncPolicy.publish_ref`` defaults ``integrate_to_main=True`` which makes
  the execution manager squash-merge AND delete the ref (execution.py
  ``_integrate_published_ref``), so we pass ``integrate_to_main=False`` and
  never attach a review_fn (the review gate's merge_fn would squash-merge on
  pass instead).
- ``sync="merge_to_main"``: plain default mount policy; the manager converts it
  to a pinned publish ref and squash-merges under its integration lock.
- The review gate only attaches when ``mounts[0]`` is a git mount with sync
  (execution.py ``_prepare_git_mount``), so schema retries for every call that
  is NOT ``merge_to_main``-with-schema ride ``runner.with_continuation`` —
  workspace sync-back precedes the exit-condition check on every attempt.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import posixpath
import re
import shlex
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Literal, Protocol

from opentelemetry import trace
from pydantic import BaseModel, ConfigDict, Field, field_validator

from plato.agents.mounts import AgentWorkspaceMount, GitCheckoutPolicy, GitSyncPolicy
from plato.git_ops.repo import rev_parse
from plato.transports.git import GitPushConflict, GitTransport
from plato.utils.subprocess import run_ssh
from plato.workflows.structured import (
    build_result_protocol_block,
    build_schema_continuation_instruction,
    build_schema_exit_condition,
    build_schema_review_fn,
    read_and_validate_result,
)

if TYPE_CHECKING:
    from plato.runtimes.base import RuntimeInfo
    from plato.worlds.base import BaseWorld
    from plato.worlds.config import AgentConfig
    from plato.worlds.workspace import Workspace

logger = logging.getLogger(__name__)


# Opt fields that participate in the journal/replay cache key. ``label``,
# ``phase``, ``timeout_s`` and ``setup_timeout_s`` are presentation/limit knobs
# and deliberately excluded so renaming a phase never invalidates the replay
# cache. ``setup`` IS keyed: different provisioning means different work.
_KEYED_OPT_FIELDS: Final[set[str]] = {
    "output_schema",
    "agent",
    "model",
    "effort",
    "workspace",
    "data",
    "sync",
    "base",
    "setup",
}

_SETUP_TIMEOUT_DEFAULT_S: Final[float] = 300.0


def canonical_json(value: Any) -> str:
    """Deterministic JSON used for call-key derivation (journal + runtime share it)."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def derive_call_key(prompt: str, opts: AgentCallOpts) -> str:
    """Derive the 16-hex-char replay key for a call: sha256(prompt + NUL + keyed opts)."""
    keyed_opts = opts.model_dump(include=_KEYED_OPT_FIELDS)
    digest = hashlib.sha256((prompt + "\x00" + canonical_json(keyed_opts)).encode("utf-8"))
    return digest.hexdigest()[:16]


class AgentCallOpts(BaseModel):
    """Options for one workflow ``agent()`` call."""

    label: str | None = None
    phase: str | None = None
    output_schema: dict[str, Any] | None = Field(default=None, alias="schema")
    agent: str = "default"
    model: str | None = None
    effort: str | None = None
    workspace: str | None = None  # None = no code workspace; "code" = the git workspace
    # Read-only dataset selection: False = none; True = the default `data`
    # workspace (/workspace/data); a list selects by name — "data" for the
    # default, any other entry a config-declared dataset (/workspace/datasets/<name>,
    # mounted per the dataset's configured transport: direct per-VM fuse or NFS).
    data: bool | list[str] = False

    @field_validator("data")
    @classmethod
    def _normalize_data(cls, value: bool | list[str]) -> bool | list[str]:
        # Deterministic replay key: the selection is a set, not a sequence, and
        # True is canonicalized to ["data"] so equivalent selections share a key.
        if value is True:
            return ["data"]
        if isinstance(value, list):
            return sorted(set(value))
        return value

    sync: Literal["publish_ref", "merge_to_main"] = "publish_ref"
    base: str | None = None  # base ref/SHA for checkout; None = current main
    # Wall budget for the WHOLE call: VM acquire, mounts, setup, agent turns.
    # A timed-out call's error reports how much of it setup consumed.
    timeout_s: float | None = None
    # Deterministic provisioning: a shell command the backend runs on the agent
    # VM (workspaces mounted, agent not yet started). Non-zero exit fails the
    # call. Moves mechanical startup (app boot, seeding, env fixes) out of
    # agent turns — validators wake up to a ready environment.
    setup: str | None = None
    setup_timeout_s: float | None = None
    model_config = ConfigDict(populate_by_name=True)


class AgentCallRequest(BaseModel):
    """A fully-keyed agent call handed to the backend by the runtime."""

    call_id: str  # f"c{seq:04d}-{key}"
    # Namespaces result paths and git refs per submission — without it, serve
    # mode's fresh per-submission runtimes reuse c0001-<key> across workflows,
    # colliding result files and publish refs.
    workflow_id: str = ""

    @property
    def scoped_id(self) -> str:
        """workflow-qualified id for result paths / git refs / display names."""
        return f"{self.workflow_id}/{self.call_id}" if self.workflow_id else self.call_id

    key: str  # sha256(prompt + "\x00" + canonical_json(keyed_opts))[:16]
    occurrence: int
    prompt: str  # user prompt WITHOUT result-protocol footer
    opts: AgentCallOpts


class AgentCallOutcome(BaseModel):
    """Result of one backend execution (or failure) of an agent call."""

    status: Literal["ok", "error", "invalid_output", "timeout"]
    result_text: str | None = None  # contents of result.md when no schema
    result_json: Any | None = None  # validated JSON when schema given
    published_ref: str | None = None
    # Hidden ref where a FAILED agent's git state (committed + dirty + untracked)
    # was best-effort captured before its VM was destroyed. Discoverable and
    # un-merged; None when there was nothing to salvage or the call had no git
    # workspace. Only set on non-ok outcomes.
    salvage_ref: str | None = None
    merged: bool = False
    # SHA of the resulting commit on shared main for merge_to_main calls.
    # Squash-merging rewrites history, so any hash the agent reported from
    # inside its VM does not exist on main — this is the authoritative one.
    merged_sha: str | None = None
    attempts: int = 1
    agent_task_span_id: str | None = None
    error: str | None = None
    cost_usd: float | None = None


class AgentBackend(Protocol):
    """Anything the workflow runtime can dispatch agent calls to."""

    async def run_call(self, request: AgentCallRequest) -> AgentCallOutcome: ...

    def take_cancelled_salvage_ref(self, call_id: str) -> str | None:
        """Salvage ref captured while ``run_call`` unwound under cancellation.

        Cancellation gives ``run_call`` no way to return an outcome, so the
        backend stashes the ref and the runtime collects it here (once) when
        writing the cancelled call's journal record.
        """
        ...


def _publish_ref_name(call_id: str) -> str:
    return f"refs/plato/wf/{call_id}"


def setup_cgroup_name(scoped_id: str) -> str:
    """Cgroup dir name for a call's setup processes (matched by the pool reset)."""
    return "plato-wf-setup-" + re.sub(r"[^A-Za-z0-9_.-]", "-", scoped_id)


# Wrapper exit code when the cgroup-v2 join fails. The setup command is NOT
# run in that case: every agent image derives from agent-base on Plato's
# kernel+init, where the v2 unified mount and cgroup.kill are platform
# invariants — a failed join means infra breakage to surface loudly, never a
# condition to accommodate by running provisioning untracked.
SETUP_NO_CGROUP_EXIT: Final[int] = 97


def build_setup_command(
    setup: str,
    workdir: str,
    log_path: str,
    cgroup_name: str,
    cgroup_root: str = "/sys/fs/cgroup",
) -> str:
    """Wrap a call's ``setup`` command for SSH execution on the agent VM.

    Runs in ``workdir`` with combined output captured to ``log_path`` (on the
    results mount, so it syncs back with the call's artifacts and the agent can
    read it). ``setup`` itself is intentionally NOT quoted — it is a shell
    command line, pipelines and `&&` included.

    Before exec, the wrapper shell joins a fresh cgroup v2 under
    ``<cgroup_root>/<cgroup_name>`` so every process the setup spawns —
    daemonized servers included — stays kernel-tracked for the warm-pool
    reset's ``cgroup.kill`` (see warmpool._runtime_reset_commands). If the
    join fails, the wrapper exits :data:`SETUP_NO_CGROUP_EXIT` WITHOUT running
    the command — there is never an untracked-process window.

    ``cgroup_root`` exists for tests (a fake root makes the join exercisable
    without privileges); production always uses the default.
    """
    cg_path = f"{cgroup_root.rstrip('/')}/{cgroup_name}"
    inner = (
        f"cg={shlex.quote(cg_path)}; "
        # cgroup.controllers at the ROOT = v2 unified mount (absent on v1-only
        # and hybrid layouts); cgroup.kill inside the created dir = kernel
        # >=5.14 — the reset's cleanup write. Both are required before any
        # setup process may exist.
        f"if [ -f {shlex.quote(cgroup_root.rstrip('/'))}/cgroup.controllers ] "
        '&& { mkdir "$cg" 2>/dev/null || [ -d "$cg" ]; } '
        '&& [ -f "$cg/cgroup.kill" ] '
        '&& echo $$ > "$cg/cgroup.procs" 2>/dev/null; then '
        'echo "PLATO_SETUP_CGROUP=$cg"; '
        f'else echo "PLATO_SETUP_CGROUP=none" >&2; exit {SETUP_NO_CGROUP_EXIT}; fi; '
        f"mkdir -p {shlex.quote(posixpath.dirname(log_path))} && "
        f"cd {shlex.quote(workdir)} && {{ {setup}\n}} >{shlex.quote(log_path)} 2>&1"
    )
    return f"bash -lc {shlex.quote(inner)}"


def build_setup_note(setup: str, log_path: str) -> str:
    """Instruction addendum telling the agent its setup already ran."""
    return (
        "\n\n---\n"
        "## SETUP (already done for you)\n"
        "Before your session started, this command was run in your workspace and exited 0:\n"
        "```\n"
        f"{setup}\n"
        "```\n"
        f"Its full output is at {log_path}."
    )


def _ref_exists(bare_repo_path: str, ref: str) -> bool:
    """True when ``ref`` resolves in the local bare repo (sync — run in a thread)."""
    try:
        rev_parse(bare_repo_path, ref)
    except Exception:
        return False
    return True


class WorldAgentBackend:
    """Bridges workflow agent calls to ``BaseWorld.agent()`` fan-out.

    One instance per workflow world session. Holds no per-call state; the
    runtime owns journaling, budget checks, and the concurrency semaphore —
    this class owns mount construction, retry wiring, and result collection.
    """

    def __init__(
        self,
        world: BaseWorld,
        *,
        agent_profiles: dict[str, AgentConfig],
        code_workspace: Workspace | None,
        results_workspace: Workspace,
        data_workspace: Workspace | None = None,
        dataset_workspaces: dict[str, Workspace] | None = None,
        results_dir: Path,
        max_concurrent_envs: int,
        schema_retries: int,
    ) -> None:
        self._world = world
        self._agent_profiles = agent_profiles
        self._code_workspace = code_workspace
        self._results_workspace = results_workspace
        self._data_workspace = data_workspace
        self._dataset_workspaces = dataset_workspaces or {}
        self._results_dir = results_dir
        self._max_parallel = max_concurrent_envs
        self._schema_retries = schema_retries
        self._tracer = trace.get_tracer("plato.workflows.backend")
        # call_id -> salvage ref captured while that call unwound under
        # cancellation (cancellation returns no outcome to carry it).
        self._cancelled_salvage_refs: dict[str, str] = {}

    def take_cancelled_salvage_ref(self, call_id: str) -> str | None:
        """Pop the salvage ref stashed when ``call_id`` was cancelled in flight."""
        return self._cancelled_salvage_refs.pop(call_id, None)

    async def run_call(self, request: AgentCallRequest) -> AgentCallOutcome:
        """Execute one agent call end-to-end. Never raises (CancelledError excepted)."""
        opts = request.opts
        span_attrs: dict[str, Any] = {
            "plato.workflow.call_id": request.call_id,
            "plato.workflow.call_key": request.key,
            "plato.workflow.occurrence": request.occurrence,
            "plato.workflow.agent": opts.agent,
            "plato.workflow.sync": opts.sync,
        }
        if opts.label:
            span_attrs["plato.workflow.label"] = opts.label
        if opts.phase:
            span_attrs["plato.workflow.phase"] = opts.phase

        with self._tracer.start_as_current_span("workflow.call", attributes=span_attrs) as span:
            try:
                outcome = await self._run_call_inner(request)
            except asyncio.CancelledError:
                # Cancellation returns no outcome; mirror its salvage ref onto
                # the span so cancelled calls trace like other failures.
                span.set_attribute("plato.workflow.call_status", "cancelled")
                cancelled_ref = self._cancelled_salvage_refs.get(request.call_id)
                if cancelled_ref:
                    span.set_attribute("plato.workflow.salvage_ref", cancelled_ref)
                raise
            span.set_attribute("plato.workflow.call_status", outcome.status)
            span.set_attribute("plato.workflow.attempts", outcome.attempts)
            if outcome.published_ref:
                span.set_attribute("plato.workflow.published_ref", outcome.published_ref)
            if outcome.salvage_ref:
                span.set_attribute("plato.workflow.salvage_ref", outcome.salvage_ref)
            if outcome.merged:
                span.set_attribute("plato.workflow.merged", True)
            if outcome.merged_sha:
                span.set_attribute("plato.workflow.merged_sha", outcome.merged_sha)
            if outcome.error:
                span.set_attribute("plato.workflow.error", outcome.error[:2000])
            return outcome

    async def _run_call_inner(self, request: AgentCallRequest) -> AgentCallOutcome:
        opts = request.opts
        schema = opts.output_schema

        config = self._resolve_agent_config(opts)
        if config is None:
            known = ", ".join(sorted(self._agent_profiles)) or "<none>"
            return AgentCallOutcome(
                status="error",
                error=f"unknown agent profile {opts.agent!r} (known: {known})",
            )

        try:
            mounts = self._build_mounts(request)
        except ValueError as exc:
            return AgentCallOutcome(status="error", error=str(exc))

        code_mount = mounts[0] if opts.workspace == "code" else None
        use_review_gate = opts.workspace == "code" and opts.sync == "merge_to_main" and schema is not None

        # Attempt counter shared by both retry paths: the review_fn / exit
        # condition runs exactly once per agent execution (after sync-back),
        # so counting invocations counts executions.
        attempt_counter = {"count": 0}

        display_name = f"wf-{opts.label or request.scoped_id}"
        review_fn = None
        if use_review_gate:
            inner_review_fn = build_schema_review_fn(self._results_dir, request.scoped_id, schema)

            async def counting_review_fn(*args: Any, **kwargs: Any) -> Any:
                attempt_counter["count"] += 1
                return await inner_review_fn(*args, **kwargs)

            review_fn = counting_review_fn

        runner = self._world.agent(
            config,
            display_name=display_name,
            mounts=mounts,
            review_fn=review_fn,
            max_review_continuations=self._schema_retries,
            review_exhaustion_policy="fail",
        )

        if not use_review_gate:
            # Structured-output (and missing-result nudge) retries for every
            # other call shape. The review gate would be silently dropped for
            # non-git-primary mounts, and MUST NOT attach to publish_ref calls
            # (its merge_fn squash-merges the ref on pass) — with_continuation
            # works for all of them: sync-back runs before each exit check.
            inner_exit = build_schema_exit_condition(self._results_dir, request.scoped_id, schema)

            async def counting_exit_condition() -> bool:
                attempt_counter["count"] += 1
                return await inner_exit()

            runner.with_continuation(
                exit_condition=counting_exit_condition,
                max_continuations=self._schema_retries if schema is not None else 1,
                continuation_instruction=build_schema_continuation_instruction(
                    self._results_dir, request.scoped_id, schema
                ),
            )

        # Pre-create the call's result directory on the shared results mount.
        # The agent must never construct this path itself: a mistyped call id
        # (observed in the wild: one dropped hex char) writes to a sibling dir
        # the exit condition can never see, and the agent then trusts that
        # stray file through every retry.
        await asyncio.to_thread((self._results_dir / request.scoped_id).mkdir, parents=True, exist_ok=True)

        setup_log: str | None = None
        # Setup wall-clock, read by the timeout handler: timeout_s spans the
        # WHOLE call (VM acquire, mounts, setup, agent turns), so a timeout
        # error must say how much of the budget provisioning consumed instead
        # of silently masking it as agent slowness.
        setup_state: dict[str, float] = {}
        if opts.setup:
            # Deterministic provisioning runs on the VM after workspaces are
            # mounted but before the agent's first turn (AgentTask.on_prepare
            # ordering in task._run_on_runtime). Failure raises out of
            # runner.run() into the generic error path below — the agent never
            # starts against a half-provisioned VM.
            workdir = code_mount.agent_path if code_mount is not None else self._results_workspace.mount_path
            results_base = self._results_workspace.mount_path.rstrip("/")
            setup_log = f"{results_base}/{request.scoped_id}/setup.log"
            setup_cmd = build_setup_command(opts.setup, workdir, setup_log, setup_cgroup_name(request.scoped_id))
            setup_timeout = int(opts.setup_timeout_s or _SETUP_TIMEOUT_DEFAULT_S)

            async def _setup_hook(info: RuntimeInfo) -> None:
                if info.ssh_key_path is None:
                    raise RuntimeError("setup= requires an SSH-capable agent runtime")
                started = time.monotonic()
                try:
                    exit_code, _stdout, stderr = await run_ssh(
                        info.ssh_key_path, info.hostname, setup_cmd, timeout=setup_timeout
                    )
                finally:
                    setup_state["elapsed_s"] = time.monotonic() - started
                if exit_code == SETUP_NO_CGROUP_EXIT:
                    # The wrapper refused to run the command: cgroup v2 with
                    # cgroup.kill is a platform invariant on the agent-base
                    # image, so this is infra breakage to surface, not a
                    # condition to degrade around. Nothing was spawned.
                    raise RuntimeError(
                        "setup= aborted before running: cgroup v2 with cgroup.kill is "
                        "unavailable on this agent runtime — platform invariant violated "
                        "(all agent images derive from agent-base on Plato's kernel/init); "
                        "the setup command was NOT executed"
                    )
                if exit_code != 0:
                    _, tail, _ = await run_ssh(
                        info.ssh_key_path,
                        info.hostname,
                        f"tail -c 2000 {shlex.quote(setup_log)} 2>/dev/null",
                        timeout=30,
                    )
                    raise RuntimeError(f"setup command failed (exit {exit_code}): {tail.strip() or stderr.strip()}")
                logger.info("Workflow call %s: setup command completed", request.call_id)

            runner.on_prepare(_setup_hook)

        full_instruction = (
            request.prompt
            + "\n\n"
            + build_result_protocol_block(
                request.scoped_id,
                schema,
                results_mount_path=self._results_workspace.mount_path,
            )
        )
        if opts.setup and setup_log is not None:
            full_instruction += build_setup_note(opts.setup, setup_log)

        try:
            if opts.timeout_s is not None:
                await asyncio.wait_for(runner.run(full_instruction), timeout=opts.timeout_s)
            else:
                await runner.run(full_instruction)
        except asyncio.CancelledError:
            # Workflow cancel / external teardown. The execution manager's
            # cancellation unwind has already salvaged (shielded, bounded)
            # by the time CancelledError exits runner.run(), so the ref is
            # on the runner — stash it for the runtime's cancelled-call
            # journal record; cancellation itself carries no outcome.
            if runner.salvage_ref:
                self._cancelled_salvage_refs[request.call_id] = runner.salvage_ref
            raise
        except TimeoutError:
            # wait_for cancelled runner.run(); the execution manager's
            # cancellation handler destroys the checked-out pooled VM (it is
            # not returned for reuse), so a timed-out call never leaks a
            # warm-pool slot.
            timeout_detail = f"agent call timed out after {opts.timeout_s}s"
            if setup_state.get("elapsed_s"):
                # timeout_s budgets the WHOLE call — say how much provisioning
                # ate so a slow setup is never misread as a slow agent.
                timeout_detail += f" (setup consumed {setup_state['elapsed_s']:.0f}s of the budget)"
            logger.warning("Workflow call %s: %s", request.call_id, timeout_detail)
            return AgentCallOutcome(
                status="timeout",
                attempts=max(1, attempt_counter["count"]),
                agent_task_span_id=runner.last_execution_span_id or None,
                salvage_ref=runner.salvage_ref,
                error=timeout_detail,
            )
        except GitPushConflict as exc:
            logger.warning("Workflow call %s lost a git push race: %s", request.call_id, exc)
            return AgentCallOutcome(
                status="error",
                attempts=max(1, attempt_counter["count"]),
                agent_task_span_id=runner.last_execution_span_id or None,
                salvage_ref=runner.salvage_ref,
                error=f"GitPushConflict: {exc} (conflict_ref={exc.conflict_ref})",
            )
        except Exception as exc:
            logger.exception("Workflow call %s failed", request.call_id)
            return AgentCallOutcome(
                status="error",
                attempts=max(1, attempt_counter["count"]),
                agent_task_span_id=runner.last_execution_span_id or None,
                salvage_ref=runner.salvage_ref,
                error=f"{type(exc).__name__}: {exc}",
            )

        attempts = max(1, attempt_counter["count"])
        agent_task_span_id = runner.last_execution_span_id or None

        published_ref: str | None = None
        if code_mount is not None and opts.sync == "publish_ref":
            published_ref = await self._verify_published_ref(code_mount, request.scoped_id)
        merged = runner.merged
        merged_sha = runner.merged_commit

        # The result is ALWAYS read from the results workspace after the run —
        # runner.run() only returns the runtime id.
        ok, value, validation_error = read_and_validate_result(self._results_dir, request.scoped_id, schema)
        if ok:
            return AgentCallOutcome(
                status="ok",
                result_text=value if schema is None else None,
                result_json=value if schema is not None else None,
                published_ref=published_ref,
                merged=merged,
                merged_sha=merged_sha,
                attempts=attempts,
                agent_task_span_id=agent_task_span_id,
            )

        status: Literal["error", "invalid_output"] = "invalid_output" if schema is not None else "error"
        if runner.continuation_exhausted:
            validation_error = f"{validation_error} (retries exhausted after {attempts} execution(s))"
        return AgentCallOutcome(
            status=status,
            published_ref=published_ref,
            merged=merged,
            merged_sha=merged_sha,
            attempts=attempts,
            agent_task_span_id=agent_task_span_id,
            error=validation_error,
        )

    def _resolve_agent_config(self, opts: AgentCallOpts) -> AgentConfig | None:
        """Resolve the profile + per-call overrides into a concrete AgentConfig.

        The resolved config is deterministic for a given (agent, model, effort)
        combo so ``BaseWorld.agent()`` reuses one execution manager / warm pool
        per combo (the manager key hashes the full config dump).
        """
        base = self._agent_profiles.get(opts.agent)
        if base is None:
            return None
        config_dict = dict(base.config)
        if opts.model is not None:
            config_dict["model_name"] = opts.model
        if opts.effort is not None:
            config_dict["effort"] = opts.effort
        return base.model_copy(
            update={"config": config_dict, "max_parallel": self._max_parallel},
            deep=True,
        )

    def _resolve_data_selection(self, selection: bool | list[str]) -> list[Workspace]:
        """Map a call's ``data`` opt to read-only dataset workspaces.

        ``True`` -> the default ``data`` workspace; a list selects by name,
        where ``"data"`` is the default and anything else must be a
        config-declared dataset. Unknown names fail the call (soft-fail to
        None via the run_call exception handler), listing what exists.
        """
        if selection is False:
            return []
        names = ["data"] if selection is True else list(selection)
        resolved: list[Workspace] = []
        for name in names:
            if name == "data":
                if self._data_workspace is None:
                    raise ValueError("data workspace requested but the world has none")
                resolved.append(self._data_workspace)
            elif name in self._dataset_workspaces:
                resolved.append(self._dataset_workspaces[name])
            else:
                known = sorted(self._dataset_workspaces)
                raise ValueError(f"unknown dataset {name!r} (known: {['data', *known]})")
        return resolved

    def _build_mounts(self, request: AgentCallRequest) -> list[AgentWorkspaceMount]:
        """Build the mount list, primary first (mounts[0] drives workdir + git gate)."""
        opts = request.opts
        results_mount = self._results_workspace.mount()
        # Appended last on purpose: mounts[0] drives the workdir and the git
        # review gate; dataset mounts are passive read-only views (per-VM
        # fuse or NFS, per dataset config).
        extra = [ws.mount() for ws in self._resolve_data_selection(opts.data)]
        if opts.workspace is None:
            return [results_mount, *extra]
        if opts.workspace != "code":
            raise ValueError(f"unknown workspace {opts.workspace!r} (expected None or 'code')")
        if self._code_workspace is None:
            raise ValueError("workspace='code' requested but the world has no code workspace")

        if opts.sync == "publish_ref":
            # integrate_to_main=False is mandatory: the default (True) makes the
            # execution manager squash-merge the published ref into main and
            # delete it, destroying the unique-ref-per-call contract.
            code_mount = self._code_workspace.mount().with_git_options(
                checkout=GitCheckoutPolicy(
                    ref=opts.base,  # None = clone default main at run start
                    branch_name=f"plato-task/wf-{request.scoped_id}",
                ),
                sync=GitSyncPolicy.publish_ref(
                    _publish_ref_name(request.scoped_id),
                    exact=True,
                    integrate_to_main=False,
                ),
            )
        else:
            # merge_to_main: keep the workspace default policy — the execution
            # manager pins main's SHA after warm-pool acquire, rewrites the
            # checkout, and squash-merges under its integration lock.
            if opts.base is not None:
                logger.warning(
                    "Workflow call %s: base=%r is ignored for sync='merge_to_main' "
                    "(the execution manager pins main's current SHA at run start)",
                    request.call_id,
                    opts.base,
                )
            code_mount = self._code_workspace.mount()
        return [code_mount, results_mount, *extra]

    async def _verify_published_ref(self, code_mount: AgentWorkspaceMount, call_id: str) -> str | None:
        """Return the call's publish ref iff it actually exists in the local bare.

        The per-run cloned transport (where sync-back records ``published_ref``)
        is internal to the execution manager, so we check the shared bare repo
        directly. Missing ref = the agent made no commits (or sync-back skipped).
        """
        transport = code_mount.transport
        if not isinstance(transport, GitTransport):
            return None
        ref = _publish_ref_name(call_id)
        exists = await asyncio.to_thread(_ref_exists, transport.bare_repo_path, ref)
        if not exists:
            logger.warning("Workflow call %s: publish ref %s not found in bare repo", call_id, ref)
            return None
        return ref
