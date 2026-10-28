"""Uniform part plans for multipart uploads and ranged downloads.

The uniform multipart layout follows these storage constraints:

* ``part_size = max(floor, next_pow2(ceil(size / 8000)))`` where ``floor`` is the
  configured ``multipart_chunksize`` clamped up to 5 MiB and down to 4000 MiB.
* Every part but the last is exactly ``part_size``; the plan never exceeds 10,000
  parts.
* If the power-of-two size would pass the 4000 MiB cap, fall back to
  ``ceil(size / 10000)`` rounded up to 1 MiB; if that still exceeds the cap the
  object cannot be uploaded and ``PartPlanError`` is raised.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from istari_digital_client._transfer.errors import PartPlanError

MIB = 1024 * 1024
MIN_PART_SIZE = 5 * MIB  # S3's minimum for every part but the last
# Covers Azure's Put Block limit (4000 MiB) and stays under S3's 5 GiB.
MAX_PART_SIZE = 4000 * MIB
MAX_PARTS = 10_000
TARGET_PARTS = 8000  # aim this low so the plan has headroom under MAX_PARTS


def next_pow2(n: int) -> int:
    """Smallest power of two >= ``n`` (1 for n <= 1)."""
    if n <= 1:
        return 1
    return 1 << (n - 1).bit_length()


def _round_up(n: int, multiple: int) -> int:
    return -(-n // multiple) * multiple


def clamp_part_size(min_part_size: int) -> int:
    """Clamp a configured floor into ``[MIN_PART_SIZE, MAX_PART_SIZE]``."""
    return min(max(int(min_part_size), MIN_PART_SIZE), MAX_PART_SIZE)


@dataclass(frozen=True)
class PartPlan:
    """A uniform split of ``size`` bytes into parts of ``part_size`` (last may be shorter)."""

    size: int
    part_size: int

    def __post_init__(self) -> None:
        """Reject impossible plans early."""
        if self.size < 0 or self.part_size <= 0:
            raise PartPlanError(
                f"invalid plan: size={self.size} part_size={self.part_size}"
            )

    @property
    def num_parts(self) -> int:
        """Part count; an empty object still has one (empty) part."""
        return max(1, -(-self.size // self.part_size))

    def part_range(self, part_number: int) -> tuple[int, int]:
        """``(offset, length)`` of 1-based ``part_number``."""
        if not 1 <= part_number <= self.num_parts:
            raise PartPlanError(
                f"part {part_number} outside plan of {self.num_parts} parts"
            )
        offset = (part_number - 1) * self.part_size
        return offset, min(self.part_size, self.size - offset)

    def ranges(self) -> Iterator[tuple[int, int, int]]:
        """Yield ``(part_number, offset, length)`` in ascending order."""
        for n in range(1, self.num_parts + 1):
            offset, length = self.part_range(n)
            yield n, offset, length


def plan_parts(size: int, min_part_size: int) -> PartPlan:
    """Choose the uniform part size for ``size`` bytes given the configured floor."""
    if size < 0:
        raise PartPlanError(f"negative size {size}")
    floor = clamp_part_size(min_part_size)
    part_size = max(floor, next_pow2(-(-size // TARGET_PARTS)))
    if part_size > MAX_PART_SIZE:
        part_size = max(floor, _round_up(-(-size // MAX_PARTS), MIB))
        if part_size > MAX_PART_SIZE:
            raise PartPlanError(
                f"{size} bytes cannot be split into <= {MAX_PARTS} parts of <= {MAX_PART_SIZE} bytes"
            )
    return PartPlan(size=size, part_size=part_size)


def split_ranges(size: int, part_size: int) -> list[tuple[int, int]]:
    """``[(offset, length), ...]`` covering ``size`` bytes in ``part_size`` steps (empty for 0)."""
    if size <= 0:
        return []
    return [
        (offset, length) for _, offset, length in PartPlan(size, part_size).ranges()
    ]


def is_valid_part_size(part_size: int, size: int) -> bool:
    """Whether ``part_size`` is an acceptable uniform plan for ``size`` bytes."""
    return (
        MIN_PART_SIZE <= part_size <= MAX_PART_SIZE
        and PartPlan(size, part_size).num_parts <= MAX_PARTS
    )


@dataclass(frozen=True)
class ResumeDecision:
    """Outcome of matching discovered parts against the object: adopt or restart."""

    plan: PartPlan | None
    landed: frozenset[int]

    @property
    def resumable(self) -> bool:
        """True when the landed parts fit one valid uniform plan."""
        return self.plan is not None

    def missing(self) -> list[int]:
        """Part numbers still to upload, ascending, if ``resumable`` is true.

        An empty list also represents invalid metadata; callers must check
        ``resumable`` before treating it as an already-complete upload.
        """
        if self.plan is None:
            return []
        return [n for n in range(1, self.plan.num_parts + 1) if n not in self.landed]


def resume_decision(parts: Sequence[tuple[int, int]], size: int) -> ResumeDecision:
    """Decide whether discovered ``(part_number, size)`` pairs can be adopted.

    Server-derived boundaries win: if every landed part except possibly the plan's
    last one shares a single size that is a valid plan for ``size`` bytes, and each
    landed part is exactly what that plan prescribes, the plan is adopted and only
    the missing numbers need uploading. A lone part fixes the boundaries only if
    it is part 1 or its number times its length equals the object's size. Other
    lone non-first parts are ambiguous even when the current local plan matches;
    restart rather than infer historical settings. Non-uniform or invalid metadata
    also means cancel and start fresh.
    """
    if not parts:
        return ResumeDecision(plan=None, landed=frozenset())
    numbers = [n for n, _ in parts]
    if len(set(numbers)) != len(numbers) or min(numbers) < 1:
        return ResumeDecision(plan=None, landed=frozenset())
    by_number = dict(parts)
    highest = max(numbers)
    # The highest-numbered landed part may be the plan's short last part; every
    # other landed part must be a full part, so those fix the candidate size.
    full = [s for n, s in parts if n != highest]
    candidates = set(full) if full else {by_number[highest]}
    if len(candidates) != 1:
        return ResumeDecision(plan=None, landed=frozenset())
    part_size = candidates.pop()
    if part_size <= 0 or not is_valid_part_size(part_size, size):
        return ResumeDecision(plan=None, landed=frozenset())
    plan = PartPlan(size=size, part_size=part_size)
    for n, s in parts:
        if n > plan.num_parts or plan.part_range(n)[1] != s:
            return ResumeDecision(plan=None, landed=frozenset())
    # A lone non-first part does not establish the server's stride unless it is
    # an exact final part. The locally inferred size may fit, but other valid
    # layouts can place the same part at a different offset.
    if not full and highest != 1 and highest * by_number[highest] != size:
        return ResumeDecision(plan=None, landed=frozenset())
    return ResumeDecision(plan=plan, landed=frozenset(numbers))
