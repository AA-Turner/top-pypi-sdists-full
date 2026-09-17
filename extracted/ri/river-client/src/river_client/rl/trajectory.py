"""Token-exact trajectories. Messages are an inspection/environment view only."""

from __future__ import annotations

import base64
import copy
import math
import uuid
from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np

from river_client.images import ImageHandle
from river_client.renderers import ModelInputChunk
from river_client.types import PolicyVersion, Sample


def encode_state(value):
    """JSON-safe encoding, including image bytes in messages and environment state."""
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
    kv_cache_policy_version: PolicyVersion | None
    retained_kv: bool
    routing_handle: str | None
    routing_num_tokens: int | None
    run: int
    logprobs: np.ndarray | None
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
        retained_kv=False,
        kv_cache_policy_version=None,
        routing_handle=None,
        routing_num_tokens=None,
    ):
        if isinstance(kv_cache_policy_version, dict):
            kv_cache_policy_version = PolicyVersion(**kv_cache_policy_version)
        if isinstance(policy_version, dict):
            policy_version = PolicyVersion(**policy_version)
        if kind not in {"prompt", "generated", "framing"} or run < 0:
            raise ValueError("invalid span kind or run")
        stored = []
        for chunk in chunks:
            if chunk["type"] == "text":
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
                ids = np.array(ids, dtype=np.int32, copy=True)
                ids.flags.writeable = False
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
        lp = None
        if kind == "generated":
            if policy_step is None or policy_step < 0:
                raise ValueError("generated spans require a nonnegative policy_step")
            lp = np.array(logprobs, dtype=np.float32, copy=True)
            if lp.shape != (n,) or not np.all(np.isfinite(lp)):
                raise ValueError("generated tokens require one finite logprob each")
            lp.flags.writeable = False
        elif logprobs is not None or policy_step is not None:
            raise ValueError("only generated spans carry logprobs and policy_step")
        for name, value in (
            ("kind", kind),
            ("_chunks", tuple(stored)),
            ("logprobs", lp),
            ("policy_step", policy_step),
            ("policy_version", policy_version),
            ("kv_cache_policy_version", kv_cache_policy_version),
            ("retained_kv", retained_kv),
            ("routing_handle", routing_handle),
            ("routing_num_tokens", routing_num_tokens),
            ("run", run),
        ):
            object.__setattr__(self, name, value)

    @property
    def chunks(self) -> list[ModelInputChunk]:
        return [
            {**c, "tokens": c["tokens"].tolist()} if c["type"] == "text" else dict(c)
            for c in self._chunks
        ]

    def __len__(self):
        return sum(
            len(c["tokens"]) if c["type"] == "text" else c["expected_tokens"]
            for c in self._chunks
        )

    def state_dict(self):
        return {
            "kind": self.kind,
            "chunks": self.chunks,
            "logprobs": None if self.logprobs is None else self.logprobs.tolist(),
            "policy_step": self.policy_step,
            "retained_kv": self.retained_kv,
            "routing_handle": self.routing_handle,
            "routing_num_tokens": self.routing_num_tokens,
            "kv_cache_policy_version": None
            if self.kv_cache_policy_version is None
            else asdict(self.kv_cache_policy_version),
            "policy_version": None
            if self.policy_version is None
            else asdict(self.policy_version),
            "run": self.run,
        }


class Trajectory:
    """Append-only spans, split into independent conditioning runs by ``rewrite``.

    Generated ids never pass through a renderer. ``messages`` and ``final_text``
    may be decoded for tools, rewards and inspection, but never for training.
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
                policy_step=sample.model_step if policy_step is None else policy_step,
                run=self.run,
                policy_version=sample.policy_version,
                retained_kv=sample.retained_kv,
                kv_cache_policy_version=sample.kv_cache_policy_version,
                routing_handle=routing.handle if routing else None,
                routing_num_tokens=routing.num_tokens if routing else None,
            )
        )

    def append_framing(self, chunks: list[ModelInputChunk]):
        self._spans.append(Span("framing", chunks, run=self.run))

    def rewrite(self, messages, *, chunks: list[ModelInputChunk]):
        """Explicit compaction: preserve old runs and start a new datum.

        Supply freshly rendered chunks for the rewritten messages. This costs a
        full prefix-cache miss; it cannot retroactively change earlier samples.
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
    ) -> list[dict]:
        if not math.isfinite(advantage):
            raise ValueError("advantage must be finite")
        if max_staleness is not None and (max_staleness < 0 or current_step is None):
            raise ValueError(
                "staleness masking needs current_step and a nonnegative limit"
            )
        data = []
        for run in range(self.run + 1):
            spans = [s for s in self._spans if s.run == run]
            generated = [i for i, s in enumerate(spans) if s.kind == "generated"]
            if not generated:
                continue
            spans = spans[: generated[-1] + 1]
            n = sum(map(len, spans))
            old = np.zeros(n, dtype=np.float32)
            adv = np.zeros(n, dtype=np.float32)
            offset = 0
            for span in spans:
                if span.kind == "generated":
                    if offset == 0:
                        raise ValueError("generated tokens need a conditioning prefix")
                    old[offset - 1 : offset + len(span) - 1] = span.logprobs
                    age = 0 if current_step is None else current_step - span.policy_step
                    if age < 0:
                        raise ValueError(
                            "trajectory contains a policy step newer than the trainer"
                        )
                    if max_staleness is None or age <= max_staleness:
                        adv[offset - 1 : offset + len(span) - 1] = advantage
                offset += len(span)
            chunks = [c for s in spans for c in s.chunks]
            datum = {"old_logprobs": old.tolist(), "advantages": adv.tolist()}
            if any(c["type"] == "image" for c in chunks):
                datum["model_input"] = chunks
            else:
                datum["input_ids"] = [t for c in chunks for t in c["tokens"]]
                datum["attention_mask"] = [1] * n
            last = spans[-1]
            if last.routing_handle is not None and any(
                last is s for s in self._spans[: self._routing_recovery_start]
            ):
                datum["_rl_recovered_routing"] = True
            elif last.routing_handle is not None:
                if last.routing_num_tokens != n - 1:
                    raise ValueError(
                        "routing handle does not align with the training datum"
                    )
                datum["expert_routing_handle"] = last.routing_handle.encode("utf-8")
            elif any(s.routing_handle is not None for s in spans):
                raise ValueError("routing disappeared before the final sampled segment")
            data.append(datum)
        return data

    def state_dict(self):
        return encode_state(
            {
                "version": 1,
                "spans": [s.state_dict() for s in self._spans],
                **{k: v for k, v in vars(self).items() if k != "_spans"},
            }
        )

    @classmethod
    def from_state_dict(cls, state, *, recovering=False):
        state = decode_state(copy.deepcopy(state))
        if state.pop("version") != 1:
            raise ValueError("unsupported trajectory state version")
        spans = [Span(**s) for s in state.pop("spans")]
        if not spans or spans[0].kind != "prompt" or spans[0].run != 0:
            raise ValueError("trajectory state must start with a prompt in run zero")
        previous = 0
        for s in spans[1:]:
            if s.run not in (previous, previous + 1) or (s.run != previous) != (
                s.kind == "prompt"
            ):
                raise ValueError("invalid trajectory run boundary")
            previous = s.run
        result = cls(spans[0].chunks, id=state.get("id"))
        result.__dict__.update(state)
        result._spans = spans
        if recovering:
            result._routing_recovery_start = len(spans)
        return result
