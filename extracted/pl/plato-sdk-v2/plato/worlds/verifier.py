"""Code-first verifier runtime with marker-file durability."""

from __future__ import annotations

import asyncio
import contextvars
import functools
import inspect
import json
import logging
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Literal, get_type_hints

from pydantic import BaseModel, Field

from plato.otel import emit_step, start_debug_span

logger = logging.getLogger(__name__)

VerifierMode = Literal["soft", "hard"]
VerifierSignal = Literal["pass", "fail", "error", "warn", "skip", "unknown"]


class VerifierOutput(BaseModel):
    """Canonical structured return type for verifier functions."""

    signal: str | bool = "unknown"
    summary: str = ""
    data: dict[str, Any] = Field(default_factory=dict)


class VerificationOutputContract(BaseModel):
    """How verifier return values are parsed into a normalized verification signal."""

    signal_path: str = Field(
        default="signal",
        description="Dotted path used to extract the signal from verifier output",
    )
    summary_path: str = Field(
        default="summary",
        description="Dotted path used to extract a human-readable summary",
    )
    data_path: str = Field(
        default="data",
        description="Dotted path used to extract structured verifier payload",
    )
    pass_values: list[str] = Field(
        default_factory=lambda: ["pass", "ok", "success", "true"],
        description="Case-insensitive raw values treated as pass signals",
    )
    fail_values: list[str] = Field(
        default_factory=lambda: ["fail", "failed", "error", "false"],
        description="Case-insensitive raw values treated as fail signals",
    )
    unknown_is_failure: bool = Field(
        default=False,
        description="Treat unknown signals as failures when true",
    )


class VerifierResult(BaseModel):
    """Normalized verifier signal used for logging and failure policy."""

    verifier_id: str
    stage: str
    signal: VerifierSignal
    summary: str = ""
    data: dict[str, Any] = Field(default_factory=dict)
    mode: VerifierMode
    cached: bool = False
    duration_ms: float = 0.0


class VerifierRuntimeConfig(BaseModel):
    """Runtime verifier context passed directly into @verifier-decorated calls."""

    model_config = {"arbitrary_types_allowed": True}

    tracer: Any
    stage: str
    step_number: int
    base_dir: Path | None = None
    workspace: Any | None = None
    relative_dir: str | Path | None = None
    contract: VerificationOutputContract
    mode: VerifierMode


class VerifierRunContext(BaseModel):
    """World-level verifier defaults used when calling @verifier functions directly."""

    model_config = {"arbitrary_types_allowed": True}

    tracer: Any
    stage: str
    step_number: int
    base_dir: Path | None = None
    workspace: Any | None = None
    relative_dir: str | Path | None = None
    contract: VerificationOutputContract
    mode: VerifierMode


class _VerifierMarker(BaseModel):
    result: VerifierResult
    output: Any | None = None


