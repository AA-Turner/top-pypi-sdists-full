"""Convert a canonical ``SKILL.md`` into a target assistant's on-disk format.

The source ``SKILL.md`` is assistant-agnostic: common prose plus optional inline blocks
``<!-- assistant:<selector> -->…<!-- /assistant:<selector> -->`` carrying content that only
some assistants should see. A selector is a plain name (``codex`` — kept only for Codex) or a
negated name (``!claude`` — kept for every assistant but Claude, i.e. the "all non-Claude
assistants, present and future" bucket). Every assistant — Claude included — is materialized
through a :class:`SkillConverter`, which strips the blocks that do not match its selector
(keeping the ones that do, markers removed) and applies the assistant's frontmatter /
``$ARGUMENTS`` rules.

Each converter is a pure string→string transform of the ``SKILL.md`` text. Materializing
skills on disk (copying subtrees, filtering by ``assistants:``, merging per-assistant
sub-directories, choosing the deploy location) belongs to the per-assistant deployment
module, not here.

One transform needs to know the full set of deployed skill names: rewriting a cross-skill
reference to the target assistant's invocation syntax. A ``SKILL.md`` written for Claude
delegates with the slash form (``invoke /code-review``); Codex invokes skills with ``$name``.
The deployment module passes the skill-name set into :meth:`SkillConverter.convert`, and a
converter with a :attr:`~SkillConverter.skill_ref_prefix` swaps ``/name`` → ``<prefix>name``
for exactly those names, never touching path-like slashes (``../references/…``, ``./foo``).
"""

import re
from abc import ABC, abstractmethod
from typing import Any

import yaml

_DELIMITER = "---"
# A leading YAML frontmatter block: an opening '---' line, any content, a closing '---'
# line. Body is everything after and is preserved verbatim.
_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)

# Match the ``$ARGUMENTS`` / ``${ARGUMENTS}`` placeholder as a whole token only — the
# negative lookahead stops it matching *inside* a longer identifier such as
# ``$ARGUMENTS_REFS`` (which is a different token, not the placeholder).
_ARGUMENTS_RE = re.compile(r"\$\{ARGUMENTS\}|\$ARGUMENTS(?![A-Za-z0-9_])")

# The left/right guards for a cross-skill reference rewrite (``/name`` → ``$name``). The
# lookbehind refuses any slash that is part of a path — one preceded by a word char, ``.``,
# ``/`` or ``~`` (``../references/…``, ``./foo``, ``https://host/x``, ``~/bin``) — so only a
# slash in invocation position (start of line, after a space, ``(``, backtick, …) qualifies.
# The lookahead refuses a trailing name char, ``-`` or ``/`` so ``/ci-run`` never fires inside
# ``/ci-run-local`` or a path segment ``/code-review/x``.
_REF_LEFT_GUARD = r"(?<![\w./~-])"
_REF_RIGHT_GUARD = r"(?![\w/-])"

# An inline per-assistant block: ``<!-- assistant:<selector> -->`` … ``<!-- /assistant:<selector> -->``.
# A selector is an assistant name (``codex``), kept only for that assistant, or a negated name
# (``!claude``), kept for every assistant *except* that one — the way to target "all future
# assistants but not Claude" without enumerating them.
# The trailing ``(?:[ \t]*\r?\n)?`` swallows the rest of the marker's own line *only* when the
# marker sits alone on it (block form), so a dropped block leaves no blank line and a kept block
# no dangling newline; an inline marker (text right after ``-->``) keeps its surrounding spaces.
_ASSISTANT_NAME = r"[A-Za-z0-9_-]+"
_SELECTOR = rf"!?{_ASSISTANT_NAME}"
_OPEN_TAG_RE = re.compile(rf"<!--[ \t]*assistant:({_SELECTOR})[ \t]*-->(?:[ \t]*\r?\n)?")


def _close_tag_re(selector: str) -> re.Pattern[str]:
    return re.compile(rf"<!--[ \t]*/assistant:{re.escape(selector)}[ \t]*-->(?:[ \t]*\r?\n)?")


