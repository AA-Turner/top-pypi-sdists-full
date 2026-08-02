"""Domain dataclasses for the EKS node group optimizer.

Every field carries a signal (predictive/observed eviction, price, clock) or a
derived score; the methods expose the credit-adjusted compute and cost-per-work
so callers never re-implement the burstable/flex penalty logic.
"""

from dataclasses import dataclass, field

from .. import perf
from ..eks import NodeGroup
from ..eks_cpu import CpuUtil
from ..spot_advisor import _RATE_EMOJI, _RATE_LABEL

_RATE_MIDPOINT = {0: 2.5, 1: 7.5, 2: 12.5, 3: 17.5, 4: 25.0}
_RECOMMENDED_SPOT = 5  # pools in a recommended SPOT mix (diversification)
_RECOMMENDED_OD = 3


@dataclass
class TypeOption:
    """A compatible instance type with every signal and the global score."""

    instance_type: str
    rate_index: int | None
    spot_price: float | None
    ondemand_price: float | None
    clock_ghz: float | None
    vendor: str
    microarch: str | None
    observed_evictions: int | None = None  # region-wide per type (spot reclamation is a pool, not a node-group, fact)
    observed_launches: int | None = None
    score: float | None = None  # global weighted score 0-100 (higher = better)
    recommendable: bool = True  # passes the family preference (not burstable/accelerated)
    # True when Datadog confirms the node group's sustained load stays under this
    # throttled type's baseline → the throttle never triggers, so drop the penalty.
    sustained_relief: bool = False

    @property
    def observed_rate(self) -> float | None:
        if not self.observed_launches:
            return None
        return 100.0 * (self.observed_evictions or 0) / self.observed_launches

    def price(self, capacity_type: str) -> float | None:
        return self.ondemand_price if capacity_type.upper() == "ON_DEMAND" else self.spot_price

    def perf(self, vcpu: int) -> float | None:
        # Sustained (credit-adjusted) compute: burstable/flex types are penalised to
        # their baseline, so score / cost-per-work reflect sustained load, not burst.
        # When Datadog confirms the real load fits under the baseline, the throttle
        # never fires, so we credit the full burst peak instead.
        if self.sustained_relief:
            return perf.effective_compute(self.instance_type, vcpu, self.clock_ghz)
        return perf.sustained_compute(self.instance_type, vcpu, self.clock_ghz)

    def cost_per_work(self, vcpu: int, capacity_type: str) -> float | None:
        return perf.cost_per_work(self.price(capacity_type), self.instance_type, vcpu, self.clock_ghz)

    @property
    def throttle_kind(self) -> str | None:
        """``'burstable'`` (t*), ``'flex'`` (*-flex), or ``None`` — CPU-throttle class."""
        return perf.throttle_kind(self.instance_type)

    @property
    def is_burstable(self) -> bool:
        """True for any CPU-throttled type (burstable t* or flex) — penalised on sustained perf."""
        return perf.baseline_ratio(self.instance_type) < 1.0

    @property
    def rate_label(self) -> str:
        return _RATE_LABEL.get(self.rate_index, "n/a") if self.rate_index is not None else "n/a"

    @property
    def rate_emoji(self) -> str:
        return _RATE_EMOJI.get(self.rate_index, "❔") if self.rate_index is not None else "❔"


@dataclass
class MixCandidate:
    """One candidate instance-type mix, scored by Spot Placement Score (SPOT only)."""

    strategy: str  # how it was built: "score" | "reliability" | "cost"
    options: list[TypeOption]
    placement: int | None = None  # Spot Placement Score 1-10 of this mix as a request

    @property
    def instance_types(self) -> list[str]:
        return [o.instance_type for o in self.options]

    @property
    def mean_score(self) -> float:
        scores = [o.score for o in self.options if o.score is not None]
        return sum(scores) / len(scores) if scores else 0.0


@dataclass
class NodeGroupPlan:
    ng: NodeGroup
    observed_evictions: int
    shape: tuple[int, int] | None
    current: list[TypeOption] = field(default_factory=list)
    compatible: list[TypeOption] = field(default_factory=list)  # all same-shape/arch, scored, sorted desc
    note: str = ""
    # Sustained per-node CPU utilisation (p95 + p99 fractions) from Datadog over the
    # window; None when no signal. p95 drives the throttled-type (t*/flex) headroom call.
    observed_cpu: CpuUtil | None = None
    # Spot Placement Score (1-10) of the current mix as a diversified request (SPOT only).
    current_placement: int | None = None
    # Placement-scored candidate mixes (SPOT only); ``chosen`` is the selected one.
    candidates: list[MixCandidate] = field(default_factory=list)
    chosen: MixCandidate | None = None

    @property
    def current_types(self) -> set[str]:
        return {o.instance_type for o in self.current}

    @property
    def recommended_placement(self) -> int | None:
        """Placement score of the chosen mix (None when not scored)."""
        return self.chosen.placement if self.chosen else None

    def _score_led(self) -> list[TypeOption]:
        n = _RECOMMENDED_SPOT if self.ng.is_spot else _RECOMMENDED_OD
        return [o for o in self.compatible if o.recommendable][:n]

    def recommended(self) -> list[TypeOption]:
        """The proposed mix: the placement-chosen candidate, else the top-scoring types."""
        return self.chosen.options if self.chosen is not None else self._score_led()

    def others(self) -> list[TypeOption]:
        """Recommendable compatible types not in the current mix — the comparison field, ranked by score.

        Non-recommendable families (burstable) are hidden here; GPU/accelerated
        types are already absent from ``compatible``. Currently-used types — even
        off-family ones — stay visible via the ``current`` list.
        """
        return [o for o in self.compatible if o.instance_type not in self.current_types and o.recommendable]


@dataclass
class EnvEvictions:
    """Per-environment eviction totals, decoupled from the current node groups.

    ``total`` is every spot interruption observed in the env's clusters over the
    window. ``in_scope`` is the share attributed to a **current** node group;
    ``out_of_scope`` (total − in_scope) lands on node groups that are renamed,
    deleted, or simply outside the optimization perimeter — ``orphans`` breaks
    it down by node group label so that information is surfaced, not lost.
    """

    total: int = 0
    in_scope: int = 0
    orphans: dict[str, int] = field(default_factory=dict)

    @property
    def out_of_scope(self) -> int:
        return self.total - self.in_scope


@dataclass
class MixMetrics:
    cost: float | None
    perf: float | None
    cost_per_work: float | None
    eviction_risk: float | None
