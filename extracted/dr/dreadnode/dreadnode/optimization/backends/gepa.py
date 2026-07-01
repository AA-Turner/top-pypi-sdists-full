from __future__ import annotations

import asyncio
import importlib
import inspect
import queue
import typing as t
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from dreadnode.optimization.backends.base import (
    CandidateT,
    OptimizationAdapter,
    OptimizationBackend,
    OptimizationBackendError,
    OptimizationDependencyError,
    OptimizationEvaluationBatch,
    invoke_with_supported_args,
    normalize_evaluation_result,
)
from dreadnode.optimization.events import (
    BudgetUpdated,
    CandidateAccepted,
    CandidateRejected,
    IterationStart,
    OptimizationEnd,
    OptimizationError,
    OptimizationStart,
    ParetoFrontUpdated,
    ValsetEvaluated,
)
from dreadnode.optimization.result import OptimizationResult

if t.TYPE_CHECKING:
    from types import ModuleType

    from dreadnode.optimization.api import Optimization


class _GEPAAdapterBridge(t.Generic[CandidateT]):
    """Bridge a Dreadnode adapter into GEPA's adapter contract."""

    def __init__(
        self,
        *,
        adapter: OptimizationAdapter[CandidateT],
        evaluation_batch_cls: type[t.Any],
    ) -> None:
        self._adapter = adapter
        self._evaluation_batch_cls = evaluation_batch_cls
        self.propose_new_texts = None
        proposal_fn = getattr(adapter, "propose_new_texts", None)
        proposal_enabled = getattr(adapter, "proposal_enabled", proposal_fn is not None)
        if proposal_fn is not None and proposal_enabled:
            self.propose_new_texts = proposal_fn

    def evaluate(
        self,
        batch: list[t.Any],
        candidate: CandidateT,
        *,
        capture_traces: bool = False,
    ) -> t.Any:
        result = self._adapter.evaluate(batch, candidate, capture_traces=capture_traces)
        if inspect.isawaitable(result):
            result = asyncio.run(t.cast("t.Awaitable[OptimizationEvaluationBatch]", result))
        batch_result = t.cast("OptimizationEvaluationBatch", result)
        return self._evaluation_batch_cls(
            outputs=batch_result.outputs,
            scores=batch_result.scores,
            trajectories=batch_result.trajectories,
            objective_scores=batch_result.objective_scores,
        )

    def make_reflective_dataset(
        self,
        candidate: CandidateT,
        eval_batch: t.Any,
        components_to_update: list[str],
    ) -> dict[str, list[dict[str, t.Any]]]:
        trajectories = getattr(eval_batch, "trajectories", None)
        objective_scores = getattr(eval_batch, "objective_scores", None)
        dreadnode_batch = OptimizationEvaluationBatch(
            outputs=list(getattr(eval_batch, "outputs", []) or []),
            scores=list(getattr(eval_batch, "scores", []) or []),
            trajectories=list(trajectories) if isinstance(trajectories, list) else trajectories,
            objective_scores=(
                list(objective_scores) if isinstance(objective_scores, list) else objective_scores
            ),
        )
        return self._adapter.make_reflective_dataset(
            candidate,
            dreadnode_batch,
            list(components_to_update),
        )


@dataclass
class _WorkerSuccess:
    result: t.Any


@dataclass
class _WorkerFailure:
    error: Exception


def _raise_worker_failure(error: Exception) -> t.NoReturn:
    raise error