def _selector_matches(selector: str, assistant: str) -> bool:
    """Whether a block tagged ``selector`` is kept for ``assistant``. A plain name matches that
    assistant; a ``!name`` selector matches every assistant other than ``name``."""
    if selector.startswith("!"):
        return assistant != selector[1:]
    return assistant == selector


def strip_assistant_blocks(body: str, assistant: str) -> str:
    """Resolve the ``<!-- assistant:X -->…<!-- /assistant:X -->`` blocks in ``body`` for
    ``assistant``: keep the blocks whose selector matches (markers removed), drop the others
    entirely. A selector is a plain name (``codex``) or a negated name (``!claude``, matching
    every assistant but that one). Text outside any block is preserved verbatim.

    Blocks do not nest. Raise :class:`ValueError` on an unterminated block or a nested open.
    """
    out: list[str] = []
    pos = 0
    while True:
        opened = _OPEN_TAG_RE.search(body, pos)
        if opened is None:
            out.append(body[pos:])
            return "".join(out)
        out.append(body[pos : opened.start()])
        selector = opened.group(1)
        closed = _close_tag_re(selector).search(body, opened.end())
        if closed is None:
            raise ValueError(f"unterminated <!-- assistant:{selector} --> block")
        inner = body[opened.end() : closed.start()]
        if _OPEN_TAG_RE.search(inner):
            raise ValueError(f"nested assistant blocks are not supported (inside assistant:{selector})")
        if _selector_matches(selector, assistant):
            out.append(inner)
        pos = closed.end()


def _split_frontmatter(md_text: str) -> tuple[str, str]:
    """Split ``md_text`` into ``(frontmatter_block, body)``.

    Raise :class:`ValueError` when there is no valid frontmatter: the first line must
    be ``---`` and a closing ``---`` line must follow. The body is returned untouched.
    """
    match = _FRONTMATTER_RE.match(md_text)
    if match is None:
        first_line = md_text.splitlines()[0].strip() if md_text.strip() else ""
        if first_line != _DELIMITER:
            raise ValueError("SKILL.md has no YAML frontmatter (missing opening '---')")
        raise ValueError("SKILL.md frontmatter is not terminated (missing closing '---')")
    return match.group(1), md_text[match.end() :]


