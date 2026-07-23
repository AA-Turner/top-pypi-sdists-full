"""Shared base for the model-evasion (adversarial-example) attacks.

Unlike the sampler-based image attacks in :mod:`dreadnode.airt.image` (which
operate on a local numeric array), these take a :class:`PredictionTargetSpec`
and probe the endpoint directly, so they share the exact target contract used by
the extraction and membership attacks and emit the same rich ``airt_*`` finding.

Each concrete algorithm lives in its own module under this package
(``boundary``, ``hopskipjump``, ``simba``, ``square``, ``zoo``, ``text``,
``deepwordbug``, ``textfooler``, ``pwws``, ``bae``, ``textbugger``) as a
``run(attack)`` coroutine plus a public factory function. :class:`ModelEvasionAttack`
holds the shared state (query counting, previews, image rendering, per-step
tracing, the result builder) and dispatches to the selected module's ``run``.

Each run reports the concrete evasion story an operator needs: did the label
flip (attack success), how far the input had to move (distance), the
original -> adversarial class, the query cost, a distance-vs-query convergence
curve, and previews of the original vs perturbed input.
"""

import typing as t
from dataclasses import dataclass, field

import numpy as np

from dreadnode.airt._base import BlackBoxAttack
from dreadnode.airt.targets.prediction import (
    Prediction,
    PredictionTargetSpec,
    QueryInput,
)

EvasionStrategy = t.Literal[
    "boundary",
    "hopskipjump",
    "simba",
    "square",
    "zoo",
    "text",
    "deepwordbug",
    "textfooler",
    "pwws",
    "bae",
    "textbugger",
]
DistanceNorm = t.Literal["l2", "linf", "tokens"]

#: Text strategies use a token-fraction distance; numeric strategies use L2/Linf.
_TEXT_STRATEGIES = frozenset({"text", "deepwordbug", "textfooler", "pwws", "bae", "textbugger"})


# --------------------------------------------------------------------------- #
# Result
# --------------------------------------------------------------------------- #
@dataclass
class EvasionResult:
    strategy: str
    success: bool
    original_class: int | str | None
    adversarial_class: int | str | None
    distance_norm: str
    distance_value: float
    #: Confidence the target assigns to the original class after perturbation
    #: (lower = more degraded); used to grade partial (degradation) results.
    residual_confidence: float
    query_count: int
    #: (query_index, best_distance_so_far) convergence curve for charting.
    distance_curve: list[tuple[int, float]]
    original_preview: str
    perturbed_preview: str
    #: For image modality: base64 PNG data URLs of the original and adversarial
    #: images, so the finding can show them side by side (None for text/tabular).
    original_image: str | None = None
    adversarial_image: str | None = None
    #: For text modality: how many tokens were changed and the total token count,
    #: so the finding can say "3 of 780 words changed" instead of a bare fraction.
    tokens_changed: int | None = None
    tokens_total: int | None = None
    #: A sample of real (input -> prediction) pairs from the perturbation probes.
    query_samples: list[dict[str, t.Any]] = field(default_factory=list)
    #: Full perturbation profile (standard adversarial-robustness metrics). For
    #: numeric inputs: L2 / Linf magnitude, L0 sparsity (how many features moved)
    #: and the perturbation-to-input ratio. For text: L0 is the tokens changed.
    l2_distance: float | None = None
    linf_distance: float | None = None
    l0_changed: int | None = None
    perturbation_ratio: float | None = None
    #: Text only: character-level edit distance (Levenshtein) between the original
    #: and adversarial text, and that distance normalised by the original length.
    #: L0 counts whole words changed; Levenshtein captures sub-word (typo) edits.
    levenshtein: int | None = None
    levenshtein_normalized: float | None = None

    @property
    def best_score(self) -> float:
        """Maps to the finding classifier: >=0.5 -> evasion, (0,0.5) -> degradation,
        0 -> robust. A flip is a full success; otherwise grade by how much the
        original-class confidence was driven down."""
        if self.success:
            return 1.0
        return round(max(0.0, min(0.49, 1.0 - self.residual_confidence)), 4)

    @property
    def metrics_detail(self) -> dict[str, t.Any]:
        return {
            "distance_curve": self.distance_curve,
            "distance_norm": self.distance_norm,
            "distance_value": round(self.distance_value, 6),
            "original_class": self.original_class,
            "adversarial_class": self.adversarial_class,
            "residual_confidence": round(self.residual_confidence, 4),
            "original_preview": self.original_preview,
            "perturbed_preview": self.perturbed_preview,
            "original_image": self.original_image,
            "adversarial_image": self.adversarial_image,
            "tokens_changed": self.tokens_changed,
            "tokens_total": self.tokens_total,
            "query_samples": self.query_samples,
            "l2_distance": self.l2_distance,
            "linf_distance": self.linf_distance,
            "l0_changed": self.l0_changed,
            "perturbation_ratio": self.perturbation_ratio,
            "levenshtein": self.levenshtein,
            "levenshtein_normalized": self.levenshtein_normalized,
        }


