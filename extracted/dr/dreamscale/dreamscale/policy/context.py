"""Observation context: the older camera frames a windowed policy sees.

With context on, an Isaac 0.5 request uses each camera's last three frames at the control
period (1/30 s, its training spacing), oldest first. The run loop observes on the ticks
just before a request; where the server accepts history frames, each of those frames is
sent as soon as it is captured and the request names them, so only the newest frame is
uploaded with the request. Otherwise the request carries all three as one JPEG strip per
camera. A missing or stale older frame is replaced by
the oldest one available (Perceptron's own padding at the start of an episode), never by a
frame from further back.

FLUX 3 Action SO-101 instead takes one older frame at a fixed offset: the frame captured 7
ticks (233 ms) before the observation (``ObservationHistory.at_offsets``). Its requests come
almost back to back, so the run loop keeps an observation on every tick that could be 7
ticks before a request, also while a request is in flight. Those stay local; the request
carries its t-7 frame in a two-frame strip. Without one within half a tick of t-7, the
request goes up alone and the server uses the current frame for both snapshots.
"""

from __future__ import annotations

import logging
import time
from collections import deque
from typing import Any

from dreamscale import wire

log = logging.getLogger("dreamscale.policy")

# A measured window repeats the earlier tick over a gap of at most this many missing ticks (a
# caller's loop hiccup: a GC pause, a USB stall); past it, the window starts again after the gap,
# as at an episode start, rather than refuse every call until the gap ages out of it.
MAX_PADDED_GAP_TICKS = 3


class ContextObservation:
    """An observation whose cameras also carry the older frames (oldest first)."""

    def __init__(
        self, current: Any, older: tuple[Any, ...], keys: tuple[int, ...] | None = None,
        *, state_samples: tuple[Any, ...] = (),
    ) -> None:
        self.current = current
        self.older = older
        # Capture keys of the older frames when the server already holds them.
        self.keys = keys
        self.state_samples = state_samples

    def __getattr__(self, name: str) -> Any:
        # State, frames and timestamps are the newest observation's.
        return getattr(self.current, name)

    def to_wire(self, *, session_id: str, observation_id: int, instruction: str) -> Any:
        if not self.older:
            return self.current.to_wire(
                session_id=session_id, observation_id=observation_id, instruction=instruction,
            )
        if self.keys is not None:
            with wire.history_keys(self.keys):
                return self.current.to_wire(
                    session_id=session_id, observation_id=observation_id, instruction=instruction
                )
        captured = []
        for observation in self.older:
            with wire.captured_frames() as frames:
                observation.to_wire(
                    session_id=session_id, observation_id=observation_id, instruction=instruction
                )
            captured.append(frames)
        history = {camera: [frames[camera] for frames in captured] for camera in captured[-1]}
        with wire.history_frames(history):
            return self.current.to_wire(
                session_id=session_id, observation_id=observation_id, instruction=instruction
            )


