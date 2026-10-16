"""Nemotron checkpoint templates, XML function calls, and Super VL image spans."""

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


class NemotronSuperVLRenderer(Nemotron35Renderer):
    """Checkpoint chat template plus RADIO image spans for inference and training."""

    def _messages(self, messages):
        normalized = []
        for message in messages:
            content = message.get("content")
            if isinstance(content, list) and any(p["type"] == "image" for p in content):
                result = super()._messages([{**message, "content": ""}])[0]
                parts = []
                for part in content:
                    if part["type"] == "image":
                        parts.append({"type": "image"})
                    else:
                        text = super()._messages(
                            [{**message, "content": [part], "unparsed_tool_calls": []}]
                        )[0]["content"]
                        parts.append({"type": "text", "text": text})
                if result["content"]:
                    parts.append({"type": "text", "text": result["content"]})
                result["content"] = parts
                normalized.append(result)
            else:
                normalized.extend(super()._messages([message]))
        return normalized

    @staticmethod
    def _images(messages):
        return [
            part
            for message in messages
            if isinstance(message.get("content"), list)
            for part in message["content"]
            if part["type"] == "image"
        ]

    def build_sample_prompt(self, messages, *, tools=None):
        images = self._images(messages)
        return SamplePrompt(
            self.build_prompt_str(messages, tools=tools),
            [p["image"] for p in images],
            [p["format"] for p in images],
        )

    def build_continuation_prompt(self, messages, *, last_stop):
        prompt = super().build_continuation_prompt(messages, last_stop=last_stop)
        images = self._images(messages)
        return SamplePrompt(
            prompt.prompt, [p["image"] for p in images], [p["format"] for p in images]
        )

    def build_training_example(self, messages, *, max_length=None, **kwargs):
        from river_client.renderers.base import (
            TrainingExample,
            _ChunkBuilder,
            _truncate_chunks_to_length,
            image_part_size,
        )

        images = self._images(messages)
        if not images:
            return super().build_training_example(
                messages, max_length=max_length, **kwargs
            )
        example = super().build_training_example(messages, max_length=None, **kwargs)
        marker = self.tokenizer.convert_tokens_to_ids("<image>")
        if example.input_ids.count(marker) != len(images):
            raise ValueError("Nemotron image placeholders do not match supplied images")
        builder = _ChunkBuilder()
        image_iter = iter(images)
        for token, weight in zip(example.input_ids, example.weights, strict=True):
            if token != marker:
                builder.add_text([token], weight)
                continue
            part = next(image_iter)
            height, width = image_part_size(part)
            start = self.tokenizer.encode("<img>", add_special_tokens=False)
            end = self.tokenizer.encode("</img>", add_special_tokens=False)
            builder.add_text(start, 0.0)
            builder.add_image(
                data=part["image"],
                format=part["format"],
                expected_tokens=nemotron_image_tokens(height, width),
                placeholder_id=marker,
            )
            builder.add_text(end, 0.0)
        builder.finish()
        chunks, count = builder.chunks, len(builder.flat_ids)
        if max_length is not None:
            chunks, count = _truncate_chunks_to_length(chunks, max_length)
        return TrainingExample(
            builder.flat_ids[:count], builder.weights[:count], chunks
        )


def nemotron_image_tokens(
    height,
    width,
    *,
    patch_size=16,
    merge_size=2,
    min_num_patches=1024,
    max_num_patches=13312,
):
    """RADIO image token accounting, without importing a training runtime."""
    import math

    if height <= 0 or width <= 0:
        raise ValueError("Nemotron images must have positive dimensions")
    h, w = round(height / patch_size + 0.5), round(width / patch_size + 0.5)
    scale = min(math.sqrt(max_num_patches / (h * w)), 1.0)
    h, w = max(1, math.floor(scale * h)), max(1, math.floor(scale * w))
    if max_num_patches > min_num_patches and h * w < min_num_patches:
        scale = math.sqrt(min_num_patches / (h * w))
        h, w = math.ceil(scale * h), math.ceil(scale * w)
    rem = h % merge_size
    if rem:
        up = merge_size - rem
        h = h + up if (h + up) * w <= max_num_patches else max(merge_size, h - rem)
    rem = w % merge_size
    if rem:
        up = merge_size - rem
        w = w + up if h * (w + up) <= max_num_patches else max(merge_size, w - rem)
    return h * w // merge_size**2
