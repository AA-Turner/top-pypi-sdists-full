# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The robot's data plane on serve(): its observations as it makes them (POST /observe), its acts after them (POST /act
{"call": "act", "episode_id", "seq"}) and its episodes' ends (POST /act/episode_end), on its stream (GET /stream,
engine.stream_intake) - the same messages, answers and refusals as a worker of the hosted platform's, from the same
modules: engine.stream keeps each episode's observations in order, engine.obs_format turns each sequence_ai.Video, Depth
and Tactile back. A robot's client is the same either way; only the address it connects to differs.

    plane = DataPlane()
    status, body, kind = await plane.observe(raw, content_type)          # a post: {"through": n}, or a refusal
    observation = await plane.act(call)                                   # the newest, once the ones before are in

In one sentence: a post's frames - msgpack or JSON, sequence_base.contract.observe.ObserveRequest - have what the robot
compressed turned back and are kept by episode, in order (StreamStore.put), answered {"through": how far the episode is
whole} → each whole frame goes on, in order, to the copy here (StreamStore.forward → _Copy.observe), which turns its
marked items back on a thread of its own and keeps it as the episode's newest → an act, which names its episode and how
many observations came before it, waits until each of them reached the copy, STREAM_WAIT_S at most (StreamStore.before)
→ the policy is called on the newest → one that never comes refuses the act 409 conflict, details.reason
frames_missing and details.from the first missing, which the robot sends again from there.

Every refusal is the platform's ErrorBody (sequence_base.contract.errors): {detail, code, retryable, retry_after_s,
request_id, hint, details}, with its code's status, as a robot's client reads any worker's.

Needs sequence-base (installed on Python 3.10 and later); a marked item needs its codecs too
(sequence-ai installs them on Python 3.10 or later).
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import json
from typing import Any, Callable, Optional

from sequence_base.codec import blocks as _blocks
from sequence_base.codec import compressed as _compressed
from sequence_base.constants.limits import MAX_STREAM_BYTES
from sequence_base.contract.errors import ERRORS, ErrorBody, ErrorCode
from sequence_base.contract.observe import FRAMES_MISSING, FRAMES_OVER_LIMIT, ObserveRequest

from ..network import msgpack_io
from . import obs_format
from .stream import StreamError, StreamStore

__all__ = ["DataPlane", "Refused"]

_JSON = "application/json"


class Refused(Exception):
    """A post, an act or an episode's end the data plane refuses: the ErrorBody it is answered with, and its status."""

    def __init__(self, code: "ErrorCode | str", detail: str, *, details: Optional[dict] = None,
                 retry_after_s: Optional[float] = None) -> None:
        super().__init__(detail)
        self.code = code if isinstance(code, ErrorCode) else ErrorCode[code]
        self.details, self.retry_after_s = details or {}, retry_after_s

    @property
    def status(self) -> int:
        return ERRORS[self.code].status

    def body(self) -> bytes:
        """The ErrorBody, as JSON."""
        said = ErrorBody(detail=str(self), code=self.code, retry_after_s=self.retry_after_s, details=self.details)
        return json.dumps(said.model_dump(mode="json")).encode()


class _Copy:
    """The copy of the policy on serve(): each episode's frames, as they come in order, turned back (obs_format) on a
    thread of its own - one a frame, every episode's in turn - and the newest kept for its act. `on_frame(episode, seq,
    frame)`: told of each frame as the robot sent it - its marked items still encoded - in order (a recorder)."""

    def __init__(self, on_frame: Optional[Callable[[str, int, Any], None]] = None) -> None:
        self.on_frame = on_frame
        self._observed = obs_format.Observed()
        self._thread = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="sequence_ai-decode")

    async def observe(self, episode_id: str, frames: list, handed: Callable[[], None]) -> list:
        """StreamStore.forward's: each of `frames` - (seq, inputs), in order - turned back and kept, its answer
        {"ok": True}; one that does not read ends the episode's frames here, {"ok": False, "error"}."""
        answers = []
        loop = asyncio.get_running_loop()
        for seq, inputs in frames:
            if self.on_frame is not None:
                self.on_frame(episode_id, seq, inputs)
            try:
                await loop.run_in_executor(self._thread, self._observed.take, episode_id, seq, inputs)
            except Exception as e:  # noqa: BLE001 - an item that does not read: every act of the episode says which
                answers.append({"ok": False, "error": f"observation {seq} does not read: {type(e).__name__}: {e}"})
                break
            answers.append({"ok": True})
        return answers

    def latest(self, episode_id: str) -> Any:
        return self._observed.latest(episode_id)

    def end(self, episode_id: str) -> None:
        self._observed.end(episode_id)

    def close(self) -> None:
        self._thread.shutdown(wait=False, cancel_futures=True)