class ObservationHistory:
    """The observations of the last few control ticks, for ``frames``-frame requests."""

    def __init__(
        self,
        frames: int,
        period_s: float,
        clock: Any = time.monotonic,
        *,
        offsets: tuple[int, ...] | None = None,
        state_steps: int = 0,
    ) -> None:
        if offsets is not None:
            if (
                (not offsets and not state_steps)
                or any(type(offset) is not int or offset < 1 for offset in offsets)
                or list(offsets) != sorted(set(offsets), reverse=True)
                or frames != len(offsets) + 1
            ):
                raise ValueError("offsets are distinct tick counts before capture, oldest first")
        if frames < 1 or period_s <= 0:
            raise ValueError("context needs at least one frame and a positive period")
        self.frames = frames
        self.period_s = period_s
        self._clock = clock
        if type(state_steps) is not int or not 0 <= state_steps <= 31:
            raise ValueError("state_steps must be 0-31")
        self.state_steps = state_steps
        # Sparse windows (fixed offsets) keep their frames local and observe while a request
        # is in flight; contiguous ones (Isaac context) send frames ahead between requests.
        self.offsets = tuple(offsets) if offsets is not None else tuple(range(frames - 1, 0, -1))
        self.sparse = offsets is not None
        reach = (max((*self.offsets, state_steps)) + 2) if self.sparse else 2 * frames
        self._recent: deque[tuple[float, Any, int | None]] = deque(maxlen=max(1, reach))
        self._started_at: float | None = None
        self._moving = False
        # Intervals the SDK waited for a chunk while the robot held (model-defined "wait").
        self._holds: deque[tuple[float, float]] = deque(maxlen=max(1, reach))
        # Ticks a caller's loop skipped that a window repeated, and the windows that started
        # again after a longer stall (said once: the loop runs slower than the model's rate).
        self.padded_ticks = 0
        self.restarts = 0

    @classmethod
    def at_offsets(cls, offsets: tuple[int, ...], period_s: float, clock: Any = time.monotonic,
                   *, state_steps: int = 0):
        """A window of the frames ``offsets`` ticks before the observation (oldest first)."""
        return cls(
            len(offsets) + 1, period_s, clock, offsets=tuple(offsets), state_steps=state_steps
        )

    @property
    def observe_steps(self) -> range:
        """Ticks ahead of a request on which the run loop keeps an observation."""
        return range(1, (max((*self.offsets, self.state_steps))
                         if self.sparse else self.frames - 1) + 1)

    @property
    def sends_ahead(self) -> bool:
        return not self.sparse

    def push(self, observation: Any, at: float | None = None, key: int | None = None) -> None:
        """Keep an observation; ``key`` names its frames if they were sent ahead."""
        if self.frames > 1 or self.state_steps:
            captured_at = self._clock() if at is None else at
            if self._started_at is None:
                self._started_at = captured_at
            self._recent.append((captured_at, observation, key))

    def window(self, observation: Any, at: float | None = None) -> Any:
        """``observation`` with its older frames, or unchanged for single-frame requests."""
        if self.frames == 1 and not self.state_steps:
            return observation
        now = self._clock() if at is None else at
        if self._started_at is None:
            self._started_at = now
        if self.state_steps:
            return self._measured_window(observation, now)
        if self.sparse:
            return self._sparse_window(observation, now)
        older: list[Any] = []
        keys: list[int | None] = []
        # Walk back one period at a time; stop at the first gap (frames must be contiguous).
        for step in range(1, self.frames):
            target = now - step * self.period_s
            match = min(
                (
                    entry
                    for entry in self._recent
                    if entry[1] is not observation and all(entry[1] is not o for o in older)
                ),
                key=lambda entry: abs(entry[0] - target),
                default=None,
            )
            if match is None or abs(match[0] - target) >= 0.5 * self.period_s:
                break
            older.insert(0, match[1])
            keys.insert(0, match[2])
        # Name frames the server holds only for a complete window; a padded window goes
        # up as a strip (padding repeats frames that were never sent ahead).
        sent = len(keys) == self.frames - 1 and all(key is not None for key in keys)
        oldest = older[0] if older else observation
        older = [oldest] * (self.frames - 1 - len(older)) + older
        return ContextObservation(observation, tuple(older), tuple(keys) if sent else None)

    def _measured_window(self, observation: Any, now: float) -> ContextObservation:
        """Every measured tick plus sparse VAE frames, counted in ticks rather than matched
        to exact timestamps, so a loop's jitter cannot drop one. A missing tick (a gap of
        1.5 periods or more) repeats the held tick inside an SDK chunk wait or before motion
        began (episode-start padding), and over a gap of the caller's own of at most
        MAX_PADDED_GAP_TICKS; past that, the window starts again after the gap, as at an
        episode start (the ticks before it are dropped, the oldest after it repeats)."""
        recent = sorted(
            (entry for entry in self._recent if entry[0] <= now and entry[1] is not observation),
            key=lambda entry: entry[0],
        )
        need = max((*self.offsets, self.state_steps))
        ticks: list[tuple[float, Any, int | None]] = []  # ticks[k - 1]: k ticks before now
        cursor = now
        for entry in reversed(recent):
            steps = max(1, round((cursor - entry[0]) / self.period_s))
            held = entry[0] < self._started_at or any(
                start < cursor and end > entry[0] for start, end in self._holds
            )
            if steps > 1 and not held:
                if steps - 1 > MAX_PADDED_GAP_TICKS:
                    self._restart(steps - 1)
                    break  # the window starts again after this gap
                self.padded_ticks += steps - 1
            ticks.extend([entry] * steps)
            cursor = entry[0]
            if len(ticks) >= need:
                break
        if len(ticks) < need:
            # an episode's (or a restarted window's) start: its oldest tick repeats
            oldest = ticks[-1] if ticks else (now, observation, None)
            ticks.extend([oldest] * (need - len(ticks)))
        states = tuple(ticks[step - 1][1] for step in range(self.state_steps, 0, -1))
        older = [ticks[offset - 1] for offset in self.offsets]
        keys = tuple(entry[2] for entry in older)
        return ContextObservation(
            observation, tuple(entry[1] for entry in older),
            keys if keys and all(key is not None for key in keys) else None,
            state_samples=states,
        )

    def _sparse_window(self, observation: Any, now: float) -> Any:
        """Every offset's frame within half a period of its slot, or the observation alone."""
        older: list[Any] = []
        keys: list[int | None] = []
        for offset in self.offsets:
            target = now - offset * self.period_s
            match = min(
                (entry for entry in self._recent if entry[1] is not observation),
                key=lambda entry: abs(entry[0] - target),
                default=None,
            )
            if match is None or abs(match[0] - target) >= 0.5 * self.period_s:
                return observation
            older.append(match[1])
            keys.append(match[2])
        sent = all(key is not None for key in keys)
        return ContextObservation(observation, tuple(older), tuple(keys) if sent else None)

    def _restart(self, missing: int) -> None:
        if not self.restarts:
            log.warning(
                "The robot's loop skipped %d control ticks (%.0f ms); the FLUX history window "
                "starts again after the gap. Call next_action() every %.0f ms (the model's "
                "rate) to keep its full history.",
                missing, missing * self.period_s * 1000, self.period_s * 1000,
            )
        self.restarts += 1

    def clear(self) -> None:
        self._recent.clear()
        self._holds.clear()
        self._started_at = None
        self._moving = False

    def hold(self, start: float, end: float) -> None:
        """The SDK waited for a chunk from ``start`` to ``end`` with no command to send, so
        the robot held its last measured tick. Measured windows repeat that tick for the
        interval, whatever its length."""
        if self.state_steps and end > start:
            self._holds.append((start, end))

    def begin_motion(self, at: float | None = None) -> None:
        """The episode's first action executes now. Until then the robot held its starting
        state while the first chunk was computed, so measured windows pad those ticks like
        episode-start ticks. Once per episode."""
        if not self.state_steps or self._moving or self._started_at is None:
            return
        self._moving = True
        self._started_at = max(self._started_at, self._clock() if at is None else at)