class _VerifierScope(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    stage: str
    step_number: int
    base_dir: Path
    contract: VerificationOutputContract
    mode: VerifierMode
    tracer: Any
    failures: list[str] = Field(default_factory=list)
    atif_step_id: int = 0
    total_runs: int = 0
    cached_runs: int = 0

    def marker_path(self, verifier_id: str) -> Path:
        return self.base_dir / "verifiers" / self.stage / verifier_id / "result.json"

    def next_step_id(self) -> int:
        self.atif_step_id += 1
        return self.atif_step_id


_SCOPE: contextvars.ContextVar[_VerifierScope | None] = contextvars.ContextVar(
    "plato_world_verifier_scope",
    default=None,
)
_RUN_CONTEXT: contextvars.ContextVar[VerifierRunContext | None] = contextvars.ContextVar(
    "plato_world_verifier_run_context",
    default=None,
)
_MISSING = object()


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _lookup_path(payload: Any, dotted_path: str) -> Any:
    if not dotted_path:
        return None
    current = payload
    for part in dotted_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue
        return None
    return current


def _normalize_signal(raw_signal: Any, contract: VerificationOutputContract) -> VerifierSignal:
    if isinstance(raw_signal, bool):
        return "pass" if raw_signal else "fail"
    lowered = _to_text(raw_signal).lower()
    if not lowered:
        return "unknown"
    if lowered in {s.lower() for s in contract.pass_values}:
        return "pass"
    if lowered in {s.lower() for s in contract.fail_values}:
        if lowered in {"error", "exception"}:
            return "error"
        return "fail"
    if lowered in {"warn", "warning"}:
        return "warn"
    if lowered in {"skip", "skipped"}:
        return "skip"
    return "unknown"


def _normalize_output(
    *,
    raw_output: Any,
    verifier_id: str,
    stage: str,
    mode: VerifierMode,
    contract: VerificationOutputContract,
) -> VerifierResult:
    payload: Any
    if isinstance(raw_output, BaseModel):
        payload = raw_output.model_dump(mode="python")
    else:
        payload = VerifierOutput(
            signal="error",
            summary="Verifier returned non-structured output; expected a Pydantic BaseModel",
            data={"output_type": type(raw_output).__name__},
        ).model_dump(mode="python")

    signal_raw = _lookup_path(payload, contract.signal_path)
    summary_raw = _lookup_path(payload, contract.summary_path)
    data_raw = _lookup_path(payload, contract.data_path)

    signal = "pass" if signal_raw is None else _normalize_signal(signal_raw, contract)
    summary = _to_text(summary_raw)

    if isinstance(data_raw, dict):
        data = data_raw
    elif data_raw is None:
        if isinstance(payload, dict):
            data = payload
        else:
            data = {"raw_output": payload}
    else:
        data = {"value": data_raw}

    return VerifierResult(
        verifier_id=verifier_id,
        stage=stage,
        signal=signal,
        summary=summary,
        data=data,
        mode=mode,
    )


def _is_failure_signal(signal: VerifierSignal, contract: VerificationOutputContract) -> bool:
    if signal in {"fail", "error"}:
        return True
    if signal == "unknown" and contract.unknown_is_failure:
        return True
    return False


def _serialize_output(raw_output: Any) -> Any | None:
    if isinstance(raw_output, BaseModel):
        return raw_output.model_dump(mode="python")
    return None


def _coerce_runtime_cfg(raw: Any) -> VerifierRuntimeConfig:
    if isinstance(raw, VerifierRuntimeConfig):
        return raw
    return VerifierRuntimeConfig.model_validate(raw)


def _coerce_run_context(raw: Any) -> VerifierRunContext:
    if isinstance(raw, VerifierRunContext):
        return raw
    return VerifierRunContext.model_validate(raw)


def _runtime_cfg_from_run_context(
    *,
    run_context: VerifierRunContext,
) -> VerifierRuntimeConfig:
    return VerifierRuntimeConfig(
        tracer=run_context.tracer,
        stage=run_context.stage,
        step_number=run_context.step_number,
        base_dir=run_context.base_dir,
        workspace=run_context.workspace,
        relative_dir=run_context.relative_dir,
        contract=run_context.contract,
        mode=run_context.mode,
    )


def set_verifier_run_context(config: VerifierRunContext | dict[str, Any]) -> contextvars.Token:
    """Set world-level verifier defaults for subsequent @verifier calls."""
    return _RUN_CONTEXT.set(_coerce_run_context(config))


def reset_verifier_run_context(token: contextvars.Token) -> None:
    """Reset verifier run context to the previous value."""
    _RUN_CONTEXT.reset(token)


def get_verifier_run_context() -> VerifierRunContext | None:
    """Return current world-level verifier defaults."""
    return _RUN_CONTEXT.get()


def _resolve_return_model(fn: Any) -> type[BaseModel] | None:
    try:
        return_hint = get_type_hints(fn).get("return")
    except Exception:  # noqa: BLE001
        return None
    if isinstance(return_hint, type) and issubclass(return_hint, BaseModel):
        return return_hint
    return None


def _deserialize_output(output_payload: Any | None, return_model: type[BaseModel] | None) -> Any:
    if output_payload is None:
        return _MISSING
    if return_model is None:
        return output_payload
    try:
        return return_model.model_validate(output_payload)
    except Exception:  # noqa: BLE001
        logger.warning("Failed to deserialize verifier cached output", exc_info=True)
        return _MISSING


def _write_marker(path: Path, result: VerifierResult, output: Any | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _VerifierMarker(result=result, output=output).model_dump(mode="python")
    path.write_text(json.dumps(payload, indent=2, default=str))


def _read_marker(path: Path) -> tuple[VerifierResult, Any | None]:
    payload = json.loads(path.read_text())
    if isinstance(payload, dict) and "result" in payload:
        marker = _VerifierMarker.model_validate(payload)
        return marker.result, marker.output
    # Backward compatibility with old marker format.
    return VerifierResult.model_validate(payload), None


def _log_signal(scope: _VerifierScope | None, result: VerifierResult) -> None:
    if scope is None:
        return

    emit_step(
        scope.tracer,
        step_id=scope.next_step_id(),
        source="system",
        message=f"Verifier {result.verifier_id}: {result.signal}",
        observation={
            "verification": {
                "stage": result.stage,
                "id": result.verifier_id,
                "signal": result.signal,
                "summary": result.summary,
                "data": result.data,
                "mode": result.mode,
                "cached": result.cached,
                "duration_ms": result.duration_ms,
            }
        },
    )


def _finalize_result(
    *,
    scope: _VerifierScope | None,
    result: VerifierResult,
) -> VerifierResult:
    if scope is not None:
        scope.total_runs += 1
        if result.cached:
            scope.cached_runs += 1
        if _is_failure_signal(result.signal, scope.contract) and scope.mode == "hard":
            scope.failures.append(f"{result.verifier_id}={result.signal} ({result.summary or 'no summary'})")
    _log_signal(scope, result)
    return result


def _sync_run(
    fn: Any,
    verifier_id: str,
    return_model: type[BaseModel] | None,
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, VerifierResult]:
    scope = _SCOPE.get()

    stage = scope.stage if scope is not None else "unspecified"
    mode: VerifierMode = scope.mode if scope is not None else "soft"
    contract = scope.contract if scope is not None else VerificationOutputContract()
    marker_path = scope.marker_path(verifier_id) if scope is not None else None

    start = time.perf_counter()
    cached = False
    output: Any = _MISSING
    if marker_path is not None and marker_path.exists():
        cached_result, cached_output_payload = _read_marker(marker_path)
        maybe_output = _deserialize_output(cached_output_payload, return_model)
        if maybe_output is not _MISSING:
            result = cached_result
            output = maybe_output
            cached = True
    if output is _MISSING:
        try:
            raw_output = fn(*args, **kwargs)
            output = raw_output
        except Exception as exc:  # noqa: BLE001
            result = _normalize_output(
                raw_output=VerifierOutput(
                    signal="error",
                    summary=f"{type(exc).__name__}: {exc}",
                    data={"exception_type": type(exc).__name__},
                ),
                verifier_id=verifier_id,
                stage=stage,
                mode=mode,
                contract=contract,
            )
            duration_ms = (time.perf_counter() - start) * 1000
            result = result.model_copy(update={"cached": False, "duration_ms": duration_ms})
            _finalize_result(scope=scope, result=result)
            raise
        result = _normalize_output(
            raw_output=raw_output,
            verifier_id=verifier_id,
            stage=stage,
            mode=mode,
            contract=contract,
        )
        if marker_path is not None:
            serialized_output = _serialize_output(raw_output)
            if serialized_output is not None:
                _write_marker(marker_path, result, serialized_output)
            else:
                logger.warning(
                    "Skipping verifier marker write for %s: output is not a BaseModel",
                    verifier_id,
                )

    duration_ms = (time.perf_counter() - start) * 1000
    result = result.model_copy(update={"cached": cached, "duration_ms": duration_ms})
    finalized = _finalize_result(scope=scope, result=result)
    return output, finalized


async def _async_run(
    fn: Any,
    verifier_id: str,
    return_model: type[BaseModel] | None,
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, VerifierResult]:
    scope = _SCOPE.get()

    stage = scope.stage if scope is not None else "unspecified"
    mode: VerifierMode = scope.mode if scope is not None else "soft"
    contract = scope.contract if scope is not None else VerificationOutputContract()
    marker_path = scope.marker_path(verifier_id) if scope is not None else None

    start = time.perf_counter()
    cached = False
    output: Any = _MISSING
    if marker_path is not None and marker_path.exists():
        cached_result, cached_output_payload = _read_marker(marker_path)
        maybe_output = _deserialize_output(cached_output_payload, return_model)
        if maybe_output is not _MISSING:
            result = cached_result
            output = maybe_output
            cached = True
    if output is _MISSING:
        try:
            raw_output = await fn(*args, **kwargs)
            output = raw_output
        except Exception as exc:  # noqa: BLE001
            result = _normalize_output(
                raw_output=VerifierOutput(
                    signal="error",
                    summary=f"{type(exc).__name__}: {exc}",
                    data={"exception_type": type(exc).__name__},
                ),
                verifier_id=verifier_id,
                stage=stage,
                mode=mode,
                contract=contract,
            )
            duration_ms = (time.perf_counter() - start) * 1000
            result = result.model_copy(update={"cached": False, "duration_ms": duration_ms})
            _finalize_result(scope=scope, result=result)
            raise
        result = _normalize_output(
            raw_output=raw_output,
            verifier_id=verifier_id,
            stage=stage,
            mode=mode,
            contract=contract,
        )
        if marker_path is not None:
            serialized_output = _serialize_output(raw_output)
            if serialized_output is not None:
                _write_marker(marker_path, result, serialized_output)
            else:
                logger.warning(
                    "Skipping verifier marker write for %s: output is not a BaseModel",
                    verifier_id,
                )

    duration_ms = (time.perf_counter() - start) * 1000
    result = result.model_copy(update={"cached": cached, "duration_ms": duration_ms})
    finalized = _finalize_result(scope=scope, result=result)
    return output, finalized


def verifier(fn: Any | None = None, *, stage: str | None = None) -> Any:
    """Decorate a function with verifier logging while preserving return type."""

    def decorator(inner_fn: Any) -> Any:
        verifier_id = inner_fn.__name__
        resolved_stage = stage
        return_model = _resolve_return_model(inner_fn)
        is_async = asyncio.iscoroutinefunction(inner_fn)

        def _resolve_runtime_cfg(
            *,
            scope: _VerifierScope | None,
            runtime_cfg_raw: Any | None,
        ) -> VerifierRuntimeConfig | None:
            if runtime_cfg_raw is not None:
                if scope is not None:
                    raise RuntimeError("verifier_runtime cannot be used while verifier_scope is active")
                runtime_cfg = _coerce_runtime_cfg(runtime_cfg_raw)
                if resolved_stage is not None and runtime_cfg.stage != resolved_stage:
                    raise RuntimeError(
                        f"verifier runtime stage '{runtime_cfg.stage}' does not match decorator stage '{resolved_stage}'"
                    )
                return runtime_cfg

            if scope is None:
                run_context = get_verifier_run_context()
                if run_context is not None:
                    runtime_cfg = _runtime_cfg_from_run_context(run_context=run_context)
                    if resolved_stage is not None and runtime_cfg.stage != resolved_stage:
                        raise RuntimeError(
                            f"verifier run context stage '{runtime_cfg.stage}' does not match decorator stage '{resolved_stage}'"
                        )
                    return runtime_cfg
            return None

        if is_async:

            @functools.wraps(inner_fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                scope = _SCOPE.get()
                runtime_cfg = _resolve_runtime_cfg(
                    scope=scope,
                    runtime_cfg_raw=kwargs.pop("verifier_runtime", None),
                )
                if runtime_cfg is not None:
                    with verifier_scope(
                        tracer=runtime_cfg.tracer,
                        stage=runtime_cfg.stage,
                        step_number=runtime_cfg.step_number,
                        base_dir=runtime_cfg.base_dir,
                        workspace=runtime_cfg.workspace,
                        relative_dir=runtime_cfg.relative_dir,
                        contract=runtime_cfg.contract,
                        mode=runtime_cfg.mode,
                    ):
                        output, _ = await _async_run(inner_fn, verifier_id, return_model, *args, **kwargs)
                        return output

                if scope is None:
                    return await inner_fn(*args, **kwargs)
                tracer = scope.tracer
                if tracer is None:
                    output, _ = await _async_run(inner_fn, verifier_id, return_model, *args, **kwargs)
                    return output
                with start_debug_span(tracer, "verification.run") as span:
                    span.set_attribute("verification.verifier_id", verifier_id)
                    span.set_attribute("verification.stage", scope.stage)
                    output, result = await _async_run(inner_fn, verifier_id, return_model, *args, **kwargs)
                    span.set_attribute("verification.signal", result.signal)
                    span.set_attribute("verification.mode", result.mode)
                    span.set_attribute("verification.cached", result.cached)
                    span.set_attribute("verification.duration_ms", result.duration_ms)
                    return output

            return async_wrapper

        @functools.wraps(inner_fn)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            scope = _SCOPE.get()
            runtime_cfg = _resolve_runtime_cfg(
                scope=scope,
                runtime_cfg_raw=kwargs.pop("verifier_runtime", None),
            )
            if runtime_cfg is not None:
                with verifier_scope(
                    tracer=runtime_cfg.tracer,
                    stage=runtime_cfg.stage,
                    step_number=runtime_cfg.step_number,
                    base_dir=runtime_cfg.base_dir,
                    workspace=runtime_cfg.workspace,
                    relative_dir=runtime_cfg.relative_dir,
                    contract=runtime_cfg.contract,
                    mode=runtime_cfg.mode,
                ):
                    output, _ = _sync_run(inner_fn, verifier_id, return_model, *args, **kwargs)
                    return output

            if scope is None:
                return inner_fn(*args, **kwargs)
            tracer = scope.tracer
            if tracer is None:
                output, _ = _sync_run(inner_fn, verifier_id, return_model, *args, **kwargs)
                return output
            with start_debug_span(tracer, "verification.run") as span:
                span.set_attribute("verification.verifier_id", verifier_id)
                span.set_attribute("verification.stage", scope.stage)
                output, result = _sync_run(inner_fn, verifier_id, return_model, *args, **kwargs)
                span.set_attribute("verification.signal", result.signal)
                span.set_attribute("verification.mode", result.mode)
                span.set_attribute("verification.cached", result.cached)
                span.set_attribute("verification.duration_ms", result.duration_ms)
                return output

        return sync_wrapper

    if fn is None:
        return decorator
    return decorator(fn)


@contextmanager
def verifier_scope(
    *,
    tracer: Any,
    stage: str,
    step_number: int,
    base_dir: Path | None = None,
    workspace: Any | None = None,
    relative_dir: str | Path | None = None,
    contract: VerificationOutputContract,
    mode: VerifierMode,
):
    """Set runtime verifier scope for decorated function calls."""
    if base_dir is not None and workspace is not None:
        raise TypeError("verifier_scope accepts either base_dir or workspace, not both")
    if base_dir is None and workspace is None:
        raise TypeError("verifier_scope requires either base_dir or workspace")

    if workspace is not None:
        workspace_path = getattr(workspace, "path", None)
        if workspace_path is None:
            raise TypeError("workspace must provide a .path attribute")
        resolved_base_dir = Path(workspace_path)
        if relative_dir is not None:
            resolved_base_dir = resolved_base_dir / Path(relative_dir)
    else:
        resolved_base_dir = Path(base_dir)  # type: ignore[arg-type]

    scope = _VerifierScope(
        stage=stage,
        step_number=step_number,
        base_dir=resolved_base_dir,
        contract=contract,
        mode=mode,
        tracer=tracer,
    )
    token = _SCOPE.set(scope)
    try:
        with tracer.start_as_current_span("verification.batch") as span:
            span.set_attribute("verification.stage", stage)
            span.set_attribute("verification.step_number", step_number)
            span.set_attribute("verification.mode", mode)
            span.set_attribute("atif.agent.name", "webclone-verifier")
            span.set_attribute("atif.agent.version", "0.1.0")
            yield
            span.set_attribute("verification.total_runs", scope.total_runs)
            span.set_attribute("verification.cached_runs", scope.cached_runs)
            span.set_attribute("verification.failures", len(scope.failures))
    finally:
        _SCOPE.reset(token)

    if scope.failures and mode == "hard":
        joined = "; ".join(scope.failures)
        raise RuntimeError(f"Verifier hard-fail in stage '{stage}': {joined}")


def verifier_mode_for_stage(
    *,
    stage: str,
    default_mode: VerifierMode,
    stage_modes: dict[str, VerifierMode],
) -> VerifierMode:
    return stage_modes.get(stage, default_mode)


async def run_with_verifier_scope(
    fn: Any,
    *fn_args: Any,
    verifier_tracer: Any,
    verifier_stage: str,
    verifier_step_number: int,
    verifier_base_dir: Path | None = None,
    verifier_workspace: Any | None = None,
    verifier_relative_dir: str | Path | None = None,
    verifier_contract: VerificationOutputContract,
    verifier_mode: VerifierMode,
    **fn_kwargs: Any,
) -> Any:
    """Run a callable under verifier scope without explicit context-manager syntax."""
    with verifier_scope(
        tracer=verifier_tracer,
        stage=verifier_stage,
        step_number=verifier_step_number,
        base_dir=verifier_base_dir,
        workspace=verifier_workspace,
        relative_dir=verifier_relative_dir,
        contract=verifier_contract,
        mode=verifier_mode,
    ):
        result = fn(*fn_args, **fn_kwargs)
        if inspect.isawaitable(result):
            return await result
        return result


__all__ = [
    "VerificationOutputContract",
    "VerifierMode",
    "VerifierOutput",
    "VerifierRunContext",
    "VerifierRuntimeConfig",
    "VerifierResult",
    "get_verifier_run_context",
    "reset_verifier_run_context",
    "set_verifier_run_context",
    "verifier",
    "verifier_mode_for_stage",
    "verifier_scope",
    "run_with_verifier_scope",
]