class DataPlane:
    """
    serve()'s side of a robot's data plane (the module's docstring).

    store     the episodes' observations in order (StreamStore unless given)
    copy      the copy of the policy the frames go to, in order: observe(episode_id, frames, handed) -> answers, as
              StreamStore.forward hands them; latest(episode_id); end(episode_id) - one that keeps each episode's newest
              observation unless given (a policy with an observe function of its own brings its own)
    on_frame  told (episode, seq, frame) of each frame as the robot sent it, in order: the recorder's
    """

    def __init__(self, *, store: Optional[StreamStore] = None, copy: Any = None,
                 on_frame: Optional[Callable[[str, int, Any], None]] = None) -> None:
        self.store = store if store is not None else StreamStore()
        self.copy = copy if copy is not None else _Copy(on_frame=on_frame)

    async def observe(self, raw: bytes, content_type: str) -> int:
        """POST /observe: a post of one episode's observations kept and forwarded; how far its episode is whole.
        Refused 400 (invalid_request) for a body that does not read, 413 (payload_too_large, frames_over_limit) for an
        episode or a server past what it keeps."""
        try:
            body = msgpack_io.unpack(raw) if content_type == msgpack_io.MEDIA_TYPE else json.loads(raw)
            post = ObserveRequest.model_validate(body)
            grew = 0
            frames = []
            for f in post.frames:
                inputs, more = _compressed.expand(f.inputs, limit=MAX_STREAM_BYTES)
                frames.append((f.seq, inputs))
                grew += more
            contents = {}
            for bid, value in post.blocks.items():
                content, more = _compressed.expand(value, limit=MAX_STREAM_BYTES)
                if len(bid) != _blocks.ID_BYTES or not isinstance(content, (bytes, bytearray)):
                    raise ValueError(f"a block is {_blocks.ID_BYTES} bytes of id and the bytes it holds")
                contents[bytes(bid)] = bytes(content)
                grew += more
        except Exception as e:  # noqa: BLE001 - MsgpackError, JSON's, pydantic's, CompressedError: it does not read
            raise Refused(ErrorCode.INVALID_REQUEST, f"the observations do not read: {e}"[:500],
                          details={"reason": "observe"}) from None
        if post.params:
            raise Refused(ErrorCode.INVALID_REQUEST, "a robot's observations carry no inference parameters",
                          details={"reason": "params"})
        try:
            through = self.store.put(post.episode_id, frames, post.skipped, len(raw) + grew, blocks=contents,
                                     sent=len(raw))
        except StreamError as e:
            raise Refused(ErrorCode.PAYLOAD_TOO_LARGE, str(e), details={"reason": FRAMES_OVER_LIMIT}) from None
        if post.frames or post.skipped:
            asyncio.ensure_future(self.store.forward(post.episode_id, self.copy.observe))
        return through

    async def act(self, episode_id: Any, seq: Any) -> Any:
        """An act's observation: once every observation of `episode_id` before `seq` reached the copy, the newest.
        Refused 400 for an act that names no episode or no `seq`, 409 (conflict, frames_missing, from) for observations
        that did not come, 409 (conflict, no_observation) for an episode none came for yet, 400 for one that does not
        read, 503 while the copy has not taken observations that are here."""
        if not isinstance(episode_id, str) or not episode_id:
            raise Refused(ErrorCode.INVALID_REQUEST, "an act names its episode_id", details={"reason": "episode_id"})
        if isinstance(seq, bool) or not isinstance(seq, int) or seq < 0:
            raise Refused(ErrorCode.INVALID_REQUEST, "`seq` is how many observations the act's episode sent before it, "
                          "from 0", details={"reason": "seq"})
        if self.store.stalled(episode_id):
            asyncio.ensure_future(self.store.forward(episode_id, self.copy.observe))
        try:
            await self.store.before(episode_id, seq)
        except StreamError as e:
            if e.busy:
                raise Refused(ErrorCode.BUSY, str(e), retry_after_s=1.0, details={"reason": "copy_busy"}) from None
            raise Refused(ErrorCode.CONFLICT, str(e), details={"reason": FRAMES_MISSING, "from": e.first}) from None
        try:
            return self.copy.latest(episode_id)
        except obs_format.NoObservation as e:
            raise Refused(ErrorCode.CONFLICT, str(e), details={"reason": "no_observation"}) from None

    def end(self, episode_id: Any) -> None:
        """POST /act/episode_end: everything kept of the episode goes. Refused 400 for no episode_id."""
        if not isinstance(episode_id, str) or not episode_id:
            raise Refused(ErrorCode.INVALID_REQUEST, "episode_id is required", details={"reason": "episode_id"})
        self.store.end(episode_id)
        self.copy.end(episode_id)

    def close(self) -> None:
        """Stop the copy's decoding thread."""
        closing = getattr(self.copy, "close", None)
        if closing is not None:
            closing()