class TickHistory:
    """The frames ``offsets`` executed actions before each request, those the episode has
    reached (Hy-VLA: 25, 20, 15, 10 and 5 ticks back).

    Ticks are the robot's executed actions: a wait for a chunk doesn't advance them. Each
    observation is stamped with the tick it was taken at (the latest of a tick stands for
    it). A request at tick ``s`` carries, oldest first, the latest observation taken at or
    before ``s - offset`` for each offset ``s`` has reached; offsets not yet reached are
    left out (the server fills their slots with black, as Hy-VLA was trained), so a
    camera's strip holds 1-6 frames. With ``start`` (Long-WAM) they are the episode's first
    observation instead, sent once and repeated by the server, as upstream's window repeats
    its first frame. Only an episode start (``clear``) resets it: a new instruction keeps the
    frames before it.
    """

    sparse = True
    sends_ahead = False
    state_steps = 0

    def __init__(self, offsets: tuple[int, ...], *, start: bool = False):
        offsets = tuple(offsets)
        if (
            not offsets
            or any(type(offset) is not int or not 1 <= offset <= 64 for offset in offsets)
            or list(offsets) != sorted(set(offsets), reverse=True)
        ):
            raise ValueError("a tick history needs distinct offsets of 1-64 ticks, oldest first")
        self.offsets = offsets
        self.frames = len(offsets) + 1
        self.start = start
        self._observed: deque[tuple[int, Any]] = deque()
        self._first: Any | None = None  # the episode's tick-0 observation (``start``)
        self._tick = 0
        self.padded_ticks = 0

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def observe_steps(self) -> range:
        """Ticks ahead of a request on which the run loop keeps an observation."""
        return range(1, self.offsets[0] + 1)

    def executed(self) -> None:
        """The robot executed one action of a chunk (a held tick doesn't count)."""
        self._tick += 1

    def push(self, observation: Any, at: float | None = None, key: int | None = None) -> None:
        if self._observed and self._observed[-1][0] == self._tick:
            self._observed.pop()  # the latest observation of a tick stands for it
        self._observed.append((self._tick, observation))
        if self._tick == 0:
            self._first = observation
        # Keep the newest observation at or before the oldest tick a request can still need.
        oldest = self._tick - self.offsets[0]
        while len(self._observed) > 1 and self._observed[1][0] <= oldest:
            self._observed.popleft()

    def window(self, observation: Any, at: float | None = None) -> Any:
        older = []
        for offset in self.offsets:
            if self._tick < offset:
                continue
            target = self._tick - offset
            seen = next((seen for tick, seen in reversed(self._observed) if tick <= target),
                        None)
            if seen is not None:
                older.append(seen)
        first = self._first
        if (self.start and first is not None and self._tick < self.offsets[0]
                and (older[0] if older else observation) is not first):
            older.insert(0, first)
        return ContextObservation(observation, tuple(older)) if older else observation

    def clear(self) -> None:
        self._observed.clear()
        self._first = None
        self._tick = 0

    def hold(self, start: float, end: float) -> None:
        """A wait for a chunk advances no tick."""

    def begin_motion(self, at: float | None = None) -> None:
        """Ticks count executed actions from the episode's start, whenever motion begins."""


