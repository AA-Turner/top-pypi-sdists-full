"""``attribute_vote`` -- one stable attribute value per track.

Normative source: ``classification-primitives.md`` §5.3. The primitive
``_REJECTED_PRIMITIVES['attribute_classify']`` asked for by name: per-track attribute
stabilisation, written four times in legacy with four different algorithms (EMA, majority
vote, running mean, modal), replaced here with one implementation and explicit config fields
for the two points -- ``include_current`` and ``tie_policy`` -- where the four disagreed and
the disagreement was invisible in the output.

**A real bug fixed in passing.** ``advanced_tracker.TrackClassAggregator``'s docstring
promises "the most recent among tied classes" on a tie; its implementation is
``Counter(window).most_common(1)[0][0]``, which -- because ``Counter`` preserves
first-insertion order and ``most_common`` sorts stably by count -- actually returns the
**oldest** tied class. ``tie_policy: "oldest"`` reproduces the real (buggy) behaviour;
``"newest"`` reproduces what the docstring claimed but the code never did. Neither is a
silent default here: :attr:`~matrice_analytics.engine.manifest.models.AttributeVoteConfig.
tie_policy` must be chosen deliberately.

Runs **after** ``track`` (``REQUIRES = ("detect", "track")``) and, when an app also runs
``attribute_count`` on the same attribute, **before** it -- enforced by
``AppManifest._check_attribute_order`` -- because counting unstabilised labels and then
stabilising them is exactly the flicker all four legacy stabilisers existed to remove.

**Ordering alone does not achieve that** -- this stage never mutates ``ctx.detections``
(see :meth:`AttributeVote._relabelled`'s docstring), so a same-attribute ``attribute_count``
stage does not see this stage's decision just because it ran later. ``attribute_count``
reads it explicitly, per detection, from ``ctx.previous[...].tracks[track_id].attributes
[attribute]`` (``attribute_count.py`` ``_resolve``) -- ``ctx.previous`` is exactly the set of
earlier stages' outputs the ordering requirement makes available to read from. A real gap
until this was added: the two primitives were fully decoupled and the ordering validator
was enforcing a precondition for a read that did not yet exist.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import ClassVar

from matrice_analytics.engine.manifest.models import AttributeVoteConfig
from matrice_analytics.engine.primitives.base import (
    AttributeRef,
    FrameContext,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    TrackState,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["AttributeVote"]


@register(name="attribute_vote")
class AttributeVote:
    """Per-track temporal stabilisation of one decoded attribute.

    Publishes the decision on :attr:`~matrice_analytics.engine.primitives.base.
    PrimitiveOutput.tracks` as ``TrackState.attributes[self._attribute]`` -- the sanctioned
    channel for per-track information a later stage reads -- and does not mutate
    ``ctx.detections`` (frozen); a primitive that could change the frame the next stage sees
    would be action at a distance.

    Outputs, each resolvable as ``<stage>.<name>``:

    ``stable_count``
        Subjects this frame with a committed value (``min_votes`` cleared, or ``method`` is
        ``modal``, which commits immediately).
    ``undecided_count``
        Subjects with no track id, or no history and no usable observation yet.
    ``switch_count``
        How many committed values **changed** this frame versus their previous commit.
    ``switch_total``
        Window-scope only: the running sum of ``switch_count`` across the window, cleared by
        ``reset()``.
    ``tracked_count``
        Distinct tracks this stage published a decision for this frame.
    """

    name: ClassVar[str] = "attribute_vote"
    Config: ClassVar[type[AttributeVoteConfig]] = AttributeVoteConfig

    __slots__ = (
        "_attribute",
        "_category_format",
        "_config",
        "_expose",
        "_include_current",
        "_method",
        "_min_confidence",
        "_min_votes",
        "_state",
        "_subject",
        "_tie_policy",
        "_window_frames",
    )

    def __init__(self, config: AttributeVoteConfig, state: StateStore) -> None:
        """Bind a validated config and an already-scoped state store.

        Raises:
            ValueError: ``config.method == "ema"``. Not implemented by this rollout phase
                (``classification-primitives.md`` §5.3): ``ema`` needs the full ``top_k``
                probability vector, which :class:`~matrice_analytics.engine.primitives.base.
                AttributeRef` does not carry. Refusing loudly here is better than degrading
                to a one-hot vote that looks like an EMA and is not one.
        """
        if config.method == "ema":
            raise ValueError(
                "attribute_vote.method='ema' is not implemented yet. It needs the producer's "
                "full top_k probability vector, which the decoded AttributeRef does not "
                "carry -- use 'majority' or 'modal' until the producer contract carries "
                "top-k (classification-primitives.md §5.3, §6)."
            )
        self._config = config
        self._state = state
        self._attribute = config.attribute
        self._subject: tuple[str, ...] = tuple(config.subject)
        self._method = config.method
        self._window_frames = int(config.window_frames)
        self._min_votes = int(config.min_votes)
        self._include_current = bool(config.include_current)
        self._tie_policy = config.tie_policy
        self._min_confidence = float(config.min_confidence)
        self._expose = bool(config.expose_attribute_as_category)
        self._category_format = config.category_format

    # -- per frame ------------------------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Stabilise each tracked subject's attribute for one frame.

        Publishes the decision on ``PrimitiveOutput.tracks`` as
        ``TrackState.attributes[self._attribute]``.
        """
        tracks: dict[int, TrackState] = {}
        stable = undecided = switches = 0

        for det in ctx.of_entity(*self._subject):
            if det.track_id is None:
                # No identity, so no history to vote over. Counted as undecided rather than
                # passed through: a per-track stabiliser with no track is not stabilising,
                # and reporting it as stable would hide a broken `track` stage.
                undecided += 1
                continue
            track_id = int(det.track_id)
            ref = det.attributes.get(self._attribute)
            decided, switched = self._decide(track_id, ref)
            if decided is None:
                undecided += 1
                continue
            stable += 1
            switches += int(switched)
            first_seen = self._state.get(f"first.{track_id}")
            if first_seen is None:
                # StateStore has no set_default; get-then-set, and PERSISTENT because a
                # track's first sighting must survive the window boundary or every duration
                # derived from it resets on the 60s tick.
                first_seen = ctx.frame_ts
                self._state.set(f"first.{track_id}", first_seen, lifetime=Lifetime.PERSISTENT)
            tracks[track_id] = TrackState(
                track_id=track_id,
                entity=det.entity,
                zone=ctx.zone,
                first_seen=float(first_seen),
                last_seen=ctx.frame_ts,
                state=decided,
                attributes={
                    self._attribute: decided,
                    f"{self._attribute}_confidence": ref.confidence if ref else 0.0,
                },
            )

        self._prune(ctx, tracks)
        self._accumulate(stable, undecided, switches, len(tracks))
        return PrimitiveOutput(
            values={
                "stable_count": stable,
                "undecided_count": undecided,
                "switch_count": switches,
                "tracked_count": len(tracks),
            },
            tracks=tracks,
            wire_detections=self._relabelled(ctx, tracks) if self._expose else None,
        )

    def _decide(self, track_id: int, ref: AttributeRef | None) -> tuple[str | None, bool]:
        """One track's stabilised value, and whether it changed this frame.

        Returns ``(None, False)`` when there is nothing to decide -- no observation and no
        history. ``None`` is *undecided*, never the string ``"unknown"``: publishing a
        placeholder label puts it in the same keyspace as the real values, which is how
        legacy loses the distinction (``vehicle_type_classification.py:955``).
        """
        previous = self._state.get(f"stable.{track_id}")
        history: list[str] = list(self._state.get(f"votes.{track_id}") or ())

        if ref is None or ref.confidence < self._min_confidence:
            # Occlusion / a crop the classifier declined. Hold the last committed value --
            # the same policy `dwell`'s gap rule applies to a track that is not seen: an
            # absence is not evidence of change.
            return (previous, False) if previous else (None, False)

        observed = ref.label
        if self._include_current:
            history.append(observed)
        decided = self._vote(history, observed, previous)
        if not self._include_current:
            history.append(observed)

        trimmed = history[-self._window_frames :]
        self._state.set(f"votes.{track_id}", trimmed, lifetime=Lifetime.PERSISTENT)
        self._state.set(f"stable.{track_id}", decided, lifetime=Lifetime.PERSISTENT)
        return decided, bool(previous) and decided != previous

    def _vote(self, history: Sequence[str], observed: str, previous: str | None) -> str:
        """The two implemented methods, one place.

        ``majority`` below ``min_votes`` returns the raw observation, which is
        ``GenderStabilizer``'s behaviour and not a bug: an early frame is unvoted, not
        undecided, and returning ``previous`` there would pin a track to its first sighting.
        """
        if self._method == "majority" and len(history) < self._min_votes:
            return observed
        if not history:
            return observed
        counts = Counter(history)
        top = max(counts.values())
        tied = [label for label in counts if counts[label] == top]
        if len(tied) == 1:
            return tied[0]
        if self._tie_policy == "previous" and previous:
            return previous
        if self._tie_policy == "newest":
            return next(label for label in reversed(history) if label in tied)
        return next(label for label in history if label in tied)

    def _relabelled(
        self, ctx: FrameContext, tracks: Mapping[int, TrackState]
    ) -> tuple[PipelineDetection, ...]:
        """This zone's detections with ``category`` replaced by the stabilised value.

        ``expose_attribute_as_category`` only. Mirrors ``line_crossing``'s
        ``expose_corridor_state``: it REPLACES the detector's coarse class on the wire rather
        than sitting beside it, which is why it is opt-in.
        """
        return tuple(
            det.model_copy(update={"category": self._category_for(det, tracks)})
            for det in ctx.detections
            if det.track_id is not None and int(det.track_id) in tracks
        )

    def _category_for(self, det: PipelineDetection, tracks: Mapping[int, TrackState]) -> str:
        """The wire ``category`` string for one detection, per ``category_format``.

        ``diagnostic`` reads the CURRENT raw observation straight from
        ``det.attributes[self._attribute]`` -- the intake-decoded value for THIS frame,
        independent of and unmodified by this stage's own vote -- not anything derived from
        ``tracks``, which only ever holds the stabilised decision.
        """
        stable = tracks[int(det.track_id)].state
        if self._category_format == "value_only":
            return stable
        ref = det.attributes.get(self._attribute)
        current = ref.label if ref is not None else "—"
        return f"{det.category} | now: {current} | stable: {stable}"

    def _prune(self, ctx: FrameContext, current_tracks: Mapping[int, TrackState]) -> None:
        """Drop per-track history for tracks the tracker itself has retired.

        All four legacy stabilisers ship a ``prune(active_track_ids)`` for exactly this, and
        omitting it is an unbounded per-track dict on a busy camera (``classification-
        primitives.md`` §5.3, risk 7). "Active" is read from the upstream ``track`` stage's
        published :class:`TrackState`\\ s -- which persist for a track the tracker still
        considers alive even when it is not in this exact frame's detections (occlusion) --
        never from ``current_tracks``, which is only this stage's own subject-filtered,
        decided subset and would prune a perfectly live track the moment it goes undecided
        for one frame.
        """
        active: set[int] | None = None
        for output in ctx.previous.values():
            if not output.tracks:
                continue
            if active is None:
                active = set()
            active.update(output.tracks)
        if active is None:
            # No upstream tracker output at all (e.g. a unit test constructing FrameContext
            # directly). Nothing to prune against safely -- pruning here would delete every
            # track's history on the very first frame.
            return
        active.update(current_tracks)
        for prefix in ("votes.", "stable.", "first."):
            for key in list(self._state.keys(lifetime=Lifetime.PERSISTENT)):
                if not key.startswith(prefix):
                    continue
                try:
                    track_id = int(key[len(prefix) :])
                except ValueError:
                    continue
                if track_id not in active:
                    self._state.delete(key)

    def _accumulate(self, stable: int, undecided: int, switches: int, tracked: int) -> None:
        """Fold this frame into the window, in the state store.

        ``Lifetime.WINDOW`` throughout, mirroring ``attribute_count``: every one of these is
        a measurement *of* the window (``09`` §4 rule 2). ``switch_total`` is the one
        cumulative counter -- the running sum of switches across the window, distinct from
        ``switch_count``'s per-frame (and, at window scope, last-frame) reading.
        """
        self._state.set("last.stable", stable, lifetime=Lifetime.WINDOW)
        self._state.set("last.undecided", undecided, lifetime=Lifetime.WINDOW)
        self._state.set("last.switches", switches, lifetime=Lifetime.WINDOW)
        self._state.set("last.tracked", tracked, lifetime=Lifetime.WINDOW)
        if switches:
            self._state.incr("total.switches", switches, lifetime=Lifetime.WINDOW)
        elif self._state.get("total.switches") is None:
            self._state.set("total.switches", 0.0, lifetime=Lifetime.WINDOW)
        self._state.incr("frames", 1, lifetime=Lifetime.WINDOW)

    # -- per window -----------------------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window: the last frame's readings, plus the window's switch total.

        Args:
            frames: Unused -- the state store is authoritative, for the same reason
                ``attribute_count.window`` ignores it.
        """
        del frames
        if not float(self._state.get("frames") or 0.0):
            return WindowOutput()
        values: dict[str, Scalar] = {
            "stable_count": int(self._state.get("last.stable") or 0),
            "undecided_count": int(self._state.get("last.undecided") or 0),
            "switch_count": int(self._state.get("last.switches") or 0),
            "switch_total": int(self._state.get("total.switches") or 0),
            "tracked_count": int(self._state.get("last.tracked") or 0),
        }
        return WindowOutput(values=values)

    def reset(self) -> None:
        """``end_window()``, not ``clear()`` -- per-track vote history is PERSISTENT and must
        survive the window boundary, or a track's stabilised label re-flickers once per
        interval (``classification-primitives.md`` §5.3)."""
        self._state.end_window()
