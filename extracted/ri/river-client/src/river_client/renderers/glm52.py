"""GLM-5.2 text renderer using its checkpoint-owned template."""

from river_client.renderers.base import ParsedResponse, SamplePrompt, ToolSpec
from river_client.renderers.checkpoint_text import CheckpointTextRenderer
from river_client.renderers.glm53 import parse_glm53_content_blocks


class Glm52Renderer(CheckpointTextRenderer):
    def __init__(
        self,
        tokenizer,
        *,
        thinking=True,
        strip_thinking_from_history=False,
        reasoning_effort="max",
    ):
        super().__init__(
            tokenizer,
            thinking=thinking,
            strip_thinking_from_history=strip_thinking_from_history,
        )
        if reasoning_effort not in ("high", "max"):
            raise ValueError("GLM-5.2 reasoning_effort must be 'high' or 'max'")
        self.reasoning_effort = reasoning_effort

    def _template_kwargs(self):
        return {
            "enable_thinking": self.thinking,
            "clear_thinking": self.strip_thinking_from_history,
            "reasoning_effort": self.reasoning_effort,
        }

    def get_stop_strings(self):
        return ["<|observation|>", "<|user|>", "<|endoftext|>"]

    def build_continuation_prompt(self, messages, *, last_stop):
        suffix = self._observation_suffix(messages)
        if last_stop in ("<|observation|>", "<|user|>") and suffix.startswith(
            last_stop
        ):
            suffix = suffix[len(last_stop) :]
        return SamplePrompt(suffix, [], [])

    def parse_response(
        self, text: str, *, tools: list[ToolSpec] | None = None
    ) -> ParsedResponse:
        stopped = False
        for stop in self.get_stop_strings():
            if text.endswith(stop):
                text, stopped = text[: -len(stop)], True
                break
        # 5.2 and 5.3 share the arg_key/arg_value call dialect.
        parts, calls = parse_glm53_content_blocks(
            text, thinking=self.thinking, tools=tools
        )
        message = {"role": "assistant", "content": parts or ""}
        valid = [c for c in calls if "function" in c]
        invalid = [c for c in calls if "error" in c]
        if valid:
            message["tool_calls"] = valid
        if invalid:
            message["unparsed_tool_calls"] = invalid
        return ParsedResponse(message, stopped)
