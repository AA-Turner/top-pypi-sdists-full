"""Cross-token ``<thinking>`` stripping for streaming LLM output (no Rich dependency)."""


def _emit_safe_before_incomplete_open(pending: str, open_tag: str) -> tuple[str, str]:
    """Emit a prefix that cannot still complete ``open_tag``; keep a possible prefix tail."""
    n = len(pending)
    if not n:
        return "", ""
    lo = len(open_tag)
    # Earliest index where pending[i:] is a nonempty prefix of open_tag (incomplete or complete).
    min_i = n
    start = max(0, n - (lo - 1))
    for i in range(start, n):
        tail = pending[i:]
        if tail and open_tag.startswith(tail):
            min_i = min(min_i, i)
    if min_i < n:
        return pending[:min_i], pending[min_i:]
    return pending, ""


class ThinkingSuppressionFilter:
    """Strip ``<thinking>...</thinking>`` from a token stream; tags may span tokens."""

    __slots__ = ("_in_thinking", "_pending")

    def __init__(self) -> None:
        self._pending = ""
        self._in_thinking = False

    def feed(self, piece: str) -> str:
        self._pending += piece
        out: list[str] = []
        open_tag, close_tag = "<thinking>", "</thinking>"

        while True:
            if not self._in_thinking:
                idx = self._pending.find(open_tag)
                if idx == -1:
                    emit, self._pending = _emit_safe_before_incomplete_open(self._pending, open_tag)
                    if emit:
                        out.append(emit)
                    break
                if idx > 0:
                    out.append(self._pending[:idx])
                self._pending = self._pending[idx + len(open_tag) :]
                self._in_thinking = True
                continue
            j = self._pending.find(close_tag)
            if j == -1:
                break
            self._pending = self._pending[j + len(close_tag) :]
            self._in_thinking = False

        return "".join(out)

    def flush_display_tail(self) -> str:
        if self._in_thinking:
            return ""
        tail = self._pending
        self._pending = ""
        return tail

    @property
    def in_thinking(self) -> bool:
        return self._in_thinking