class EpisodeHistory:
    """The episode's first observation and the one ``recent_offset`` executed actions before
    each request (a contract with ``history_anchor``; InternW0-Δ's first).

    Ticks are the robot's executed actions, upstream's logical step: a wait for a chunk
    doesn't advance them. Each observation is stamped with the tick it was taken at; a
    request at tick ``s`` carries the anchor and, from tick ``recent_offset`` on, the latest
    observation taken at or before ``s - recent_offset``. Upstream's deploy pipeline reads
    the same frame: its memory repeats the last observed frame over ticks it didn't observe.
    The run loop observes every tick before a request, so the frame is exact there.
    """

    frames = 3
    sparse = True
    sends_ahead = False

    def __init__(self, recent_offset: int):
        if type(recent_offset) is not int or not 1 <= recent_offset <= 64:
            raise ValueError("an episode history needs a tick offset of 1-64")
        self.recent_offset = recent_offset
        self._observed: deque[tuple[int, Any]] = deque()
        self._anchor: Any | None = None
        self._tick = 0

    @property
    def observe_steps(self) -> range:
        """Ticks ahead of a request on which the run loop keeps an observation."""
        return range(1, self.recent_offset + 1)

    def executed(self) -> None:
        """The robot executed one action of a chunk (a held tick doesn't count)."""
        self._tick += 1

    def push(self, observation: Any, at: float | None = None, key: int | None = None) -> None:
        if self._anchor is None:
            self._anchor = observation
        if self._observed and self._observed[-1][0] == self._tick:
            self._observed.pop()  # the latest observation of a tick stands for it
        self._observed.append((self._tick, observation))
        # Keep the newest observation at or before the oldest tick a request can still need.
        oldest = self._tick - self.recent_offset
        while len(self._observed) > 1 and self._observed[1][0] <= oldest:
            self._observed.popleft()

    def window(self, observation: Any, at: float | None = None) -> Any:
        if self._anchor is None:
            # The episode's first request: these frames are its anchor.
            self._anchor = observation
            return observation
        older = [self._anchor]
        if self._tick >= self.recent_offset:
            target = self._tick - self.recent_offset
            older.append(next(
                (seen for tick, seen in reversed(self._observed) if tick <= target),
                self._anchor,
            ))
        return ContextObservation(observation, tuple(older))

    def clear(self) -> None:
        self._observed.clear()
        self._anchor = None
        self._tick = 0

    def hold(self, start: float, end: float) -> None:
        """A wait for a chunk advances no tick."""

    def begin_motion(self, at: float | None = None) -> None:
        """The anchor is the episode's first frame, whenever motion begins."""


class EpisodeObservation:
    """A request's observation in an episode the server keeps (``EpisodeTicks``): the newest
    observation, the one taken a control step before it (its state travels as the request's
    ``state_history``), and the request's step since the episode's first request."""

    def __init__(self, current: Any, previous: Any, step: int) -> None:
        self.current = current
        self.previous = previous
        self.step = step

    def __getattr__(self, name: str) -> Any:
        return getattr(self.current, name)

    def to_wire(self, *, session_id: str, observation_id: int, instruction: str) -> Any:
        return self.current.to_wire(
            session_id=session_id, observation_id=observation_id, instruction=instruction
        )


