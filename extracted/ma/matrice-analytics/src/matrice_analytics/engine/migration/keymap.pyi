"""Auto-generated stub for module: keymap."""
from typing import Any

# Functions
def key_map_for(usecase: str) -> Any:
    """
    The verification key map for a legacy use case.
    
        Args:
            usecase: The legacy use-case name, e.g. ``people_counting``.
    
        Returns:
            Its :class:`UsecaseKeyMap`, or :data:`EMPTY_KEY_MAP` when none is registered.  An
            unregistered use case is **not** an error: it means no key correspondence has been
            established yet, and every key difference stays BREAKING until one is.
    """
    ...

# Classes
class MetricKeyPair:
    # Two spellings of one measurement: a legacy key and its new-engine counterpart.
    #
    #     Attributes:
    #         legacy_key: ``metrics[].key`` as the legacy bridge publishes it.
    #         new_key: ``metrics[].key`` as the manifest publishes it.
    #         evidence: What settles the claim that these are the same measurement -- a
    #             payload-diff run in which both sides read the same value, or the ``file:line``
    #             that produces each.  **Required.**  Without it the pairing is an opinion, and an
    #             opinion that suppresses a difference is how a regression gets promoted.
    #         note: Anything a reviewer needs beyond the evidence.

    ...
class MetricSide:
    # Which payload a key appears on.

    LEGACY: str
    NEW: str

class UnpairedMetricKey:
    # A key that **deliberately** has no counterpart -- not a key nobody has looked at.
    #
    #     ``occupancy_percentage`` is legacy-only because it is a fraction of a configured
    #     capacity, and the new engine is given no capacity; ``peak_occupancy`` is new-only
    #     because legacy never computed a within-window maximum.  Neither is a rename waiting to
    #     be found, so neither is BREAKING -- but both are *reported*, because a metric that
    #     stops being published is a chart that stops drawing, and the app owner has to know.
    #
    #     Attributes:
    #         key: The metric key.
    #         side: Which payload it appears on.  A key registered ``NEW`` that turns up on the
    #             **legacy** payload is *not* explained by this entry and stays BREAKING -- the
    #             registration is a statement about one side, not a blanket amnesty for the name.
    #         rationale: Why no counterpart exists.  Not "we did not port it": what it measures,
    #             and why the other engine has nothing that measures it.
    #         evidence: Doc section or ``file:line``.  **Required.**

    ...
class UsecaseKeyMap:
    # One legacy use case's metric-key correspondence.
    #
    #     Keyed by the *legacy* use-case name, because that is the side being retired and the side
    #     the harness is invoked with (``payload_diff.py --usecase``).

    def is_empty(self: Any) -> bool:
        """
        Whether this map says nothing -- every key is then unmapped, hence BREAKING.
        """
        ...

    def legacy_key_for(self: Any, new_key: str) -> str | None:
        """
        The legacy key this new-engine key should be compared against.
        """
        ...

    def new_key_for(self: Any, legacy_key: str) -> str | None:
        """
        The new-engine key this legacy key should be compared against.
        """
        ...

    def pair_for_legacy(self: Any, legacy_key: str) -> Any | None:
        """
        The pairing that claims ``legacy_key``, if any.
        """
        ...

    def pair_for_new(self: Any, new_key: str) -> Any | None:
        """
        The pairing that claims ``new_key``, if any.
        """
        ...

    def unpaired_for(self: Any, key: str, side: Any) -> Any | None:
        """
        The "deliberately has no counterpart" entry for ``key`` **on that side**.
        
                Side-sensitive on purpose: ``current_occupancy`` is registered as new-only, so a
                ``current_occupancy`` that shows up on the *legacy* payload is unexplained and stays
                BREAKING.
        """
        ...

