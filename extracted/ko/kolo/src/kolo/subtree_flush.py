from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

TRACKING_PROBE_INTERVAL = 1024
ROOT_SUBTREE_NAME = "<root>"


# NOTE: The Python and Rust subtree-flush trackers still implement the same
# state machine independently. Keep the shared contract in
# `python/tests/data/subtree_flush_tracker_contract.json` in sync with any
# heuristic changes so both runtimes stay aligned.


@dataclass
class FlushCandidate:
    start_index: int
    end_index: int
    resident_bytes: int
    co_name: str
    segment_count: int = 1


@dataclass
class OpenSubtree:
    start_index: int
    start_bytes: int
    co_name: str
    flush_candidate: Optional[FlushCandidate] = None


class SubtreeFlushTracker:
    def __init__(self, flush_subtree_bytes: int | None):
        self.flush_subtree_bytes = flush_subtree_bytes
        self.subtree_stack: dict[str, list[OpenSubtree]] = {}
        self.thread_cumulative_bytes: dict[str, int] = {}
        self.flush_tracking_armed: set[str] = set()
        self.flush_in_progress: set[str] = set()
        self._probed_frame_index: dict[str, int] = {}
        self._next_tracking_probe: dict[str, int] = {}
        # Precompute thresholds to avoid per-event recomputation
        self._low_water_bytes = self._compute_low_water_bytes()
        self._tracking_start_bytes = self._compute_tracking_start_bytes()

    def _compute_low_water_bytes(self) -> int:
        if self.flush_subtree_bytes is None:
            return 0
        return self.flush_subtree_bytes // 2

    def _compute_tracking_start_bytes(self) -> int:
        if self.flush_subtree_bytes is None:
            return 0
        if self.flush_subtree_bytes < 1024 * 1024:
            return 0
        # Arm close to the flush threshold: only track subtrees for the last
        # max(flush_bytes/8, 64MB) of data. For 500MB default this means
        # arming at 436MB instead of 1MB, avoiding subtree bookkeeping for
        # 99% of traces that never approach the flush point.
        window = max(self.flush_subtree_bytes // 8, 64 * 1024 * 1024)
        return max(0, self.flush_subtree_bytes - window)

    def low_water_bytes(self) -> int:
        return self._low_water_bytes

    def tracking_start_bytes(self) -> int:
        return self._tracking_start_bytes

    def current_bytes(self, thread_id: str) -> int:
        return self.thread_cumulative_bytes.get(thread_id, 0)

    def push_open_subtree(
        self,
        thread_id: str,
        *,
        start_index: int,
        start_bytes: int,
        co_name: str,
    ) -> None:
        self._stack_for_thread(thread_id).append(
            OpenSubtree(
                start_index=start_index,
                start_bytes=start_bytes,
                co_name=co_name,
            )
        )

    def pop_open_subtree(self, thread_id: str) -> OpenSubtree | None:
        stack = self.subtree_stack.get(thread_id)
        if not stack or len(stack) == 1:
            return None
        return stack.pop()

    def record_closed_segment(
        self,
        thread_id: str,
        *,
        start_index: int,
        end_index: int,
        resident_bytes: int,
        co_name: str,
    ) -> None:
        if resident_bytes <= 0:
            return

        parent = self._stack_for_thread(thread_id)[-1]
        parent.flush_candidate = self._extend_flush_candidate(
            parent.flush_candidate,
            start_index=start_index,
            end_index=end_index,
            resident_bytes=resident_bytes,
            co_name=co_name,
        )

    def select_flush_candidate(
        self, thread_id: str
    ) -> tuple[OpenSubtree, FlushCandidate] | None:
        candidates: list[tuple[int, OpenSubtree, FlushCandidate]] = []
        for depth, subtree in enumerate(self.subtree_stack.get(thread_id, [])):
            if subtree.flush_candidate is not None:
                candidates.append((depth, subtree, subtree.flush_candidate))

        if not candidates:
            return None

        _, owner, candidate = max(
            candidates,
            key=lambda item: (
                item[2].resident_bytes,
                -item[0],
                -item[2].start_index,
            ),
        )
        return owner, candidate

    def clear_flush_candidate(self, thread_id: str, owner: OpenSubtree) -> None:
        owner.flush_candidate = None

    def shift_flush_state_after_flush(
        self,
        thread_id: str,
        *,
        start_index: int,
        end_index: int,
        resident_delta: int,
    ) -> None:
        frame_delta = 1 - (end_index - start_index)

        for subtree in self.subtree_stack.get(thread_id, []):
            if subtree.start_index >= end_index:
                subtree.start_index += frame_delta
                subtree.start_bytes += resident_delta

            candidate = subtree.flush_candidate
            if candidate is None:
                continue
            if candidate.start_index >= end_index:
                candidate.start_index += frame_delta
                candidate.end_index += frame_delta

    def begin_flush(self, thread_id: str) -> bool:
        if self.flush_subtree_bytes is None:
            return False

        current_bytes = self.current_bytes(thread_id)
        if (
            current_bytes < self.flush_subtree_bytes
            or thread_id in self.flush_in_progress
        ):
            return False

        self.flush_in_progress.add(thread_id)
        return True

    def finish_flush(self, thread_id: str) -> None:
        self.flush_in_progress.discard(thread_id)

    def reset(self, frames_by_thread: dict[str, list[bytes]] | None = None) -> None:
        self.subtree_stack.clear()
        self.thread_cumulative_bytes.clear()
        self.flush_tracking_armed.clear()
        self.flush_in_progress.clear()
        self._probed_frame_index.clear()
        self._next_tracking_probe.clear()
        if frames_by_thread is None:
            return

        for thread_id, frames in frames_by_thread.items():
            self.subtree_stack[thread_id] = [self._root_subtree()]
            base_index = len(frames)
            self._probed_frame_index[thread_id] = base_index
            self._next_tracking_probe[thread_id] = base_index + TRACKING_PROBE_INTERVAL

    def _stack_for_thread(self, thread_id: str) -> list[OpenSubtree]:
        return self.subtree_stack.setdefault(thread_id, [self._root_subtree()])

    @staticmethod
    def _root_subtree() -> OpenSubtree:
        return OpenSubtree(
            start_index=0,
            start_bytes=0,
            co_name=ROOT_SUBTREE_NAME,
        )

    def _extend_flush_candidate(
        self,
        candidate: FlushCandidate | None,
        *,
        start_index: int,
        end_index: int,
        resident_bytes: int,
        co_name: str,
    ) -> FlushCandidate:
        if candidate is None or candidate.end_index != start_index:
            return FlushCandidate(
                start_index=start_index,
                end_index=end_index,
                resident_bytes=resident_bytes,
                co_name=co_name,
                segment_count=1,
            )

        candidate.end_index = end_index
        candidate.resident_bytes += resident_bytes
        candidate.segment_count += 1
        return candidate
