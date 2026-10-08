"""What the daemon's model rounds cost (T10, P1).

Every model response is recorded as it arrives (`agent.UsageMeter`, a
capability around the model request): a `rounds` row in the session's store (model, input /
cached / output tokens, the tools it called, its estimated dollars) and the
device's daily token counter. So a long run is counted while it runs, not after
it (A2), and `probe daemon status` shows each session's tokens, its cache-hit
share and an estimate in dollars.

The estimate uses the gateway's own list prices (charts/research-os/templates/
_litellm.tpl and the CHANGELOG entry that added the Opus route). A model not in
the table is shown in tokens only: an unknown price is never read as free.
There is NO spend limit here (F2, Richard 2026-09-26), and no fuse anywhere
since the server's team fuse and the device token fuse were removed (Richard
2026-09-28: "we dont want any limit").

`probe daemon status` imports this module without the AI libraries installed:
nothing here imports them at load time.
"""

from __future__ import annotations

from typing import Any

#: USD per million tokens: (uncached input, cache read, cache write, output).
#: gemini-3.8-flash: Google's Standard-tier introductory rates, read 2026-09-03
#: (they double on 2027-01-01). claude-opus-5-5: the gateway's route price.
#: claude-sonnet-5, claude-opus-5: Anthropic's list prices, read 2026-10-06 (the
#: write is the 5-minute cache's, the only one the daemon writes).
#: Cache writes are priced as writes when the server reports them
#: (`prompt_tokens_details.cache_write_tokens`, which Pydantic AI reads into
#: `cache_write_tokens`); an older server's are counted as uncached input.
PRICES: dict[str, tuple[float, float, float, float]] = {
    "gemini-3.8-flash": (0.75, 0.075, 0.75, 3.75),
    "claude-opus-5-5": (4.00, 0.20, 5.00, 20.00),
    "claude-sonnet-5": (2.00, 0.20, 2.50, 10.00),
    "claude-opus-5": (5.00, 0.50, 6.25, 25.00),
    # gpt-6.1-sol up to 272K prompt tokens; LONG_CONTEXT below has the rest.
    "gpt-6.1-sol": (2.00, 0.10, 2.50, 10.00),
    "claude-haiku-4-5": (1.00, 0.10, 1.25, 5.00),
    # Anthropic pricing page, 2026-10-07. Haiku 5.5 up to 100K prompt tokens;
    # LONG_CONTEXT (where the tier lives) has the rest once it is on main.
    "claude-sonnet-5-5": (2.00, 0.20, 2.50, 10.00),
    "claude-haiku-5-5": (0.10, 0.01, 0.125, 0.50),
    "gpt-6-luna": (0.10, 0.01, 0.10, 0.50),
    "gpt-5.6-terra": (2.00, 0.20, 2.00, 12.00),
}


def price_key(model: str | None) -> str | None:
    """The table's name for a model as a response reports it: provider prefixes
    (`gemini/`, `anthropic:`) and the companion route's `companion-` dropped; a
    dated or versioned suffix of a known name still matches."""
    if not model:
        return None
    name = model.strip().lower()
    for sep in ("/", ":"):
        name = name.rsplit(sep, 1)[-1]
    name = name.removeprefix("companion-")
    if name in PRICES:
        return name
    # The LONGEST matching key: `claude-opus-5-5-<date>` must not price as `claude-opus-5`.
    return max((key for key in PRICES if name.startswith(key + "-") or name.startswith(key + "@")),
               key=len, default=None)


#: Models billed at other rates once a prompt passes a size: (the size, the
#: prices from there). Every token of such a request is billed at them, as
#: OpenAI does and as the proxy's `*_above_272k_tokens` fields meter it (#2451):
#: the size counts the whole prompt, cached and written tokens included.
LONG_CONTEXT: dict[str, tuple[int, tuple[float, float, float, float]]] = {
    "gpt-6.1-sol": (272_000, (4.00, 0.20, 5.00, 15.00)),
    # Anthropic pricing page, 2026-10-07: Haiku 5.5 prompts over 100K tokens.
    "claude-haiku-5-5": (100_000, (0.50, 0.05, 0.625, 2.50)),
}


def cost(model: str | None, *, input_tokens: int, cache_read_tokens: int = 0, cache_write_tokens: int = 0,
         output_tokens: int = 0) -> float | None:
    """Estimated dollars of one response, or None when the model's price is unknown.
    `input_tokens` counts every input token, the cached ones included (as Pydantic
    AI reports it)."""
    key = price_key(model)
    if key is None:
        return None
    p_in, p_read, p_write, p_out = PRICES[key]
    long = LONG_CONTEXT.get(key)
    if long is not None and int(input_tokens) > long[0]:
        p_in, p_read, p_write, p_out = long[1]
    uncached = max(0, int(input_tokens) - int(cache_read_tokens) - int(cache_write_tokens))
    return (uncached * p_in + int(cache_read_tokens) * p_read + int(cache_write_tokens) * p_write
            + int(output_tokens) * p_out) / 1_000_000


def response_cost(response: Any) -> float | None:
    u = response.usage
    return cost(response.model_name, input_tokens=u.input_tokens, cache_read_tokens=u.cache_read_tokens,
                cache_write_tokens=u.cache_write_tokens, output_tokens=u.output_tokens)


def tool_names(response: Any) -> list[str]:
    from pydantic_ai.messages import ToolCallPart

    return [p.tool_name for p in response.parts if isinstance(p, ToolCallPart)]


def fmt_usage(summary: dict) -> str:
    """`1,234,567 tokens in (82% cached) / 34,567 out, ~$1.23` for a status line."""
    inp, cached, out = summary["input_tokens"], summary["cached_tokens"], summary["output_tokens"]
    share = f"{cached / inp:.0%} cached" if inp and cached else "none cached"
    text = f"{inp:,} tokens in ({share}) / {out:,} out"
    if summary["rounds"] and summary["unpriced_rounds"] == summary["rounds"]:
        return text + f" (no price known for {', '.join(summary['models']) or 'the model'}: tokens only)"
    text += f", ~${summary['usd']:.2f}"
    if summary["unpriced_rounds"]:
        text += f" (+{summary['unpriced_rounds']} rounds of a model with no known price)"
    return text
