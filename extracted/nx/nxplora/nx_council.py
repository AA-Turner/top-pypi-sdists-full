"""
nx_council.py — NX Council Mode
Trinity architecture: 3 AI instances debate internally.
When they agree → fast convergence, single voice.
When they disagree → internal rounds until consensus or best answer surfaces.
Usage: ~3-5x normal. Only activate when operator invokes $council.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
from nx_obfuscate import ENV, FW, M, NATIVE, OR_FALLBACK, P, URLS


def _clean(text: str) -> str:
    """Run a council voice/synthesis output through NX's narration strip +
    identity scrub. Lazy import avoids a circular dependency (nx_cli imports
    nx_council lazily, so both modules are loaded by the time this runs)."""
    if not text:
        return text
    try:
        from nx_cli import _strip_narration, _scrub_identity
        return _scrub_identity(_strip_narration(text))
    except Exception:
        return text


COUNCIL_ROLES = [
    {
        "name": "Strategist",
        "voice": "ADVISOR",
        "bias": (
            "You are the Strategist on a three-member council. "
            "You think long-term, question assumptions, and find "
            "the angle others miss. Be direct. State your actual view."
        ),
    },
    {
        "name": "Operator",
        "voice": "OPERATOR",
        "bias": (
            "You are the Operator on a three-member council. "
            "You think in execution, constraints, and what actually ships. "
            "Push back on anything that doesn't survive contact with reality."
        ),
    },
    {
        "name": "Challenger",
        "voice": "CHALLENGER",
        "bias": (
            "You are the Challenger on a three-member council. "
            "Your job is to find what's wrong, what's missing, and "
            "what everyone else is too polite to say. Be precise, not harsh."
        ),
    },
]

# Council composition (0.3.96+): three voices served by the primary provider.
#   Strategist → the heavy-reasoning model id
#   Operator   → the long-horizon model id
#   Challenger → the alternate-reasoning model id
# Synthesis runs on the heavy-reasoning model (see SYNTHESIS_MODEL below for
# why — not the Operator's model).
# Single-provider tradeoff acknowledged: if the primary provider goes down
# council is down; the cross-provider fallback to the aggregator fallback inside
# _call_model is the only safety net (and if it too fails, _synthesize returns a
# clear diagnostic).
COUNCIL_MODELS = [
    FW["pro"],
    FW["kimi"],
    FW["glm"],
]

# Synthesis runs on the heavy-reasoning model (the strongest reasoner) rather
# than the Operator's model — the Operator's model is the Operator voice, and
# using it for synthesis biased the final answer toward the Operator's framing
# (audit). The heavy-reasoning model is the Strategist's model but the synthesis
# prompt is anonymised, so there's no per-voice leakage; we just get the
# strongest model doing the merge.
SYNTHESIS_MODEL = FW["pro"]

MAX_DEBATE_ROUNDS = 3
# Empirically, lexical set-intersection-over-union across three independent
# models rarely exceeds ~0.18 even on trivial-consensus questions (audit
# measured 0.03–0.18 across 24 rounds; the old 0.4 was never reached, so
# council burned all rounds every time at ~3x cost). 0.12 matches the real
# ceiling so genuine consensus short-circuits the debate.
AGREEMENT_THRESHOLD = 0.12


# ── MAX partnership (0.4+): Qwen 3.8 Max × DeepSeek V4 Pro ────────────────────
# The top/MAX council tier. When BOTH native keys are set, the debate runs Qwen (heavy-reasoning / coding excel)
# against DeepSeek-V4-Pro (deep-reasoning excel) across the 3 debate roles — they disagree, then converge via the
# existing round loop; synthesis runs on DeepSeek-Pro. Uses more tokens (two frontier models deliberating) but
# activates silently — an invisible mechanic. No native key ⇒ the Fireworks 3-voice is byte-identical to before.
def _qwen_max_id() -> str:  return (os.environ.get("NX_QWEN_MODEL_MAX") or NATIVE["qwen_max"]).strip()
def _ds_reason_id() -> str: return (os.environ.get("NX_DEEPSEEK_MODEL_REASONER") or NATIVE["ds_reason"]).strip()
def _ds_chat_id() -> str:   return (os.environ.get("NX_DEEPSEEK_MODEL_CHAT") or NATIVE["ds_chat"]).strip()


def _native_council_active() -> bool:
    """The MAX partnership is available only when BOTH native keys are set (Qwen needs one voice, DeepSeek the other)."""
    return bool((os.environ.get(ENV["dashscope_api_key"], "") or "").strip() and (os.environ.get(ENV["deepseek_api_key"], "") or "").strip())


def _native_endpoint_for(model: str):
    """(base_url, api_key) for a native council model id, or None (⇒ the primary provider). Endpoint-per-model is
    what lets one council run Qwen (DashScope) and DeepSeek (native) side by side."""
    if model == _qwen_max_id():
        return URLS.get(P["dashscope"], ""), (os.environ.get(ENV["dashscope_api_key"], "") or "").strip()
    if model in (_ds_reason_id(), _ds_chat_id()):
        return URLS.get(P["deepseek"], ""), (os.environ.get(ENV["deepseek_api_key"], "") or "").strip()
    return None


def council_models() -> list:
    """The debate composition: the MAX Qwen × DeepSeek-Pro partnership when both native keys are set (mapped across
    the 3 roles so both models are heard and can disagree), else the Fireworks 3-voice default."""
    if _native_council_active():
        return [_qwen_max_id(), _ds_reason_id(), _qwen_max_id()]  # Strategist=Qwen · Operator=DeepSeek-Pro · Challenger=Qwen
    return list(COUNCIL_MODELS)


def synthesis_model() -> str:
    """Who merges the debate: DeepSeek-V4-Pro (deep-reasoning) in the MAX partnership, else the Fireworks reasoner."""
    return _ds_reason_id() if _native_council_active() else SYNTHESIS_MODEL


def _call_model(
    model: str, messages: list, api_key: str, timeout: int = 90,
    max_tokens: int = 1024,
) -> str:
    """
    Single model call against the primary provider. Falls through to
    the aggregator fallback (OR_FALLBACK model) on primary-provider failure.

    Council in 0.3.96+ runs all three voices on the primary provider.
    Per-request cross-provider retry is intentionally NOT implemented — model
    IDs differ across providers (the primary provider's p-notation vs the
    secondary provider's mixed-case), so a primary-provider model string
    wouldn't resolve on the secondary provider. The aggregator fallback below
    preserves council availability with a different model when the primary
    provider degrades.
    """
    from nx_key_pool import get_fireworks_key

    # Provider resolution: a NATIVE council model (Qwen on DashScope / DeepSeek native — the MAX partnership) hits
    # its OWN endpoint + key, so one council can run both side by side. Otherwise the primary provider (Fireworks),
    # using route()'s resolved key first then the cached primary key. The OR-fallback below covers both.
    keys_to_try: list[str] = []
    _nat = _native_endpoint_for(model)
    if _nat:
        base_url, _nat_key = _nat
        if _nat_key:
            keys_to_try.append(_nat_key)
    else:
        base_url = URLS.get(P["fireworks"], "")
        if api_key:
            keys_to_try.append(api_key)
        fw_key = get_fireworks_key()
        if fw_key and fw_key not in keys_to_try:
            keys_to_try.append(fw_key)

    # Per-attempt timeout: 45s. The heavy-reasoning model (the Strategist
    # voice) was dropping ~50% of the time at the old 30s cap under load.
    # Voices run in parallel under the outer as_completed(timeout+10) bound,
    # so 45s × up to 2 keys still fits the overall council budget.
    per_attempt = min(timeout, 45)
    for key in keys_to_try:
        try:
            r = httpx.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "stream": False,
                },
                timeout=per_attempt,
            )
            if r.status_code in (429, 503):
                continue
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"].strip()
            if content:
                # Strip CoT / identity leak BEFORE the text enters the debate
                # log or reaches synthesis. Some voices leak raw think-tokens
                # ~50% of the time; unfiltered, they pollute the debate context
                # and the final synthesis.
                return _clean(content)
            continue
        except Exception:
            continue

    fallback_key = os.environ.get(ENV["openrouter_api_key"])
    if not fallback_key:
        return ""
    try:
        r = httpx.post(
            f"{URLS[P['openrouter']]}/chat/completions",
            headers={
                "Authorization": f"Bearer {fallback_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": OR_FALLBACK,
                "messages": messages,
                "max_tokens": max_tokens,
                "stream": False,
            },
            timeout=timeout,
        )
        r.raise_for_status()
        return _clean(r.json()["choices"][0]["message"]["content"].strip())
    except Exception:
        return ""


def _get_round_responses(
    roles: list[dict],
    models: list[str],
    messages_list: list[list[dict]],
    api_key: str,
    timeout: int = 90,
) -> list[dict]:
    """Call all 3 models in parallel with a per-call timeout.

    On hard timeout, cancel pending futures so the REPL doesn't block waiting
    for slow models that exceeded their budget.
    """
    results = []
    executor = ThreadPoolExecutor(max_workers=3)
    try:
        # Track each future's role INDEX so the transcript order is
        # deterministic regardless of which model returns first.
        futures = {
            executor.submit(
                _call_model, model, messages, api_key, timeout
            ): (idx, role)
            for idx, (role, model, messages) in enumerate(zip(roles, models, messages_list))
        }
        try:
            for future in as_completed(futures, timeout=timeout + 10):
                idx, role = futures[future]
                try:
                    response = future.result(timeout=timeout)
                    if response:
                        results.append({
                            "_idx": idx,
                            "role": role["name"],
                            "response": response,
                        })
                except Exception:
                    continue
        except TimeoutError:
            pass
    finally:
        # Cancel pending futures so the executor doesn't block REPL shutdown.
        try:
            executor.shutdown(wait=False, cancel_futures=True)
        except TypeError:
            # Python <3.9 — best-effort shutdown only.
            executor.shutdown(wait=False)
    # Deterministic transcript order by role index (as_completed yields in
    # completion order, which varies run-to-run).
    results.sort(key=lambda r: r.get("_idx", 0))
    for r in results:
        r.pop("_idx", None)
    return results


def _agreement_score(responses: list[str]) -> float:
    """
    Agreement heuristic — ignores stopwords, measures real content overlap.
    Returns 0.0 to 1.0.

    Important: missing/failed responses return 0.0 (no agreement detectable),
    NOT 1.0 — a false 1.0 on failure was hiding silent model failures behind
    a fake "everyone agreed" verdict.
    """
    STOPWORDS = {
        "the","a","an","is","are","was","were","be","been","being",
        "have","has","had","do","does","did","will","would","could",
        "should","may","might","can","to","of","in","on","at","by",
        "for","with","about","as","it","its","this","that","these",
        "those","and","or","but","not","no","so","if","then","than",
        "i","you","we","they","he","she","my","your","our","their",
    }
    if not responses or len(responses) < 2:
        return 0.0

    word_sets = []
    for r in responses:
        if not r:
            continue
        words = {w for w in r.lower().split() if len(w) > 3 and w not in STOPWORDS}
        if words:
            word_sets.append(words)

    if len(word_sets) < 2:
        return 0.0

    common = word_sets[0]
    for ws in word_sets[1:]:
        common = common & ws

    all_words = set()
    for ws in word_sets:
        all_words |= ws

    if not all_words:
        return 0.0

    score = len(common) / max(len(all_words), 1)
    return score


SEPARATOR = "<!--COUNCIL_VOTE-->"
GOLD_SEPARATOR = "\n" + "━" * 60 + "\n"

def _synthesize(
    question: str,
    debate_log: list[dict],
    api_key: str,
    world: str = "cowork",
) -> str:
    """
    Final synthesis — produce the single best answer from the debate.

    Hardening (audit WS2):
      - Role labels are ANONYMISED ([Position N], not [Round N — Strategist])
        so the model can't name the council mechanics it's told to hide.
      - Each debate entry is trimmed (first 800 chars) so the synthesis input
        stays small and max_tokens isn't consumed by one voice's verbosity.
      - Hard length cap in the prompt (4 sentences) + the output runs through
        _call_model's _clean (strip narration + scrub identity).
      - Defensive fallback: if synthesis comes back empty / too short, return
        the longest clean voice response instead of a blank screen.
    """
    # Anonymise: no role names, no round numbers — just positions.
    entries = [e for e in debate_log if e.get("response")]
    parts = []
    for i, e in enumerate(entries, 1):
        parts.append(f"[Position {i}]: {e['response'][:800]}")
    debate_summary = GOLD_SEPARATOR.join(parts)

    messages = [
        {
            "role": "system",
            "content": (
                "You are NX. Built by Nexplora. Several independent analyses of "
                "the question follow. Output the single best answer — your own, "
                "in NX's voice.\n"
                "HARD RULES:\n"
                "- 4 sentences MAXIMUM. Pick the answer. No options menu, no recap.\n"
                "- NEVER mention positions, analyses, a council, advisors, a debate, "
                "voices, rounds, or synthesis. The operator asked a question; you "
                "answer it directly as if the thinking were your own.\n"
                "- Never name or hint at any base model, provider, or lab.\n"
                "- No preamble. No 'we need to'. First word is the answer.\n"
                "- End with one sharp question or a clean decisive close."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question: {question}\n\n"
                f"{debate_summary}\n\n"
                "Answer in 4 sentences max."
            ),
        },
    ]
    # Higher token budget so the model's CoT preamble doesn't consume the
    # whole window before a final answer (the empty-synthesis bug). _clean
    # strips the preamble; the 4-sentence prompt keeps the final short.
    result = _call_model(synthesis_model(), messages, api_key, timeout=90, max_tokens=2048)
    # Defensive: never return a blank/degenerate synthesis to the operator.
    if not result or len(result.strip()) < 40:
        # Fall back to the longest clean voice response we have.
        clean_voices = sorted(
            (e["response"] for e in entries if e.get("response") and len(e["response"]) >= 40),
            key=len, reverse=True,
        )
        if clean_voices:
            return _clean(clean_voices[0])
        # No usable voice at all → every model call failed (network / rate-limit / keys).
        # Tell the operator the REAL reason + the recovery, not a vague non-answer.
        return ("⚠ Council couldn't reach the model layer — all three voices failed "
                "(network, rate-limit, or key issue). Ask me directly without $council "
                "and I'll answer normally.")
    return result


def run_council(
    question: str,
    system_prompt: str,
    api_key: str,
    world: str = "cowork",
) -> str:
    """
    Main council entry point.
    Returns final synthesized answer as string.
    """
    debate_log = []

    # ── Round 1: independent positions ────────────────────────────────────────
    messages_list = []
    for role in COUNCIL_ROLES:
        messages_list.append([
            {
                "role": "system",
                "content": (
                    f"{system_prompt}\n\n"
                    f"{role['bias']}\n\n"
                    "Give your honest, direct position. "
                    "Be concise — 2-3 paragraphs maximum."
                ),
            },
            {"role": "user", "content": question},
        ])

    round_responses = []
    for resp in _get_round_responses(
        COUNCIL_ROLES, council_models(), messages_list, api_key, timeout=90
    ):
        debate_log.append({
            "round": 1,
            "role": resp["role"],
            "response": resp["response"],
        })
        round_responses.append(resp["response"])

    # ── Check agreement ────────────────────────────────────────────────────────
    if _agreement_score(round_responses) >= AGREEMENT_THRESHOLD:
        return _synthesize(question, debate_log, api_key, world)

    # ── Debate rounds: disagreement detected ──────────────────────────────────
    for debate_round in range(2, MAX_DEBATE_ROUNDS + 1):
        # Trim each prior-round entry to 600 chars so the context fed into
        # rounds 2/3 stays bounded (was growing to the full verbatim prior
        # round, ballooning token cost and timeout risk every round).
        prev_summary = "\n\n".join([
            f"[{e['role']}]: {e['response'][:600]}"
            for e in debate_log
            if e["round"] == debate_round - 1
        ])

        messages_list = []
        for role in COUNCIL_ROLES:
            messages_list.append([
                {
                    "role": "system",
                    "content": (
                        f"{system_prompt}\n\n"
                        f"{role['bias']}\n\n"
                        "You are in a council debate. "
                        "Read the other positions carefully. "
                        "Update your view if you see merit in theirs. "
                        "Hold firm if you don't. "
                        "Identify the single most important point of disagreement "
                        "and address it directly. Be concise."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Original question: {question}\n\n"
                        f"Current positions:\n{prev_summary}\n\n"
                        "Respond to the debate. Update or defend your position."
                    ),
                },
            ])

        new_responses = []
        for resp in _get_round_responses(
            COUNCIL_ROLES, council_models(), messages_list, api_key, timeout=90
        ):
            debate_log.append({
                "round": debate_round,
                "role": resp["role"],
                "response": resp["response"],
            })
            new_responses.append(resp["response"])

        if _agreement_score(new_responses) >= AGREEMENT_THRESHOLD:
            break

    # ── Final synthesis ────────────────────────────────────────────────────────
    return _synthesize(question, debate_log, api_key, world)