class _GEPAProgressCallback:
    """Translate synchronous GEPA callbacks into Dreadnode optimization events."""

    def __init__(
        self,
        *,
        event_queue: queue.Queue[
            OptimizationStart
            | IterationStart
            | CandidateAccepted
            | CandidateRejected
            | ValsetEvaluated
            | BudgetUpdated
            | ParetoFrontUpdated
            | _WorkerSuccess
            | _WorkerFailure
        ],
        optimization_id: t.Any,
        optimization_name: str,
    ) -> None:
        self._event_queue = event_queue
        self._optimization_id = optimization_id
        self._optimization_name = optimization_name

    def on_iteration_start(self, event: Mapping[str, t.Any]) -> None:
        self._put(
            IterationStart(
                optimization_id=self._optimization_id,
                optimization_name=self._optimization_name,
                iteration=self._as_int(event.get("iteration")),
            )
        )

    def on_candidate_accepted(self, event: Mapping[str, t.Any]) -> None:
        self._put(
            CandidateAccepted(
                optimization_id=self._optimization_id,
                optimization_name=self._optimization_name,
                iteration=self._as_int(event.get("iteration")),
                candidate_index=self._as_int(event.get("new_candidate_idx")),
                score=self._as_float(event.get("new_score")),
                parent_indices=self._coerce_int_list(event.get("parent_ids")),
            )
        )

    def on_candidate_rejected(self, event: Mapping[str, t.Any]) -> None:
        self._put(
            CandidateRejected(
                optimization_id=self._optimization_id,
                optimization_name=self._optimization_name,
                iteration=self._as_int(event.get("iteration")),
                previous_score=self._as_float(event.get("old_score")),
                candidate_score=self._as_float(event.get("new_score")),
                reason=str(event.get("reason", "")),
            )
        )

    def on_valset_evaluated(self, event: Mapping[str, t.Any]) -> None:
        self._put(
            ValsetEvaluated(
                optimization_id=self._optimization_id,
                optimization_name=self._optimization_name,
                iteration=self._as_int(event.get("iteration")),
                candidate_index=self._as_int(event.get("candidate_idx")),
                candidate=event.get("candidate"),
                average_score=self._as_float(event.get("average_score")),
                num_examples_evaluated=self._as_int(event.get("num_examples_evaluated")),
                total_valset_size=self._as_int(event.get("total_valset_size")),
                is_best_program=bool(event.get("is_best_program", False)),
                parent_indices=self._coerce_int_list(event.get("parent_ids")),
            )
        )

    def on_budget_updated(self, event: Mapping[str, t.Any]) -> None:
        self._put(
            BudgetUpdated(
                optimization_id=self._optimization_id,
                optimization_name=self._optimization_name,
                iteration=self._as_int(event.get("iteration")),
                metric_calls_used=self._as_int(event.get("metric_calls_used")),
                metric_calls_delta=self._as_int(event.get("metric_calls_delta")),
                metric_calls_remaining=self._as_optional_int(event.get("metric_calls_remaining")),
            )
        )

    def on_pareto_front_updated(self, event: Mapping[str, t.Any]) -> None:
        new_front = self._coerce_int_list(event.get("new_front"))
        self._put(
            ParetoFrontUpdated(
                optimization_id=self._optimization_id,
                optimization_name=self._optimization_name,
                iteration=self._as_optional_int(event.get("iteration")),
                frontier_size=len(new_front),
                frontier_candidate_indices=new_front,
                displaced_candidate_indices=self._coerce_int_list(
                    event.get("displaced_candidates")
                ),
            )
        )

    def _put(
        self,
        event: OptimizationStart
        | IterationStart
        | CandidateAccepted
        | CandidateRejected
        | ValsetEvaluated
        | BudgetUpdated
        | ParetoFrontUpdated,
    ) -> None:
        self._event_queue.put(event)

    def _as_int(self, value: object) -> int:
        return int(value) if isinstance(value, int | float) else 0

    def _as_optional_int(self, value: object) -> int | None:
        return int(value) if isinstance(value, int | float) else None

    def _as_float(self, value: object) -> float | None:
        return float(value) if isinstance(value, int | float) else None

    def _coerce_int_list(self, value: object) -> list[int]:
        if not isinstance(value, Iterable):
            return []
        return [int(item) for item in value if isinstance(item, int | float)]


