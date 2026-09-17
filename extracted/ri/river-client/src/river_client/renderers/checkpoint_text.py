"""Text-only rendering through a checkpoint's own chat template."""

from __future__ import annotations

import json

from river_client.renderers.base import Renderer, TrainingExample, TrainOnWhat


class CheckpointTextRenderer(Renderer):
    """Shared normalization and SFT masking; subclasses own model syntax."""

    def __init__(self, tokenizer, *, thinking=True, strip_thinking_from_history=True):
        super().__init__(tokenizer)
        self.thinking = thinking
        self.strip_thinking_from_history = strip_thinking_from_history

    def _messages(self, messages):
        result = []
        for message in messages:
            m = dict(message)
            content = m.get("content") or ""
            if not isinstance(content, str):
                parts = []
                for part in content:
                    if part["type"] == "text":
                        parts.append(part["text"])
                    elif part["type"] == "thinking":
                        if not isinstance(m.get("reasoning_content"), str):
                            parts.append(f"<think>{part['thinking']}</think>")
                    else:
                        raise ValueError(
                            f"{type(self).__name__} supports text only; got {part['type']}"
                        )
                content = "".join(parts)
            m["content"] = content + "".join(
                c["raw_text"] for c in m.pop("unparsed_tool_calls", [])
            )
            if m.get("tool_calls"):
                calls = []
                for call in m["tool_calls"]:
                    function = dict(call["function"])
                    args = function.get("arguments", {})
                    if isinstance(args, str):
                        args = json.loads(args)
                    if not isinstance(args, dict):
                        raise ValueError("Tool arguments must be a JSON object")  # noqa: TRY004 - malformed configuration/tool value
                    function["arguments"] = args
                    calls.append({**call, "function": function})
                m["tool_calls"] = calls
            result.append(m)
        return result

    def _template_kwargs(self):
        raise NotImplementedError

    def _render(self, messages, *, generation, tools=None):
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=generation,
            tools=tools,
            **self._template_kwargs(),
        )
        if not isinstance(text, str):
            raise TypeError("Checkpoint chat template must return a string")
        return text

    def build_prompt_str(self, messages, *, tools=None):
        return self._render(self._messages(messages), generation=True, tools=tools)

    def _observation_suffix(self, messages):
        # Keep a preceding non-tool turn for templates that group tool results.
        # Only the new suffix is appended; sampled assistant tokens never enter Jinja.
        if any(m["role"] not in ("user", "tool") for m in messages):
            raise ValueError("Continuations require user or tool observations")
        anchor = [{"role": "user", "content": ""}]
        prefix = self._render(anchor, generation=False)
        full = self._render(anchor + self._messages(messages), generation=True)
        if not full.startswith(prefix):
            raise ValueError("Checkpoint template rewrites its continuation anchor")
        return full[len(prefix) :]

    def build_training_example(
        self,
        messages,
        *,
        train_on=TrainOnWhat.LAST_ASSISTANT,
        train_on_eos=True,
        max_length=None,
        tools=None,
    ):
        messages = self._messages(messages)

        def encode(text):
            return list(self.tokenizer.encode(text, add_special_tokens=False))

        ids = encode(self._render(messages, generation=False, tools=tools))
        weights = [0.0] * len(ids)
        targets = [i for i, m in enumerate(messages) if m["role"] == "assistant"]
        if train_on == TrainOnWhat.LAST_ASSISTANT:
            targets = targets[-1:]
        elif train_on != TrainOnWhat.ALL_ASSISTANT:
            targets = []
        for index in targets:
            empty = [dict(m) for m in messages]
            empty[index]["content"] = ""
            empty[index].pop("reasoning_content", None)
            empty[index].pop("tool_calls", None)
            other = encode(self._render(empty, generation=False, tools=tools))
            start = 0
            while start < min(len(ids), len(other)) and ids[start] == other[start]:
                start += 1
            suffix = 0
            while (
                suffix < min(len(ids), len(other)) - start
                and ids[-suffix - 1] == other[-suffix - 1]
            ):
                suffix += 1
            end = len(ids) - suffix
            # Include only a directly adjacent assistant terminator, never a role header.
            for stop in self.get_stop_strings():
                tokens = encode(stop)
                if tokens and ids[end : end + len(tokens)] == tokens:
                    if train_on_eos:
                        end += len(tokens)
                    break
                if tokens and ids[max(start, end - len(tokens)) : end] == tokens:
                    if not train_on_eos:
                        end -= len(tokens)
                    break
            weights[start:end] = [1.0] * (end - start)
        if max_length is not None:
            ids, weights = ids[:max_length], weights[:max_length]
        return TrainingExample(input_ids=ids, weights=weights)
