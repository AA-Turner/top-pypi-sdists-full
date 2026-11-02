"""CONTROL TOKENS — declared machine lines, stripped at the streaming source.

## The defect class this module closes (wall W9 tail, 2026-09-15)

A mandate's output contract sometimes asks a model to end its prose with one
machine line addressed to the SERVER, never to the person: the vision-interview
room's ``WRAP_RATING: 4`` is the canonical one. Every path that turned that
generation into something a person reads had to know about the line and strip it
itself. One path did (the orchestrated round); the direct chat path did not, and
``WRAP_RATING: 4`` was printed into a person's own interview as if the expert
had said it.

Fixing the two room contracts fixed that instance. The CLASS is wider: the
canonical streaming emitter — the ONE seam every provider's visible text passes
through on its way to every client — had no idea control tokens existed. So any
mandate that emits a control line into its prose leaks it to every client, and
keeps leaking until someone notices and patches the renderer of the day.

So the rule is:

🚨 **A control token is DECLARED here, stripped at the emitter, and delivered as
a structured ``control_token`` event.** Never a regex in a renderer, never a
second stripper in a service, never a client that "knows" to hide a line.

## What belongs in the registry

A token belongs here when a mandate/agent INSTRUCTION asks a model to emit a
``NAME: value`` line inside text that reaches a human-visible stream. A protocol
line that only ever drives a machine-only transcript (a benchmark harness that
no person reads) does not — but it must be named in that harness's own
allowlist so the census guard (``scripts/check_control_tokens_declared.py``)
can tell "deliberately not filtered" from "nobody declared it".

## How the streaming filter behaves

Providers deliver text in arbitrary deltas, so a control line arrives split
("WRAP_", "RATING: ", "4\\n"). The filter therefore holds back a trailing
PARTIAL line — but ONLY when that partial could still become a declared token
(cheap case-insensitive prefix test against the declared names). Ordinary prose
is never delayed by a single character: the test fails on the first byte and the
text goes straight to the wire.

🚨 Only a LINE START can be held. A delta is not a line: once the first bytes
of a line are on the wire, the rest of that line is released unexamined, and a
line that already carries a declared name is held only while its separator can
still follow. Judging each delta as a fresh line held a one-line JSON answer
from a mid-word ``"used…"`` delta until END (2026-09-24).

A complete line that matches a declared token is removed whole (its newline
with it) and its value is routed as a structured event. A line that merely
started like a token and then turned out to be prose is released intact.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace

__all__ = [
    "ControlTokenSpec",
    "ControlTokenHit",
    "ControlTokenRegistry",
    "FilteredText",
    "ControlTokenFilter",
    "CONTROL_TOKEN_REGISTRY",
    "register_control_token",
    "strip_control_tokens",
]


def _build_pattern(name: str, value_pattern: str) -> re.Pattern[str]:
    """One matcher shape for every token: ``NAME: value`` on a line of its own.

    ``=`` is accepted beside ``:`` and the name is case-insensitive because
    models paraphrase their own contract; the value group is the token's
    declared shape so a sentence that merely mentions the name is never eaten.
    """
    return re.compile(
        rf"^[ \t]*{re.escape(name)}[ \t]*[:=][ \t]*(?P<value>{value_pattern})[ \t]*$",
        re.IGNORECASE,
    )


def _build_bare_pattern(name: str) -> re.Pattern[str]:
    """A bare protocol word alone on its line — no value, no separator."""
    return re.compile(rf"^[ \t]*{re.escape(name)}[ \t]*(?P<value>)$", re.IGNORECASE)


@dataclass(frozen=True)
class ControlTokenSpec:
    """One declared machine line: who asks for it, how to find it, what it means."""

    #: The literal line prefix the model is told to emit, e.g. ``WRAP_RATING``.
    name: str
    #: Which mandate / contract asks a model to emit it. Free text, but it must
    #: name something a human can go read — this is what the census guard and
    #: the per-mandate knob key off.
    declared_by: str
    #: Human sentence: what the value MEANS. Shown in the leak scream.
    purpose: str
    #: Regex for the value, WITHOUT groups of its own meaning — the whole value
    #: is captured for the structured event.
    value_pattern: str = r".+"
    #: A token with NO value: a bare protocol word on its own line (the bench
    #: harness's ``FINAL``). ``value_pattern`` is ignored and the event carries
    #: an empty value.
    bare: bool = False
    #: The per-mandate knob's default. ``False`` declares a token that is known
    #: but deliberately left in the visible stream (a machine-only transcript).
    filter_enabled: bool = True

    pattern: re.Pattern[str] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("a control token needs a name")
        if not self.declared_by:
            raise ValueError(
                f"control token {self.name!r} must name the mandate that emits it "
                "— an undeclared owner is how the W9 tail happened"
            )
        object.__setattr__(
            self,
            "pattern",
            _build_bare_pattern(self.name.strip())
            if self.bare
            else _build_pattern(self.name.strip(), self.value_pattern),
        )

    def match(self, line: str) -> str | None:
        """The token's value when ``line`` IS this control line, else ``None``."""
        m = self.pattern.match(line)
        return None if m is None else m.group("value").strip()


