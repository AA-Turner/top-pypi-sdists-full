"""Render only environment-authored text; sampled token ids remain untouched."""

from river_client.client import _image_placeholder_token_id


def prompt_chunks(renderer, messages, *, tools=None):
    prompt = renderer.build_sample_prompt(messages, tools=tools)
    return sample_prompt_chunks(renderer, prompt)


def sample_prompt_chunks(renderer, prompt):
    ids = list(renderer.tokenizer.encode(prompt.prompt, add_special_tokens=False))
    if not prompt.images:
        return [{"type": "text", "tokens": ids}]
    placeholder = _image_placeholder_token_id(renderer.tokenizer)
    locations = [i for i, token in enumerate(ids) if token == placeholder]
    if len(locations) != len(prompt.images):
        raise ValueError("renderer must emit one unexpanded placeholder per image")
    chunks, start = [], 0
    for i, location in enumerate(locations):
        if location > start:
            chunks.append({"type": "text", "tokens": ids[start:location]})
        chunks.append(
            renderer.image_chunk(prompt.images[i], format=prompt.image_formats[i])
        )
        start = location + 1
    if start < len(ids):
        chunks.append({"type": "text", "tokens": ids[start:]})
    return chunks


def sample_stop(renderer, tokens):
    for stop in sorted(renderer.get_stop_strings(), key=len, reverse=True):
        ids = list(renderer.tokenizer.encode(stop, add_special_tokens=False))
        if ids and list(tokens[-len(ids) :]) == ids:
            return stop
    return None


def continuation_chunks(renderer, traj, messages):
    if any(message["role"] == "assistant" for message in messages):
        raise ValueError("continuations accept only new environment messages")
    limit = max(
        len(renderer.tokenizer.encode(s, add_special_tokens=False))
        for s in renderer.get_stop_strings()
    )
    last = []
    for span in reversed(traj.spans):
        if span.kind != "generated" or len(last) >= limit:
            break
        last = [t for c in span.chunks for t in c["tokens"]][-limit:] + last
    prompt = renderer.build_continuation_prompt(
        messages, last_stop=sample_stop(renderer, last)
    )
    # Tokenize framing and new text together, including around image boundaries.
    return sample_prompt_chunks(renderer, prompt)
