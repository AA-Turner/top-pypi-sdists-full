"""Mock matching: which recorded span occurrence serves which replayed call.

Matching is a strategy with two responsibilities and one shared state shape:

- ``build_index(root)`` turns the original trace's span tree into a lookup
  the strategy understands (stored on the replay context as ``mock_tree``).
- ``claim(replay_ctx, ...)`` is called once per replayed child-span
  invocation and returns ``(call_index, entry)``: the occurrence index this
  invocation owns (``None`` when nothing is claimable) and the recorded
  entry to serve (``None`` on a miss). A claim MUST happen for every
  invocation sharing a ``(trace_function_key, span_name)`` pair, mocked or
  not, so later occurrences keep lining up.

``PositionalMatcher`` is the only strategy today: recorded occurrences are
numbered in original span-start order, replayed calls claim indexes in
arrival order, and inputs are ignored. ``raw_args``/``raw_kwargs`` are part
of the ``claim`` interface anyway so an input-aware strategy can slot in
without touching call sites; this strategy does not read them.

TODO(ankur): when a second strategy exists (input-fingerprint-first matching
for concurrent same-name calls), promote MATCHER to a per-replay choice
(a ``replay(match=...)`` kwarg over a small registry/factory). Deliberately
not built while there is one strategy: keep this module the only place that
knows how matching works, so the move is mechanical.
"""

from __future__ import annotations

import threading
from typing import Any

VariantChain = tuple[tuple[str, str], ...]

KEY_PART_SEPARATOR = "\x1f"


def counter_key(
    trace_function_key: str, span_name: str, variant_chain: VariantChain = ()
) -> str:
    key = f"{trace_function_key}:{span_name}"
    if not variant_chain:
        return key
    parts = [key]
    for chain_span_name, variant in variant_chain:
        parts.extend((chain_span_name, variant))
    return KEY_PART_SEPARATOR.join(parts)


def extend_variant_chain(
    variant_chain: VariantChain, span_name: str, variant: str | None
) -> VariantChain:
    if not variant:
        return variant_chain
    return (*variant_chain, (span_name, variant))


def _recorded_variant(node: dict[str, Any]) -> str | None:
    variant = node.get("variant")
    return variant if isinstance(variant, str) and variant else None


class PositionalMatcher:
    """Order-of-occurrence matching, per ``(trace_function_key, span_name)``."""

    def __init__(self) -> None:
        self._lock = threading.Lock()

    def build_index(self, root: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """Walk the children of a root span tree node depth-first and build a
        lookup keyed by ``f"{traceFunctionKey}:{spanName}:{call_index}"``.

        The root node itself is excluded: at replay time the runtime root span
        is ``is_root_span=True`` and never queries the mock tree.

        The compound ``(key, name)`` match is what disambiguates same-key spans
        that come from the fluent ``client.get_function(key).span(...)``
        pattern: every wrapped callable shares ``trace_function_key`` but
        differs in ``span_name``. The counter is per ``(key, name)`` pair so
        repeated same-name calls (including recursion) still order by
        occurrence.

        ``externalSpanId`` is copied so the lazy path can pull a payload-free
        span's recorded output on demand. ``output``/``outputMeta`` are copied
        ONLY when the node carried them inline (eager ``mock="all"`` tree, or
        an older server that ignores ``includeOutputs`` and returns outputs
        anyway): their absence, not a ``None`` value, is what signals the lazy
        fetch. So the key presence is preserved verbatim rather than defaulted
        to ``None``.
        """
        spans: dict[str, dict[str, Any]] = {}
        counters: dict[str, int] = {}

        def walk(node: dict[str, Any], variant_chain: VariantChain) -> None:
            key = node.get("traceFunctionKey")
            if key:
                name = node.get("spanName") or key
                variant_chain = extend_variant_chain(
                    variant_chain, name, _recorded_variant(node)
                )
                node_key = counter_key(key, name, variant_chain)
                index = counters.get(node_key, 0)
                counters[node_key] = index + 1
                entry: dict[str, Any] = {
                    "sourceSpanId": node.get("sourceSpanId"),
                    "externalSpanId": node.get("externalSpanId"),
                }
                if "output" in node:
                    entry["output"] = node["output"]
                if "outputMeta" in node:
                    entry["outputMeta"] = node["outputMeta"]
                spans[f"{node_key}:{index}"] = entry
            for child in node.get("children", []) or []:
                walk(child, variant_chain)

        for child in root.get("children", []) or []:
            walk(child, ())

        return spans

    def records_variants(self, root: dict[str, Any]) -> bool:
        pending = list(root.get("children", []) or [])
        while pending:
            node = pending.pop()
            if _recorded_variant(node) is not None:
                return True
            pending.extend(node.get("children", []) or [])
        return False

    def matched_variant_chain(
        self, replay_ctx: dict[str, Any] | None, variant_chain: VariantChain
    ) -> VariantChain:
        if not replay_ctx or not replay_ctx.get("mock_tree_has_variants"):
            return ()
        return variant_chain

    def key_for(
        self,
        replay_ctx: dict[str, Any] | None,
        *,
        trace_function_key: str,
        span_name: str,
        variant_chain: VariantChain = (),
    ) -> str:
        return counter_key(
            trace_function_key,
            span_name,
            self.matched_variant_chain(replay_ctx, variant_chain),
        )

    def claim(
        self,
        replay_ctx: dict[str, Any] | None,
        *,
        trace_function_key: str,
        span_name: str,
        is_root_span: bool,
        raw_args: tuple[Any, ...] | None = None,
        raw_kwargs: dict[str, Any] | None = None,
        variant_chain: VariantChain = (),
    ) -> tuple[int | None, dict[str, Any] | None]:
        """Claim this invocation's occurrence index and look up its entry.

        Returns ``(None, None)`` when there is nothing to claim: the root
        span, no replay context, or a context with neither a mock tree nor
        overrides. The counter advance is locked because replayed siblings
        can claim concurrently (``asyncio.gather``, and thread pools under
        ``trace_across_threads``).
        """
        if is_root_span or not replay_ctx:
            return (None, None)
        if "mock_tree" not in replay_ctx and not replay_ctx.get("mock_overrides"):
            return (None, None)
        key = self.key_for(
            replay_ctx,
            trace_function_key=trace_function_key,
            span_name=span_name,
            variant_chain=variant_chain,
        )
        with self._lock:
            counters = replay_ctx.setdefault("call_counters", {})
            call_index = counters.get(key, 0)
            counters[key] = call_index + 1
        entry = (replay_ctx.get("mock_tree") or {}).get(f"{key}:{call_index}")
        return (call_index, entry)


# TODO(ankur): single module-level instance until strategies become a
# per-replay choice; see the module docstring for the intended factory shape.
MATCHER = PositionalMatcher()
