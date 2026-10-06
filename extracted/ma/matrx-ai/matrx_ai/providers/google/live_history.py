"""Fold a Google realtime session's traffic into completed turns.

``GoogleLiveSession`` / ``GoogleMusicSession`` stream; they never return a
turn. The host still keeps every turn the ONE way (owner ruling 2026-10-05:
conversation + messages + cost row + request snapshot, through
``matrx_ai.agents.run_history``). This module is the provider half of that:
it reads the session's client messages and provider events (the JSON-safe
dicts ``receive()`` yields) and hands back finished :class:`LiveTurn` values.

Audio is never kept inline. :func:`store_turn_audio` saves each turn's audio
through the host's snapshot blob store (the same ``(bytes, mime, sha256) ->
file_id`` seam the snapshot redactor uses) and leaves only the file reference
in the snapshot payload; messages carry transcripts only.
"""

from __future__ import annotations

import base64
import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger("matrx_ai.providers.google.live_history")

#: Most audio bytes one turn keeps per direction (CAPS knob; beyond it the
#: turn records ``audio_truncated`` instead of growing without bound).
MAX_TURN_AUDIO_BYTES = 8 * 1024 * 1024


@dataclass
class _AudioBuffer:
    mime_type: str = ""
    chunks: list[bytes] = field(default_factory=list)
    size: int = 0
    truncated: bool = False

    def add(self, data: bytes, mime_type: str) -> None:
        if not data:
            return
        self.mime_type = self.mime_type or mime_type
        if self.size + len(data) > MAX_TURN_AUDIO_BYTES:
            self.truncated = True
            return
        self.chunks.append(data)
        self.size += len(data)

    def block(self) -> dict[str, Any] | None:
        if not self.chunks:
            return None
        return {
            "data": base64.b64encode(b"".join(self.chunks)).decode("ascii"),
            "mime_type": self.mime_type or "application/octet-stream",
            "bytes": self.size,
            "truncated": self.truncated,
        }


@dataclass
class LiveTurn:
    """One finished exchange of a realtime session."""

    user_text: str
    output_text: str
    usage_metadata: dict[str, Any] | None
    input_audio: dict[str, Any] | None
    output_audio: dict[str, Any] | None
    interrupted: bool = False
    client_inputs: list[dict[str, Any]] = field(default_factory=list)
    events: int = 0

    def response_payload(self) -> dict[str, Any]:
        return {
            "output_text": self.output_text,
            "output_audio": self.output_audio,
            "usage_metadata": self.usage_metadata,
            "interrupted": self.interrupted,
            "provider_events": self.events,
        }

    def request_payload(self, session_config: dict[str, Any]) -> dict[str, Any]:
        return {
            "session_config": session_config,
            "client_inputs": self.client_inputs,
            "input_transcript": self.user_text,
            "input_audio": self.input_audio,
        }


def _text_of_turns(turns: Any) -> str:
    out: list[str] = []
    for turn in turns if isinstance(turns, list) else [turns]:
        if isinstance(turn, str):
            out.append(turn)
            continue
        if not isinstance(turn, dict):
            continue
        for part in turn.get("parts") or []:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                out.append(part["text"])
    return "".join(out)


