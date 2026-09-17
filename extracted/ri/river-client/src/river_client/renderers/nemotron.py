"""Nemotron 3.5 Lightning: checkpoint template and XML function calls."""

from river_client.renderers.base import ParsedResponse, SamplePrompt, ToolSpec
from river_client.renderers.checkpoint_text import CheckpointTextRenderer
from river_client.renderers.qwen3 import parse_qwen_content_blocks


class Nemotron35Renderer(CheckpointTextRenderer):
    def _template_kwargs(self):
        return {
            "enable_thinking": self.thinking,
            "truncate_history_thinking": self.strip_thinking_from_history,
        }

    def get_stop_strings(self):
        return ["<|im_end|>", "</s>"]

    def build_continuation_prompt(self, messages, *, last_stop):
        # Both EOS alternatives close a generation; im_end is needed only when
        # a segment ended without any retained terminator.
        prefix = "" if last_stop in self.get_stop_strings() else "<|im_end|>"
        return SamplePrompt(prefix + "\n" + self._observation_suffix(messages), [], [])

    def parse_response(
        self, text: str, *, tools: list[ToolSpec] | None = None
    ) -> ParsedResponse:
        stopped = False
        for stop in self.get_stop_strings():
            if text.endswith(stop):
                text, stopped = text[: -len(stop)], True
                break
        if self.thinking and "<think>" not in text:
            text = "<think>" + text
        parsed = parse_qwen_content_blocks(text)
        if parsed is None:
            return ParsedResponse({"role": "assistant", "content": text}, stopped)
        parts, calls = parsed
        message = {"role": "assistant", "content": parts}
        valid = [c for c in calls if "function" in c]
        invalid = [c for c in calls if "error" in c]
        if valid:
            message["tool_calls"] = valid
        if invalid:
            message["unparsed_tool_calls"] = invalid
        return ParsedResponse(message, stopped)