class EpisodeTicks:
    """An episode the server keeps (a contract with ``episode_tick_steps``; Verne V0.5's
    first): its memory reads the camera frames of every ``tick_steps``-th executed step.

    Steps are the robot's executed actions from the episode's first request (step 0); a wait
    for a chunk doesn't advance them. Each tick's frames are sent ahead as soon as they are
    observed (``history_frame``, keyed by the step), so the server encodes them before the
    request that reads them. Each request names its step and how many requests the episode
    made before it (``RuntimeRequestContext.episode``), and carries the state of the step
    before it. ``clear`` starts a new episode.
    """

    sparse = True
    sends_ahead = True
    # The manual loop (next_action) sends ticks ahead too: the server needs every tick.
    pushes_ahead_in_steps = True
    # Keep an observation on every step (the run loop observes each one).
    state_steps = 1
    frames = 1

    def __init__(self, tick_steps: int, executed_per_chunk: int, seed: int = 0) -> None:
        if type(tick_steps) is not int or not 1 <= tick_steps <= 64:
            raise ValueError("episode ticks are every 1-64 executed steps")
        if type(executed_per_chunk) is not int or executed_per_chunk < 1:
            raise ValueError("a chunk executes at least one action")
        self.tick_steps = tick_steps
        self.executed_per_chunk = executed_per_chunk
        self.seed = seed
        self.clear()

    @property
    def tick(self) -> int:
        return self._step

    @property
    def observe_steps(self) -> range:
        return range(1, 2)

    def executed(self) -> None:
        """The robot executed one action of a chunk (a held step doesn't count)."""
        self._step += 1

    def send_key(self) -> int | None:
        """The key the observation of this step is sent ahead under (the step), once per tick
        after the episode's first request; None when this step's frames stay local."""
        step = self._step
        if not self._requested or step % self.tick_steps or step in self._sent:
            return None
        self._sent.add(step)
        while len(self._sent) > 64:
            self._sent.discard(min(self._sent))
        return step

    def push(self, observation: Any, at: float | None = None, key: int | None = None) -> None:
        if self._latest is not None and self._latest[0] < self._step:
            self._previous = self._latest
        self._latest = (self._step, observation)

    def window(self, observation: Any, at: float | None = None) -> Any:
        previous = observation
        if self._previous is not None and self._previous[0] == self._step - 1:
            previous = self._previous[1]
        elif self._latest is not None and self._latest[0] == self._step - 1:
            previous = self._latest[1]
        return EpisodeObservation(observation, previous, self._step)

    def predict_window(self, observation: Any) -> EpisodeObservation:
        """A raw ``predict()`` call: the robot ran every executed action of each earlier chunk
        (the step advances by them), unless a loop counted its steps itself."""
        self._step = max(self._step, self._chunks * self.executed_per_chunk)
        return self.window(observation)

    @property
    def requested(self) -> bool:
        """Whether this episode has sent a request (``predict()`` or a step's)."""
        return self._requested

    def take_chunk(self) -> int:
        """The request about to be sent: its count in the episode (the server's noise draw)."""
        self._requested = True
        chunk = self._chunks
        self._chunks += 1
        return chunk

    def clear(self) -> None:
        self._step = 0
        self._chunks = 0
        self._requested = False
        self._sent: set[int] = set()
        self._latest: tuple[int, Any] | None = None
        self._previous: tuple[int, Any] | None = None

    def hold(self, start: float, end: float) -> None:
        """A wait for a chunk advances no step."""

    def begin_motion(self, at: float | None = None) -> None:
        """Steps count executed actions from the episode's first request."""


def history_ticks(history: Any) -> int:
    """How many ticks before an observation its window reads: ``policy.contract``'s
    ``past_observations`` (0 without a window)."""
    if isinstance(history, TickHistory):
        return history.offsets[0]
    if not isinstance(history, ObservationHistory):
        return 0
    if history.sparse:
        return max((*history.offsets, history.state_steps))
    return history.frames - 1


def window_from_ticks(history: Any, observation: Any, past: Any) -> tuple[Any, int]:
    """``predict(past_observations=)``: ``observation`` with the window ``history``'s rules
    build from the given ticks (oldest first, one per control tick, ending just before it),
    and how many of the ticks it reads were filled in. Stateless: a fresh window of the same
    kind, the ticks placed one period apart, so episode-start padding applies exactly as
    in ``next_action()``'s windows; a caller who passes fewer ticks gets that padding."""
    need = history_ticks(history)
    if not need:
        return observation, 0
    ticks = list(past or ())[-need:]
    if isinstance(history, TickHistory):
        # One past observation per executed tick: the observation is tick len(ticks) of a
        # fresh episode, so offsets past its start are left out (black on the server) or,
        # with ``start``, its first tick sent once.
        episode = TickHistory(history.offsets, start=history.start)
        for tick in ticks:
            episode.push(tick)
            episode.executed()
        return episode.window(observation), need - len(ticks)
    fresh = (
        ObservationHistory.at_offsets(
            history.offsets, history.period_s, state_steps=history.state_steps
        )
        if history.sparse
        else ObservationHistory(history.frames, history.period_s)
    )
    now = 0.0
    for age, tick in zip(range(len(ticks), 0, -1), ticks, strict=True):
        fresh.push(tick, at=now - age * history.period_s)
    return fresh.window(observation, at=now), need - len(ticks)
