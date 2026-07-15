"""Assessment orchestrator for AI Red Teaming.

Coordinates multi-attack assessments with automatic result tracking.

Usage::

    from dreadnode.airt import Assessment, tap_attack

    async with Assessment(
        name="My Assessment",
        target=target,
        model="groq/llama-3.3-70b-versatile",
        goal="Extract sensitive information",
    ) as assessment:
        await assessment.run(tap_attack)                                    # baseline
        await assessment.run(tap_attack, transforms=[adapt_language("es")]) # with transform
    # auto-completes on exit
"""

from __future__ import annotations

import contextlib
import contextvars
import os
import signal
import threading
import typing as t
from pathlib import Path

from loguru import logger

from dreadnode.airt.analytics.engine import AttackResult
from dreadnode.generators.proxy import resolve_dn_model_to_generator

if t.TYPE_CHECKING:
    import types
    from collections.abc import AsyncIterator, Callable

    from dreadnode.airt.analytics.types import GoalCategory
    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.config import Profile
    from dreadnode.core.task import Task
    from dreadnode.optimization.study import Study

_current_assessment: contextvars.ContextVar[Assessment | None] = contextvars.ContextVar(
    "_current_assessment", default=None
)


def _get_platform_context() -> tuple[ApiClient, Profile] | None:
    """Get the API client and profile if connected to the platform."""
    try:
        from dreadnode.app.main import DEFAULT_INSTANCE

        if DEFAULT_INSTANCE.can_sync:
            return DEFAULT_INSTANCE.api, DEFAULT_INSTANCE.profile
    except Exception:
        logger.debug("Unable to resolve platform context for AIRT assessment")
    return None


# Thread-local storage for injected platform context
_thread_local = threading.local()


def _set_platform_context(api: ApiClient, profile: Profile) -> None:
    """Set platform context for the current thread (used by AIRT CLI)."""
    _thread_local.api = api
    _thread_local.profile = profile


def _get_platform_context_with_fallback() -> tuple[ApiClient, Profile] | None:
    """Get platform context with CLI injection fallback."""
    # First try thread-local injected context (from AIRT CLI)
    if hasattr(_thread_local, "api") and hasattr(_thread_local, "profile"):
        return _thread_local.api, _thread_local.profile

    # Fallback to global DEFAULT_INSTANCE
    return _get_platform_context()


