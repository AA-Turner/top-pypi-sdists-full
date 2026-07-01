// ── Live context-window meter ──────────────────────────────────────────────
//
// The meter used to read from the gateway's `engine.context_window`, which
// is only populated when the engine commits to the Merkle DAG — *not* on
// every chat message. That made the meter show stale numbers that didn't
// update while the user was actively chatting.
//
// The fix: compute the meter client-side from the React `messages` array
// (the actual running conversation) + the active persona's system prompt
// (what the LLM will actually see on the next request). The server still
// provides the authoritative model context-window size via
// `/api/chat/context_meter`, but the breakdown + totals come from here.
//
// Token estimation uses a chars/4 heuristic. It's intentionally rough —
// the goal is "live indicator that ticks" not "byte-exact token accounting".
// Modern GPT/Claude tokenisers average 3.5-4.5 chars per token for English,
// so 4 is a defensible midpoint. Off by a few percent is fine for a meter.

import type { ContextMeter } from "@/lib/types";

type ContextMeterBreakdown = NonNullable<ContextMeter["breakdown"]>;

export interface DisplayMessageLite {
  role: "user" | "assistant" | "system" | "tool" | string;
  content: string;
  /** When true, message is still streaming and we want a live-update pulse. */
  pending?: boolean;
}

/** Estimate token count for an arbitrary string using a chars/4 heuristic. */
export function estimateTokens(text: string | null | undefined): number {
  if (!text) return 0;
  if (typeof text !== "string") return 0;
  // Round up so a 1-char string reports 1 token (not 0).
  return Math.max(1, Math.ceil(text.length / 4));
}

/**
 * Compute the live context-meter payload from the running message list.
 *
 * @param messages The actual displayed conversation (React state).
 * @param systemPrompt The active persona's system prompt text — what the
 *                     LLM will see in the system slot of the next request.
 * @param modelWindow The active model's context window (tokens). 0 if unknown.
 * @param meta Optional metadata about the model/provider/auto-compact state.
 */
export function computeLiveContextMeter(
  messages: DisplayMessageLite[],
  systemPrompt: string,
  modelWindow: number,
  meta: {
    model?: string;
    provider?: string;
    autoCompactPct?: number;        // 0..1
    lastAutoCompactAt?: string | null;
  } = {},
): ContextMeter {
  const autoCompactPct = clamp(meta.autoCompactPct ?? 0.5, 0.05, 0.95);

  const breakdown: ContextMeterBreakdown = {
    system: 0,
    user: 0,
    assistant: 0,
    tool: 0,
    other: 0,
  };

  // 1. System prompt — straight chars/4.
  breakdown.system = estimateTokens(systemPrompt);

  // 2. Conversation messages. Normalise the role into one of our buckets.
  for (const m of messages ?? []) {
    if (!m || !m.content) continue;
    const role = (m.role || "other").toLowerCase();
    const t = estimateTokens(m.content);
    if (role === "system") breakdown.system += t;
    else if (role === "user") breakdown.user += t;
    else if (role === "assistant") breakdown.assistant += t;
    else if (role === "tool") breakdown.tool += t;
    else breakdown.other += t;
  }

  const usedTokens =
    breakdown.system +
    breakdown.user +
    breakdown.assistant +
    breakdown.tool +
    breakdown.other;

  const totalTokens = modelWindow > 0 ? modelWindow : Math.max(usedTokens, 1);
  const usedPct = totalTokens > 0 ? usedTokens / totalTokens : 0;
  const thresholdTokens = Math.floor(totalTokens * autoCompactPct);
  const tokensUntilAutoCompact = Math.max(0, thresholdTokens - usedTokens);
  const pctUntilAutoCompact =
    totalTokens > 0 ? tokensUntilAutoCompact / totalTokens : 0;

  return {
    used_tokens: usedTokens,
    total_tokens: totalTokens,
    used_pct: usedPct,
    remaining_tokens: Math.max(0, totalTokens - usedTokens),
    remaining_pct: totalTokens > 0 ? 1 - usedPct : 0,
    auto_compact_threshold_tokens: thresholdTokens,
    auto_compact_threshold_pct: autoCompactPct,
    tokens_until_auto_compact: tokensUntilAutoCompact,
    pct_until_auto_compact: pctUntilAutoCompact,
    breakdown,
    model: meta.model || "",
    provider: meta.provider || "",
    last_auto_compact_at: meta.lastAutoCompactAt ?? null,
  };
}

function clamp(n: number, lo: number, hi: number): number {
  if (!Number.isFinite(n)) return lo;
  return Math.min(hi, Math.max(lo, n));
}

/**
 * Hook-style helper that recomputes the meter whenever any input changes.
 * Caller wires this into their own state via useMemo.
 */
export function makeLiveMeterDeps(
  messages: DisplayMessageLite[],
  systemPrompt: string,
  totalWindow: number,
  model: string,
  provider: string,
  autoCompactPct: number,
  lastAutoCompactAt: string | null,
): ContextMeter {
  return computeLiveContextMeter(messages, systemPrompt, totalWindow, {
    model,
    provider,
    autoCompactPct,
    lastAutoCompactAt,
  });
}
