"""Shared base for the model-extraction attacks against a black-box predict API.

Each attack runs a *query campaign* against a :class:`PredictionTargetSpec`, trains a
surrogate that replicates the target's decision boundary, and reports how faithfully
the surrogate reproduces the target (fidelity / agreement) for the queries spent.

Unlike the evasion samplers (which optimise one input against a scalar objective),
extraction collects ``(input, output)`` pairs and fits a model - so these are attack
*functions*, not samplers. They still emit an ``airt_*`` summary span so the platform
ingests them exactly like every other AIRT attack.

Each concrete algorithm lives in its own module under this package
(``equation_solving``, ``jacobian``, ``copycat``, ``knockoff``, ``activethief``,
``distillation``) as a ``run(attack)`` coroutine plus a public factory function.
:class:`ModelExtractionAttack` holds the shared state (pool prep, featurisation,
query counting, surrogate fitting, per-step tracing, the result builder) and
dispatches to the selected module's ``run``.

The tabular/text surrogates use scikit-learn; the image soft-label surrogate uses
torch and is import-guarded (only loaded when ``surrogate="torch_mlp"``).
"""

import typing as t
from dataclasses import dataclass, field

import numpy as np
from loguru import logger

from dreadnode.airt._base import BlackBoxAttack
from dreadnode.airt.targets.prediction import (
    Prediction,
    PredictionTargetSpec,
    QueryInput,
)

ExtractionStrategy = t.Literal[
    "equation_solving", "jacobian", "copycat", "knockoff", "activethief", "distillation"
]
SurrogateName = t.Literal["auto", "logistic", "random_forest", "mlp", "torch_mlp"]
#: Which surrogate engine to use. "auto" prefers ART's CopycatCNN/KnockoffNets
#: when the library is installed (copycat/knockoff only), else the native engine.
ExtractionEngine = t.Literal["auto", "native", "art"]

#: A pool of query inputs, or a zero-arg callable returning one.
QueryPool = t.Sequence[QueryInput] | t.Callable[[], t.Sequence[QueryInput]]


# --------------------------------------------------------------------------- #
# Pure metric helpers (no I/O - unit-tested directly)
# --------------------------------------------------------------------------- #
def predictions_to_labels(preds: t.Sequence[Prediction]) -> np.ndarray:
    return np.array([p.hard_label for p in preds])


def predictions_to_proba(preds: t.Sequence[Prediction], num_classes: int) -> np.ndarray:
    """Stack soft vectors into an ``(n, num_classes)`` array, one-hotting hard labels
    when a prediction has no soft output."""
    rows: list[list[float]] = []
    for p in preds:
        vec = p.vector
        if vec is not None and len(vec) == num_classes:
            rows.append([float(v) for v in vec])
        else:
            one_hot = [0.0] * num_classes
            label = p.hard_label
            if isinstance(label, (int, np.integer)) and 0 <= int(label) < num_classes:
                one_hot[int(label)] = 1.0
            rows.append(one_hot)
    return np.asarray(rows, dtype=np.float64)


def top1_fidelity(surrogate_labels: np.ndarray, target_labels: np.ndarray) -> float:
    """Fraction of eval points where surrogate and target agree on the top-1 label."""
    if len(target_labels) == 0:
        return 0.0
    return float(np.mean(surrogate_labels == target_labels))


def soft_fidelity(surrogate_proba: np.ndarray, target_proba: np.ndarray) -> float:
    """1 - mean total-variation distance between the two probability vectors (0..1)."""
    if surrogate_proba.size == 0:
        return 0.0
    tv = 0.5 * np.sum(np.abs(surrogate_proba - target_proba), axis=1)
    return float(1.0 - np.mean(tv))


def kl_divergence(surrogate_proba: np.ndarray, target_proba: np.ndarray) -> float:
    """Mean KL(target || surrogate) over the eval set, in nats. Zero means the
    surrogate reproduces the target's confidence distribution exactly; larger
    values mean the labels may match while the calibration diverges."""
    if surrogate_proba.size == 0:
        return 0.0
    eps = 1e-12
    p = np.clip(target_proba, eps, 1.0)
    q = np.clip(surrogate_proba, eps, 1.0)
    per_row = np.sum(p * np.log(p / q), axis=1)
    return float(np.mean(per_row))