@dataclass(frozen=True)
class ControlTokenHit:
    """One control line that was stripped out of a visible stream."""

    name: str
    value: str
    declared_by: str


class ControlTokenRegistry:
    """THE registry. Declared once at import; read by the emitter and the guard."""

    def __init__(self) -> None:
        self._specs: dict[str, ControlTokenSpec] = {}
        #: mandate key → filtering enabled. Absent means "use the spec default".
        self._mandate_overrides: dict[str, bool] = {}

    # -- declaration ---------------------------------------------------
    def register(self, spec: ControlTokenSpec) -> ControlTokenSpec:
        """Declare a token. Re-registering the SAME spec is a no-op (imports
        run more than once); re-registering a DIFFERENT one for the same name
        raises, because two matchers for one token is the original defect."""
        key = spec.name.upper()
        existing = self._specs.get(key)
        if existing is not None:
            same = (
                existing.bare == spec.bare
                and existing.value_pattern == spec.value_pattern
                and existing.declared_by == spec.declared_by
                and existing.filter_enabled == spec.filter_enabled
            )
            if not same:
                raise ValueError(
                    f"control token {spec.name!r} is already declared by "
                    f"{existing.declared_by!r} with a different contract; one token "
                    "has exactly ONE matcher — change the declaration, do not add a second"
                )
            return existing
        self._specs[key] = spec
        return spec

    def get(self, name: str) -> ControlTokenSpec | None:
        return self._specs.get(name.upper())

    def specs(self) -> tuple[ControlTokenSpec, ...]:
        return tuple(self._specs[k] for k in sorted(self._specs))

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._specs))

    # -- the knob ------------------------------------------------------
    def set_mandate_filtering(self, mandate_key: str, enabled: bool) -> None:
        """THE PER-MANDATE KNOB. ``enabled=False`` lets one mandate's stream
        carry its declared control lines verbatim (a machine-only transcript
        consumer that parses them itself)."""
        self._mandate_overrides[mandate_key] = enabled

    def clear_mandate_filtering(self, mandate_key: str) -> None:
        self._mandate_overrides.pop(mandate_key, None)

    def mandate_filtering(self, mandate_key: str | None) -> bool | None:
        if mandate_key is None:
            return None
        return self._mandate_overrides.get(mandate_key)

    def active_specs(self, mandate_key: str | None = None) -> tuple[ControlTokenSpec, ...]:
        override = self.mandate_filtering(mandate_key)
        if override is False:
            return ()
        if override is True:
            return tuple(replace(s, filter_enabled=True) for s in self.specs())
        return tuple(s for s in self.specs() if s.filter_enabled)


CONTROL_TOKEN_REGISTRY = ControlTokenRegistry()


def register_control_token(
    *,
    name: str,
    declared_by: str,
    purpose: str,
    value_pattern: str = r".+",
    bare: bool = False,
    filter_enabled: bool = True,
) -> ControlTokenSpec:
    """Declare a control token on the canonical registry."""
    return CONTROL_TOKEN_REGISTRY.register(
        ControlTokenSpec(
            name=name,
            declared_by=declared_by,
            purpose=purpose,
            value_pattern=value_pattern,
            bare=bare,
            filter_enabled=filter_enabled,
        )
    )


@dataclass(frozen=True)
class FilteredText:
    """Visible text plus every control line taken out of it."""

    text: str
    hits: tuple[ControlTokenHit, ...] = ()

    @property
    def found(self) -> bool:
        return bool(self.hits)


def _line_could_start_token(partial: str, specs: tuple[ControlTokenSpec, ...]) -> bool:
    """Could this incomplete line still become one of ``specs``?

    True for a prefix of a declared name (``"WRAP_"``), for a line that already
    carries the full name (``"WRAP_RATING: "`` — value not streamed yet), and
    for leading whitespace alone. False — the overwhelmingly common case — for
    the first byte of ordinary prose, which is why normal streaming is never
    delayed.
    """
    candidate = partial.lstrip(" \t").upper()
    if not candidate:
        return bool(specs)
    for spec in specs:
        name = spec.name.upper()
        if name.startswith(candidate):
            return True
        # The full name is already here: only the declared separator (or, for a
        # bare word, nothing at all) may follow it. "USED CARS" can never become
        # ``USED: …`` and must not wait for a newline a one-line answer never sends.
        if candidate.startswith(name) and _TOKEN_TAIL[spec.bare].match(candidate[len(name) :]):
            return True
    return False


#: Every line break ``str.splitlines`` honors — "did this line end?" must use
#: the SAME set the splitter uses, or a ``\u2028``-terminated delta reads as
#: an unfinished line and the next real line is waved through as its tail.
_LINE_BREAKS = frozenset("\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029")


def _ends_line(text: str) -> bool:
    return bool(text) and text[-1] in _LINE_BREAKS


