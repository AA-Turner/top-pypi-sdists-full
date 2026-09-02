"""LangGraph workflow runner for the work-on-issue workflow.

This module provides the entry point for running the LangGraph-based
work-on-issue workflow when ``--engine langchain`` is selected.
It supports both Jira issue keys (e.g., PROJECT-1234) and GitHub issue
numbers (e.g., #42).
"""

import sys
import uuid
from pathlib import Path
from typing import Any


def run_langchain_workflow(
    issue_key: str,
    *,
    interactive: bool = False,
    model: str | None = None,
    resume: bool = False,
    resume_data: dict | None = None,
    worktree_key: str | None = None,
) -> None:
    """Run the LangGraph-based work-on-issue workflow.

    This is invoked when ``--engine langchain`` (or ``--use-langchain``) is
    provided on the CLI.  It builds and invokes the compiled StateGraph with
    real tool integrations.  Supports both Jira issue keys (e.g., PROJECT-1234)
    and GitHub issue numbers (e.g., #42).

    Args:
        issue_key: Jira issue key (e.g., PROJECT-1234) or GitHub issue number.
        interactive: Whether to start the Copilot session interactively.
        model: Copilot model to use.
        resume: Whether to resume from an existing checkpoint.
        resume_data: Structured resume payload passed as ``Command(resume=...)``
            when resuming an interrupted or incomplete execution checkpoint.
        worktree_key: The active worktree key for scoping the thread identity.
            Only ``None`` is treated as "not provided"; any other value is
            normalized (stripped), validated, and used directly without
            consulting bootstrap state.  An explicit non-``None`` value that
            fails validation exits with an error rather than falling back.
            When ``None``, the key is resolved from bootstrap state.  This
            allows callers that already hold the normalized invocation worktree
            key (e.g. when ``AGENTIC_DEVTOOLS_STATE_DIR`` is set and bootstrap
            state is empty) to propagate it explicitly into the runner.
    """
    # FR-009: Dependency guard — surface actionable install message.
    try:
        from langgraph.graph.state import CompiledStateGraph  # noqa: F401
    except ImportError:  # pragma: no cover
        print(
            "ERROR: LangGraph dependencies are not available.\n\nInstall them with:\n  pip install agentic-devtools\n",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        from langgraph.checkpoint.sqlite import SqliteSaver  # noqa: F401
    except ImportError:  # pragma: no cover
        print(
            "ERROR: LangGraph checkpoint dependencies are not available.\n"
            "\n"
            "Install them with:\n"
            "  pip install agentic-devtools\n",
            file=sys.stderr,
        )
        sys.exit(1)

    from agentic_devtools.state import get_bootstrap_state, get_state_dir, is_safe_dir_segment

    from .checkpointing import get_checkpointer, resolve_effective_workflow_state_dir, validate_checkpoint_state_dir
    from .execution_lock import ExecutionLock
    from .graph_builder import build_work_on_issue_graph
    from .safety.mode import ExecutionMode, resolve_execution_mode_from_state

    # Resolve and validate execution mode before initialising any stateful
    # infrastructure (lock file, checkpointer database, policy state).
    # Restricted mode is read-only and must be rejected before creating any
    # local artifacts.
    execution_mode = resolve_execution_mode_from_state()
    if execution_mode is ExecutionMode.restricted:
        print(
            "ERROR: execution_mode=restricted is read-only and cannot run "
            "the work-on-issue workflow because it performs local mutations.\n"
            "Use execution_mode=dry_run for simulation or execution_mode=live to apply changes.",
            file=sys.stderr,
        )
        sys.exit(1)
    dry_run_enabled = execution_mode is not ExecutionMode.live

    # Resolve the state directory first so that environment overrides and
    # pinned paths take precedence, establishing the database scope.  The
    # thread ID uses the validated invocation worktree key, with bootstrap state as fallback (FR-004):
    # get_state_dir() permits arbitrary AGENTIC_DEVTOOLS_STATE_DIR paths and
    # validated pins, so state_dir.name is only a directory basename and MUST
    # NOT be used as the authoritative worktree key.
    state_dir = get_state_dir()

    # Resolve the active worktree key.  The caller may pass the normalized
    # invocation key directly (e.g. when AGENTIC_DEVTOOLS_STATE_DIR is set and
    # _ensure_bootstrap_identity_and_scope skips set_bootstrap_state(), leaving
    # bootstrap state empty).  Treat only None as "not provided" — an explicit
    # non-None value that fails validation is an error, not a fallback signal.
    # Normalize (strip) before validation so the stored value matches the
    # validated segment (is_safe_dir_segment strips internally but the runner
    # would otherwise retain the raw padded string in the thread ID).
    if worktree_key is not None:
        normalized_explicit = worktree_key.strip()
        if not is_safe_dir_segment(normalized_explicit):
            print(
                f"ERROR: The provided worktree_key {worktree_key!r} is not a valid scope identifier. "
                "Run the workflow initializer to establish a valid worktree scope.",
                file=sys.stderr,
            )
            sys.exit(1)
        resolved_worktree_key = normalized_explicit
    else:
        bootstrap = get_bootstrap_state()
        resolved_worktree_key = bootstrap.get("worktree_key", "")
        if not is_safe_dir_segment(resolved_worktree_key):
            print(
                "ERROR: No valid worktree key found in bootstrap state. "
                "Run the workflow initializer first to establish a worktree scope.",
                file=sys.stderr,
            )
            sys.exit(1)

    try:
        validate_checkpoint_state_dir(state_dir, worktree_key=resolved_worktree_key)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    # Resolve the effective state directory after any legacy-root checkpoint
    # redirect so that ExecutionLock and get_checkpointer() use the same
    # directory.  Without this, a state_dir that aliases the legacy repo-root
    # path causes get_checkpointer() to redirect the database to the canonical
    # worktree directory while the lock remains in the non-canonical directory,
    # allowing two concurrent invocations to hold different locks while writing
    # to the same database/thread.
    try:
        effective_state_dir = resolve_effective_workflow_state_dir(
            state_dir=state_dir,
            worktree_key=resolved_worktree_key,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    # Normalize issue_key once so both thread identity and graph state use the
    # same canonical string representation.
    if isinstance(issue_key, str):
        issue_key_str = issue_key
    elif type(issue_key) is int:
        issue_key_str = str(issue_key)
    else:
        print(
            f"ERROR: issue_key must be a string or integer, got {type(issue_key).__name__}.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build a worktree-scoped thread ID using the length-prefixed injective
    # encoding required by FR-004.  Length prefixes ensure unambiguous parsing
    # even when issue_key or worktree_key contains the literal "--worktree-"
    # or ":" substrings.  Convert issue_key to str defensively: state-backed
    # callers may pass an integer (agdt-set JSON-parses numeric IDs).
    issue_key_bytes = len(issue_key_str.encode("utf-8"))
    worktree_key_bytes = len(resolved_worktree_key.encode("utf-8"))
    thread_id = (
        f"work-on-issue-{issue_key_bytes}:{issue_key_str}--worktree-{worktree_key_bytes}:{resolved_worktree_key}"
    )
    lock = ExecutionLock(state_dir=effective_state_dir, thread_id=thread_id)

    try:
        lock.acquire()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    # Initialize checkpointer to None so the finally block can safely reference
    # it even when get_checkpointer() raises before assignment.
    checkpointer = None
    try:
        # Initialize infrastructure components for autonomous execution.
        policy_state = _initialize_infrastructure(effective_state_dir)

        # Initialize checkpointer after lock acquisition so the entire execution
        # (including checkpoint storage) is single-writer per thread scope.
        # Pass effective_state_dir (after any legacy-root redirect) so both the
        # lock and checkpointer use the same directory and the TOCTOU gap of a
        # second get_state_dir() call is also closed.
        checkpointer = get_checkpointer(state_dir=effective_state_dir, worktree_key=resolved_worktree_key)

        compiled = build_work_on_issue_graph(checkpointer=checkpointer)

        # FR-009: Generate or restore run_id from checkpoint.
        run_id: str | None = None
        if resume:
            # Restore run_id from graph state via compiled.get_state() —
            # SqliteSaver.get() returns a CheckpointTuple whose graph channel
            # values live under checkpoint["channel_values"], not at the top
            # level of the return value.  compiled.get_state() wraps this and
            # exposes channel values via the .values attribute.
            temp_config: dict[str, Any] = {"configurable": {"thread_id": thread_id}}
            state_snapshot: Any = compiled.get_state(temp_config)  # type: ignore[arg-type]
            if state_snapshot is not None:
                candidate = state_snapshot.values.get("run_id")
                if isinstance(candidate, str) and candidate:
                    run_id = candidate
                # Preserve the persisted restriction: if the checkpoint was created
                # with dry_run=True, never promote it to live on resume without an
                # explicit mode change.  Use most-restrictive-wins semantics so
                # an operator can add restrictions but cannot accidentally relax them.
                persisted_dry_run = state_snapshot.values.get("dry_run")
                if persisted_dry_run is True and not dry_run_enabled:
                    print(
                        "INFO: Resuming with dry_run=True preserved from checkpoint. "
                        "The session was originally started in dry-run mode. "
                        "Start a new session with execution_mode=live to run without simulation.",
                        file=sys.stderr,
                    )
                    dry_run_enabled = True
        if not run_id:
            run_id = str(uuid.uuid4())

        config: dict[str, Any] = {
            "configurable": {
                "thread_id": thread_id,
                "run_id": run_id,
            }
        }

        if resume:
            # Resume from existing checkpoint.
            from langgraph.types import Command

            # Check if there is an existing checkpoint to resume from.
            checkpoint = checkpointer.get(config)  # type: ignore[arg-type]
            if checkpoint is None:
                print(
                    f"ERROR: No existing checkpoint found for issue {issue_key}.\n"
                    "Cannot resume without a prior interrupted workflow run.\n"
                    "\n"
                    "Start a fresh run without --resume.",
                    file=sys.stderr,
                )
                sys.exit(1)

            # Enforce the currently resolved safety mode into the checkpoint
            # before resuming.  LangGraph restores the checkpoint's persisted
            # state verbatim, so a session that was interrupted while live could
            # resume with dry_run=False even if the operator has since switched
            # to dry_run or restricted mode.  Patching the channel value here
            # guarantees that planning/completion nodes see the correct flag on
            # their very first access regardless of what was stored.
            compiled.update_state(config, {"dry_run": dry_run_enabled, "run_id": run_id})  # type: ignore[arg-type]

            # Determine resume payload based on gate type.
            resume_value: Any
            if resume_data is not None:
                resume_value = resume_data
            else:
                resume_value = True

            print(f"[langchain] Resuming workflow for {issue_key_str}...")
            try:
                result = compiled.invoke(Command(resume=resume_value), config=config)  # type: ignore[call-overload]
            except Exception as e:
                if type(e).__name__ == "GraphInterrupt":
                    _print_pause_message(issue_key_str)
                    return
                print(f"ERROR: Workflow resume failed: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Fresh invocation.
            initial_state: dict[str, Any] = {
                "issue_key": issue_key_str,
                "step": "",
                "status": "",
                "plan": "",
                "error": None,
                "retry_count": 0,
                "events": [],
                "agent_context": {
                    "interactive": interactive,
                    "model": model,
                },
                "affected_paths": [],
                "dry_run": dry_run_enabled,
                "token_usage_prompt": 0,  # nosec B105 - billing telemetry schema, not a secret
                "token_usage_completion": 0,  # nosec B105 - billing telemetry schema, not a secret
                # Persist run_id in graph state so SqliteSaver checkpoints it
                # and --resume can restore it without relying on configurable.
                "run_id": run_id,
            }
            initial_state.update(policy_state)

            print(f"[langchain] Starting workflow for {issue_key_str}...")
            try:
                result = compiled.invoke(initial_state, config=config)  # type: ignore[call-overload]
            except Exception as e:
                if type(e).__name__ == "GraphInterrupt":
                    _print_pause_message(issue_key_str)
                    return
                print(f"ERROR: Workflow execution failed: {e}", file=sys.stderr)
                sys.exit(1)

        # Determine outcome: pause or completion.
        if _is_workflow_paused(result):
            _print_pause_message(issue_key_str)
            return

        # True completion.
        final_step = result.get("step", "unknown")
        final_status = result.get("status", "unknown")
        if final_status in {"failed", "blocked"}:
            print(
                f"ERROR: Workflow terminated unsuccessfully: step={final_step}, status={final_status}",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"[langchain] Workflow completed: step={final_step}, status={final_status}")
    finally:
        lock.release()
        # Close the checkpointer's underlying SQLite connection to avoid
        # leaking file descriptors / holding the DB file locked.
        if checkpointer is not None and hasattr(checkpointer, "conn"):
            checkpointer.conn.close()


def _initialize_infrastructure(state_dir: Path | str) -> dict[str, int]:
    """Initialize infrastructure components for autonomous workflow execution.

    Loads policy values used by the workflow (token budget and retry budget)
    and logs them for observability. Returns state defaults that should be
    seeded into fresh workflow executions. If policy loading fails, emits a
    warning and continues with runtime defaults.

    Args:
        state_dir: Path to the workflow state directory (str or Path).

    Returns:
        A mapping of policy-backed state defaults for fresh executions.
    """
    import sys

    # Initialize PolicyLoader for budget enforcement
    try:
        from agentic_devtools.orchestration.policies.loader import PolicyLoader

        loader = PolicyLoader()
        policy = loader.load()
        max_tokens = policy.shared.max_tokens
        retry_budget = policy.work_on_issue.retry_budget
        print(
            f"[langchain] Policy loaded: state_dir={state_dir}, max_tokens={max_tokens}, retry_budget={retry_budget}",
            file=sys.stderr,
        )
        return {"retry_budget": retry_budget}
    except Exception as exc:
        print(
            f"[langchain] WARNING: Policy loading failed for state_dir={state_dir}, using defaults: {exc}",
            file=sys.stderr,
        )
        return {}


def _is_workflow_paused(result: object) -> bool:
    """Return True if the workflow is in a non-terminal paused or in-progress state.

    When a LangGraph workflow with a checkpointer pauses (e.g., at an
    interrupt checkpoint), ``invoke()`` returns the current state dict
    instead of raising ``GraphInterrupt``. This helper treats known terminal
    statuses (``completed``, ``failed``, ``blocked``) as non-paused and
    returns ``True`` for ``active`` or a missing status — indicating the
    workflow has not yet reached a terminal outcome.

    Raises ``RuntimeError`` if ``invoke()`` returns a non-dict value, which
    indicates an unexpected LangGraph return type (likely a bug).
    """
    if not isinstance(result, dict):
        raise RuntimeError(
            f"Unexpected LangGraph invoke() return type: {type(result).__name__!r}. "
            "Expected a state dict. This is likely a bug in the workflow definition."
        )
    return result.get("status") not in {"completed", "failed", "blocked"}


def _print_pause_message(issue_key: str) -> None:
    """Print workflow checkpoint pause instructions to stderr."""
    print(
        f"\n[langchain] Workflow paused at checkpoint — not yet complete.\n"
        f"Resume with: agdt-initiate-work-on-jira-issue-workflow "
        f"--issue-key {issue_key} --engine langchain --resume",
        file=sys.stderr,
    )