def per_class_fidelity(surrogate_labels: np.ndarray, target_labels: np.ndarray) -> dict[str, float]:
    """Top-1 agreement restricted to eval points the *target* assigns to each class."""
    out: dict[str, float] = {}
    for c in np.unique(target_labels):
        mask = target_labels == c
        if mask.any():
            out[str(c)] = float(np.mean(surrogate_labels[mask] == target_labels[mask]))
    return out


# --------------------------------------------------------------------------- #
# Surrogate models - a uniform predict_label / predict_proba interface over
# sklearn classifiers, sklearn soft-label regressors, and a linear (equation-
# solving) recovery.
# --------------------------------------------------------------------------- #
@dataclass
class _Surrogate:
    kind: str  # "classifier" | "soft" | "linear"
    name: str
    classes: np.ndarray
    estimator: t.Any = None
    weights: np.ndarray | None = None  # linear: (n_features + 1, n_classes)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        x = np.atleast_2d(x)
        if self.kind == "classifier":
            proba = self.estimator.predict_proba(x)
            return _align_proba(proba, self.estimator.classes_, self.classes)
        if self.kind == "soft":
            raw = np.atleast_2d(self.estimator.predict(x)).astype(np.float64)
            raw = np.clip(raw, 0.0, None)
            sums = raw.sum(axis=1, keepdims=True)
            sums[sums == 0] = 1.0
            return raw / sums
        if self.kind == "torch":
            import torch

            with torch.no_grad():
                logits = self.estimator(torch.tensor(x, dtype=torch.float32))
                return torch.softmax(logits, dim=1).cpu().numpy().astype(np.float64)
        if self.kind == "art":
            # ART's PyTorchClassifier.predict returns the model's raw outputs
            # (logits here - the thieved net ends in a Linear layer). Normalise to
            # a probability simplex so soft-fidelity / TV distance are well-defined.
            raw = np.asarray(
                self.estimator.predict(np.ascontiguousarray(x, dtype=np.float32)),
                dtype=np.float64,
            )
            row_sums = raw.sum(axis=1)
            already_proba = np.all(raw >= 0) and np.allclose(row_sums, 1.0, atol=1e-3)
            if already_proba:
                return raw
            raw = raw - raw.max(axis=1, keepdims=True)
            exp = np.exp(raw)
            return exp / exp.sum(axis=1, keepdims=True)
        # linear: softmax over x.W (+bias row)
        assert self.weights is not None
        logits = np.hstack([x, np.ones((x.shape[0], 1))]) @ self.weights
        logits -= logits.max(axis=1, keepdims=True)
        exp = np.exp(logits)
        return exp / exp.sum(axis=1, keepdims=True)

    def predict_label(self, x: np.ndarray) -> np.ndarray:
        return self.classes[np.argmax(self.predict_proba(x), axis=1)]


def _align_proba(proba: np.ndarray, est_classes: np.ndarray, classes: np.ndarray) -> np.ndarray:
    """Reindex an estimator's predict_proba columns onto the target's full class list."""
    out = np.zeros((proba.shape[0], len(classes)))
    index = {c: i for i, c in enumerate(classes)}
    for j, c in enumerate(est_classes):
        if c in index:
            out[:, index[c]] = proba[:, j]
    return out


def _sklearn_classifier(name: str) -> t.Any:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neural_network import MLPClassifier

    if name == "logistic":
        return LogisticRegression(max_iter=1000)
    if name == "mlp":
        return MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=0)
    return RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=0)


def _sklearn_regressor(name: str) -> t.Any:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.neural_network import MLPRegressor

    if name == "logistic":
        return Ridge()
    if name == "mlp":
        return MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=0)
    return RandomForestRegressor(n_estimators=200, n_jobs=-1, random_state=0)


def _resolve_surrogate(name: SurrogateName, modality: str) -> str:
    if name != "auto":
        return name
    if modality == "image":
        return "torch_mlp"
    if modality == "tabular":
        return "random_forest"
    return "logistic"  # text (TF-IDF is applied upstream) and default


def _fit_hard(x: np.ndarray, y: np.ndarray, name: str, classes: np.ndarray) -> _Surrogate:
    if name == "torch_mlp":
        onehot = np.eye(len(classes))[np.searchsorted(classes, y)]
        return _fit_torch_mlp(x, onehot, classes)
    est = _sklearn_classifier(name)
    est.fit(x, y)
    return _Surrogate(kind="classifier", name=name, classes=classes, estimator=est)


