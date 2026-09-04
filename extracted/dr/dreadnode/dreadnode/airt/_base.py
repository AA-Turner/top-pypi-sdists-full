"""Shared base class for the black-box traditional-ML attacks.

Extraction, membership inference, and evasion all probe a black-box predict API
through the same :class:`PredictionTargetSpec` contract, count their queries,
capture a sample of the (input -> prediction) pairs they send, emit a top-level
``study`` span, and enforce a query budget. This module factors that shared
plumbing into :class:`BlackBoxAttack` so each family only implements its own
algorithm and its own result-to-span mapping.

The base also provides ``_trace_step`` - a capped per-iteration span that records
the intermediate adversarial state (distance, best score, candidate label /
confidence, queries so far). Because we own the algorithm loop, every step of the
attack trajectory is visible in the platform's Traces tab, which is exactly what
off-the-shelf frameworks (ART, TextAttack) make hard to surface.
"""

import typing as t
from contextlib import nullcontext, suppress

import numpy as np

from dreadnode.airt.targets.prediction import (
    Prediction,
    PredictionTargetSpec,
    QueryInput,
    predict_many,
)


@t.runtime_checkable
class AttackResult(t.Protocol):
    """The common surface every attack result exposes so :meth:`BlackBoxAttack.run`
    can emit spans generically."""

    query_samples: list[dict[str, t.Any]]

    @property
    def best_score(self) -> float: ...

    @property
    def metrics_detail(self) -> dict[str, t.Any]: ...


def sample_input_preview(x: t.Any, n: int = 60) -> str:
    """A compact, display-safe preview of a queried input (text snippet or a few
    numeric features) for the finding's query sample table."""
    if isinstance(x, str):
        return x if len(x) <= n else x[:n] + "..."
    try:
        arr = np.asarray(x, dtype=np.float64).ravel()
    except Exception:
        return str(x)[:n]
    head = ", ".join(f"{v:.3g}" for v in arr[:6])
    return f"[{head}{', ...' if arr.size > 6 else ''}] ({arr.size}d)"


