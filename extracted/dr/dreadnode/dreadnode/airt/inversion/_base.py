"""Shared base for the model-inversion attacks.

Given only query access to a classifier's predict API, model inversion
reconstructs a representative input for each target class by optimizing an input
to maximize the target's confidence for that class - recovering what a class
"looks like" to the model (Fredrikson et al. 2015, "Model Inversion Attacks",
MI-Face). When classes correspond to individuals, this is a concrete privacy
leak. The search is purely black-box: no gradients from the model, only the
gradient-free query loop shared with the other traditional-ML families.

Each concrete strategy lives in its own module under this package
(``confidence``, ``nes_inversion``) as a ``run(attack)`` coroutine plus a public
factory function. :class:`ModelInversionAttack` holds the shared state (query
counting, previews, image rendering, per-step tracing) and dispatches to the
selected module's ``run``.
"""

import typing as t
from dataclasses import dataclass, field

import numpy as np

from dreadnode.airt._base import BlackBoxAttack
from dreadnode.airt.targets.prediction import (
    PredictionTargetSpec,
    QueryInput,
)

InversionStrategy = t.Literal["confidence", "nes"]


# --------------------------------------------------------------------------- #
# Result
# --------------------------------------------------------------------------- #
@dataclass
class InversionResult:
    strategy: str
    num_classes: int
    #: One entry per inverted class: {"class", "achieved_confidence", "queries",
    #: "reconstruction_preview", "reconstruction_image", "reference_similarity"}.
    per_class: list[dict[str, t.Any]]
    mean_confidence: float
    #: Classes whose reconstruction cleared the 0.5 confidence threshold.
    classes_reconstructed: int
    query_count: int
    #: Mean cosine similarity of each reconstruction to the closest reference input
    #: of its class (0..1). Only set when reference samples were supplied; this is
    #: the reconstruction-quality measure - how closely the recovered input matches
    #: a real member of the class, beyond just being confidently classified.
    mean_reference_similarity: float | None = None
    #: (query_index, best_mean_confidence_so_far) convergence curve for charting.
    reconstruction_curve: list[tuple[int, float]] = field(default_factory=list)
    #: A sample of real (input -> prediction) pairs from the reconstruction probes.
    query_samples: list[dict[str, t.Any]] = field(default_factory=list)

    @property
    def best_score(self) -> float:
        """Mean confidence achieved across inverted classes (0..1) - how strongly
        the reconstructions are recognised as their target class."""
        return round(float(self.mean_confidence), 4)

    @property
    def metrics_detail(self) -> dict[str, t.Any]:
        detail: dict[str, t.Any] = {
            "per_class": self.per_class,
            "mean_confidence": round(self.mean_confidence, 4),
            "classes_reconstructed": self.classes_reconstructed,
            "reconstruction_curve": self.reconstruction_curve,
            "query_samples": self.query_samples,
        }
        if self.mean_reference_similarity is not None:
            detail["mean_reference_similarity"] = round(self.mean_reference_similarity, 4)
        return detail


