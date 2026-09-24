"""Custom Dictionary config — the unified shape that every provider translator
presents natively.

A dictionary carries terminology + pronunciation entries (resolved + merged from
the user/org/scope-type/scope levels by the `dict_resolve` RPC). It serves two
masters with ONE shape:

  • Text-gen / cleanup LLMs  → a definitions+spelling context block injected into
    the system text (so the model emits the right spellings and understands the
    terms).
  • TTS / non-function-calling models → a terse "pronounce X as Y" directive that
    survives the chat-decoration stripping non-FC models go through.

Translators read `UnifiedConfig.dictionary` and call the appropriate renderer.
The field may arrive as a `DictionaryConfig` (server auto-injection sets it
directly) or as a plain dict (when it rides `config_overrides` from a request
payload and round-trips through LLMParams.model_dump) — `coerce()` normalizes
either into a `DictionaryConfig`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

# Mirror of the agent context-policy inline policy: None → default, 0 → never.
DEFAULT_INLINE_CHARS = 200


class DictionaryEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")

    term: str
    sounds_like: list[str] = []
    pronunciation: str | None = None
    ipa: str | None = None
    definition: str | None = None
    category: str | None = None
    source_level: str | None = None
    source_name: str | None = None


class GlossaryEntry(BaseModel):
    """One translation rule from an attached term list.

    ``translation`` None with ``do_not_translate`` True means "keep the source
    term verbatim in every target language". ``target_language`` None means the
    rule applies to every target language.
    """

    model_config = ConfigDict(extra="ignore")

    term: str
    translation: str | None = None
    target_language: str | None = None
    do_not_translate: bool = False
    case_sensitive: bool = False


class DictionaryConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    # The PERSISTENT set — the global+user rollup (merged + deduped across the
    # org/scope tiers up to the user). Reused across every request; on ElevenLabs
    # it is the published, cached pronunciation dictionary.
    entries: list[DictionaryEntry] = []
    # The PER-TASK set — ad-hoc additions the user attached to *this* request only
    # (the "situational" dictionary). Never persisted; present only when the user
    # truly has a task-specific list. Applied on top of `entries`, most-specific.
    custom_entries: list[DictionaryEntry] = []
    # None → inherits the 200-char default; 0 → never inline; N → custom ceiling.
    max_inline_chars: int | None = None
    source_count: int = 0
    # Translation rules from attached term lists (translate / do-not-translate).
    # Rendered as a glossary section for chat models; vendors with a native
    # glossary (DeepL, Google) get it natively instead.
    glossary: list[GlossaryEntry] = []
    # Free prose from attached term lists — context that rides WITH the terms and
    # is never itself translated or spoken.
    context: str | None = None

    # ── construction ──────────────────────────────────────────────────────
    @classmethod
    def coerce(cls, value: DictionaryConfig | dict[str, Any] | None) -> DictionaryConfig | None:
        """Normalize a DictionaryConfig | dict | None into a DictionaryConfig | None."""
        if value is None:
            return None
        if isinstance(value, DictionaryConfig):
            return value
        if isinstance(value, dict):
            try:
                return cls.model_validate(value)
            except Exception:
                return None
        return None

    # ── queries ───────────────────────────────────────────────────────────
    @property
    def is_empty(self) -> bool:
        return not (self.entries or self.custom_entries or self.glossary or self.context)

    @property
    def all_entries(self) -> list[DictionaryEntry]:
        """Persistent + per-task, in priority order (per-task wins on conflict).

        `alias_pairs()` dedupes by lowercased form keeping the first occurrence,
        so listing `custom_entries` FIRST makes a task-specific respelling
        override the persistent one for the same term.
        """
        return [*self.custom_entries, *self.entries]

    @property
    def effective_inline_chars(self) -> int:
        return DEFAULT_INLINE_CHARS if self.max_inline_chars is None else self.max_inline_chars

    def _sorted(self) -> list[DictionaryEntry]:
        # Deterministic order → byte-identical render → prompt-cache stable.
        return sorted(self.all_entries, key=lambda e: e.term.lower())

    # ── renderers ─────────────────────────────────────────────────────────
    def render_glossary_block(self) -> str:
        """Translation glossary + term-list context for chat models.

        Deterministic (sorted) so identical lists yield a byte-identical block
        and the prompt cache holds.
        """
        lines: list[str] = []
        keep = sorted({g.term for g in self.glossary if g.do_not_translate}, key=str.lower)
        rules = sorted(
            (g for g in self.glossary if not g.do_not_translate and g.translation),
            key=lambda g: (g.term.lower(), (g.target_language or "").lower()),
        )
        if keep:
            lines.append(
                "Never translate these terms; keep them exactly as written in every language:"
            )
            lines.extend(f'- "{t}"' for t in keep)
        if rules:
            lines.append("Required translations (use exactly these renderings):")
            for g in rules:
                lang = f" [{g.target_language}]" if g.target_language else ""
                lines.append(f'- "{g.term}"{lang} -> "{g.translation}"')
        if self.context and self.context.strip():
            lines.append(
                "Context for these terms (guidance only; never translate or repeat it):\n"
                + self.context.strip()
            )
        if not lines:
            return ""
        return "Glossary:\n" + "\n".join(lines)

    def render_context_block(self) -> str:
        """Definitions + spellings + pronunciations for text-gen / cleanup LLMs."""
        if self.is_empty:
            return ""
        blocks: list[str] = []
        glossary = self.render_glossary_block()
        if not (self.entries or self.custom_entries):
            return glossary
        lines: list[str] = []
        for e in self._sorted():
            parts = [f"- **{e.term}**"]
            if e.pronunciation:
                parts.append(f'pronounced "{e.pronunciation}"')
            if e.ipa:
                parts.append(f"/{e.ipa}/")
            if e.sounds_like:
                parts.append("often misheard as: " + ", ".join(e.sounds_like))
            if e.definition:
                parts.append(f"— {e.definition}")
            lines.append(" · ".join(parts))
        blocks.append(
            "Custom dictionary (preferred spellings & pronunciations):\n" + "\n".join(lines)
        )
        if glossary:
            blocks.append(glossary)
        return "\n\n".join(blocks)

    def render_pronunciation_directive(self) -> str:
        """Terse pronunciation guidance for TTS / non-function-calling models.

        Only entries that actually carry pronunciation guidance are included
        (a definitions dump would waste the prompt and confuse a TTS model).
        """
        pairs: list[str] = []
        for e in self._sorted():
            say_as = e.pronunciation or (e.ipa and f"/{e.ipa}/")
            if say_as:
                pairs.append(f'"{e.term}" as {say_as}')
        if not pairs:
            return ""
        return "Pronounce the following terms precisely: " + "; ".join(pairs) + "."

    def render_for_system(self, supports_tools: bool) -> str:
        """Pick the right shape for the model class."""
        return (
            self.render_context_block() if supports_tools else self.render_pronunciation_directive()
        )

    # ── alias substitution (the universal, provider-agnostic primitive) ──────
    def alias_pairs(self) -> list[tuple[str, str]]:
        """(`form`, `say_as`) pairs for every entry that carries a spoken form.

        `form` is the written term (and each `sounds_like` variant); `say_as` is
        the `pronunciation` respelling. This is the alphabet-free mechanism that
        works on EVERY TTS provider — ElevenLabs alias rules, and plain text
        substitution for providers with no native dictionary (Google Gemini-TTS,
        xAI Grok). Longest `form` first so multi-word terms replace before their
        substrings.
        """
        pairs: list[tuple[str, str]] = []
        for e in self.all_entries:
            say_as = (e.pronunciation or "").strip()
            if not say_as:
                continue
            for form in [e.term, *e.sounds_like]:
                form = (form or "").strip()
                if form:
                    pairs.append((form, say_as))
        pairs.sort(key=lambda p: len(p[0]), reverse=True)
        return pairs

    def apply_aliases(self, text: str) -> str:
        """Rewrite `text`, substituting each term/sounds-like form with its
        `pronunciation` respelling (word-bounded, case-insensitive, first form
        per lowercased key wins). Used for TTS providers WITHOUT a native
        pronunciation-dictionary feature. No-op when nothing to apply."""
        if not text:
            return text
        import re

        out = text
        seen: set[str] = set()
        for frm, to in self.alias_pairs():
            key = frm.lower()
            if key in seen:
                continue
            seen.add(key)
            out = re.sub(rf"(?<!\w){re.escape(frm)}(?!\w)", to, out, flags=re.IGNORECASE)
        return out


# ── the universal TTS pronunciation floor ───────────────────────────────────
def apply_tts_dictionary(
    dictionary: DictionaryConfig | dict[str, Any] | None,
    text: str,
    *,
    provider: str = "",
    model: str = "",
) -> str:
    """Substitute every dictionary term's written form (and its sounds-like
    variants) with its `pronunciation` respelling in TTS input `text`.

    This is the provider-agnostic *floor*: it makes custom pronunciation work on
    EVERY engine that lacks a reliable native pronunciation dictionary — Groq,
    xAI, OpenAI, Google Gemini-TTS, and ElevenLabs `text_to_dialogue` (whose
    native locators don't apply). Providers WITH a native channel
    (ElevenLabs `convert` locators on supporting models, Cartesia inline tags,
    Google Cloud-TTS `customPronunciations`) layer that on top for higher
    fidelity and skip this floor for the covered terms.

    Loud & best-effort: logs (yellow) when a substitution actually fires — a
    recovery layer firing must be visible — and NEVER raises (a dictionary
    failure must never break a TTS render). No-op when there's no dictionary or
    nothing matches.
    """
    if not text:
        return text
    try:
        conf = DictionaryConfig.coerce(dictionary)
        if conf is None or conf.is_empty:
            return text
        out = conf.apply_aliases(text)
        if out != text:
            try:
                from matrx_utils import vcprint

                n = len(conf.entries) + len(conf.custom_entries)
                vcprint(
                    f"[TTS dictionary] {provider or '?'}/{model or '?'}: applied "
                    f"pronunciation substitution ({n} entries)",
                    color="yellow",
                )
            except Exception:  # noqa: BLE001 — logging must never break a render
                pass
        return out
    except Exception as exc:  # noqa: BLE001 — best-effort floor, never break TTS
        try:
            from matrx_utils import vcprint

            vcprint(f"[TTS dictionary] substitution skipped (error): {exc}", color="red")
        except Exception:
            pass
        return text
