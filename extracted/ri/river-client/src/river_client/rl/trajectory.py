"""Token-exact trajectories. Messages are an inspection/environment view only."""

from __future__ import annotations

import base64
import copy
import math
import threading
import uuid
import warnings
import weakref
from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np

from river_client.images import ImageHandle
from river_client.renderers import ModelInputChunk
from river_client.types import PolicySpan, PolicyVersion, Sample


from .requirements import LossRequirements


_RECOVERING_UNSET = object()


def _readonly_array(value, dtype):
    if (
        isinstance(value, np.ndarray)
        and value.dtype == dtype
        and value.flags.c_contiguous
        and not value.flags.writeable
    ):
        return value
    array = np.array(value, dtype=dtype, copy=True, order="C")
    array.flags.writeable = False
    return array


# Span arrays that a checkpoint may move to disk once committed.
_SPAN_ARRAYS = (
    "logprobs",
    "sampler_topk_ids",
    "sampler_topk_logprobs",
    "sampling_log_masses",
)


class _Spilled:
    """A read-only array stored in a checkpoint segment and read on access.

    ``holder`` names the segment record and reads from it; ``offset`` is
    relative to that record, so compaction can move the record by updating
    only the holder.
    """

    __slots__ = ("holder", "offset", "shape", "dtype")

    def __init__(self, holder, offset, shape, dtype):
        self.holder, self.offset = holder, offset
        self.shape, self.dtype = tuple(shape), np.dtype(dtype)

    def __len__(self):
        return self.shape[0]

    @property
    def nbytes(self):
        return math.prod(self.shape) * self.dtype.itemsize

    def read(self):
        return self.holder.read([self])[0]

    def __array__(self, dtype=None, copy=None):
        array = self.read()
        return array if dtype is None else array.astype(dtype)

    def __deepcopy__(self, memo):
        # The stored bytes never change; copies share them.
        return self

    def __reduce__(self):
        return self.read().__reduce__()

    def __repr__(self):
        return f"_Spilled(shape={self.shape}, dtype={self.dtype.str})"


def _materialized(value):
    return value.read() if isinstance(value, _Spilled) else value


def _spilled(value, shape, dtype):
    """Check a restored on-disk array's metadata against what a span needs."""
    if value.dtype != dtype or (
        len(value.shape) != 1 if shape is None else value.shape != shape
    ):
        raise ValueError("restored span array has the wrong shape or dtype")
    return value


def _spilled_or_array(value, shape, dtype):
    if isinstance(value, _Spilled):
        return _spilled(value, value.shape if shape is None else shape, dtype)
    array = _readonly_array(value, dtype)
    if shape is not None and array.shape != shape:
        raise ValueError("restored span array has the wrong shape or dtype")
    return array


def _read_spans(spans, *, topk):
    """Return private copies of ``spans`` with spilled arrays read.

    Each segment record is read once. Positions line up with ``spans``.
    Top-K candidates are read only if ``topk``.
    """
    names = _SPAN_ARRAYS if topk else ("logprobs", "sampling_log_masses")
    # A committing save may spill arrays concurrently: use one snapshot each.
    snapshots = [
        (dict(span.__dict__), [dict(c) for c in span._chunks]) for span in spans
    ]
    wanted = {}
    for values, chunks in snapshots:
        for value in (
            *(values[name] for name in names),
            *(c["tokens"] for c in chunks if c["type"] == "text"),
        ):
            if isinstance(value, _Spilled):
                wanted.setdefault(value.holder, []).append(value)
    arrays = {}
    for holder, values in wanted.items():
        arrays.update(zip(map(id, values), holder.read(values), strict=True))

    def resolved(value):
        return arrays.get(id(value), value) if isinstance(value, _Spilled) else value

    # Copies built from the snapshots, even of spans with nothing spilled yet:
    # a commit may replace a live span's arrays while the caller uses them.
    result = []
    for values, chunks in snapshots:
        for name in names:
            values[name] = resolved(values[name])
        values["_chunks"] = tuple(
            {**c, "tokens": resolved(c["tokens"])} if c["type"] == "text" else c
            for c in chunks
        )
        span = object.__new__(Span)
        span.__dict__.update(values)
        result.append(span)
    return result