class Assessment:
    """Orchestrates multi-attack assessments.

    Accepts attack factories or pre-built Study instances via ``run()``,
    tracks results, and auto-completes when done.

    Example::

        async with Assessment(name="...", target=target, model=MODEL, goal="...") as assessment:
            await assessment.run(tap_attack)
            await assessment.run(tap_attack, transforms=[adapt_language("es")])
        # auto-completes on exit
    """

    def __init__(
        self,
        name: str,
        *,
        target: Task[..., str] | None = None,
        model: str | None = None,
        goal: str | None = None,
        goal_category: str | None = None,
        attack_defaults: dict[str, t.Any] | None = None,
        description: str | None = None,
        session_id: str | None = None,
        target_model: str | None = None,
        attacker_model: str | None = None,
        judge_model: str | None = None,
        target_config: dict[str, t.Any] | None = None,
        attacker_config: dict[str, t.Any] | None = None,
        attack_manifest: list[dict[str, t.Any]] | None = None,
        workflow_run_id: str | None = None,
        workflow_script: str | None = None,
        project_id: str | None = None,
        runtime_id: str | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.target = target
        self.model = model
        self.goal = goal
        self.goal_category = goal_category
        self._attack_defaults = attack_defaults or {}

        # First-class model identifiers for platform UI
        self.target_model = target_model or model
        self.attacker_model = attacker_model or model
        self.judge_model = judge_model or model

        if target_config is None and model is not None:
            target_config = {"model": self.target_model or model}
        if attacker_config is None and model is not None:
            attacker_config = {
                "model": self.attacker_model or model,
                "evaluator_model": self.judge_model or model,
            }

        self.target_config = target_config
        self.attacker_config = attacker_config

        # Infer first-class model ids from the configs when not passed explicitly,
        # so a user who only provides target_config / attacker_config still gets
        # model metadata on the assessment header AND findings (mirrors the
        # platform-side backfill). Keys match the capability/TUI convention.
        if self.target_model is None and self.target_config:
            self.target_model = self.target_config.get("model")
        if self.attacker_model is None and self.attacker_config:
            self.attacker_model = self.attacker_config.get("model") or self.attacker_config.get(
                "attacker_model"
            )
        if self.judge_model is None and self.attacker_config:
            self.judge_model = self.attacker_config.get(
                "evaluator_model"
            ) or self.attacker_config.get("judge")

        self._attack_manifest = attack_manifest
        self._workflow_run_id = workflow_run_id
        self._workflow_script = workflow_script
        self._project_id = project_id
        self._runtime_id = runtime_id

        self._session_id = session_id or os.environ.get("DREADNODE_SESSION_ID")
        if self._session_id is None:
            session_file = Path("~/.dreadnode_session_id").expanduser()
            if session_file.is_file():
                with contextlib.suppress(OSError):
                    self._session_id = session_file.read_text(encoding="utf-8").strip() or None

        self._assessment_id: str | None = None
        self._attack_results: list[AttackResult] = []
        self._tracing_enabled: bool = False
        self._auto_registered: bool = False
        self._context_token: contextvars.Token[Assessment | None] | None = None
        # Terminal-failure latch. Once fail() runs, auto-finalization
        # (_finalize/complete/atexit) must NOT flip the status back to
        # "completed" — otherwise a failure caught inside the `async with`
        # block is masked by the clean-exit auto-complete (ENG-6822).
        self._failed: bool = False

    async def __aenter__(self) -> Assessment:
        self._context_token = _current_assessment.set(self)
        self._tracing_enabled = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                self._tracing_enabled = False
                await self.fail(reason=f"Exception: {exc_val}")
            else:
                await self._finalize()
        finally:
            self._tracing_enabled = False
            if self._context_token is not None:
                with contextlib.suppress(ValueError):
                    _current_assessment.reset(self._context_token)
                self._context_token = None

    @property
    def assessment_id(self) -> str | None:
        """Platform assessment ID, or None if not registered."""
        return self._assessment_id

    @property
    def attack_results(self) -> list[AttackResult]:
        """All collected attack results."""
        return list(self._attack_results)

    # =========================================================================
    # Platform Registration
    # =========================================================================

    async def register(self) -> str | None:
        """Register this assessment with the platform.

        Returns:
            The platform assessment ID, or None if offline.
        """
        if self._assessment_id is not None:
            return self._assessment_id

        ctx = _get_platform_context_with_fallback()
        if ctx is None:
            logger.debug("SDK offline -- assessment not registered with platform")
            return None

        api, profile = ctx
        project_id = self._project_id
        if project_id is None and profile.project_id is not None:
            project_id = profile.project_id

        if project_id is None:
            logger.warning("No project_id available -- cannot register assessment")
            return None

        try:
            # Get runtime_id - try to use a default runtime for the project
            runtime_id = getattr(self, "_runtime_id", None)
            if runtime_id is None:
                # Auto-discover a runtime for this project (CLI users shouldn't need to specify this)
                try:
                    runtimes_resp = api.list_runtimes(profile.org_key, profile.workspace_key)
                    runtime_items = runtimes_resp.get("items", [])
                    matching_runtimes = [r for r in runtime_items if r["project_id"] == project_id]
                    if matching_runtimes:
                        runtime_id = matching_runtimes[0]["id"]
                        logger.debug(f"Auto-selected runtime {runtime_id} for project {project_id}")
                    else:
                        logger.warning(f"No runtimes found for project {project_id}")
                except Exception as e:
                    logger.debug(f"Failed to auto-discover runtime for project: {e}")

            result = api.create_airt_assessment(
                profile.org_key,
                profile.workspace_key,
                name=self.name,
                project_id=project_id,
                runtime_id=runtime_id,
                description=self.description,
                session_id=self._session_id,
                target_model=self.target_model,
                attacker_model=self.attacker_model,
                judge_model=self.judge_model,
                target_config=self.target_config,
                attacker_config=self.attacker_config,
                attack_manifest=self._attack_manifest,
                workflow_run_id=self._workflow_run_id,
                workflow_script=self._workflow_script,
            )
        except Exception as e:
            logger.error(f"Failed to register assessment: {e}")
            return None

        self._assessment_id = result["id"]
        logger.info(f"Assessment registered: {self._assessment_id}")
        return self._assessment_id

    # =========================================================================
    # Tracing
    # =========================================================================

    @contextlib.asynccontextmanager
    async def trace(self) -> AsyncIterator[Assessment]:
        """Context manager that enables tracing and auto-completes on exit.

        Kept for backward compatibility. Prefer ``async with Assessment(...) as a:``.
        """
        async with self as a:
            yield a

    async def _finalize(self) -> None:
        """Flush pending OTEL spans and mark complete."""
        if not self._attack_results:
            return

        # Flush pending OTEL spans BEFORE marking complete so CH has data
        # when the API materializes findings on status change.
        # dn.shutdown() would kill the trace provider, breaking any
        # subsequent assessments in the same process.
        with contextlib.suppress(Exception):
            from dreadnode.app.main import DEFAULT_INSTANCE

            provider = DEFAULT_INSTANCE._logfire._tracer_provider
            if hasattr(provider, "force_flush"):
                provider.force_flush(timeout_millis=10_000)

        await self.complete()

    async def run(
        self,
        attack: Study[t.Any] | Callable[..., Study[t.Any]],
        /,
        **kwargs: t.Any,
    ) -> t.Any:
        """Run an attack and upload its result.

        Accepts either a pre-built Study or an attack factory function.
        When given a factory, assessment defaults (goal, target, model)
        are filled in automatically.

        Args:
            attack: A Study instance, or an attack factory function
                (``tap_attack``, ``pair_attack``, ``goat_attack``, etc.).
            **kwargs: When ``attack`` is a factory, these override
                assessment defaults (transforms, n_iterations, etc.).

        Returns:
            The StudyResult from the attack execution.

        Examples::

            # Pass a factory — assessment fills in goal/target/model
            await assessment.run(tap_attack)
            await assessment.run(tap_attack, transforms=[adapt_language("es")])
            await assessment.run(pair_attack, n_streams=20)

            # Pass a pre-built Study (TUI/capability path)
            study = tap_attack(goal, target, model, model, ...)
            await assessment.run(study)
        """
        await self._ensure_started()

        from dreadnode.optimization.study import Study as StudyClass

        if isinstance(attack, StudyClass):
            study = attack
        elif callable(attack):
            study = self._build_study(attack, **kwargs)
        else:
            raise TypeError(
                f"Expected a Study instance or attack factory callable, got {type(attack).__name__}"
            )

        if self._assessment_id and not study.airt_assessment_id:
            study.airt_assessment_id = self._assessment_id
        # Inject assessment-level defaults into pre-built studies
        if self.goal_category and not study.airt_goal_category:
            study.airt_goal_category = self.goal_category
        if self.goal_category and not study.airt_category:
            study.airt_category = self.goal_category
        if self.goal_category and not study.airt_sub_category:
            study.airt_sub_category = self.goal_category
        # Propagate the assessment's model identifiers so findings carry the
        # target/judge metadata without the caller passing airt_* kwargs to the
        # attack factory (e.g. multimodal_attack, which the user builds directly).
        if self.target_model and not study.airt_target_model:
            study.airt_target_model = self.target_model
        if self.judge_model and not study.airt_evaluator_model:
            study.airt_evaluator_model = self.judge_model
        if self.attacker_model and not study.airt_attacker_model:
            study.airt_attacker_model = self.attacker_model

        from dreadnode.airt.analytics.types import GoalCategory

        result = await study.run()

        try:
            goal_category: GoalCategory = GoalCategory(study.airt_goal_category)
        except (ValueError, KeyError):
            goal_category = GoalCategory.JAILBREAK_GENERAL

        ar = AttackResult.from_study(
            result,
            attack_name=study.airt_attack_name or study.name,
            goal=study.airt_goal or "",
            goal_category=goal_category,
            compliance_tags=study.compliance_tags,
            transforms_applied=study.airt_transforms or [],
            execution_time_s=getattr(result, "execution_time_s", 0.0),
        )
        self._attack_results.append(ar)

        return result

    def _build_study(
        self,
        factory: Callable[..., Study[t.Any]],
        **kwargs: t.Any,
    ) -> Study[t.Any]:
        """Create a Study from an attack factory using assessment defaults.

        The factory's first 4 positional args (goal, target, attacker_model,
        evaluator_model) are filled from assessment defaults. Remaining
        kwargs are merged: assessment.attack_defaults < per-call kwargs.
        """
        goal = kwargs.pop("goal", None) or self.goal
        target = kwargs.pop("target", None) or self.target
        model = kwargs.pop("model", None) or self.model
        attacker_model = kwargs.pop("attacker_model", None) or self.attacker_model or model
        judge_model = kwargs.pop("judge_model", None) or self.judge_model or attacker_model

        # Route dn/* attacker/judge models through the LiteLLM proxy, mirroring the
        # target path (_build_target). Without this, dn/* identifiers reach litellm
        # unresolved and fail with "LLM Provider NOT provided".
        attacker_model = resolve_dn_model_to_generator(attacker_model)
        judge_model = resolve_dn_model_to_generator(judge_model)

        if goal is None:
            raise ValueError("goal must be set on the assessment or passed to run()")
        if target is None:
            raise ValueError("target must be set on the assessment or passed to run()")
        if model is None:
            raise ValueError("model must be set on the assessment or passed to run()")

        merged = {**self._attack_defaults, **kwargs}
        merged.setdefault("airt_goal_category", self.goal_category)
        # Derive category/sub_category from goal_category for compliance mapping
        # parity with TUI path (attack_runner sets these explicitly).
        if self.goal_category:
            merged.setdefault("airt_category", self.goal_category)
            merged.setdefault("airt_sub_category", self.goal_category)
        merged.setdefault("airt_target_model", self.target_model or model)

        # Filter merged params to only include those supported by the attack factory.
        # If the factory accepts **kwargs, pass everything through.
        import inspect

        factory_sig = inspect.signature(factory)
        params = list(factory_sig.parameters.values())
        has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params)

        # Count positional-or-keyword params to determine how many positional args to pass.
        # Most attacks: (goal, target, attacker_model, evaluator_model) = 4
        # Some attacks like deep_inception_attack: (goal, target, evaluator_model) = 3
        positional_params_list = [
            p
            for p in params
            if p.kind
            in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ]
        positional_names = {p.name for p in positional_params_list}
        n_positional = len(positional_params_list)

        if n_positional >= 4:
            positional_args = (goal, target, attacker_model, judge_model)
        elif n_positional == 3:
            # Attacks with 3 positional args (e.g. deep_inception_attack: goal, target, evaluator)
            positional_args = (goal, target, judge_model)
        else:
            positional_args = (goal, target)

        if has_var_keyword:
            filtered_merged = {k: v for k, v in merged.items() if k not in positional_names}
        else:
            supported_params = {p.name for p in params}
            filtered_merged = {
                k: v
                for k, v in merged.items()
                if k in supported_params and k not in positional_names
            }

        return factory(*positional_args, **filtered_merged)

    async def _ensure_started(self) -> None:
        """Auto-register, set status to running, and enable tracing on first run() call."""
        if not self._auto_registered:
            self._auto_registered = True
            await self.register()
            # Notify the platform that execution has started (sets started_at server-side)
            if self._assessment_id is not None:
                ctx = _get_platform_context_with_fallback()
                if ctx is not None:
                    api, session = ctx
                    try:
                        api.update_airt_assessment(
                            session.org_key,
                            session.workspace_key,
                            self._assessment_id,
                            status="running",
                        )
                    except Exception as e:
                        logger.debug("Failed to set assessment to running: {}", e)
            if not self._tracing_enabled:
                self._context_token = _current_assessment.set(self)
                self._tracing_enabled = True
                import atexit

                atexit.register(self._atexit_finalize)
                # Handle Ctrl+C and container shutdown (SIGTERM) gracefully
                for sig in (signal.SIGINT, signal.SIGTERM):
                    prev = signal.getsignal(sig)
                    signal.signal(sig, self._make_signal_handler(prev))

    def _make_signal_handler(
        self, prev_handler: signal.Handlers | None
    ) -> t.Callable[[int, t.Any], None]:
        """Create a signal handler that finalizes then chains to previous handler."""

        def handler(signum: int, frame: t.Any) -> None:
            self._atexit_finalize()
            if callable(prev_handler):
                prev_handler(signum, frame)
            elif prev_handler == signal.SIG_DFL:
                signal.signal(signum, signal.SIG_DFL)
                os.kill(os.getpid(), signum)

        return handler

    def _atexit_finalize(self) -> None:
        """Synchronous atexit handler — uses sync httpx so it works reliably.

        Unlike async finalization, this bypasses the event loop entirely.
        Modeled after W&B/Sentry SDKs which never rely on async in cleanup.
        """
        if not self._tracing_enabled:
            return
        self._tracing_enabled = False

        # Flush OTEL spans synchronously
        with contextlib.suppress(Exception):
            from dreadnode.app.main import DEFAULT_INSTANCE

            provider = DEFAULT_INSTANCE._logfire._tracer_provider
            if hasattr(provider, "force_flush"):
                provider.force_flush(timeout_millis=10_000)

        # Use the sync API client directly — no async gymnastics
        ctx = _get_platform_context_with_fallback()
        if ctx is None or self._assessment_id is None:
            return

        api, profile = ctx
        status = "completed" if (self._attack_results and not self._failed) else "failed"
        with contextlib.suppress(Exception):
            api.update_airt_assessment(
                profile.org_key,
                profile.workspace_key,
                self._assessment_id,
                status=status,
            )
            logger.info("Assessment auto-finalized as {} via atexit", status)

    async def done(self) -> None:
        """Finalize the assessment: upload pending results, complete, flush.

        Optional — called automatically via atexit or trace() exit.
        Call explicitly to ensure finalization happens before your script ends.
        """
        try:
            await self._finalize()
        finally:
            self._tracing_enabled = False
            if self._context_token is not None:
                with contextlib.suppress(ValueError):
                    _current_assessment.reset(self._context_token)
                self._context_token = None

    # =========================================================================
    # Lifecycle
    # =========================================================================

    async def complete(self) -> bool:
        """Mark the assessment as completed.

        Returns:
            True if successfully marked, False otherwise.
        """
        # A failed assessment is terminal — never auto-complete over it.
        if self._failed:
            logger.debug("Skipping complete(): assessment already marked as failed")
            return False

        ctx = _get_platform_context_with_fallback()
        if ctx is None or self._assessment_id is None:
            return False

        api, profile = ctx
        try:
            api.update_airt_assessment(
                profile.org_key,
                profile.workspace_key,
                self._assessment_id,
                status="completed",
            )
        except Exception as e:
            logger.error(f"Failed to complete assessment: {e}")
            return False

        logger.info("Assessment marked as completed")
        return True

    async def fail(self, reason: str | None = None) -> bool:
        """Mark the assessment as failed on the platform.

        Args:
            reason: Optional failure reason.

        Returns:
            True if successfully marked, False otherwise.
        """
        # Latch terminal failure first — even offline / before registration —
        # so any later auto-finalization won't re-complete (ENG-6822).
        self._failed = True

        ctx = _get_platform_context_with_fallback()
        if ctx is None or self._assessment_id is None:
            return False

        api, profile = ctx
        try:
            kwargs: dict[str, t.Any] = {"status": "failed"}
            if reason:
                kwargs["description"] = f"{self.description or ''}\n\nFailure: {reason}".strip()
            api.update_airt_assessment(
                profile.org_key,
                profile.workspace_key,
                self._assessment_id,
                **kwargs,
            )
        except Exception as e:
            logger.error(f"Failed to mark assessment as failed: {e}")
            return False

        logger.info("Assessment marked as failed")
        return True