# --------------------------------------------------------------------------- #
# Attack
# --------------------------------------------------------------------------- #
class ModelInversionAttack(BlackBoxAttack):
    """A configured model-inversion run. ``await attack.run()`` reconstructs a
    representative input for each target class by maximizing the target's
    confidence for that class, and returns an :class:`InversionResult`."""

    attack_domain = "model_inversion"
    default_goal = "Reconstruct a representative training input for each class"
    default_goal_category = "model_inversion"

    def __init__(
        self,
        *,
        target: PredictionTargetSpec,
        strategy: InversionStrategy,
        num_classes: int,
        input_dim: int | None = None,
        input_shape: tuple[int, ...] | None = None,
        target_classes: t.Sequence[int] | None = None,
        reference_inputs: t.Mapping[int, t.Sequence[QueryInput]] | None = None,
        modality: str = "tabular",
        max_queries: int = 800,
        max_iterations: int = 40,
        seed: int | None = None,
        airt_assessment_id: str | None = None,
        airt_target_model: str | None = None,
        airt_goal: str | None = None,
        airt_goal_category: str | None = None,
    ) -> None:
        super().__init__(
            target=target,
            modality=modality,
            max_queries=max_queries,
            max_iterations=max_iterations,
            seed=seed,
            airt_assessment_id=airt_assessment_id,
            airt_target_model=airt_target_model,
            airt_goal=airt_goal,
            airt_goal_category=airt_goal_category,
        )
        self.strategy = strategy
        self.num_classes = num_classes
        # input_dim = feature-vector length; inferred from input_shape when omitted.
        self.input_dim = input_dim if input_dim is not None else self._dim_from_shape(input_shape)
        self.input_shape = input_shape
        self.target_classes = (
            list(target_classes) if target_classes is not None else list(range(num_classes))
        )
        self.reference_inputs = (
            {
                int(c): [np.asarray(r, dtype=np.float64).ravel() for r in refs]
                for c, refs in reference_inputs.items()
            }
            if reference_inputs is not None
            else None
        )

    @staticmethod
    def _dim_from_shape(shape: tuple[int, ...] | None) -> int | None:
        if not shape:
            return None
        dim = 1
        for s in shape:
            dim *= int(s)
        return dim

    # -- reconstruction helpers -------------------------------------------- #
    def _effective_dim(self) -> int:
        """Feature-vector length to optimize over. Falls back to a reference
        input's length when ``input_dim`` was not supplied."""
        if self.input_dim is not None:
            return int(self.input_dim)
        if self.reference_inputs:
            for refs in self.reference_inputs.values():
                if refs:
                    return int(refs[0].size)
        raise ValueError("input_dim (or input_shape / reference_inputs) is required")

    def _neutral_input(self, cls: int) -> np.ndarray:
        """Starting reconstruction for a class: the mean of that class's reference
        inputs when provided, else a zero vector."""
        dim = self._effective_dim()
        if self.reference_inputs and self.reference_inputs.get(cls):
            return np.mean(np.stack(self.reference_inputs[cls]), axis=0).astype(np.float64)
        return np.zeros(dim, dtype=np.float64)

    def _class_confidence(self, vec: t.Sequence[float] | None, cls: int) -> float:
        """Confidence the target assigns to ``cls`` (probability vector entry)."""
        if vec is not None and 0 <= cls < len(vec):
            return float(vec[cls])
        return 0.0

    def _reconstruction_image(self, x: np.ndarray) -> str | None:
        """A base64 PNG of ``x`` for image-modality runs, else None."""
        if self.modality != "image":
            return None
        from dreadnode.airt.evasion._base import _to_image_data_url

        return _to_image_data_url(x)

    def _reference_similarity(self, x: np.ndarray, cls: int) -> float | None:
        """Cosine similarity of ``x`` to the closest reference input of ``cls``,
        or None when no references are provided."""
        if not self.reference_inputs or not self.reference_inputs.get(cls):
            return None
        best = -1.0
        for ref in self.reference_inputs[cls]:
            if ref.size != x.size:
                continue
            denom = float(np.linalg.norm(x) * np.linalg.norm(ref))
            if denom == 0.0:
                continue
            sim = float(np.dot(x, ref) / denom)
            best = max(best, sim)
        return round(best, 4) if best > -1.0 else None

    def _preview(self, x: np.ndarray, n: int = 8) -> str:
        """A compact preview of a reconstruction vector for step traces / findings."""
        vals = ", ".join(f"{v:.3g}" for v in x[:n])
        return f"[{vals}{', ...' if len(x) > n else ''}]"

    # -- run scaffold ------------------------------------------------------ #
    @property
    def _attack_name(self) -> str:
        return f"{self.strategy}_inversion"

    def _span_attributes(self, result: InversionResult) -> dict[str, t.Any]:
        from dreadnode.tracing.constants import (
            AIRT_ATTRIBUTE_BEST_SCORE,
            AIRT_ATTRIBUTE_INPUT_MODALITY,
            AIRT_ATTRIBUTE_QUERY_COUNT,
        )

        return {
            AIRT_ATTRIBUTE_BEST_SCORE: result.best_score,
            AIRT_ATTRIBUTE_QUERY_COUNT: result.query_count,
            AIRT_ATTRIBUTE_INPUT_MODALITY: self.modality,
        }

    #: strategy -> the module under this package that implements it.
    _STRATEGY_MODULES: t.ClassVar[dict[str, str]] = {
        "confidence": "confidence",
        "nes": "nes_inversion",
    }

    async def _execute(self) -> InversionResult:
        import importlib

        with self._phase("reconstruct + probe target", max_queries=self.max_queries):
            module = importlib.import_module(
                f"dreadnode.airt.inversion.{self._STRATEGY_MODULES[self.strategy]}"
            )
            return await module.run(self)


# --------------------------------------------------------------------------- #
# Shared result builder
# --------------------------------------------------------------------------- #
def build_inversion_result(
    attack: ModelInversionAttack,
    per_class: list[dict[str, t.Any]],
    curve: list[tuple[int, float]],
) -> InversionResult:
    """Roll per-class reconstructions up into an :class:`InversionResult` (mean
    confidence, count above the 0.5 threshold, query count)."""
    confidences = [float(entry["achieved_confidence"]) for entry in per_class]
    mean_conf = float(np.mean(confidences)) if confidences else 0.0
    reconstructed = sum(1 for c in confidences if c >= 0.5)
    sims = [
        float(entry["reference_similarity"])
        for entry in per_class
        if entry.get("reference_similarity") is not None
    ]
    mean_ref_sim = float(np.mean(sims)) if sims else None
    return InversionResult(
        strategy=attack.strategy,
        num_classes=attack.num_classes,
        per_class=per_class,
        mean_confidence=mean_conf,
        classes_reconstructed=reconstructed,
        query_count=attack._query_count,
        mean_reference_similarity=mean_ref_sim,
        reconstruction_curve=curve,
        query_samples=attack._query_samples,
    )
