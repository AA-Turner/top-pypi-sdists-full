"""OpenAI completions (`POST .../completions`): one prompt in, text out. The prompt is the whole conversation, so
after a watch's first snapshot only each reply is sent."""

from __future__ import annotations

from ..dialect import Dialect, Reply, make_turn, read_count, read_first_choice, read_frame_json
from ..sse import SseFrame


class CompletionsDialect(Dialect):
    name = "completions"
    path_suffix = "/completions"

    def read_history(self, request: dict) -> list[dict]:
        prompt = request.get("prompt")
        return [make_turn("user", prompt)] if prompt else []

    def read_reply(self, body: dict) -> Reply:
        choice = read_first_choice(body)
        text = choice.get("text") if isinstance(choice.get("text"), str) else ""
        return _make_reply(text, choice.get("finish_reason"), body.get("usage"))

    def read_stream(self, frames: list[SseFrame]) -> Reply:
        text: list[str] = []
        finish = usage = None
        for frame in frames:
            chunk = read_frame_json(frame)
            if chunk is None:
                continue
            if chunk.get("error"):
                finish = "error"
            usage = chunk.get("usage") or usage
            choice = read_first_choice(chunk)
            finish = choice.get("finish_reason") or finish
            if isinstance(choice.get("text"), str):
                text.append(choice["text"])
        return _make_reply("".join(text), finish, usage)



def _make_reply(text: str, finish, usage) -> Reply:
    usage = usage if isinstance(usage, dict) else {}
    output_tokens = read_count(usage.get("completion_tokens"))
    return Reply(turns=[make_turn("assistant", text, tokens=output_tokens)],
                 finish_reason=str(finish) if finish else None, input_tokens=read_count(usage.get("prompt_tokens")),
                 output_tokens=output_tokens, history_items=0)  # fmt: skip