class GEPABackend(OptimizationBackend[CandidateT]):
    """GEPA-backed implementation of Dreadnode optimize_anything."""

    dependency_name = "gepa"

    async def stream(
        self,
        optimization: Optimization[CandidateT],
    ) -> t.AsyncGenerator[
        OptimizationStart
        | IterationStart
        | CandidateAccepted
        | CandidateRejected
        | ValsetEvaluated
        | BudgetUpdated
        | ParetoFrontUpdated
        | OptimizationEnd[CandidateT]
        | OptimizationError[CandidateT],
        None,
    ]:
        dataset = self._resolve_trainset(optimization)
        yield OptimizationStart(
            optimization_id=optimization.optimization_id,
            optimization_name=optimization.name,
            backend="gepa",
            objective=optimization.objective,
            dataset_size=len(dataset or []),
            valset_size=len(optimization.valset or dataset or []),
            seed_candidate=optimization.seed_candidate,
            uses_adapter=optimization.adapter is not None,
        )

        try:
            optimize_module, api_module, adapter_module = self._import_gepa_modules()
            gepa_entrypoint = (
                api_module.optimize
                if optimization.adapter is not None
                else optimize_module.optimize_anything
            )
            gepa_kwargs = self._build_gepa_kwargs(
                optimization=optimization,
                optimize_module=optimize_module,
                api_module=api_module,
                adapter_module=adapter_module,
            )
            if optimization.adapter is not None:
                event_queue: queue.Queue[
                    IterationStart
                    | CandidateAccepted
                    | CandidateRejected
                    | ValsetEvaluated
                    | BudgetUpdated
                    | ParetoFrontUpdated
                    | _WorkerSuccess
                    | _WorkerFailure
                ] = queue.Queue()
                callbacks = list(t.cast("list[t.Any]", gepa_kwargs.get("callbacks", [])))
                callbacks.append(
                    _GEPAProgressCallback(
                        event_queue=event_queue,
                        optimization_id=optimization.optimization_id,
                        optimization_name=optimization.name,
                    )
                )
                gepa_kwargs["callbacks"] = callbacks

                def run_gepa() -> None:
                    try:
                        run_result = gepa_entrypoint(**gepa_kwargs)
                    except Exception as exc:
                        event_queue.put(_WorkerFailure(exc))
                    else:
                        event_queue.put(_WorkerSuccess(run_result))

                worker = asyncio.create_task(asyncio.to_thread(run_gepa))
                while True:
                    queue_item = await asyncio.to_thread(event_queue.get)
                    if isinstance(queue_item, _WorkerSuccess):
                        await worker
                        result = queue_item.result
                        break
                    if isinstance(queue_item, _WorkerFailure):
                        await worker
                        _raise_worker_failure(queue_item.error)
                    yield queue_item
            else:
                result = await asyncio.to_thread(gepa_entrypoint, **gepa_kwargs)
        except Exception as exc:
            yield OptimizationError(
                optimization_id=optimization.optimization_id,
                optimization_name=optimization.name,
                error=str(exc),
            )
            raise

        normalized = self._normalize_result(optimization=optimization, result=result)
        yield ParetoFrontUpdated(
            optimization_id=optimization.optimization_id,
            optimization_name=optimization.name,
            frontier_size=len(normalized.pareto_frontier),
            best_score=normalized.best_score,
        )
        yield OptimizationEnd(
            optimization_id=optimization.optimization_id,
            optimization_name=optimization.name,
            result=normalized,
            best_candidate=normalized.best_candidate,
            best_score=normalized.best_score,
            frontier_size=len(normalized.pareto_frontier),
            history_length=len(normalized.history),
        )

    def _import_gepa_modules(self) -> tuple[ModuleType, ModuleType, ModuleType]:
        try:
            optimize_module = importlib.import_module("gepa.optimize_anything")
            api_module = importlib.import_module("gepa.api")
            adapter_module = importlib.import_module("gepa.core.adapter")
        except ImportError as exc:
            raise OptimizationDependencyError(
                "GEPA support requires the 'gepa' package to be installed."
            ) from exc
        return optimize_module, api_module, adapter_module

    def _build_gepa_kwargs(
        self,
        *,
        optimization: Optimization[CandidateT],
        optimize_module: ModuleType,
        api_module: ModuleType,
        adapter_module: ModuleType,
    ) -> dict[str, t.Any]:
        if optimization.adapter is not None:
            return self._build_adapter_kwargs(
                optimization=optimization,
                api_module=api_module,
                adapter_module=adapter_module,
            )
        if optimization.evaluator is None:
            raise OptimizationBackendError("GEPA optimization requires an evaluator or an adapter.")

        kwargs: dict[str, t.Any] = {
            "seed_candidate": optimization.seed_candidate,
            "objective": optimization.objective,
            "background": optimization.background,
            "dataset": self._resolve_trainset(optimization),
            "valset": optimization.valset,
            "evaluator": self._build_evaluator(optimization),
        }
        config = self._build_gepa_config(optimize_module, optimization)
        if config is not None:
            kwargs["config"] = config
        return {key: value for key, value in kwargs.items() if value is not None}

    def _build_adapter_kwargs(
        self,
        *,
        optimization: Optimization[CandidateT],
        api_module: ModuleType,
        adapter_module: ModuleType,
    ) -> dict[str, t.Any]:
        if optimization.evaluator is not None:
            raise OptimizationBackendError(
                "GEPA adapter optimization does not accept a separate evaluator."
            )
        trainset = self._resolve_trainset(optimization)
        if trainset is None:
            raise OptimizationBackendError(
                "GEPA adapter optimization requires a dataset, trainset, or adapter.dataset."
            )
        if not isinstance(optimization.seed_candidate, dict):
            raise OptimizationBackendError(
                "GEPA adapter optimization requires a dict[str, str] seed_candidate."
            )

        unsupported = self._unsupported_adapter_settings(optimization)
        if unsupported:
            raise OptimizationBackendError(
                "GEPA adapter optimization does not support these Dreadnode settings yet: "
                + ", ".join(sorted(unsupported))
            )

        kwargs: dict[str, t.Any] = {
            "seed_candidate": dict(optimization.seed_candidate),
            "trainset": trainset,
            "valset": optimization.valset,
            "adapter": _GEPAAdapterBridge(
                adapter=optimization.adapter,
                evaluation_batch_cls=adapter_module.EvaluationBatch,
            ),
        }

        kwargs.update(
            self._select_kwargs(
                optimization.config.engine.to_gepa_kwargs(),
                supported_keys={
                    "run_dir",
                    "seed",
                    "display_progress_bar",
                    "raise_on_exception",
                    "use_cloudpickle",
                    "track_best_outputs",
                    "max_metric_calls",
                    "val_evaluation_policy",
                    "candidate_selection_strategy",
                    "frontier_type",
                    "cache_evaluation",
                },
            )
        )
        if optimization.config.reflection is not None:
            kwargs.update(optimization.config.reflection.to_gepa_kwargs())
        if optimization.config.merge is not None:
            kwargs["use_merge"] = True
            kwargs.update(optimization.config.merge.to_gepa_kwargs())
        kwargs.update(optimization.config.tracking.to_gepa_kwargs())
        if optimization.config.stop_callbacks is not None:
            kwargs["stop_callbacks"] = optimization.config.stop_callbacks

        # Keep the supported-key filtering explicit so GEPA API changes fail loudly.
        optimize_signature = inspect.signature(api_module.optimize)
        accepts_var_keyword = any(
            parameter.kind == inspect.Parameter.VAR_KEYWORD
            for parameter in optimize_signature.parameters.values()
        )
        unknown = sorted(set(kwargs) - set(optimize_signature.parameters))
        if unknown and not accepts_var_keyword:
            raise OptimizationBackendError(
                "GEPA adapter optimization produced unsupported keyword arguments: "
                + ", ".join(unknown)
            )
        return kwargs

    def _build_gepa_config(
        self,
        optimize_module: ModuleType,
        optimization: Optimization[CandidateT],
    ) -> t.Any:
        config_kwargs = dict(optimization.config.extra)

        engine_kwargs = optimization.config.engine.to_gepa_kwargs()
        if engine_kwargs:
            engine_cls = getattr(optimize_module, "EngineConfig", None)
            if engine_cls is not None:
                config_kwargs["engine"] = engine_cls(**engine_kwargs)

        reflection_cfg = optimization.config.reflection
        if reflection_cfg is not None:
            reflection_kwargs = reflection_cfg.to_gepa_kwargs()
            reflection_cls = getattr(optimize_module, "ReflectionConfig", None)
            if reflection_kwargs and reflection_cls is not None:
                config_kwargs["reflection"] = reflection_cls(**reflection_kwargs)

        tracking_cfg = optimization.config.tracking
        tracking_kwargs = tracking_cfg.to_gepa_kwargs()
        tracking_cls = getattr(optimize_module, "TrackingConfig", None)
        if tracking_kwargs and tracking_cls is not None:
            config_kwargs["tracking"] = tracking_cls(**tracking_kwargs)

        merge_cfg = optimization.config.merge
        if merge_cfg is not None:
            merge_kwargs = merge_cfg.to_gepa_kwargs()
            merge_cls = getattr(optimize_module, "MergeConfig", None)
            if merge_kwargs and merge_cls is not None:
                config_kwargs["merge"] = merge_cls(**merge_kwargs)

        refiner_cfg = optimization.config.refiner
        if refiner_cfg is not None:
            refiner_kwargs = refiner_cfg.to_gepa_kwargs()
            refiner_cls = getattr(optimize_module, "RefinerConfig", None)
            if refiner_kwargs and refiner_cls is not None:
                config_kwargs["refiner"] = refiner_cls(**refiner_kwargs)

        if optimization.config.stop_callbacks is not None:
            config_kwargs["stop_callbacks"] = optimization.config.stop_callbacks

        gepa_config_cls = getattr(optimize_module, "GEPAConfig", None)
        if gepa_config_cls is None or not config_kwargs:
            return None
        return gepa_config_cls(**config_kwargs)

    def _build_evaluator(
        self,
        optimization: Optimization[CandidateT],
    ) -> t.Callable[..., float | tuple[float, dict[str, t.Any]]]:
        evaluator = optimization.evaluator
        if evaluator is None:
            raise OptimizationBackendError("Missing evaluator for GEPA optimization.")

        def wrapped(candidate: CandidateT, *args: t.Any) -> float | tuple[float, dict[str, t.Any]]:
            result = invoke_with_supported_args(evaluator, candidate, *args)
            if inspect.isawaitable(result):
                result = asyncio.run(t.cast("t.Awaitable[t.Any]", result))
            evaluation = normalize_evaluation_result(t.cast("t.Any", result))
            if evaluation.score is None:
                raise OptimizationBackendError(
                    "Optimization evaluators must return a scalar score or named scores."
                )

            side_info = dict(evaluation.side_info)
            if evaluation.scores:
                side_info.setdefault("scores", evaluation.scores)
            if evaluation.evaluation_result is not None:
                side_info.setdefault("evaluation_result", evaluation.evaluation_result)
            if evaluation.traces is not None:
                side_info.setdefault("traces", evaluation.traces)
            if side_info:
                return evaluation.score, side_info
            return evaluation.score

        return wrapped

    def _normalize_result(
        self,
        *,
        optimization: Optimization[CandidateT],
        result: t.Any,
    ) -> OptimizationResult[CandidateT]:
        if hasattr(result, "candidates") and hasattr(result, "val_aggregate_scores"):
            candidates = list(getattr(result, "candidates", []) or [])
            aggregate_scores = list(getattr(result, "val_aggregate_scores", []) or [])
            best_idx = getattr(result, "best_idx", None)
            if not isinstance(best_idx, int):
                best_idx = (
                    max(range(len(aggregate_scores)), key=aggregate_scores.__getitem__)  # ty: ignore[no-matching-overload] - ty limitation with __getitem__ as key
                    if aggregate_scores
                    else 0
                )
            best_scores_by_idx = list(getattr(result, "val_aggregate_subscores", []) or [])
            frontier_indices = self._collect_frontier_indices(result)
            best_score = None
            if 0 <= best_idx < len(aggregate_scores):
                best_score = float(aggregate_scores[best_idx])
            best_scores = (
                dict(best_scores_by_idx[best_idx])
                if 0 <= best_idx < len(best_scores_by_idx)
                and isinstance(best_scores_by_idx[best_idx], Mapping)
                else {}
            )
            best_candidate = getattr(result, "best_candidate", None)
            if best_candidate is None and 0 <= best_idx < len(candidates):
                best_candidate = self._normalize_candidate(result, candidates[best_idx])
            metadata = {
                key: getattr(result, key)
                for key in (
                    "total_metric_calls",
                    "num_full_val_evals",
                    "run_dir",
                    "seed",
                    "objective_pareto_front",
                    "best_outputs_valset",
                )
                if hasattr(result, key) and getattr(result, key) is not None
            }
            discovery_eval_counts = getattr(result, "discovery_eval_counts", None)
            if discovery_eval_counts is not None:
                metadata["discovery_eval_counts"] = list(discovery_eval_counts)
            return OptimizationResult(
                backend="gepa",
                seed_candidate=optimization.seed_candidate,
                best_candidate=best_candidate,
                best_score=best_score,
                best_scores=best_scores,
                objective=optimization.objective,
                train_size=len(self._resolve_trainset(optimization) or []),
                val_size=len(optimization.valset or self._resolve_trainset(optimization) or []),
                pareto_frontier=[
                    self._normalize_candidate(result, candidates[idx])
                    for idx in frontier_indices
                    if 0 <= idx < len(candidates)
                ],
                history=[self._normalize_candidate(result, candidate) for candidate in candidates],
                metadata=metadata,
                raw_result=result,
            )

        best_candidate = getattr(result, "best_candidate", None)
        best_score = getattr(result, "best_score", None)
        pareto_frontier = list(getattr(result, "pareto_frontier", []) or [])
        history = list(getattr(result, "history", []) or [])

        metadata: dict[str, t.Any] = {}
        for field_name in ("best_score", "best_val_score", "total_metric_calls"):
            if hasattr(result, field_name):
                metadata[field_name] = getattr(result, field_name)

        return OptimizationResult(
            backend="gepa",
            seed_candidate=optimization.seed_candidate,
            best_candidate=best_candidate,
            best_score=float(best_score) if isinstance(best_score, int | float) else None,
            best_scores={},
            objective=optimization.objective,
            train_size=len(optimization.effective_dataset or []),
            val_size=len(optimization.valset or []),
            pareto_frontier=pareto_frontier,
            history=history,
            metadata=metadata,
            raw_result=result,
        )

    def _resolve_trainset(self, optimization: Optimization[CandidateT]) -> list[t.Any] | None:
        dataset = optimization.effective_dataset
        if dataset is not None:
            return dataset
        if optimization.adapter is None:
            return None
        adapter_dataset = getattr(optimization.adapter, "dataset", None)
        if adapter_dataset is None:
            return None
        return list(adapter_dataset)

    def _unsupported_adapter_settings(self, optimization: Optimization[CandidateT]) -> set[str]:
        unsupported: set[str] = set()
        default_engine = optimization.config.engine.__class__()
        for field_name in (
            "max_candidate_proposals",
            "parallel",
            "max_workers",
            "cache_evaluation_storage",
            "best_example_evals_k",
            "capture_stdio",
        ):
            if getattr(optimization.config.engine, field_name) != getattr(
                default_engine, field_name
            ):
                unsupported.add(f"engine.{field_name}")
        if optimization.background is not None:
            unsupported.add("background")
        if optimization.config.refiner is not None:
            unsupported.add("refiner")
        if optimization.config.extra:
            unsupported.add("config.extra")
        for section_name in ("engine", "reflection", "merge", "tracking"):
            section = getattr(optimization.config, section_name)
            if section is not None and getattr(section, "extra", {}):
                unsupported.add(f"{section_name}.extra")
        return unsupported

    def _select_kwargs(
        self,
        raw_kwargs: dict[str, t.Any],
        *,
        supported_keys: set[str],
    ) -> dict[str, t.Any]:
        return {
            key: value
            for key, value in raw_kwargs.items()
            if key in supported_keys and value is not None
        }

    def _collect_frontier_indices(self, result: t.Any) -> list[int]:
        frontier_indices: set[int] = set()
        per_val_instance = getattr(result, "per_val_instance_best_candidates", None)
        if isinstance(per_val_instance, Mapping):
            for indices in per_val_instance.values():
                frontier_indices.update(self._coerce_indices(indices))
        per_objective = getattr(result, "per_objective_best_candidates", None)
        if isinstance(per_objective, Mapping):
            for indices in per_objective.values():
                frontier_indices.update(self._coerce_indices(indices))
        if not frontier_indices and hasattr(result, "best_idx"):
            best_idx = result.best_idx
            if isinstance(best_idx, int):
                frontier_indices.add(best_idx)
        return sorted(frontier_indices)

    def _coerce_indices(self, values: object) -> set[int]:
        if not isinstance(values, Iterable):
            return set()
        return {value for value in values if isinstance(value, int)}

    def _normalize_candidate(self, result: t.Any, candidate: t.Any) -> t.Any:
        str_candidate_key = getattr(result, "_str_candidate_key", None)
        if (
            isinstance(candidate, Mapping)
            and isinstance(str_candidate_key, str)
            and str_candidate_key in candidate
        ):
            return candidate[str_candidate_key]
        return candidate