class LiveTurnCollector:
    """Accumulates one Gemini Live session's traffic; yields completed turns.

    A turn closes on the provider's ``turn_complete``. Google may report the
    turn's ``usage_metadata`` in that message or just after it, so a completed
    turn with no usage yet is held until the usage arrives, the next turn
    starts, or the session ends (:meth:`drain`).
    """

    def __init__(self) -> None:
        self._reset()
        self._pending: LiveTurn | None = None

    def _reset(self) -> None:
        self._typed: list[str] = []
        self._input_transcript: list[str] = []
        self._output_text: list[str] = []
        self._output_transcript: list[str] = []
        self._input_audio = _AudioBuffer()
        self._output_audio = _AudioBuffer()
        self._client_inputs: list[dict[str, Any]] = []
        self._usage: dict[str, Any] | None = None
        self._interrupted = False
        self._events = 0
        self._active = False

    # ── client → provider ──────────────────────────────────────────────────
    def observe_client(self, message: dict[str, Any]) -> None:
        kind = str(message.get("type", ""))
        if kind == "audio":
            try:
                raw = base64.b64decode(str(message.get("data") or ""))
            except (ValueError, TypeError):
                return
            self._input_audio.add(raw, str(message.get("mime_type") or "audio/pcm;rate=16000"))
            self._active = True
            return
        if kind == "realtime_text":
            self._typed.append(str(message.get("text") or ""))
            self._client_inputs.append({"type": kind, "text": message.get("text")})
            self._active = True
            return
        if kind == "client_content":
            self._typed.append(_text_of_turns(message.get("turns")))
            self._client_inputs.append(
                {"type": kind, "turns": message.get("turns"),
                 "turn_complete": message.get("turn_complete", True)}
            )
            self._active = True
            return
        if kind in {"image", "video"}:
            self._client_inputs.append(
                {"type": kind, "data": message.get("data"), "mime_type": message.get("mime_type")}
            )
            self._active = True

    # ── provider → client ──────────────────────────────────────────────────
    def observe_provider(self, event: dict[str, Any]) -> list[LiveTurn]:
        done: list[LiveTurn] = []
        usage = event.get("usage_metadata")
        content = event.get("server_content") if isinstance(event.get("server_content"), dict) else None
        starts_activity = bool(content) and not content.get("turn_complete") and any(
            content.get(k) for k in ("model_turn", "input_transcription", "output_transcription")
        )
        if isinstance(usage, dict):
            if self._pending is not None and self._pending.usage_metadata is None and not self._active:
                self._pending.usage_metadata = usage
                done.append(self._pending)
                self._pending = None
            else:
                self._usage = usage
        if starts_activity and self._pending is not None:
            done.append(self._pending)
            self._pending = None
        if content:
            self._events += 1
            self._active = True
            model_turn = content.get("model_turn")
            if isinstance(model_turn, dict):
                for part in model_turn.get("parts") or []:
                    if not isinstance(part, dict):
                        continue
                    if isinstance(part.get("text"), str) and not part.get("thought"):
                        self._output_text.append(part["text"])
                    blob = part.get("inline_data")
                    if isinstance(blob, dict) and blob.get("data"):
                        try:
                            raw = base64.b64decode(str(blob["data"]))
                        except (ValueError, TypeError):
                            raw = b""
                        self._output_audio.add(raw, str(blob.get("mime_type") or "audio/pcm"))
            for key, sink in (
                ("input_transcription", self._input_transcript),
                ("output_transcription", self._output_transcript),
            ):
                piece = content.get(key)
                if isinstance(piece, dict) and isinstance(piece.get("text"), str):
                    sink.append(piece["text"])
            if content.get("interrupted"):
                self._interrupted = True
            if content.get("turn_complete"):
                turn = self._close()
                if turn.usage_metadata is None:
                    if self._pending is not None:
                        done.append(self._pending)
                    self._pending = turn
                else:
                    done.append(turn)
        return done

    def _close(self) -> LiveTurn:
        typed = "".join(self._typed).strip()
        heard = "".join(self._input_transcript).strip()
        turn = LiveTurn(
            user_text="\n".join(t for t in (typed, heard) if t),
            output_text=("".join(self._output_text) or "".join(self._output_transcript)).strip(),
            usage_metadata=self._usage,
            input_audio=self._input_audio.block(),
            output_audio=self._output_audio.block(),
            interrupted=self._interrupted,
            client_inputs=list(self._client_inputs),
            events=self._events,
        )
        self._reset()
        return turn

    def drain(self) -> list[LiveTurn]:
        """Session ended: every held or unfinished turn that carried traffic."""
        out: list[LiveTurn] = []
        if self._pending is not None:
            out.append(self._pending)
            self._pending = None
        if self._active:
            turn = self._close()
            turn.interrupted = True
            out.append(turn)
        return out


async def _store_block(
    block: dict[str, Any] | None, *, user_id: str | None, organization_id: str | None
) -> dict[str, Any] | None:
    if not block or not block.get("data"):
        return block
    from matrx_ai.providers.snapshot_redactors import get_snapshot_blob_store

    raw = base64.b64decode(str(block["data"]))
    sha = hashlib.sha256(raw).hexdigest()
    ref = {k: v for k, v in block.items() if k != "data"}
    ref["sha256"] = sha
    store = get_snapshot_blob_store()
    if store is None:
        # Never inline: without a store the bytes are dropped, and the block
        # SAYS so (a client host keeps snapshots server-side only).
        ref["stored"] = False
        ref["reason"] = "no snapshot blob store is bound in this process"
        logger.warning("realtime audio not stored: no snapshot blob store bound")
        return ref
    try:
        ref["file_id"] = await store(
            raw, str(block.get("mime_type") or "application/octet-stream"), sha,
            user_id=user_id, organization_id=organization_id,
        )
        ref["stored"] = True
    except Exception as exc:  # noqa: BLE001 — the turn is still kept; the loss is stated
        ref["stored"] = False
        ref["reason"] = f"{type(exc).__name__}: {exc}"[:300]
        logger.warning("realtime audio store failed: %r", exc)
    return ref


