"""Auto-generated stub for module: differ."""
from typing import Any

# Functions
def diff_results_agg(legacy: Any[str, Any] | None, new: Any[str, Any] | None) -> Any:
    """
    Compare two ``results-agg`` payloads structurally and classify every difference.
    
        The three parts of the payload are compared three different ways, because they are
        three different shapes (contract §2):
    
        * **the envelope** -- field by field, split into identity (BREAKING) and label
          (BENIGN) fields;
        * **``tracking_stats``** -- zone-keyed (**FROZEN-2**), and for every zone all four
          count lists (**PY-2**/**FROZEN-5**), matched by ``category``;
        * **``metrics[]``** -- matched by ``(key, zone)``, **never by list position**: the
          array's order is not contractual, the backend indexes by ``key``, and a positional
          comparison both invents differences and hides an ``agg_type`` swap.
    
        Args:
            legacy: The legacy ``results-agg`` payload, or ``None`` when the legacy side
                produced nothing (then ``legacy_error`` should say why).
            new: The new engine's ``results-agg`` payload.
            context: Facts the deliberate-change predicates need.  ``global_counts_agree`` is
                filled in here and any caller-supplied value is overwritten.
            tolerance: What may be forgiven.  See :class:`TolerancePolicy`.
            key_map: The verification-only metric-key correspondence
                (:mod:`~matrice_analytics.engine.migration.keymap`).  Defaults to the map
                registered for ``context.usecase``, or an empty one -- in which case every key
                that differs in spelling is BREAKING, which is the safe default.  Pass
                :data:`~matrice_analytics.engine.migration.keymap.EMPTY_KEY_MAP` explicitly to
                see the raw, unmapped truth.
            legacy_error: Why the legacy side produced nothing.  Forces
                :attr:`Verdict.LEGACY_UNAVAILABLE`.
            notes: Free-text findings for the report.
    
        Returns:
            A :class:`DiffReport`.  :attr:`DiffReport.passed` is the verdict.
    """
    ...

# Classes
class Classification:
    # What one difference means for a migration wave.

    BENIGN: str
    BREAKING: str
    IMPROVEMENT: str

class DeliberateChange:
    # A known, intended behaviour change -- recognised, never flagged as breakage.
    #
    #     The ``citation`` is the point of this class.  Without it, "we meant to do that" is
    #     unfalsifiable, and a real regression that happens to look like an intended change gets
    #     waved through by whoever is running the wave that day.

    def explains(self: Any, difference: Any, context: Any) -> bool:
        """
        Whether this registered change accounts for ``difference``.
        """
        ...

class DiffContext:
    # Facts about the port that some classifications depend on.
    #
    #     A difference cannot be classified from its two values alone.  "This zone count moved
    #     by one" is BREAKING for an app that never changed its reference point and an
    #     IMPROVEMENT for one that did -- so the deliberate-change predicates read this.

    ...
class DiffReport:
    # The structured answer, plus the one bit a migration wave needs.

    def benign(self: Any) -> tuple[Any, ...]: ...

    def breaking(self: Any) -> tuple[Any, ...]: ...

    def improvements(self: Any) -> tuple[Any, ...]: ...

    def passed(self: Any) -> bool:
        """
        Does this port pass?  True only for :attr:`Verdict.PASS`.
        """
        ...

    def render(self: Any) -> str:
        """
        The readable report the CLI prints.
        """
        ...

    def to_dict(self: Any) -> dict[str, Any]:
        """
        The full JSON report -- what ``--json`` prints and what a wave archives.
        """
        ...

    def verdict(self: Any) -> Any:
        """
        ``PASS`` / ``FAIL`` / ``LEGACY_UNAVAILABLE`` -- see :class:`Verdict`.
        """
        ...

class Difference:
    # One place the two payloads disagree, and what that disagreement means.

    def is_breaking(self: Any) -> bool: ...

    def render(self: Any) -> str:
        """
        One line for the human-readable report.
        """
        ...

    def to_dict(self: Any) -> dict[str, Any]:
        """
        The JSON form the ``--json`` CLI mode emits.
        """
        ...

class TolerancePolicy:
    # What the comparison is allowed to forgive, stated explicitly.
    #
    #     Every entry exists because the two engines *provably* differ on it for a reason that
    #     cannot reach a consumer.  Nothing here is a convenience.
    #
    #     Attributes:
    #         float_abs_tol: Absolute tolerance on ``metrics[].data``.  ``data`` is a float on
    #             the wire (contract §1 rule 6) and both engines reach it through a different
    #             number of float operations -- a percentage computed as ``a / b * 100`` differs
    #             in the last bit depending on the order.  Counts are **ints** and get no
    #             tolerance at all (see :attr:`int_counts_are_exact`).
    #         float_rel_tol: Relative tolerance, for the same reason at large magnitudes.
    #         timestamps_may_differ: Every timestamp is allowed to differ.  The legacy window
    #             boundary and its ``input_timestamp`` come from ``time.time()``
    #             (``legacy_analytics_bridge.py:3009,3013``); the new engine's come from frame
    #             time (**PY-13**).  They therefore *always* differ, on every run, and a policy
    #             that called that BREAKING would never pass anything.
    #         uuids_may_differ: A value that is a UUID on both sides may differ.  Ids are
    #             opaque to every consumer except the backend's find-or-create, which only needs
    #             them stable *within* a stream, not equal *across* engines.
    #         empty_string_equals_absent: ``""`` and an absent key are the same value for an
    #             optional string.  Contract §1 rule 7 forbids ``None`` and requires ``""``;
    #             ``to_payload`` uses ``exclude_none=True`` so an unset optional simply does not
    #             serialise.  Both spellings reach the Go parser as the zero value.
    #         absent_count_is_zero: A category absent from a count list is a count of zero.
    #             The legacy builder emits an explicit ``{"category": "person", "count": 0}``;
    #             the new engine omits the entry.  A dashboard cannot tell them apart.
    #         int_counts_are_exact: Counts are never tolerated.  ``current_counts`` feeds
    #             ``raw_analytics.count``, the primary series -- one person of drift there is
    #             exactly the class of bug this harness exists to catch.
    #         ignored_paths: Paths never compared, for diagnostics that are not payload.

    def numbers_equal(self: Any, left: float, right: float) -> bool:
        """
        Whether two floats are equal under this policy.
        """
        ...

class Verdict:
    # The single answer a migration wave asks for.

    FAIL: str
    LEGACY_UNAVAILABLE: str
    PASS: str