def _fit_soft(x: np.ndarray, proba: np.ndarray, name: str, classes: np.ndarray) -> _Surrogate:
    if name == "torch_mlp":
        return _fit_torch_mlp(x, proba, classes)
    est = _sklearn_regressor(name)
    est.fit(x, proba)
    return _Surrogate(kind="soft", name=name, classes=classes, estimator=est)


def _fit_torch_mlp(
    x: np.ndarray, target_proba: np.ndarray, classes: np.ndarray, *, epochs: int = 200
) -> _Surrogate:
    """Soft-label MLP surrogate trained with torch (image path). Distils the target's
    probability vectors via KL divergence. Falls back to the sklearn MLP if torch is
    unavailable so the attack still runs."""
    try:
        import torch
        from torch import nn
    except ImportError:
        logger.warning("torch unavailable - falling back to sklearn MLP surrogate")
        est = _sklearn_regressor("mlp")
        est.fit(x, target_proba)
        return _Surrogate(kind="soft", name="mlp", classes=classes, estimator=est)

    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(x.shape[1], 128), nn.ReLU(), nn.Linear(128, len(classes)))
    xt = torch.tensor(x, dtype=torch.float32)
    yt = torch.tensor(target_proba, dtype=torch.float32)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(epochs):
        opt.zero_grad()
        loss = nn.functional.kl_div(
            nn.functional.log_softmax(model(xt), dim=1), yt, reduction="batchmean"
        )
        loss.backward()
        opt.step()
    model.eval()
    return _Surrogate(kind="torch", name="torch_mlp", classes=classes, estimator=model)


def _fit_linear(x: np.ndarray, proba: np.ndarray, classes: np.ndarray) -> _Surrogate:
    """Recover a linear model by least-squares inversion of the softmax (Tramèr'16).

    Solves ``[X | 1] . W = log(p)`` per class; exact when the target is linear."""
    log_p = np.log(np.clip(proba, 1e-9, 1.0))
    design = np.hstack([x, np.ones((x.shape[0], 1))])
    weights, *_ = np.linalg.lstsq(design, log_p, rcond=None)
    return _Surrogate(kind="linear", name="linear", classes=classes, weights=weights)


def _numeric_gradient_sign(surrogate: _Surrogate, x: np.ndarray, eps: float = 1e-2) -> np.ndarray:
    """Finite-difference sign of the top-class probability wrt each feature - the
    surrogate's Jacobian direction, used for augmentation and transfer crafting."""
    x = np.atleast_2d(x)
    base = surrogate.predict_proba(x)
    top = np.argmax(base, axis=1)
    grad = np.zeros_like(x)
    for j in range(x.shape[1]):
        bumped = x.copy()
        bumped[:, j] += eps
        p = surrogate.predict_proba(bumped)
        grad[:, j] = (p[np.arange(len(x)), top] - base[np.arange(len(x)), top]) / eps
    return np.sign(grad)


# --------------------------------------------------------------------------- #
# Result
# --------------------------------------------------------------------------- #
@dataclass
class ExtractionResult:
    strategy: str
    surrogate_model: str
    fidelity: float
    soft_fidelity: float
    agreement_rate: float
    surrogate_accuracy: float | None
    transfer_success: float | None
    query_count: int
    query_budget: int
    per_class_fidelity: dict[str, float]
    fidelity_vs_budget: list[tuple[int, float]]
    #: Mean KL(target || surrogate) over the eval set. Low means the surrogate
    #: matched the target's confidence, not just its labels.
    kl_divergence: float = 0.0
    #: Target accuracy on the labeled eval set, and surrogate/target ratio. Only
    #: set when ground-truth labels were supplied.
    target_accuracy: float | None = None
    accuracy_ratio: float | None = None
    surrogate: _Surrogate | None = field(default=None, repr=False)
    #: Set when export_model=True and the surrogate was pushed to Hub Models.
    hub_model: dict[str, t.Any] | None = None
    #: A sample of real (input -> prediction) pairs from the query campaign.
    query_samples: list[dict[str, t.Any]] = field(default_factory=list)

    @property
    def metrics_detail(self) -> dict[str, t.Any]:
        detail: dict[str, t.Any] = {
            "per_class_fidelity": self.per_class_fidelity,
            "fidelity_vs_budget": self.fidelity_vs_budget,
            "soft_fidelity": round(self.soft_fidelity, 4),
            # A surrogate was trained in memory to measure fidelity; it is only
            # saved to Hub Models when export_model=True. The finding uses these
            # flags to tell "cloned but not saved" from "cloned and downloadable".
            "surrogate_trained": self.surrogate is not None,
            "exported": self.hub_model is not None,
            "kl_divergence": round(self.kl_divergence, 4),
        }
        if self.surrogate_accuracy is not None:
            detail["surrogate_accuracy"] = round(self.surrogate_accuracy, 4)
        if self.target_accuracy is not None:
            detail["target_accuracy"] = round(self.target_accuracy, 4)
        if self.accuracy_ratio is not None:
            detail["accuracy_ratio"] = round(self.accuracy_ratio, 4)
        if self.hub_model is not None:
            detail["hub_model"] = self.hub_model
        if self.query_samples:
            detail["query_samples"] = self.query_samples
        return detail