def encode_state(value):
    """Encode image handles and bytes without copying numeric arrays."""
    if isinstance(value, ImageHandle):
        return {"__river_image_handle__": asdict(value)}
    if isinstance(value, bytes):
        return {"__river_bytes__": base64.b64encode(value).decode("ascii")}
    if isinstance(value, (list, tuple)):
        return [encode_state(item) for item in value]
    if isinstance(value, dict):
        return {key: encode_state(item) for key, item in value.items()}
    return value


def decode_state(value):
    if isinstance(value, dict):
        if set(value) == {"__river_image_handle__"}:
            return ImageHandle(**value["__river_image_handle__"])
        if set(value) == {"__river_bytes__"}:
            return base64.b64decode(value["__river_bytes__"], validate=True)
        return {key: decode_state(item) for key, item in value.items()}
    if isinstance(value, list):
        return [decode_state(item) for item in value]
    return value


@dataclass(frozen=True, init=False)
class Span:
    kind: Literal["prompt", "generated", "framing"]
    policy_step: int | None
    policy_version: PolicyVersion | None
    policy_spans: tuple[PolicySpan, ...]
    kv_cache_policy_version: PolicyVersion | None
    retained_kv: bool
    routing_handle: str | None
    routing_num_tokens: int | None
    run: int
    logprobs: np.ndarray | None
    sampler_topk_ids: np.ndarray | None
    sampler_topk_logprobs: np.ndarray | None
    sampling_log_masses: np.ndarray | None
    _chunks: tuple[dict, ...]

    def __init__(
        self,
        kind,
        chunks,
        *,
        logprobs=None,
        policy_step=None,
        run=0,
        policy_version=None,
        policy_spans=(),
        retained_kv=False,
        kv_cache_policy_version=None,
        routing_handle=None,
        routing_num_tokens=None,
        sampler_topk_ids=None,
        sampler_topk_logprobs=None,
        sampling_log_masses=None,
    ):
        if isinstance(kv_cache_policy_version, dict):
            kv_cache_policy_version = PolicyVersion(**kv_cache_policy_version)
        if isinstance(policy_version, dict):
            policy_version = PolicyVersion(**policy_version)
        if kind not in {"prompt", "generated", "framing"} or run < 0:
            raise ValueError("invalid span kind or run")
        policy_spans = tuple(
            PolicySpan(**span) if isinstance(span, dict) else span
            for span in policy_spans
        )
        stored = []
        for chunk in chunks:
            if chunk["type"] == "text" and isinstance(chunk["tokens"], _Spilled):
                # Restored from a checkpoint without reading it; values were
                # validated when the span was first built.
                stored.append(
                    {
                        "type": "text",
                        "tokens": _spilled(chunk["tokens"], None, np.int32),
                    }
                )
            elif chunk["type"] == "text":
                ids = np.asarray(chunk["tokens"])
                if ids.ndim != 1 or (
                    ids.size
                    and (
                        ids.dtype.kind not in "iu"
                        or np.any(ids < 0)
                        or np.any(ids > np.iinfo(np.int32).max)
                    )
                ):
                    raise ValueError(
                        "token ids must be one-dimensional nonnegative int32 values"
                    )
                ids = _readonly_array(ids, np.int32)
                stored.append({"type": "text", "tokens": ids})
            elif chunk["type"] == "image":
                if kind == "generated" or int(chunk["expected_tokens"]) <= 0:
                    raise ValueError(
                        "images must be conditioning chunks with positive expected_tokens"
                    )
                image = chunk["data"]
                stored.append(
                    {
                        **chunk,
                        "data": image
                        if isinstance(image, ImageHandle)
                        else bytes(image),
                    }
                )
            else:
                raise ValueError(f"unknown chunk type: {chunk['type']}")
        n = sum(
            len(c["tokens"]) if c["type"] == "text" else c["expected_tokens"]
            for c in stored
        )
        if n == 0:
            raise ValueError("spans must contain at least one token")
        if policy_spans:
            ends = [0, *(span.end for span in policy_spans)]
            if ends[-1] != n or any(a >= b for a, b in zip(ends, ends[1:])):
                raise ValueError("policy spans must cover generated tokens in order")
            if kind != "generated" or policy_version != policy_spans[0].policy_version:
                raise ValueError(
                    "the summary policy must be the first generated-token policy"
                )
        lp = None
        if kind == "generated":
            if policy_step is None or policy_step < 0:
                raise ValueError("generated spans require a nonnegative policy_step")
            if isinstance(logprobs, _Spilled):
                lp = _spilled(logprobs, (n,), np.float32)
            else:
                lp = _readonly_array(logprobs, np.float32)
                if lp.shape != (n,) or not np.all(np.isfinite(lp)):
                    raise ValueError("generated tokens require one finite logprob each")
        elif logprobs is not None or policy_step is not None:
            raise ValueError("only generated spans carry logprobs and policy_step")
        head_ids = head_lp = None
        if (sampler_topk_ids is None) != (sampler_topk_logprobs is None):
            raise ValueError("top-k IDs and logprobs must be supplied together")
        if isinstance(sampler_topk_ids, _Spilled) or isinstance(
            sampler_topk_logprobs, _Spilled
        ):
            if sampler_topk_ids is None or sampler_topk_logprobs is None:
                raise ValueError("top-k IDs and logprobs must be supplied together")
            source = (
                sampler_topk_ids
                if isinstance(sampler_topk_ids, _Spilled)
                else np.asarray(sampler_topk_ids)
            )
            if kind != "generated" or len(source.shape) != 2:
                raise ValueError(
                    "top-k arrays must have matching [generated tokens, K] shapes"
                )
            shape = (n, source.shape[1])
            head_ids = _spilled_or_array(sampler_topk_ids, shape, np.int32)
            head_lp = _spilled_or_array(sampler_topk_logprobs, shape, np.float32)
        elif sampler_topk_ids is not None:
            ids = np.asarray(sampler_topk_ids)
            head_lp = _readonly_array(sampler_topk_logprobs, np.float32)
            if (
                kind != "generated"
                or ids.ndim != 2
                or ids.shape[0] != n
                or ids.shape[1] < 1
                or head_lp.shape != ids.shape
            ):
                raise ValueError(
                    "top-k arrays must have matching [generated tokens, K] shapes"
                )
            # Never narrow caller-supplied ID arrays; wire/checkpoint arrays are
            # int32. Lists (such as JSON-restored state) carry no dtype, so they
            # convert when every value fits.
            limits = np.iinfo(np.int32)
            if ids.dtype.kind not in "iu" or not (
                np.can_cast(ids.dtype, np.int32, casting="safe")
                or (
                    not isinstance(sampler_topk_ids, np.ndarray)
                    and limits.min <= ids.min()
                    and ids.max() <= limits.max
                )
            ):
                raise ValueError("top-k ID dtype must convert losslessly to int32")
            head_ids = _readonly_array(ids, np.int32)
        masses = None
        if sampling_log_masses is not None:
            masses = _spilled_or_array(sampling_log_masses, None, np.float32)
            if kind != "generated" or masses.shape != (n,):
                raise ValueError("generated tokens require one sampling log mass each")
        for name, value in (
            ("kind", kind),
            ("_chunks", tuple(stored)),
            ("logprobs", lp),
            ("sampler_topk_ids", head_ids),
            ("sampler_topk_logprobs", head_lp),
            ("sampling_log_masses", masses),
            ("policy_step", policy_step),
            ("policy_version", policy_version),
            ("policy_spans", policy_spans),
            ("kv_cache_policy_version", kv_cache_policy_version),
            ("retained_kv", retained_kv),
            ("routing_handle", routing_handle),
            ("routing_num_tokens", routing_num_tokens),
            ("run", run),
        ):
            # Bypass the frozen dataclass and the read-on-access properties.
            self.__dict__[name] = value

    @property
    def chunks(self) -> list[ModelInputChunk]:
        return [
            {**c, "tokens": _materialized(c["tokens"]).tolist()}
            if c["type"] == "text"
            else dict(c)
            for c in self._chunks
        ]

    def _chunk_arrays(self):
        return [
            {**c, "tokens": _materialized(c["tokens"])}
            if c["type"] == "text"
            else dict(c)
            for c in self._chunks
        ]

    def _with_policy_step(self, policy_step):
        """Return this span stamped with ``policy_step``, sharing its arrays."""
        if policy_step < 0:
            raise ValueError("generated spans require a nonnegative policy_step")
        span = object.__new__(Span)
        span.__dict__.update(self.__dict__, policy_step=policy_step)
        return span

    def __len__(self):
        return sum(
            len(c["tokens"]) if c["type"] == "text" else c["expected_tokens"]
            for c in self._chunks
        )

    def state_dict(self):
        return self._state(read=True)

    def _state(self, *, read):
        """Return span state; without ``read``, spilled arrays stay references."""
        values = self.__dict__
        array = _materialized if read else (lambda value: value)
        return encode_state(
            {
                **(
                    {
                        "sampler_topk_ids": array(values["sampler_topk_ids"]),
                        "sampler_topk_logprobs": array(values["sampler_topk_logprobs"]),
                    }
                    if values["sampler_topk_ids"] is not None
                    else {}
                ),
                **(
                    {"sampling_log_masses": array(values["sampling_log_masses"])}
                    if values["sampling_log_masses"] is not None
                    else {}
                ),
                "kind": self.kind,
                # Token and logprob arrays are immutable; share them uncopied.
                "chunks": [
                    {**c, "tokens": array(c["tokens"])}
                    if c["type"] == "text"
                    else dict(c)
                    for c in self._chunks
                ],
                "logprobs": array(values["logprobs"]),
                "policy_step": self.policy_step,
                "retained_kv": self.retained_kv,
                "routing_handle": self.routing_handle,
                "routing_num_tokens": self.routing_num_tokens,
                "kv_cache_policy_version": None
                if self.kv_cache_policy_version is None
                else asdict(self.kv_cache_policy_version),
                "policy_spans": [asdict(span) for span in self.policy_spans],
                "policy_version": None
                if self.policy_version is None
                else asdict(self.policy_version),
                "run": self.run,
            }
        )