# --------------------------------------------------------------------------- #
# Attack
# --------------------------------------------------------------------------- #
class ModelEvasionAttack(BlackBoxAttack):
    """A configured evasion run. ``await attack.run()`` perturbs ``original``
    against the target until its prediction flips (or the query budget is spent)
    and returns an :class:`EvasionResult`."""

    attack_domain = "adversarial_ml"
    default_goal = "Flip the model's prediction with a minimal input perturbation"
    default_goal_category = "model_evasion"

    def __init__(
        self,
        *,
        target: PredictionTargetSpec,
        strategy: EvasionStrategy,
        original: QueryInput,
        num_classes: int | None = None,
        max_queries: int = 500,
        max_iterations: int = 30,
        norm: str = "l2",
        target_class: int | None = None,
        modality: str = "tabular",
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
        self.original = original
        self.num_classes = num_classes
        self.norm = "tokens" if strategy in _TEXT_STRATEGIES else norm
        self.target_class = target_class

    # -- target I/O helpers ------------------------------------------------- #
    async def _predict(self, xs: t.Sequence[QueryInput]) -> list[Prediction]:
        return await self._query(xs)

    def _img(self, x: np.ndarray) -> str | None:
        """A base64 PNG of ``x`` for image-modality runs, else None."""
        return _to_image_data_url(x) if self.modality == "image" else None

    def _label(self, pred: Prediction) -> int | str | None:
        return pred.hard_label

    def _orig_confidence(self, pred: Prediction, cls: int) -> float:
        vec = pred.vector
        if vec is not None and 0 <= cls < len(vec):
            return float(vec[cls])
        return 1.0 if pred.hard_label == cls else 0.0

    def _preview_vec(self, x: np.ndarray) -> str:
        """A compact preview of an intermediate feature vector for step traces."""
        return _preview(x)

    def _pred_summary(self, pred: Prediction) -> dict[str, t.Any]:
        """A compact (predicted_label, confidence) view of the target's response
        at one step, logged as the step span's output so the trajectory shows the
        target's evolving verdict, not just the attacker's candidate."""
        vec = pred.vector
        conf = float(max(vec)) if vec is not None and len(vec) else None
        return {
            "predicted_label": pred.hard_label,
            "confidence": round(conf, 4) if conf is not None else None,
        }

    # -- shared numeric plumbing ------------------------------------------- #
    def _numeric_result(
        self,
        x0: np.ndarray,
        best: np.ndarray,
        orig_label: t.Any,
        adv_label: t.Any,
        curve: list[tuple[int, float]],
        *,
        success: bool,
        residual: float = 0.0,
    ) -> EvasionResult:
        """Build an :class:`EvasionResult` from a numeric attack's final state -
        full L0/L2/Linf profile, previews and images. Shared by all numeric
        strategies so each algorithm only owns its search loop."""
        delta = best - x0
        dist = _dist(x0, best, self.norm) if success else 0.0
        return EvasionResult(
            strategy=self.strategy,
            success=success,
            original_class=orig_label,
            adversarial_class=adv_label if success else None,
            distance_norm=self.norm,
            distance_value=dist,
            residual_confidence=0.0 if success else float(residual),
            query_count=self._query_count,
            distance_curve=curve or [(self._query_count, dist)],
            original_preview=_preview(x0),
            perturbed_preview=_preview(best if success else x0),
            original_image=self._img(x0),
            adversarial_image=self._img(best if success else x0),
            l2_distance=float(np.linalg.norm(delta)) if success else 0.0,
            linf_distance=float(np.max(np.abs(delta))) if success else 0.0,
            l0_changed=int(np.count_nonzero(np.abs(delta) > 1e-9)) if success else 0,
            perturbation_ratio=round(float(np.linalg.norm(delta) / (np.linalg.norm(x0) + 1e-9)), 4)
            if success
            else 0.0,
        )

    async def _find_adversarial(
        self, x0: np.ndarray, orig_label: t.Any
    ) -> tuple[np.ndarray | None, t.Any]:
        """Find any adversarial point by growing isotropic Gaussian noise."""
        scale = 0.1 * (np.linalg.norm(x0) / np.sqrt(x0.size) + 1e-6)
        for _ in range(25):
            if self._over_budget():
                break
            cand = x0 + self.rng.normal(0, scale, x0.shape)
            p = (await self._predict([cand]))[0]
            if self._label(p) != orig_label and (
                self.target_class is None or self._label(p) == self.target_class
            ):
                return cand, self._label(p)
            scale *= 1.5
        return None, None

    def _numeric_setup(self, base: list[Prediction]) -> tuple[np.ndarray, t.Any, int]:
        x0 = np.asarray(self.original, dtype=np.float64).ravel()
        orig_label = self._label(base[0])
        orig_cls = int(orig_label) if isinstance(orig_label, (int, np.integer)) else 0
        return x0, orig_label, orig_cls

    # -- run scaffold ------------------------------------------------------- #
    @property
    def _attack_name(self) -> str:
        return f"{self.strategy}_evasion"

    def _study_kwargs(self) -> dict[str, t.Any]:
        return {"airt_distance_norm": self.norm}

    def _span_attributes(self, result: EvasionResult) -> dict[str, t.Any]:
        from dreadnode.tracing.constants import (
            AIRT_ATTRIBUTE_ADVERSARIAL_CLASS,
            AIRT_ATTRIBUTE_BEST_SCORE,
            AIRT_ATTRIBUTE_DISTANCE_NORM,
            AIRT_ATTRIBUTE_DISTANCE_VALUE,
            AIRT_ATTRIBUTE_IS_JAILBREAK,
            AIRT_ATTRIBUTE_ORIGINAL_CLASS,
            AIRT_ATTRIBUTE_QUERY_COUNT,
        )

        attrs: dict[str, t.Any] = {
            AIRT_ATTRIBUTE_BEST_SCORE: result.best_score,
            AIRT_ATTRIBUTE_IS_JAILBREAK: result.success,
            AIRT_ATTRIBUTE_DISTANCE_NORM: result.distance_norm,
            AIRT_ATTRIBUTE_DISTANCE_VALUE: float(result.distance_value),
            AIRT_ATTRIBUTE_QUERY_COUNT: result.query_count,
        }
        if result.original_class is not None:
            attrs[AIRT_ATTRIBUTE_ORIGINAL_CLASS] = str(result.original_class)
        if result.adversarial_class is not None:
            attrs[AIRT_ATTRIBUTE_ADVERSARIAL_CLASS] = str(result.adversarial_class)
        return attrs

    #: strategy -> the module under this package that implements it.
    _STRATEGY_MODULES: t.ClassVar[dict[str, str]] = {
        "boundary": "boundary",
        "hopskipjump": "hopskipjump",
        "simba": "simba",
        "square": "square",
        "zoo": "zoo",
        "text": "text",
        "deepwordbug": "deepwordbug",
        "textfooler": "textfooler",
        "pwws": "pwws",
        "bae": "bae",
        "textbugger": "textbugger",
    }

    async def _execute(self) -> EvasionResult:
        import importlib

        with self._phase("perturb + probe target", max_queries=self.max_queries):
            module = importlib.import_module(
                f"dreadnode.airt.evasion.{self._STRATEGY_MODULES[self.strategy]}"
            )
            return await module.run(self)


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #
def _dist(a: np.ndarray, b: np.ndarray, norm: str) -> float:
    d = b - a
    if norm == "linf":
        return float(np.max(np.abs(d)))
    return float(np.linalg.norm(d))


def levenshtein(a: str, b: str) -> int:
    """Character-level edit distance (insert / delete / substitute) between two
    strings. Complements the word-level L0 count for text evasion: L0 says how
    many words changed, Levenshtein says how many character edits it took."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _preview(x: np.ndarray, n: int = 8) -> str:
    vals = ", ".join(f"{v:.3g}" for v in x[:n])
    return f"[{vals}{', ...' if len(x) > n else ''}]"


def _trunc(text: str) -> str:
    """Return the full text - operators want the whole sample, not a snippet.
    Capped only against a pathological megabyte-scale input."""
    return text if len(text) <= 50_000 else text[:50_000] + "..."


def _to_image_data_url(x: np.ndarray) -> str | None:
    """Render a flat numeric vector as a grayscale PNG data URL, so the finding
    can display the actual image. Returns None when the vector is not a square
    (non-image) shape or PNG encoding is unavailable."""
    try:
        import base64
        import io
        import math

        from PIL import Image as _PILImage

        arr = np.asarray(x, dtype=np.float64).ravel()
        n = int(arr.size)
        # Guard: never inline a huge tensor into the finding JSON. Demo images
        # (8x8, 28x28) are tiny; anything past ~316x316 grayscale is stored by
        # reference upstream instead of embedded here.
        if n > 100_000:
            return None
        side = math.isqrt(n)
        if side < 2 or side * side != n:
            return None
        grid = arr.reshape(side, side)
        lo, hi = float(grid.min()), float(grid.max())
        norm = (grid - lo) / (hi - lo) if hi > lo else np.zeros_like(grid)
        img = _PILImage.fromarray((norm * 255.0).astype(np.uint8))
        # Upscale small demo images (8x8, 28x28) so they are viewable.
        scale = max(1, 192 // side)
        if scale > 1:
            img = img.resize((side * scale, side * scale), _PILImage.Resampling.NEAREST)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None
