"""Which rollout rows a micro-batch holds: Miles' `DataIterator.get_next` (`data/rollout.py:421`) is wrapped on the
class, so every micro-batch with tokens carries the `sample_indices` of its rows under `ROWS_FIELD`. The batch dict
`get_batch` builds from it is the one `loss_function` receives (Megatron binds it with `partial`, `model.py:552`), so
the loss hook names each row as the trainer parts do instead of guessing from token digests (S0); where in which pass
it sits tells a retried or abandoned update from the one in progress. Fails open."""

from __future__ import annotations

import functools
import logging
from dataclasses import dataclass
from typing import Any

from ..samples.mapping import to_list

logger = logging.getLogger(__name__)

#: The batch key the stamp rides under (Miles reads only the keys it asked for).
ROWS_FIELD = "probe_rows"
WRAPPED_MARK = "__probe_miles_stamp__"


@dataclass(frozen=True)
class RowStamp:
    """One micro-batch's rows: their rollout `sample_indices`, the rank's whole rollout (for the update count), and
    where the micro-batch sits in its pass over the rollout."""

    sample_indices: list[Any]
    #: Samples this rank holds for the rollout.
    rollout_rows: int
    #: Miles' own per-step micro-batch counts when it scheduled them (`num_microbatches`), else None.
    steps: int | None
    #: The iterator that served it (`id`) and its offset before it did: a pass restarts (a retry, a new rollout)
    #: when either goes back.
    source: int = 0
    position: int = 0


def install_stamp(module: Any) -> bool:
    """Wrap `DataIterator.get_next` in Miles' rollout-data module, once."""
    iterator = getattr(module, "DataIterator", None)
    original = getattr(iterator, "get_next", None)
    if not callable(original) or getattr(original, WRAPPED_MARK, False):
        return False

    @functools.wraps(original)
    def get_next(self: Any, keys: Any) -> Any:
        positions = _get_positions(self) if "tokens" in keys else None
        offset = getattr(self, "offset", 0)
        batch = original(self, keys)
        if positions is not None:
            _stamp(self, batch, positions, offset)
        return batch

    setattr(get_next, WRAPPED_MARK, True)
    iterator.get_next = get_next
    return True


def read_stamp(batch: Any) -> RowStamp | None:
    found = batch.get(ROWS_FIELD) if hasattr(batch, "get") else None
    return found if isinstance(found, RowStamp) else None


def _get_positions(iterator: Any) -> list[int] | None:
    """The rollout positions `get_next` is about to return (read before it moves its offset)."""
    try:
        if iterator.micro_batch_indices is not None:
            return list(iterator.micro_batch_indices[iterator.offset])
        return list(range(iterator.offset, iterator.offset + iterator.micro_batch_size))
    except Exception:  # noqa: BLE001 -- an iterator shape this version does not know: no stamp
        return None


def _stamp(iterator: Any, batch: Any, positions: list[int], offset: Any) -> None:
    try:
        data = iterator.rollout_data
        raw = data.get("sample_indices")
        if raw is None or not isinstance(batch, dict):
            return
        indices = to_list(raw)
        scheduled = data.get("num_microbatches")
        batch[ROWS_FIELD] = RowStamp(sample_indices=[indices[p] for p in positions], rollout_rows=len(indices),
                                     steps=len(scheduled) if scheduled is not None else None, source=id(iterator),
                                     position=int(offset))  # fmt: skip
    except Exception:  # noqa: BLE001 -- fail open: the micro-batch trains unstamped (and unrecorded)
        logger.debug("Probe could not stamp a Miles micro-batch", exc_info=True)