class BlackBoxAttack:
    """Base for a configured black-box attack against a predict API.

    Subclasses set :attr:`attack_domain` (`model_extraction` /
    `membership_inference` / `adversarial_ml`), a default goal, and implement
    :meth:`_attack_name`, :meth:`_execute`, and :meth:`_span_attributes`. The
    query counter, query-sample capture, phase/step tracing, and the top-level
    ``study`` span are shared here.
    """

    #: One of "model_extraction", "membership_inference", "adversarial_ml".
    attack_domain: str = ""
    default_goal: str = ""
    default_goal_category: str = ""

    def __init__(
        self,
        *,
        target: PredictionTargetSpec,
        modality: str = "tabular",
        max_queries: int = 500,
        max_iterations: int = 30,
        seed: int | None = None,
        airt_assessment_id: str | None = None,
        airt_target_model: str | None = None,
        airt_goal: str | None = None,
        airt_goal_category: str | None = None,
    ) -> None:
        self.target = target
        self.modality = modality
        self.max_queries = max_queries
        self.max_iterations = max_iterations
        self.rng = np.random.default_rng(seed)
        self.airt_assessment_id = airt_assessment_id
        self.airt_target_model = airt_target_model or target.name
        # Make the default goal target-aware so the same objective against
        # different models counts as distinct goals on the dashboard (e.g. evasion
        # of the fraud, digits, and sentiment classifiers = 3 goals, not 1). An
        # explicit airt_goal is respected verbatim; only the default is suffixed.
        self.airt_goal = airt_goal or (
            f"{self.default_goal} on {self.airt_target_model}"
            if self.airt_target_model
            else self.default_goal
        )
        self.airt_goal_category = airt_goal_category or self.default_goal_category
        self._query_count = 0
        #: A sample of real (input -> prediction) pairs so the finding can show
        #: the actual queries the attacker sent, not just the total count.
        self._query_samples: list[dict[str, t.Any]] = []
        #: Count of trial spans emitted this run. Each algorithm iteration is one
        #: trial (mirroring how a generative Study counts a trial per step), so the
        #: platform can count trials / incurred budget for traditional-ML attacks.
        self._trials_emitted = 0
        #: Hard safety cap on trial spans so a pathologically long loop cannot
        #: explode the trace tree.
        self._max_trial_spans = 1000

    # -- target I/O -------------------------------------------------------- #
    async def _query(self, xs: t.Sequence[QueryInput]) -> list[Prediction]:
        """Query the target, count the queries, and capture a sample."""
        preds = await predict_many(self.target, xs)
        self._query_count += len(xs)
        self._capture_samples(xs, preds)
        return preds

    def _capture_samples(
        self, xs: t.Sequence[QueryInput], preds: t.Sequence[Prediction], limit: int = 12
    ) -> None:
        for x, p in zip(xs, preds, strict=False):
            if len(self._query_samples) >= limit:
                return
            vec = p.vector
            conf = float(max(vec)) if vec is not None and len(vec) else None
            self._query_samples.append(
                {
                    "input": sample_input_preview(x),
                    "label": p.hard_label,
                    "confidence": round(conf, 4) if conf is not None else None,
                }
            )

    # -- budget ------------------------------------------------------------ #
    def _budget_left(self) -> int:
        return max(0, self.max_queries - self._query_count)

    def _over_budget(self) -> bool:
        return self._query_count >= self.max_queries

    # -- tracing ----------------------------------------------------------- #
    def _phase(self, name: str, **attrs: t.Any) -> t.Any:
        """A coarse task-span phase (e.g. 'perturb + probe target')."""
        try:
            import dreadnode as dn

            return dn.task_span(name, type="task", attributes={str(k): v for k, v in attrs.items()})
        except Exception:
            return nullcontext()

    def _trace_step(
        self,
        iteration: int,
        *,
        input: t.Any = None,
        output: t.Any = None,
        metrics: dict[str, float] | None = None,
        **attrs: t.Any,
    ) -> None:
        """Emit a **trial** span for one algorithm iteration, recording the
        intermediate adversarial state so the full attack trajectory is
        inspectable in the Traces tab and every iteration is counted as a trial.

        One iteration == one trial: this mirrors how a generative ``Study`` emits
        a trial span per refinement step, so the platform counts trials (and the
        incurred query budget) for traditional-ML attacks the same way. The span
        carries the AIRT assessment/attack attributes and is a child of the run's
        ``study`` span (opened in :meth:`run`), which is how ClickHouse links a
        trial to its assessment.

        ``input`` is the current candidate (perturbed text / feature vector /
        image preview) the attacker sent; ``output`` is the target's response at
        this step; ``metrics`` are the scalar signals (distance, confidence,
        fidelity) plotted over the run. The lightweight trial span is emitted
        every iteration; the heavier input/output previews are attached only for
        the first 20 iterations then every 10th, so a long run does not bloat the
        trace tree."""
        if self._trials_emitted >= self._max_trial_spans:
            return
        self._trials_emitted += 1
        heavy = iteration < 20 or iteration % 10 == 0
        with self._trial(iteration, **attrs) as span:
            if span is None or not hasattr(span, "log_metric"):
                return
            with suppress(Exception):
                for key, value in (metrics or {}).items():
                    span.log_metric(key, float(value), step=iteration)
                if heavy and input is not None and hasattr(span, "log_input"):
                    span.log_input("candidate", input)
                if heavy and output is not None and hasattr(span, "log_output"):
                    span.log_output("prediction", output)

    def _trial(self, iteration: int, **attrs: t.Any) -> t.Any:
        """Open a ``trial`` span for one iteration, tagged with the AIRT
        assessment/attack attributes so it is counted against this assessment."""
        try:
            from dreadnode.tracing.spans import trial_span

            ctx = trial_span(
                trial_id=f"{self._attack_name}-{iteration}-{self._trials_emitted}",
                step=int(iteration),
                airt_assessment_id=self.airt_assessment_id,
                airt_trial_index=int(iteration),
                airt_attack_name=self._attack_name,
                airt_attack_domain=self.attack_domain,
                airt_target_model=self.airt_target_model,
                airt_goal=self.airt_goal,
                airt_goal_category=self.airt_goal_category,
                airt_input_modality=self.modality,
            )
        except Exception:
            return nullcontext()
        if not attrs:
            return ctx
        # Fold any per-iteration attrs (e.g. distance norm) onto the span.
        from contextlib import contextmanager

        @contextmanager
        def _wrapped() -> t.Iterator[t.Any]:
            with ctx as span:
                if span is not None and hasattr(span, "set_attribute"):
                    with suppress(Exception):
                        for key, value in attrs.items():
                            span.set_attribute(str(key), value)
                yield span

        return _wrapped()

    # -- run scaffold ------------------------------------------------------ #
    @property
    def _attack_name(self) -> str:
        raise NotImplementedError

    def _study_kwargs(self) -> dict[str, t.Any]:
        """Extra ``study_span`` kwargs beyond the common set (e.g. distance norm)."""
        return {}

    def _span_attributes(self, result: t.Any) -> dict[str, t.Any]:
        """Map the result onto the ``AIRT_ATTRIBUTE_*`` span attributes to set.
        ``None`` values are skipped."""
        raise NotImplementedError

    async def _execute(self) -> t.Any:
        raise NotImplementedError

    async def run(self) -> t.Any:
        import json

        from dreadnode.tracing.constants import AIRT_ATTRIBUTE_METRICS_DETAIL
        from dreadnode.tracing.spans import study_span

        with study_span(
            name=self._attack_name,
            airt_assessment_id=self.airt_assessment_id,
            airt_attack_name=self._attack_name,
            airt_attack_domain=self.attack_domain,
            airt_target_model=self.airt_target_model,
            airt_input_modality=self.modality,
            airt_goal=self.airt_goal,
            airt_goal_category=self.airt_goal_category,
            **self._study_kwargs(),
        ) as span:
            result = await self._execute()
            if hasattr(result, "query_samples"):
                result.query_samples = self._query_samples
            for key, value in self._span_attributes(result).items():
                if value is not None:
                    span.set_attribute(key, value)
            span.set_attribute(AIRT_ATTRIBUTE_METRICS_DETAIL, json.dumps(result.metrics_detail))
        return result