# --------------------------------------------------------------------------- #
# Campaign context - the shared state a strategy's run() fills in.
# --------------------------------------------------------------------------- #
@dataclass
class _Campaign:
    """The prepared query campaign a strategy's ``run`` consumes: the shuffled
    train pool, the featurised eval probe, the target's eval labels/proba, the
    class list, and the training query budget (net of the eval probe)."""

    pool: list[t.Any]
    eval_raw: list[t.Any]
    eval_feat: np.ndarray
    target_eval_labels: np.ndarray
    target_eval_proba: np.ndarray
    classes: np.ndarray
    train_raw: list[t.Any]
    train_budget: int
    eval_probe_queries: int


# --------------------------------------------------------------------------- #
# Attack
# --------------------------------------------------------------------------- #
class ModelExtractionAttack(BlackBoxAttack):
    """A configured extraction run. ``await attack.run()`` executes the query
    campaign, fits the surrogate, and returns an :class:`ExtractionResult`."""

    attack_domain = "model_extraction"
    default_goal = "Steal the model's decision boundary via black-box queries"
    default_goal_category = "model_extraction"

    #: strategy -> the module under this package that implements it.
    _STRATEGY_MODULES: t.ClassVar[dict[str, str]] = {
        "equation_solving": "equation_solving",
        "jacobian": "jacobian",
        "copycat": "copycat",
        "knockoff": "knockoff",
        "activethief": "activethief",
        "distillation": "distillation",
    }

    def __init__(
        self,
        *,
        target: PredictionTargetSpec,
        strategy: ExtractionStrategy,
        query_pool: QueryPool,
        eval_pool: t.Sequence[QueryInput] | None = None,
        ground_truth: t.Sequence[int] | None = None,
        surrogate: SurrogateName = "auto",
        query_budget: int = 5000,
        num_classes: int | None = None,
        jacobian_rounds: int = 5,
        jacobian_lambda: float = 0.1,
        measure_transfer: bool = True,
        modality: str = "tabular",
        engine: ExtractionEngine = "auto",
        export_model: bool = True,
        featurizer: t.Callable[[list[t.Any]], t.Any] | None = None,
        seed: int | None = None,
        airt_assessment_id: str | None = None,
        airt_target_model: str | None = None,
        airt_goal: str | None = None,
        airt_goal_category: str | None = None,
    ) -> None:
        super().__init__(
            target=target,
            modality=modality,
            max_queries=query_budget,
            seed=seed,
            airt_assessment_id=airt_assessment_id,
            airt_target_model=airt_target_model,
            airt_goal=airt_goal,
            airt_goal_category=airt_goal_category,
        )
        self.strategy = strategy
        self.query_pool = query_pool
        self.eval_pool = eval_pool
        self.ground_truth = ground_truth
        self.surrogate_name = _resolve_surrogate(surrogate, modality)
        self.query_budget = query_budget
        self.num_classes = num_classes
        self.jacobian_rounds = jacobian_rounds
        self.jacobian_lambda = jacobian_lambda
        self.measure_transfer = measure_transfer
        self.engine = engine
        self.export_model = export_model
        self.featurizer = featurizer

    def _raw_pool(self) -> list[t.Any]:
        src = self.query_pool
        if callable(src):
            factory = t.cast("t.Callable[[], t.Sequence[QueryInput]]", src)
            return list(factory())
        return list(src)

    def _ensure_featurizer(self, corpus: list[t.Any]) -> None:
        """For text targets with no explicit featurizer, fit a TF-IDF vectorizer on the
        query corpus so the surrogate trains on numeric features while the target is
        still queried with raw text."""
        if self.featurizer is None and self.modality == "text":
            from sklearn.feature_extraction.text import TfidfVectorizer

            vec = TfidfVectorizer(max_features=2000).fit([str(t) for t in corpus])
            self.featurizer = lambda items: vec.transform([str(t) for t in items]).toarray()

    def _feat(self, items: t.Sequence[t.Any]) -> np.ndarray:
        """Map raw query items to a numeric feature matrix for the surrogate. Identity
        (flatten) for numeric inputs; the fitted featurizer for text/custom inputs."""
        if self.featurizer is not None:
            return np.asarray(self.featurizer(list(items)), dtype=np.float64)
        return np.asarray([np.asarray(x, dtype=np.float64).ravel() for x in items])

    @property
    def _numeric(self) -> bool:
        """True when raw inputs are already the surrogate's feature space (tabular/
        image-vector) - required for Jacobian augmentation and transfer crafting."""
        return self.featurizer is None

    # -- surrogate fitting per strategy ------------------------------------ #
    async def _query_soft(self, xs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Query the target for a batch, returning (proba, labels). Counts queries."""
        preds = await self._query(list(xs))
        assert self.num_classes is not None
        return predictions_to_proba(preds, self.num_classes), predictions_to_labels(preds)

    def _build_surrogate(
        self,
        x: np.ndarray,
        proba: np.ndarray,
        labels: np.ndarray,
        classes: np.ndarray,
        *,
        prefer_art: bool = True,
    ) -> _Surrogate:
        """Fit a surrogate from *already-queried* data (no target I/O).

        For ``copycat``/``knockoff`` the ART engine (CopycatCNN/KnockoffNets) is
        used when available and ``engine`` allows it, falling back to the native
        fit otherwise. ``prefer_art=False`` forces the native fit - used for the
        fidelity-vs-budget curve, whose many prefix refits stay cheap.
        """
        if (
            prefer_art
            and self.strategy in ("copycat", "knockoff")
            and self.engine in ("auto", "art")
        ):
            from dreadnode.airt.art_engine import art_extract_surrogate

            art_clf = art_extract_surrogate(self.strategy, x, proba, len(classes))
            if art_clf is not None:
                return _Surrogate(
                    kind="art",
                    name=f"art_{self.strategy}",
                    classes=classes,
                    estimator=art_clf,
                )
            if self.engine == "art":
                raise RuntimeError(
                    f"engine='art' requested but ART extraction failed for {self.strategy}"
                )
        if self.strategy == "copycat":
            return _fit_hard(x, labels, self.surrogate_name, classes)
        if self.strategy == "equation_solving":
            return _fit_linear(x, proba, classes)
        # knockoff / distillation (and jacobian's inner fit) train on soft labels
        return _fit_soft(x, proba, self.surrogate_name, classes)

    # -- campaign scaffold (shared by every strategy) ---------------------- #
    async def _prepare_campaign(self) -> _Campaign:
        """Set up the query campaign: shuffle + split into eval/train, fit the text
        featurizer, probe the target to establish the class list, and reserve the
        training budget. Shared by every strategy so each ``run`` only owns its own
        query + fit loop."""
        pool = self._raw_pool()
        eval_raw = list(self.eval_pool) if self.eval_pool is not None else None
        if eval_raw is None:
            # Shuffle before the eval/train split: real query pools are often
            # grouped by class, and an unshuffled 20% head can be a single-class
            # eval set that makes fidelity meaningless (and collapses the fit).
            order = self.rng.permutation(len(pool))
            pool = [pool[i] for i in order]
            # Cap the eval set at ~20% of the query budget so a large pool cannot
            # starve the training queries (a 2000-input pool would otherwise spend
            # the whole budget on the 400-input eval probe, breaking activethief).
            split = max(1, min(int(0.2 * len(pool)), max(2, self.query_budget // 5)))
            eval_raw, pool = pool[:split], pool[split:]

        # Fit the featurizer (text) on the full query corpus before any surrogate fit.
        self._ensure_featurizer(pool + eval_raw)

        # Establish the class list from a small probe of the target.
        probe = await self._query(eval_raw)
        if self.num_classes is None:
            vec = next((p.vector for p in probe if p.vector is not None), None)
            self.num_classes = len(vec) if vec else int(np.max(predictions_to_labels(probe)) + 1)
        classes = np.arange(self.num_classes)
        target_eval_labels = predictions_to_labels(probe)
        target_eval_proba = predictions_to_proba(probe, self.num_classes)
        eval_feat = self._feat(eval_raw)

        # Budget the training queries (reserve what the eval probe already spent).
        train_budget = max(1, self.query_budget - self._query_count)
        train_raw = pool[:train_budget]
        return _Campaign(
            pool=pool,
            eval_raw=eval_raw,
            eval_feat=eval_feat,
            target_eval_labels=target_eval_labels,
            target_eval_proba=target_eval_proba,
            classes=classes,
            train_raw=train_raw,
            train_budget=train_budget,
            eval_probe_queries=self._query_count,  # queries spent before training
        )

    async def _finalize(
        self,
        campaign: _Campaign,
        surrogate: _Surrogate,
        budget_curve: list[tuple[int, float]],
    ) -> ExtractionResult:
        """Evaluate fidelity, build the :class:`ExtractionResult`, measure transfer,
        and export the surrogate to Hub Models when it worked. Shared by every
        strategy so each ``run`` only owns its query + fit loop."""
        with self._phase("evaluate fidelity", eval_size=len(campaign.eval_feat)):
            surrogate_labels = surrogate.predict_label(campaign.eval_feat)
            surrogate_proba = surrogate.predict_proba(campaign.eval_feat)
            fidelity = top1_fidelity(surrogate_labels, campaign.target_eval_labels)
        surrogate_accuracy: float | None = None
        target_accuracy: float | None = None
        accuracy_ratio: float | None = None
        if self.ground_truth is not None:
            truth = np.asarray(self.ground_truth)
            surrogate_accuracy = top1_fidelity(surrogate_labels, truth)
            target_accuracy = top1_fidelity(campaign.target_eval_labels, truth)
            if target_accuracy > 0:
                accuracy_ratio = surrogate_accuracy / target_accuracy
        result = ExtractionResult(
            strategy=self.strategy,
            surrogate_model=surrogate.name,
            fidelity=fidelity,
            soft_fidelity=soft_fidelity(surrogate_proba, campaign.target_eval_proba),
            agreement_rate=fidelity,
            surrogate_accuracy=surrogate_accuracy,
            transfer_success=None,
            query_count=self._query_count,
            query_budget=self.query_budget,
            per_class_fidelity=per_class_fidelity(surrogate_labels, campaign.target_eval_labels),
            fidelity_vs_budget=budget_curve or [(self._query_count, fidelity)],
            kl_divergence=kl_divergence(surrogate_proba, campaign.target_eval_proba),
            target_accuracy=target_accuracy,
            accuracy_ratio=accuracy_ratio,
            surrogate=surrogate,
            query_samples=self._query_samples,
        )
        if self.measure_transfer and self._numeric:
            result.transfer_success = await self._measure_transfer(surrogate, campaign.eval_feat)
        # Register the stolen surrogate to Hub Models only when extraction actually
        # worked (fidelity >= 0.5); a robust run has no useful clone to publish. It
        # is pushed private by default (see model_export).
        if self.export_model and result.surrogate is not None and result.fidelity >= 0.5:
            from dreadnode.airt.model_export import export_surrogate_to_hub

            result.hub_model = export_surrogate_to_hub(
                result.surrogate,
                strategy=self.strategy,
                target_model=self.airt_target_model,
                fidelity=result.fidelity,
                query_count=result.query_count,
                num_classes=self.num_classes or 2,
            )
        return result

    async def _run_batch_campaign(
        self, campaign: _Campaign
    ) -> tuple[_Surrogate, list[tuple[int, float]]]:
        """The shared query + fit loop for the non-iterative strategies (copycat,
        knockoff, equation_solving, distillation): query the whole training pool
        once, fit the surrogate, then build a fidelity-vs-budget curve by retraining
        on growing prefixes of the already-queried data (no extra target queries).

        Each prefix refit emits a trace step so the fidelity-vs-budget trajectory is
        visible in the Traces tab, not just the final study span."""
        proba, labels = await self._query_soft(campaign.train_raw)
        train_feat = self._feat(campaign.train_raw)
        surrogate = self._build_surrogate(train_feat, proba, labels, campaign.classes)
        budget_curve: list[tuple[int, float]] = []
        for i, frac in enumerate((0.2, 0.4, 0.6, 0.8, 1.0)):
            k = max(2, int(frac * len(train_feat)))
            if k > len(train_feat):
                break
            partial = self._build_surrogate(
                train_feat[:k], proba[:k], labels[:k], campaign.classes, prefer_art=False
            )
            fid_k = top1_fidelity(
                partial.predict_label(campaign.eval_feat), campaign.target_eval_labels
            )
            queries = campaign.eval_probe_queries + k
            budget_curve.append((queries, round(fid_k, 4)))
            self._trace_step(
                i,
                input={"train_prefix": k, "batch_size": len(train_feat)},
                output={"fidelity": round(fid_k, 4)},
                metrics={"fidelity": round(fid_k, 4), "queries": self._query_count},
            )
        return surrogate, budget_curve

    async def _measure_transfer(self, surrogate: _Surrogate, eval_x: np.ndarray) -> float:
        """Craft adversarial perturbations on the surrogate and test if they also flip
        the target - the concrete downstream risk of a stolen model."""
        sample = eval_x[: min(50, len(eval_x))]
        if len(sample) == 0:
            return 0.0
        base_labels = surrogate.predict_label(sample)
        grad_sign = _numeric_gradient_sign(surrogate, sample)
        adv = sample + 0.3 * grad_sign
        adv_surrogate_labels = surrogate.predict_label(adv)
        flipped_on_surrogate = adv_surrogate_labels != base_labels
        if not flipped_on_surrogate.any():
            return 0.0
        target_base = predictions_to_labels(await self._query(list(sample)))
        target_adv = predictions_to_labels(await self._query(list(adv)))
        flipped_on_target = target_adv != target_base
        both = flipped_on_surrogate & flipped_on_target
        return float(np.sum(both) / np.sum(flipped_on_surrogate))

    # -- execution --------------------------------------------------------- #
    async def _execute(self) -> ExtractionResult:
        import importlib

        module = importlib.import_module(
            f"dreadnode.airt.extraction.{self._STRATEGY_MODULES[self.strategy]}"
        )
        return await module.run(self)

    @property
    def _attack_name(self) -> str:
        return f"{self.strategy}_extraction"

    def _span_attributes(self, result: ExtractionResult) -> dict[str, t.Any]:
        from dreadnode.tracing.constants import (
            AIRT_ATTRIBUTE_AGREEMENT_RATE,
            AIRT_ATTRIBUTE_BEST_SCORE,
            AIRT_ATTRIBUTE_EXTRACTION_STRATEGY,
            AIRT_ATTRIBUTE_QUERY_BUDGET,
            AIRT_ATTRIBUTE_QUERY_COUNT,
            AIRT_ATTRIBUTE_SOFT_FIDELITY,
            AIRT_ATTRIBUTE_SURROGATE_ACCURACY,
            AIRT_ATTRIBUTE_SURROGATE_FIDELITY,
            AIRT_ATTRIBUTE_SURROGATE_MODEL,
            AIRT_ATTRIBUTE_TRANSFER_SUCCESS,
        )

        return {
            AIRT_ATTRIBUTE_BEST_SCORE: result.fidelity,
            AIRT_ATTRIBUTE_SURROGATE_FIDELITY: result.fidelity,
            AIRT_ATTRIBUTE_SOFT_FIDELITY: result.soft_fidelity,
            AIRT_ATTRIBUTE_AGREEMENT_RATE: result.agreement_rate,
            AIRT_ATTRIBUTE_QUERY_COUNT: result.query_count,
            AIRT_ATTRIBUTE_QUERY_BUDGET: result.query_budget,
            AIRT_ATTRIBUTE_EXTRACTION_STRATEGY: result.strategy,
            AIRT_ATTRIBUTE_SURROGATE_MODEL: result.surrogate_model,
            AIRT_ATTRIBUTE_SURROGATE_ACCURACY: result.surrogate_accuracy,
            AIRT_ATTRIBUTE_TRANSFER_SUCCESS: result.transfer_success,
        }