async def store_turn_audio(
    turn: LiveTurn, *, user_id: str | None, organization_id: str | None
) -> LiveTurn:
    """Replace the turn's inline audio with file references (in place)."""
    turn.input_audio = await _store_block(
        turn.input_audio, user_id=user_id, organization_id=organization_id
    )
    turn.output_audio = await _store_block(
        turn.output_audio, user_id=user_id, organization_id=organization_id
    )
    return turn


def live_usage(
    usage_metadata: dict[str, Any] | None,
    *,
    model: str,
    provider_model: str,
    offering_id: str = "",
) -> Any:
    """A Live ``usage_metadata`` dict as the catalog-priced ``TokenUsage``.

    Live reports ``response_token_count`` (chat reports
    ``candidates_token_count``); cached prompt tokens are split out, thinking
    and tool-use prompt tokens counted where Google bills them. The verbatim
    block rides as ``raw_usage``. None when the provider reported no usage —
    the request row then records an honest unknown cost.
    """
    if not isinstance(usage_metadata, dict):
        return None
    from matrx_ai.config.usage_config import TokenUsage

    prompt = int(usage_metadata.get("prompt_token_count") or 0)
    cached = int(usage_metadata.get("cached_content_token_count") or 0)
    tool_prompt = int(usage_metadata.get("tool_use_prompt_token_count") or 0)
    response = int(
        usage_metadata.get("response_token_count")
        or usage_metadata.get("candidates_token_count")
        or 0
    )
    thoughts = int(usage_metadata.get("thoughts_token_count") or 0)
    return TokenUsage(
        input_tokens=max(0, prompt - cached) + tool_prompt,
        output_tokens=response + thoughts,
        cached_input_tokens=cached,
        matrx_model_name=model,
        provider_model_name=provider_model,
        api="google",
        offering_id=offering_id,
        raw_usage=dict(usage_metadata),
        metadata={"iteration": 1, "lane": "realtime"},
    )


class MusicTurnCollector:
    """Lyria RealTime: one turn per weighted-prompt set (the person's steer),
    closed when the next set arrives or the session ends. The generated audio
    rides the snapshot as a file reference."""

    def __init__(self) -> None:
        self._prompts: list[dict[str, Any]] | None = None
        self._config: dict[str, Any] = {}
        self._controls: list[str] = []
        self._audio = _AudioBuffer()
        self._chunks = 0

    def observe_client(self, message: dict[str, Any]) -> LiveTurn | None:
        kind = message.get("type")
        if kind == "weighted_prompts":
            done = self._close()
            self._prompts = list(message.get("prompts") or [])
            return done
        if kind == "config":
            self._config.update(dict(message.get("config") or {}))
        elif kind == "control":
            self._controls.append(str(message.get("action")))
        return None

    def observe_provider(self, event: dict[str, Any]) -> None:
        content = event.get("server_content")
        if not isinstance(content, dict):
            return
        for chunk in content.get("audio_chunks") or []:
            if isinstance(chunk, dict) and chunk.get("data"):
                try:
                    raw = base64.b64decode(str(chunk["data"]))
                except (ValueError, TypeError):
                    continue
                self._chunks += 1
                self._audio.add(raw, str(chunk.get("mime_type") or "audio/pcm;rate=48000"))

    def _close(self) -> LiveTurn | None:
        if self._prompts is None:
            return None
        prompt_text = "; ".join(
            f"{p.get('text')} (weight {p.get('weight')})" for p in self._prompts if isinstance(p, dict)
        )
        seconds = self._audio.size / (48_000 * 2 * 2) if self._audio.size else 0.0
        turn = LiveTurn(
            user_text=f"Music prompts: {prompt_text}",
            output_text=f"Generated {seconds:.1f}s of music ({self._chunks} audio chunks).",
            usage_metadata=None,
            input_audio=None,
            output_audio=self._audio.block(),
            client_inputs=[
                {"type": "weighted_prompts", "prompts": self._prompts},
                {"type": "config", "config": dict(self._config)},
                {"type": "controls", "actions": list(self._controls)},
            ],
            events=self._chunks,
        )
        self._audio = _AudioBuffer()
        self._chunks = 0
        self._controls = []
        return turn

    def drain(self) -> list[LiveTurn]:
        turn = self._close()
        self._prompts = None
        return [turn] if turn is not None else []


__all__ = [
    "MAX_TURN_AUDIO_BYTES",
    "LiveTurn",
    "LiveTurnCollector",
    "MusicTurnCollector",
    "live_usage",
    "store_turn_audio",
]