def _span_array(name):
    def get(span):
        return _materialized(span.__dict__[name])

    return property(get, doc=f"The span's {name} array, read from disk if spilled.")


# A checkpoint replaces committed arrays with ``_Spilled`` references to save
# memory; these properties keep reading them as ordinary arrays.
for _name in _SPAN_ARRAYS:
    setattr(Span, _name, _span_array(_name))
del _name


# The checkpoint records each restored trajectory came from, keyed by the
# trajectory: (store's record handle, its span list, its messages list).
_RESTORED_KEY = "__river_restored__"
_RESTORED = weakref.WeakKeyDictionary()
# Trainers in one process restore and save concurrently.
_RESTORED_LOCK = threading.Lock()


class Trajectory:
    """A rollout's conversation, exact model inputs, and generated spans.

    The ``messages`` and ``final_text`` views support tools, rewards, and
    inspection. Training uses the recorded token spans, preserving the exact
    inputs and outputs sampled by the model. ``rewrite`` starts a new
    conditioning run when the conversation must be compacted.

    ``loss_mask_end`` limits which generated tokens train. When an environment
    sets it, generated tokens at or past that offset (counted over every
    generated span in order, across runs) stay in the training input as
    context but get zero advantage. An environment that cuts a turn short, for
    example at the start of a degenerate repetition loop, sets it where the cut
    falls, so the reward trains the tokens that led there and not the tail that
    still has to be fed back for expert-routing replay.

    ``active_turn_max_tokens`` is engine state: the cap from the
    ``TurnResult`` whose continuation the engine accepted, kept until that
    turn ends so it survives a checkpoint taken mid-turn.
    """

    def __init__(self, chunks: list[ModelInputChunk], *, messages=None, id=None):
        self.id = id or uuid.uuid4().hex
        self._kv_cache_group = self.id
        self._kv_cache_start = 0
        self._routing_recovery_start = 0
        self._spans = [Span("prompt", chunks)]
        self.messages = copy.deepcopy(messages or [])
        self.final_text = ""
        self.last_stop_reason = ""
        self.reward: float | None = None
        self.failure: dict[str, str] | None = None
        self.truncated: str | None = None
        self.done = False
        self.turns = 0
        self.metrics: dict[str, float] = {}
        # Engine continuation state is stored with the trajectory, including
        # unfinished assistant segments, so recovery does not repeat a turn.
        self.pending_tokens: list[int] = []
        self.phase = "sample"
        self.elapsed = 0.0
        self.wrap_up = False
        self.sample_index = 0
        self.loss_mask_end: int | None = None
        self.active_turn_max_tokens: int | None = None

    @property
    def dropped(self) -> bool:
        """Whether error handling ended this rollout without a reward.

        Dropped trajectories are terminal (``done``) but never train. ``failure``
        records the operation, exception type, and message for diagnostics.
        The persisted terminal phase prevents resume from replaying them.
        """
        return self.phase == "dropped"

    @property
    def spans(self) -> tuple[Span, ...]:
        return tuple(self._spans)

    @property
    def run(self) -> int:
        return self._spans[-1].run

    @property
    def generated_tokens(self) -> int:
        return sum(len(s) for s in self._spans if s.kind == "generated")

    @property
    def context_tokens(self) -> int:
        return sum(len(s) for s in self._spans if s.run == self.run)

    def model_input(self) -> list[ModelInputChunk]:
        return [c for s in self._spans if s.run == self.run for c in s.chunks]

    def prompt_ids(self) -> list[int]:
        chunks = self.model_input()
        if any(c["type"] != "text" for c in chunks):
            raise ValueError(
                "image trajectories must use model_input(), not prompt_ids()"
            )
        return [t for c in chunks for t in c["tokens"]]

    def append_span(self, sample: Sample, *, policy_step: int | None = None):
        if self.done:
            raise ValueError("cannot append to a completed trajectory")
        if not sample.token_data_is_exact:
            raise ValueError(
                "RL requires native token ids and complete sampled logprobs; legacy reconstruction is unsafe"
            )
        routing = sample.expert_routing
        previous = next(
            (s for s in reversed(self._spans) if s.kind == "generated"), None
        )
        if previous is not None and (previous.routing_handle is not None) != (
            routing is not None
        ):
            raise ValueError(
                "routing capture must be consistent throughout a trajectory"
            )
        if routing is not None and (
            not routing.handle
            or routing.num_tokens != self.context_tokens + len(sample.tokens) - 1
        ):
            raise ValueError(
                "routing handle must cover the complete sampled prefix (n-1 tokens)"
            )
        self._spans.append(
            Span(
                "generated",
                [{"type": "text", "tokens": sample.tokens}],
                logprobs=sample.logprobs,
                sampler_topk_ids=(
                    sample.top_logprobs.token_ids
                    if sample.top_logprobs is not None
                    else None
                ),
                sampler_topk_logprobs=(
                    sample.top_logprobs.logprobs
                    if sample.top_logprobs is not None
                    else None
                ),
                sampling_log_masses=sample.sampling_log_masses,
                policy_step=sample.model_step if policy_step is None else policy_step,
                run=self.run,
                policy_version=sample.policy_version,
                policy_spans=sample.policy_spans,
                retained_kv=sample.retained_kv,
                kv_cache_policy_version=sample.kv_cache_policy_version,
                routing_handle=routing.handle if routing else None,
                routing_num_tokens=routing.num_tokens if routing else None,
            )
        )

    def append_framing(self, chunks: list[ModelInputChunk]):
        self._spans.append(Span("framing", chunks, run=self.run))

    def rewrite(self, messages, *, chunks: list[ModelInputChunk]):
        """Replace conversation context while retaining earlier training spans.

        Supply freshly rendered chunks for the replacement messages. The next
        model turn must prefill this new context; earlier samples are unchanged.
        """
        self._spans.append(Span("prompt", chunks, run=self.run + 1))
        self.messages = copy.deepcopy(messages)
        self.metrics["compactions"] = self.metrics.get("compactions", 0) + 1
        self.metrics["cache_miss_tokens"] = (
            self.metrics.get("cache_miss_tokens", 0) + self.context_tokens
        )

    def to_data(
        self,
        advantage: float,
        *,
        current_step: int | None = None,
        max_staleness: int | None = None,
        requirements: LossRequirements | None = None,
    ) -> list[dict]:
        """Return one training datum per conditioning run.

        Token ids, attention masks, behavior logprobs, advantages, and
        sampling log masses are NumPy arrays. Text chunks in ``model_input``
        share the trajectory's read-only token arrays.
        """
        return self._data(
            advantage,
            current_step=current_step,
            max_staleness=max_staleness,
            requirements=requirements,
        )[0]

    def _datum_source(self):
        """A copy of the fields training datums are built from.

        It shares the span list and its read-only arrays, and omits messages
        and other rollout state, so a batch can keep it cheaply until it is
        encoded. Each batch item names its run, and spans are only appended
        to a trajectory or replaced as a list (``_apply_policy_provenance``),
        never edited in place, so the datums it builds stay the same.
        """
        source = object.__new__(Trajectory)
        source.__dict__.update(
            phase=self.phase,
            loss_mask_end=self.loss_mask_end,
            _spans=self._spans,
            _routing_recovery_start=self._routing_recovery_start,
        )
        return source

    def _check_data(self, advantage, current_step, max_staleness):
        if self.dropped:
            raise ValueError("dropped trajectories cannot enter training")
        if not math.isfinite(advantage):
            raise ValueError("advantage must be finite")
        if max_staleness is not None and (max_staleness < 0 or current_step is None):
            raise ValueError(
                "staleness masking needs current_step and a nonnegative limit"
            )
        mask_end = self.loss_mask_end
        if mask_end is not None and (
            type(mask_end) is not int or mask_end < 0  # bool is not an offset
        ):
            raise ValueError("loss_mask_end must be a nonnegative token offset")

    def _runs(self):
        """Each run with generated tokens: its trained spans' indices, in order.

        A run's datum ends at its last generated span.
        """
        runs = {}
        for index, span in enumerate(self._spans):
            runs.setdefault(span.run, []).append(index)
        result = []
        for run in sorted(runs):
            indices = runs[run]
            generated = [
                i
                for i, index in enumerate(indices)
                if self._spans[index].kind == "generated"
            ]
            if generated:
                result.append((run, indices[: generated[-1] + 1]))
        return result

    def _layout(self, *, current_step=None, max_staleness=None):
        """Describe each datum ``_data`` returns without reading any arrays.

        Returns ``(run, length, trained, routing_handle, recovered)`` per
        datum: its input length, how many positions get the advantage (the
        loss mask's sum), and whether its last span has a routing capture or
        is restored from a checkpoint.
        """
        self._check_data(0.0, current_step, max_staleness)
        mask_end, generated_before, layout = self.loss_mask_end, 0, []
        for run, indices in self._runs():
            length = trained = 0
            for index in indices:
                span = self._spans[index]
                if span.kind == "generated":
                    if length == 0:
                        raise ValueError("generated tokens need a conditioning prefix")
                    age = 0 if current_step is None else current_step - span.policy_step
                    if age < 0:
                        raise ValueError(
                            "trajectory contains a policy step newer than the trainer"
                        )
                    if max_staleness is None or age <= max_staleness:
                        keep = len(span)
                        if mask_end is not None:
                            keep = max(0, min(keep, mask_end - generated_before))
                        trained += keep
                    generated_before += len(span)
                length += len(span)
            last = indices[-1]
            layout.append(
                (
                    run,
                    length,
                    trained,
                    self._spans[last].routing_handle is not None,
                    last < self._routing_recovery_start,
                )
            )
        return layout

    def _data(
        self,
        advantage,
        *,
        current_step=None,
        max_staleness=None,
        requirements=None,
        masks=False,
        runs=None,
    ):
        """Return ``to_data`` datums and, optionally, each datum's loss mask.

        The mask is 1.0 at every position that ``to_data`` would assign an
        advantage to, independent of the advantage's value. ``runs`` limits
        the datums to those runs; only their spans' arrays are read.
        """
        self._check_data(advantage, current_step, max_staleness)
        mask_end = self.loss_mask_end
        data, loss_masks = [], []
        selected = [
            (run, indices)
            for run, indices in self._runs()
            if runs is None or run in runs
        ]
        # Read spilled arrays once per segment record rather than per span.
        wanted = [index for _, indices in selected for index in indices]
        read = dict(
            zip(
                wanted,
                _read_spans(
                    [self._spans[index] for index in wanted],
                    topk=requirements is not None
                    and requirements.top_logprobs is not None,
                ),
                strict=True,
            )
        )
        for run, indices in selected:
            # Generated tokens in earlier spans, across runs.
            generated_before = sum(
                len(span)
                for span in self._spans
                if span.kind == "generated" and span.run < run
            )
            recovered = indices[-1] < self._routing_recovery_start
            spans = [read[index] for index in indices]
            n = sum(map(len, spans))
            with_masses = {
                s.sampling_log_masses is not None
                for s in spans
                if s.kind == "generated"
            }
            if len(with_masses) > 1:
                raise ValueError(
                    "sampling log masses must cover every generated span or none"
                )
            masses = np.zeros(n, dtype=np.float32) if True in with_masses else None
            old = np.zeros(n, dtype=np.float32)
            adv = np.zeros(n, dtype=np.float32)
            mask = np.zeros(n, dtype=np.float32) if masks else None
            metadata = {}
            if requirements is not None:
                if requirements.policy_age:
                    if current_step is None:
                        raise ValueError("policy ages require current_step")
                    metadata["policy_age_steps"] = np.zeros(n, dtype=np.int64)
                width = requirements.top_logprobs
                if width is not None:
                    if any(
                        s.sampler_topk_ids is None
                        or s.sampler_topk_ids.shape[1] != width
                        for s in spans
                        if s.kind == "generated"
                    ):
                        raise ValueError(
                            "every generated span must carry the required top-K width"
                        )
                    id_dtype = np.result_type(
                        *(
                            s.sampler_topk_ids.dtype
                            for s in spans
                            if s.kind == "generated"
                        )
                    )
                    metadata["sampler_topk_ids"] = np.zeros((n, width), dtype=id_dtype)
                    metadata["sampler_topk_logprobs"] = np.zeros(
                        (n, width), dtype=np.float32
                    )
            offset = 0
            for span in spans:
                if span.kind == "generated":
                    if offset == 0:
                        raise ValueError("generated tokens need a conditioning prefix")
                    old[offset - 1 : offset + len(span) - 1] = span.logprobs
                    if masses is not None:
                        masses[offset - 1 : offset + len(span) - 1] = (
                            span.sampling_log_masses
                        )
                    age = 0 if current_step is None else current_step - span.policy_step
                    if age < 0:
                        raise ValueError(
                            "trajectory contains a policy step newer than the trainer"
                        )
                    positions = slice(offset - 1, offset + len(span) - 1)
                    if "policy_age_steps" in metadata:
                        metadata["policy_age_steps"][positions] = age
                        start = offset - 1
                        for policy_span in span.policy_spans:
                            policy = policy_span.policy_version
                            if policy.lineage_id != span.policy_version.lineage_id:
                                raise ValueError("policy spans must share a lineage")
                            token_age = age - (policy.step - span.policy_version.step)
                            if token_age < 0:
                                raise ValueError(
                                    "trajectory contains a policy step newer than the trainer"
                                )
                            end = offset - 1 + policy_span.end
                            metadata["policy_age_steps"][start:end] = token_age
                            start = end
                    if "sampler_topk_ids" in metadata:
                        metadata["sampler_topk_ids"][positions] = span.sampler_topk_ids
                        metadata["sampler_topk_logprobs"][positions] = (
                            span.sampler_topk_logprobs
                        )
                    if max_staleness is None or age <= max_staleness:
                        keep = len(span)
                        if mask_end is not None:
                            keep = max(0, min(keep, mask_end - generated_before))
                        adv[offset - 1 : offset - 1 + keep] = advantage
                        if mask is not None:
                            mask[offset - 1 : offset - 1 + keep] = 1.0
                    generated_before += len(span)
                offset += len(span)
            chunks = [dict(c) for s in spans for c in s._chunks]
            datum = {"old_logprobs": old, "advantages": adv}
            if masses is not None:
                datum["sampling_log_masses"] = masses
            if metadata:
                datum["sampling_metadata"] = metadata
            if any(c["type"] == "image" for c in chunks):
                datum["model_input"] = chunks
            else:
                # int64 matches the wire dtype the client gives integer lists.
                datum["input_ids"] = np.concatenate(
                    [c["tokens"] for c in chunks], dtype=np.int64
                )
                datum["attention_mask"] = np.ones(n, dtype=np.int64)
            last = spans[-1]
            if recovered:
                datum["_rl_recovered_routing"] = True
            if last.routing_handle is not None:
                if last.routing_num_tokens != n - 1:
                    raise ValueError(
                        "routing handle does not align with the training datum"
                    )
                datum["expert_routing_handle"] = last.routing_handle.encode("utf-8")
            elif any(s.routing_handle is not None for s in spans):
                raise ValueError("routing disappeared before the final sampled segment")
            data.append(datum)
            loss_masks.append(mask)
        return data, loss_masks

    def state_dict(self):
        """Return recoverable state for ``from_state_dict``.

        Token ids, logprobs, and sampler candidates are the span's read-only
        NumPy arrays, shared rather than copied, so the state is not plain
        JSON. Checkpoints store these arrays in a binary sidecar.
        """
        return encode_state(
            {
                "version": 1,
                "spans": [s.state_dict() for s in self._spans],
                **{k: v for k, v in vars(self).items() if k != "_spans"},
            }
        )

    @classmethod
    def from_state_dict(cls, state, *, recovering=_RECOVERING_UNSET):
        restored = None
        if isinstance(state, dict) and _RESTORED_KEY in state:
            state = dict(state)
            restored = state.pop(_RESTORED_KEY)
        result = cls._from_state_dict(state, recovering)
        if restored is not None:
            # A checkpoint store adopts these records on its next save
            # instead of writing the restored history again.
            with _RESTORED_LOCK:
                _RESTORED[result] = (restored, result._spans, result.messages)
        return result

    @classmethod
    def _from_state_dict(cls, state, recovering):
        if recovering is not _RECOVERING_UNSET:
            warnings.warn(
                "Trajectory.from_state_dict(recovering=...) is deprecated and ignored; "
                "saved routing captures are reused whenever available.",
                DeprecationWarning,
                stacklevel=3,
            )
        state = decode_state(state)
        if state.pop("version") != 1:
            raise ValueError("unsupported trajectory state version")
        spans = [Span(**s) for s in state.pop("spans")]
        state = copy.deepcopy(state)
        if not spans or spans[0].kind != "prompt" or spans[0].run != 0:
            raise ValueError("trajectory state must start with a prompt in run zero")
        previous = 0
        for s in spans[1:]:
            if s.run not in (previous, previous + 1) or (s.run != previous) != (
                s.kind == "prompt"
            ):
                raise ValueError("invalid trajectory run boundary")
            previous = s.run
        result = cls(list(spans[0]._chunks), id=state.get("id"))
        result.__dict__.update(state)
        result._spans = spans
        return result