#: What may follow a declared name on a line that is still becoming a token:
#: ``[ \t]*`` then (for a valued token) the ``:``/``=`` separator and anything.
_TOKEN_TAIL = {
    False: re.compile(r"[ \t]*(?:[:=].*)?\Z", re.DOTALL),
    True: re.compile(r"[ \t]*\Z"),
}


class ControlTokenFilter:
    """Strips declared control lines out of a delta stream, in order.

    Not thread-safe and not re-entrant: one filter per emitter, fed from the one
    coroutine that owns the wire.
    """

    def __init__(
        self,
        *,
        mandate_key: str | None = None,
        registry: ControlTokenRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._registry = registry or CONTROL_TOKEN_REGISTRY
        self._mandate_key = mandate_key
        self._enabled = enabled
        self._pending = ""
        # True once the CURRENT line's first bytes have gone to the wire. The
        # rest of that line can never be a control line (the matcher is anchored
        # at the line start), so it is never held. Without this every delta was
        # judged as if it began a line: a one-line JSON answer whose delta
        # happened to start with "used" was held until END (2026-09-24).
        self._mid_line = False

    # -- configuration -------------------------------------------------
    @property
    def enabled(self) -> bool:
        return self._enabled and bool(self._specs())

    def configure(self, *, mandate_key: str | None = None, enabled: bool | None = None) -> None:
        if mandate_key is not None:
            self._mandate_key = mandate_key
        if enabled is not None:
            self._enabled = enabled

    def _specs(self) -> tuple[ControlTokenSpec, ...]:
        if not self._enabled:
            return ()
        return self._registry.active_specs(self._mandate_key)

    # -- the stream ----------------------------------------------------
    def feed(self, text: str) -> FilteredText:
        """Visible text for the wire, plus any completed control lines."""
        specs = self._specs()
        if not specs:
            out = self._pending + text
            self._pending = ""
            if out:
                self._mid_line = not _ends_line(out)
            return FilteredText(text=out)
        if not text:
            return FilteredText(text="")

        buffer = self._pending + text
        self._pending = ""
        lines = buffer.splitlines(keepends=True)
        trailing = ""
        if lines and not _ends_line(lines[-1]):
            trailing = lines.pop()

        visible: list[str] = []
        hits: list[ControlTokenHit] = []
        # A held partial always begins at a line start, so ``_mid_line`` is only
        # ever True with an empty pending buffer: the first segment continues a
        # line whose start is already on the wire.
        continuing = self._mid_line
        for line in lines:
            hit = None if continuing else _match_line(line.rstrip("\r\n"), specs)
            continuing = False
            if hit is None:
                visible.append(line)
            else:
                hits.append(hit)

        self._mid_line = False
        if trailing:
            if not continuing and _line_could_start_token(trailing, specs):
                self._pending = trailing
            else:
                visible.append(trailing)
                self._mid_line = True

        return FilteredText(text="".join(visible), hits=tuple(hits))

    def start_line(self) -> None:
        """A new model call begins on a fresh line, whatever the last one ended on.

        The emitter calls this at every turn boundary — otherwise a call that
        ended mid-line would make the next call's first line (``WRAP_RATING: 4``)
        a "continuation" and wave it through to the wire.
        """
        self._mid_line = False

    def flush(self) -> FilteredText:
        """End of stream: the held partial line is a control line or it is text.

        Nothing is ever dropped — a partial that never matched is released
        verbatim, in order, before the stream ends.
        """
        pending, self._pending = self._pending, ""
        self._mid_line = False
        if not pending:
            return FilteredText(text="")
        specs = self._specs()
        if specs:
            hit = _match_line(pending.rstrip("\r\n"), specs)
            if hit is not None:
                return FilteredText(text="", hits=(hit,))
        return FilteredText(text=pending)

    @property
    def has_pending(self) -> bool:
        return bool(self._pending)


def _match_line(body: str, specs: tuple[ControlTokenSpec, ...]) -> ControlTokenHit | None:
    for spec in specs:
        m = spec.pattern.match(body)
        if m is None:
            continue
        value = m.group("value").strip()
        return ControlTokenHit(name=spec.name, value=value, declared_by=spec.declared_by)
    return None


def strip_control_tokens(
    text: str | None,
    *,
    names: tuple[str, ...] | None = None,
    registry: ControlTokenRegistry | None = None,
) -> FilteredText:
    """Whole-text stripper for non-streaming paths (persistence, batch replies).

    ``names`` narrows to specific declared tokens; the default walks every
    declared token, filtered or not, because a non-streaming consumer that asks
    to strip is asking for clean text.
    """
    reg = registry or CONTROL_TOKEN_REGISTRY
    if names is None:
        specs = reg.specs()
    else:
        specs = tuple(s for n in names if (s := reg.get(n)) is not None)
    working = text or ""
    if not working or not specs:
        return FilteredText(text=working)

    visible: list[str] = []
    hits: list[ControlTokenHit] = []
    for line in working.splitlines(keepends=True):
        hit = _match_line(line.rstrip("\r\n"), specs)
        if hit is None:
            visible.append(line)
        else:
            hits.append(hit)
    return FilteredText(text="".join(visible), hits=tuple(hits))