class SkillConverter(ABC):
    """Rules for turning a canonical ``SKILL.md`` into one assistant's format.

    A concrete converter declares two things; the shared :meth:`convert` does the rest
    (splitting frontmatter, stripping the other assistants' inline blocks):

    - ``kept_frontmatter_keys`` — the frontmatter keys carried over. ``None`` keeps the
      frontmatter block verbatim (Claude, which uses ``allowed-tools`` / ``hooks`` /
      ``argument-hint``); a tuple reduces to those keys (everything else dropped).
    - ``arguments_replacement`` — text that replaces the ``$ARGUMENTS`` placeholder, or
      ``None`` to leave it untouched (for an assistant that interpolates arguments itself).
    - ``skill_ref_prefix`` — the prefix this assistant invokes a skill with, so a cross-skill
      reference ``/name`` is rewritten to ``<prefix>name`` for known skill names. ``None``
      (Claude) keeps the slash form, i.e. no rewrite.
    """

    kept_frontmatter_keys: tuple[str, ...] | None = ("name", "description")
    arguments_replacement: str | None = None
    skill_ref_prefix: str | None = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Assistant id this converter targets (matches an ``assistants:`` value)."""

    def convert(self, md_text: str, skill_names: frozenset[str] = frozenset()) -> str:
        """Convert a canonical ``SKILL.md`` string to this assistant's format.

        Render the frontmatter (per :attr:`kept_frontmatter_keys`), resolve the per-assistant
        inline blocks, neutralize ``$ARGUMENTS`` (per :attr:`arguments_replacement`) and rewrite
        cross-skill references in ``skill_names`` to this assistant's invocation syntax (per
        :attr:`skill_ref_prefix`). Raise :class:`ValueError` on missing/non-mapping frontmatter
        or a malformed block.
        """
        frontmatter, body = _split_frontmatter(md_text)
        body = strip_assistant_blocks(body, self.name)
        body = self._neutralize_arguments(body)
        rendered = f"{self._render_frontmatter(frontmatter)}\n{body}"
        return self._rewrite_skill_refs(rendered, skill_names)

    def _render_frontmatter(self, frontmatter: str) -> str:
        if self.kept_frontmatter_keys is None:
            return f"{_DELIMITER}\n{frontmatter}\n{_DELIMITER}"
        parsed: Any = yaml.safe_load(frontmatter)
        if parsed is None:
            parsed = {}
        if not isinstance(parsed, dict):
            raise ValueError("SKILL.md frontmatter is not a YAML mapping")
        kept = {key: parsed[key] for key in self.kept_frontmatter_keys if key in parsed}
        dumped = yaml.safe_dump(kept, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
        return f"{_DELIMITER}\n{dumped}\n{_DELIMITER}"

    def convert_reference(self, text: str, skill_names: frozenset[str] = frozenset()) -> str:
        """Convert a companion reference file (Markdown, no frontmatter) for this assistant.

        Resolves the per-assistant inline blocks, neutralizes ``$ARGUMENTS`` and rewrites
        cross-skill references exactly as :meth:`convert` does for a skill body, but expects and
        renders no frontmatter — reference files carry none. Files linked from a ``SKILL.md`` via
        ``../references/…`` deploy through this so their ``<!-- assistant:… -->`` blocks resolve
        per assistant.
        """
        body = self._neutralize_arguments(strip_assistant_blocks(text, self.name))
        return self._rewrite_skill_refs(body, skill_names)

    def _neutralize_arguments(self, body: str) -> str:
        if self.arguments_replacement is None:
            return body
        return _ARGUMENTS_RE.sub(self.arguments_replacement, body)

    def _rewrite_skill_refs(self, text: str, skill_names: frozenset[str]) -> str:
        """Rewrite ``/name`` → ``<skill_ref_prefix>name`` for every ``name`` in ``skill_names``
        that sits in invocation position (guarded against path-like slashes). A no-op when the
        assistant keeps the slash form (:attr:`skill_ref_prefix` is ``None``) or nothing is known."""
        if self.skill_ref_prefix is None or not skill_names:
            return text
        alternation = "|".join(re.escape(name) for name in sorted(skill_names, key=len, reverse=True))
        pattern = re.compile(rf"{_REF_LEFT_GUARD}/({alternation}){_REF_RIGHT_GUARD}")
        return pattern.sub(self.skill_ref_prefix + r"\1", text)


class ClaudeConverter(SkillConverter):
    """Claude: the canonical frontmatter is kept verbatim (``allowed-tools`` / ``hooks`` /
    ``argument-hint`` all matter) and ``$ARGUMENTS`` is left for Claude to interpolate. Only
    the other assistants' inline blocks are stripped."""

    name = "claude"
    kept_frontmatter_keys = None
    arguments_replacement = None


class CodexConverter(SkillConverter):
    """Codex: frontmatter reduced to ``name`` + ``description``; ``$ARGUMENTS`` neutralized
    (Codex does not interpolate it, so a literal placeholder would leak into the prompt); and
    cross-skill references rewritten from the slash form to Codex's ``$name`` invocation
    syntax (``invoke /code-review`` → ``invoke $code-review``)."""

    name = "codex"
    kept_frontmatter_keys = ("name", "description")
    arguments_replacement = "the user's request"
    skill_ref_prefix = "$"


_CONVERTERS: dict[str, SkillConverter] = {
    converter.name: converter for converter in (ClaudeConverter(), CodexConverter())
}


def get_skill_converter(assistant: str) -> SkillConverter:
    """Return the :class:`SkillConverter` for ``assistant``. Raises :class:`ValueError` for
    an assistant with no converter."""
    converter = _CONVERTERS.get(assistant)
    if converter is None:
        known = ", ".join(sorted(_CONVERTERS)) or "(none)"
        raise ValueError(f"no skill converter for assistant {assistant!r} (known: {known})")
    return converter


def converting_assistants() -> tuple[str, ...]:
    """Assistant ids that have a converter (every deploy target)."""
    return tuple(sorted(_CONVERTERS))


def convert_skill_md(md_text: str, skill_names: frozenset[str] = frozenset()) -> str:
    """Convenience wrapper: convert to the Codex format."""
    return get_skill_converter("codex").convert(md_text, skill_names)
