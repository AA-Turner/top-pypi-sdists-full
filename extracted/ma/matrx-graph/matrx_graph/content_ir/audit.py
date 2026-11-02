"""The never-lossy-by-accident mechanism (data-to-kinds skill, THE MERGE + TRANSLATION LAW).

Every adapter declares, per raw section, every known provider key as either
MAPPED (translated into the kind) or DROPPED (named + reasoned + approved by
Arman). A key in neither register is UNKNOWN: the provider added data we are
not consuming, and it SCREAMS — a red vcprint banner (captured durably to
``public.app_log`` by the host's observability root handler) plus a structured
entry on the returned report. It never raises: a new provider key must never
break a live call.

This module is FAMILY-AGNOSTIC on purpose. It was two drifting copies —
``search_kinds/audit.py`` and ``scraper_kinds/audit.py`` — until 2026-08-24,
and the copies had already diverged: only the scraper one had grown
:class:`DroppedValue` (THE SHOW-WHAT-YOU-HIDE LAW). Every kind family now
imports this one, and a family identifies itself through ``family`` /
``adapter_hint`` so the scream still names the exact file to edit.

``matrx_utils`` is a declared matrx-graph dependency (``pyproject.toml``:
``matrx-utils>=2.0.23``), so ``vcprint`` is imported directly — verified
2026-08-24. Nothing here imports ``aidream`` or any host module.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field


class UnknownKeys(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section: str
    keys: list[str]


class DroppedValue(BaseModel):
    """One thing the kind does NOT carry — named, reasoned, AND VALUED.

    Arman, 2026-08-23: *"on anything at all that you choose to remove or
    ignore… you still have to capture them, and you have to render them for me
    in a separate tab so that I can see exactly what we are hiding from the
    user."*

    A register that lists only key names cannot answer "is this worth keeping?"
    — you have to see the data. So the adapter records the VALUE beside the
    reason, and the demo renders it. ``preview`` is a size-bounded rendering of
    the value; ``size`` is the honest full magnitude (characters for a string,
    entries for a list/dict), so a 454-entry array reads as 454 even when only
    the first few are shown.
    """

    model_config = ConfigDict(extra="forbid")

    path: str = Field(description="Dotted path in the raw payload, e.g. 'overview.uuid'.")
    reason: str = Field(description="Why the kind does not carry it. Approved by Arman.")
    kind_of: str = Field(description="Python type name of the raw value.")
    size: int | None = Field(
        default=None, description="Characters for a string; entries for a list or dict."
    )
    preview: object | None = Field(
        default=None, description="Size-bounded rendering of the value, for human review."
    )


class TranslationReport(BaseModel):
    """What the adapter saw beyond its registers. Empty == fully accounted."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    unknown: list[UnknownKeys] = Field(default_factory=list)
    dropped: list[DroppedValue] = Field(
        default_factory=list,
        description="Everything the kind deliberately does not carry, with its actual value.",
    )

    @property
    def fully_accounted(self) -> bool:
        return not self.unknown


class KeyAudit:
    """Collects unknown raw keys, and captures dropped values, for one pass.

    ``family`` and ``adapter_hint`` exist only so the scream can name the file
    a reader must open. ``adapter_hint`` accepts a ``{provider}`` placeholder,
    which is filled with this audit's provider.
    """

    #: Longest string preview kept per dropped value. Big enough to judge what
    #: the data IS, small enough that a 114 kB duplicate does not ride along.
    PREVIEW_CHARS = 600
    #: Entries kept from a dropped list/dict. ``size`` still reports the total.
    PREVIEW_ENTRIES = 5

    def __init__(
        self,
        provider: str,
        *,
        family: str = "KIND",
        adapter_hint: str = "the adapter's MAPPED/DROPPED registers",
    ) -> None:
        self.provider = provider
        self.family = family
        self.adapter_hint = adapter_hint
        self._unknown: dict[str, set[str]] = {}
        self._dropped: list[DroppedValue] = []

    def drop(self, path: str, value: object, reason: str) -> None:
        """Record something the kind will not carry — with its actual value.

        Called for every entry in an adapter's DROPPED register that is
        actually PRESENT in this payload. Absent keys are not recorded: the
        point is to show what we are hiding, and nothing is hidden if the
        source did not send it.
        """
        if value is None or value == "" or value == [] or value == {}:
            return
        size: int | None = None
        preview: object = value
        if isinstance(value, str):
            size = len(value)
            preview = value[: self.PREVIEW_CHARS]
        elif isinstance(value, list | tuple):
            size = len(value)
            preview = list(value)[: self.PREVIEW_ENTRIES]
        elif isinstance(value, dict):
            size = len(value)
            preview = dict(list(value.items())[: self.PREVIEW_ENTRIES])
        self._dropped.append(
            DroppedValue(
                path=path,
                reason=reason,
                kind_of=type(value).__name__,
                size=size,
                preview=preview,
            )
        )

    def check(
        self,
        section: str,
        raw: Mapping[str, object],
        mapped: Iterable[str],
        dropped: Mapping[str, str],
        *,
        path_prefix: str | None = None,
    ) -> None:
        """Declare one raw section against its two registers — BOTH legs.

        Leg 1: anything in neither register is UNKNOWN and will scream.
        Leg 2: every DROPPED key actually present is captured with its value
        (THE SHOW-WHAT-YOU-HIDE LAW), so a register of key names can never
        again be the only answer to "should this be dropped?".

        ``path_prefix`` is the dotted prefix the captured drops are recorded
        under; it defaults to ``"<section>."``. Pass an explicit prefix for a
        top-level section whose keys are already the full path (``""``) or for
        a per-item loop that knows its index (``f"web.results[{i}]."``).
        """
        known = set(mapped) | set(dropped)
        for key in raw:
            if key not in known:
                self._unknown.setdefault(section, set()).add(key)
        prefix = f"{section}." if path_prefix is None else path_prefix
        for key, reason in dropped.items():
            if key in raw:
                self.drop(f"{prefix}{key}", raw[key], reason)

    def report(self) -> TranslationReport:
        unknown = [
            UnknownKeys(section=section, keys=sorted(keys))
            for section, keys in sorted(self._unknown.items())
        ]
        report = TranslationReport(
            provider=self.provider,
            unknown=unknown,
            dropped=sorted(self._dropped, key=lambda d: d.path),
        )
        if unknown:
            where = self.adapter_hint.replace("{provider}", self.provider)
            vcprint(
                {u.section: u.keys for u in unknown},
                title=(
                    f"{self.family.upper()} KIND ADAPTER — UNKNOWN {self.provider.upper()} KEYS. "
                    f"The provider is returning data we neither map nor approved dropping. "
                    f"Add each key to MAPPED or DROPPED in "
                    f"{where} (Arman approves drops)."
                ),
                color="red",
            )
        return report
