"""Text-only rendering through a checkpoint's own chat template."""

from __future__ import annotations

import json

from river_client.renderers.base import Renderer, TrainingExample, TrainOnWhat
from river_client.renderers.tool_arguments import protect_value_ends


class CheckpointTextRenderer(Renderer):
    """Shared normalization and SFT masking; subclasses own model syntax."""

    # Whether the template renders an empty ``reasoning_content`` field as an
    # empty think block; every template renders a non-empty one.
    empty_reasoning_field = False
    # The tags that end an argument value, or its call, in the template's calls.
    value_ends: tuple[str, ...] = ()

    def __init__(self, tokenizer, *, thinking=True, strip_thinking_from_history=True):
        super().__init__(tokenizer)
        self.thinking = thinking
        self.strip_thinking_from_history = strip_thinking_from_history

    def _messages(self, messages):
        last_user = max(
            (i for i, m in enumerate(messages) if m.get("role") == "user"), default=-1
        )
        return [
            self._message(message, history=index < last_user)
            for index, message in enumerate(messages)
        ]

    def _message(self, message, *, history):
        """One message as the template takes it.

        ``history`` marks a turn before the last user turn, whose reasoning a
        template may strip.
        """
        m = dict(message)
        content = m.get("content") or ""
        # A caller's string may carry its reasoning inline, which the template
        # extracts. Parts, or an empty string beside calls, carry it
        # structurally, so it is written explicitly, even when empty: the
        # template then never searches the text or a rejected block, where a
        # </think> is the model's own text, for reasoning.
        structured = m.get("role") == "assistant" and not (
            isinstance(content, str) and content
        )
        # A template that strips reasoning from earlier turns finds it by
        # cutting at </think>. Writing none into such a turn, which it would
        # drop anyway, leaves it nothing of ours to cut at.
        stripped = (
            structured
            and not self.empty_reasoning_field
            and self.strip_thinking_from_history
            and history
        )
        explicit = structured and not stripped
        reasoning = m.get("reasoning_content")
        thinking = []
        if not isinstance(content, str):
            parts = []
            for part in content:
                if part["type"] == "text":
                    parts.append(part["text"])
                elif part["type"] == "thinking":
                    thinking.append(part["thinking"])
                else:
                    raise ValueError(
                        f"{type(self).__name__} supports text only; got {part['type']}"
                    )
            content = "".join(parts)
        if isinstance(reasoning, str):
            thinking = [reasoning]
        joined = "".join(thinking)
        if explicit and (self.empty_reasoning_field or joined.strip()):
            m["reasoning_content"] = joined
        elif explicit:
            # This template ignores an empty field, so the empty block goes in
            # the content, where it finds one and adds no other.
            m.pop("reasoning_content", None)
            content = f"<think>{joined}</think>{content}"
        elif stripped:
            m.pop("reasoning_content", None)
        elif thinking and not isinstance(reasoning, str):
            content = "".join(f"<think>{t}</think>" for t in thinking) + content
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
                function["arguments"] = {
                    key: protect_value_ends(value, self.value_ends)
                    for key, value in args.items()
                }
                calls.append({**call, "function": function})
            m["tool_calls"] = calls
        return m

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
            # Removing calls can also reorder the following tool responses in
            # checkpoint templates. Their changed suffix is never assistant
            # output: cap the differential span at the first turn terminator.
            stop_tokens = [encode(stop) for stop in self.get_stop_strings()]
            for position in range(start, end):
                if any(
                    tokens and ids[position : position + len(tokens)] == tokens
                    for tokens in stop_tokens
                ):
                    end = position
                    break
            # Include the adjacent model stop token only when requested.
            for tokens in stop_tokens:
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
