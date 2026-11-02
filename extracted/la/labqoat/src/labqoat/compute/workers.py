"""Immutable opt-in worker reuse, scaling, concurrency and vectorized execution policy."""

from dataclasses import asdict, dataclass, field

from labqoat.compute.batching import Batching
from labqoat.compute.concurrency import Concurrency
from labqoat.compute.scaling import Scaling
from labqoat.json_document import JsonDocument, JsonValue


@dataclass(frozen=True, kw_only=True)
class Workers:
    """Partition reusable workers by immutable callable, parameters, model, owner, resources and seed.

    With ``memory_snapshot``, the first worker of a class on a kind of machine saves its memory, GPU memory included,
    right after its ``@compute.enter(snap=True)`` initializer; later workers on the same kind of machine continue
    from that snapshot instead of importing and initializing again, then run the ``@compute.enter()`` initializer.
    """

    scaling: Scaling = field(default_factory=Scaling)
    concurrency: Concurrency = field(default_factory=Concurrency)
    batching: Batching | None = None
    memory_snapshot: bool = False

    def __post_init__(self) -> None:
        """Ensure the hard input limit can accommodate one full declared batch."""
        if self.batching is not None and self.batching.max_batch_size > self.concurrency.max_inputs:
            raise ValueError("max_batch_size must not exceed concurrency.max_inputs")
        if type(self.memory_snapshot) is not bool:
            raise ValueError("memory_snapshot must be a boolean")

    def to_dict(self) -> dict[str, JsonValue]:
        """Capture the policy as strict JSON for publication and installed-code verification."""
        value = asdict(self)
        if self.batching is None:
            del value["batching"]
        if not self.memory_snapshot:
            del value["memory_snapshot"]
        return dict(JsonDocument.expect_dict(value))
