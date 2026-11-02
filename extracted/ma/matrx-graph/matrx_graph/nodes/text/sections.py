"""text.sections.patch — edit a markdown document section by section.

A section is marked by an invisible HTML comment, ``<!-- matrx:section:<key> -->``,
followed by its plain markdown (normally opening with a ``## Heading``); it runs
to the next marker or the end. Every markdown renderer hides the marker, so what
is stored is what the person reads. Text before the first marker is kept as is.

Each edit is ``{section_key, op: create | replace | append, markdown}``, applied in
order. An edit with a bad key, an unknown op, an empty or placeholder body, or
(``on_missing="refuse"``) a missing section is refused and reported, never
applied, and so is a body carrying a section marker line. A document in the
retired ``<key>…</key>`` shape (block tags, and no markers yet) is upgraded once,
before the edits (``upgrade_legacy_tags``), and reported as ``upgraded_legacy``;
HTML that an edit writes, inline HTML, and any document that already has markers
are kept as written. Pure: no I/O, no AI.

Behavior matches aidream's ``vision_interview/document_sections.py`` +
``scribe_apply.apply_doc_patches`` byte for byte at the default settings (parity
test: ``aidream/graph_actions/tests/test_text_sections_patch_parity.py``) with two
deliberate differences: the old code upgraded tags in ANY document on every split (inline
HTML, edit bodies and saved documents became fake sections), counted an upgrade alone as a
change, and accepted bodies carrying marker lines.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

_KEY = r"[A-Za-z_][A-Za-z0-9_.\-]*"
KEY_RE = re.compile(rf"^{_KEY}$")
_PREFIX_RE = re.compile(r"^[A-Za-z0-9_.:\-]+$")
# Block-shaped only: the open tag starts its own line and the close tag ends its own line, so
# inline HTML (``a <b>word</b> here``) is never mistaken for a retired section.
_LEGACY_SECTION_RE = re.compile(
    rf"^(?P<lead>[ \t]*)<(?P<key>{_KEY})(?:\s[^>]*)?>(?P<inner>.*?)</(?P=key)\s*>(?=[ \t]*$)",
    re.DOTALL | re.MULTILINE,
)
_H2_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)

DEFAULT_PLACEHOLDER_BODIES: tuple[str, ...] = (
    "placeholder",
    "tbd",
    "todo",
    "n/a",
    "none",
    "...",
    "…",
    "(placeholder)",
    "pending",
)
DEFAULT_MIN_BODY_CHARS = 3
DEFAULT_MARKER_PREFIX = "matrx:section"


class SectionEdit(BaseModel):
    model_config = ConfigDict(extra="ignore")
    section_key: str = Field(description="The section's key, e.g. core_idea.")
    op: str = Field(description="create, replace or append.")
    markdown: str = Field(default="", description="The section's new (or added) markdown.")


class SectionsPatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document: str = Field(default="", description="The markdown document to edit.")
    edits: list[SectionEdit] = Field(default_factory=list, description="Edits to apply, in order.")


class SectionsPatchConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    on_missing: Literal["create", "refuse"] = Field(
        default="create",
        description="When a replace or append names a section that does not exist: "
        "create it, or refuse the edit.",
    )
    placeholder_bodies: list[str] = Field(
        default_factory=lambda: list(DEFAULT_PLACEHOLDER_BODIES),
        description="Bodies refused as placeholders (compared ignoring case and "
        "surrounding # * - _ marks).",
    )
    min_body_chars: int = Field(
        default=DEFAULT_MIN_BODY_CHARS,
        ge=1,
        description="Bodies shorter than this (after trimming) are refused.",
    )
    marker_prefix: str = Field(
        default=DEFAULT_MARKER_PREFIX,
        description="Marker name: sections are marked <!-- prefix:key -->.",
    )
    upgrade_legacy_tags: bool = Field(
        default=True,
        description="Turn old <key>…</key> sections into markers first. Turn off for "
        "documents that hold real HTML tags.",
    )

    @field_validator("marker_prefix")
    @classmethod
    def _prefix_is_plain(cls, value: str) -> str:
        if not _PREFIX_RE.match(value):
            raise ValueError("marker_prefix may use letters, digits and _ . : - only.")
        return value


class AppliedEdit(KindSubModel):
    section_key: str = Field(description="The section that was edited.")
    op: str = Field(description="The edit's op: create, replace or append.")
    result: Literal["created", "replaced", "appended"] = Field(
        description="What happened to the document."
    )
    title: str = Field(description="The section's title: its first ## heading, else the key.")


class RefusedEdit(KindSubModel):
    section_key: str = Field(description="The key the edit named, as given.")
    op: str = Field(description="The edit's op, as given.")
    reason: Literal[
        "invalid_section_key",
        "unknown_op",
        "empty_or_placeholder_body",
        "body_contains_section_marker",
        "section_missing",
    ] = Field(description="Why the edit was not applied.")


class SectionInfo(KindSubModel):
    key: str = Field(description="The section's key.")
    title: str = Field(description="The section's title.")


class SectionsPatchOutput(KindModel, kind="sections_patch_result"):
    document: str = Field(description="The document after the edits.")
    applied: list[AppliedEdit] = Field(description="Edits applied, in order.")
    refused: list[RefusedEdit] = Field(description="Edits refused, in order, with the reason.")
    changed: bool = Field(
        description="True when an edit was applied and the document differs from the one given."
    )
    upgraded_legacy: bool = Field(
        default=False,
        description="True when old <key>…</key> sections were turned into markers. Alone it is "
        "not a change: save it only together with an applied edit, or on purpose."
    )
    sections: list[SectionInfo] = Field(description="Every section in the result, in order.")


@dataclass
class _Section:
    key: str
    body: str


def _marker(prefix: str, key: str) -> str:
    return f"<!-- {prefix}:{key} -->"


def _marker_re(prefix: str) -> re.Pattern[str]:
    return re.compile(
        rf"^[ \t]*<!--\s*{re.escape(prefix)}:(?P<key>{_KEY})\s*-->[ \t]*$",
        re.MULTILINE,
    )


def _convert_legacy(document: str, prefix: str) -> str:
    text = document or ""
    if not _LEGACY_SECTION_RE.search(text):
        return text

    def _sub(m: re.Match[str]) -> str:
        return (
            f"{m.group('lead')}{_marker(prefix, m.group('key'))}\n{m.group('inner').strip(chr(10))}"
        )

    converted = _LEGACY_SECTION_RE.sub(_sub, text)
    return re.sub(r"\n{3,}", "\n\n", converted).strip("\n")


class _Doc:
    """Split / render under one marker prefix (mirrors document_sections.py)."""

    def __init__(self, prefix: str, legacy: bool) -> None:
        self.prefix = prefix
        self.legacy = legacy
        self.marker_re = _marker_re(prefix)

    def prepare(self, document: str) -> str:
        # Only a TRUE legacy document (no section markers yet) is upgraded, so a saved document
        # is upgraded once and never again — even when its sections hold block HTML.
        text = document or ""
        if not self.legacy or self.marker_re.search(text):
            return text
        return _convert_legacy(text, self.prefix)

    def split(self, document: str) -> tuple[str, list[_Section]]:
        # The legacy upgrade runs ONCE, on the input document (``prepare``), never here: text an
        # edit wrote may hold real HTML (``<i>x</i>``) that must not become a section.
        text = document or ""
        matches = list(self.marker_re.finditer(text))
        if not matches:
            return text.strip("\n"), []
        preamble = text[: matches[0].start()].strip("\n")
        out: list[_Section] = []
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            out.append(_Section(key=m.group("key"), body=text[m.end() : end].strip("\n")))
        return preamble, out

    def render(self, preamble: str, sections: list[_Section]) -> str:
        parts: list[str] = []
        if preamble.strip():
            parts.append(preamble.strip("\n"))
        for section in sections:
            parts.append(f"{_marker(self.prefix, section.key)}\n{section.body.strip(chr(10))}")
        return "\n\n".join(parts)

    def read(self, document: str, key: str) -> str | None:
        for section in self.split(document)[1]:
            if section.key == key:
                return section.body
        return None

    def set(self, document: str, key: str, body: str) -> str:
        preamble, sections = self.split(document)
        body = re.sub(r"\n{3,}", "\n\n", (body or "").strip("\n"))
        for section in sections:
            if section.key == key:
                section.body = body
                break
        else:
            sections.append(_Section(key=key, body=body))
        return self.render(preamble, sections)


def section_title(body: str, key: str) -> str:
    m = _H2_RE.search(body or "")
    if m:
        return m.group("title")
    return key.replace("_", " ").replace("-", " ").strip().title()


def _is_placeholder(markdown: str, words: set[str], min_chars: int) -> bool:
    stripped = (markdown or "").strip().strip("#*-_ ").strip().lower()
    if not stripped:
        return True
    if stripped in words:
        return True
    return len(stripped) < min_chars


class SectionsPatchExecutor:
    """Create, replace or append markdown sections by invisible key markers."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.sections.patch",
        category=NodeCategory.DATA,
        display_name="Edit Document Sections",
        description=(
            "Create, replace or add to sections of a markdown document by section key. "
            "Bad keys and empty or placeholder text are refused and listed."
        ),
        input_schema=SectionsPatchInput,
        output_schema=SectionsPatchOutput,
        config_schema=SectionsPatchConfig,
        output_kind="sections_patch_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="file-pen-line",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SectionsPatchInput,
        config: SectionsPatchConfig,
    ) -> NodeResult[SectionsPatchOutput]:
        _ = ctx
        doc = _Doc(config.marker_prefix, config.upgrade_legacy_tags)
        words = {w.strip().lower() for w in config.placeholder_bodies}
        original = inputs.document or ""
        document = doc.prepare(original)
        upgraded = document != original
        applied_ops: list[tuple[str, str, str]] = []
        refused: list[RefusedEdit] = []

        for edit in inputs.edits:
            key = edit.section_key.strip()
            if not KEY_RE.match(key):
                refused.append(
                    RefusedEdit(
                        section_key=edit.section_key, op=edit.op, reason="invalid_section_key"
                    )
                )
                continue
            if edit.op not in ("create", "replace", "append"):
                refused.append(RefusedEdit(section_key=key, op=edit.op, reason="unknown_op"))
                continue
            body = (edit.markdown or "").strip("\n")
            if _is_placeholder(body, words, config.min_body_chars):
                refused.append(
                    RefusedEdit(section_key=key, op=edit.op, reason="empty_or_placeholder_body")
                )
                continue
            if doc.marker_re.search(body):
                refused.append(
                    RefusedEdit(section_key=key, op=edit.op, reason="body_contains_section_marker")
                )
                continue
            existing = doc.read(document, key)
            if existing is None and edit.op != "create" and config.on_missing == "refuse":
                refused.append(RefusedEdit(section_key=key, op=edit.op, reason="section_missing"))
                continue
            if edit.op == "append":
                merged = f"{existing}\n\n{body}" if existing else body
                document = doc.set(document, key, merged)
            else:
                document = doc.set(document, key, body)
            if existing is None:
                result = "created"
            else:
                result = "appended" if edit.op == "append" else "replaced"
            applied_ops.append((key, edit.op, result))

        _, final_sections = doc.split(document)
        bodies = {}
        for section in final_sections:
            bodies.setdefault(section.key, section.body)
        applied = [
            AppliedEdit(
                section_key=key,
                op=op,
                result=result,  # type: ignore[arg-type]
                title=section_title(bodies.get(key, ""), key),
            )
            for key, op, result in applied_ops
        ]
        return success(
            SectionsPatchOutput(
                document=document,
                applied=applied,
                refused=refused,
                changed=bool(applied) and document != original,
                upgraded_legacy=upgraded,
                sections=[
                    SectionInfo(key=s.key, title=section_title(s.body, s.key))
                    for s in final_sections
                ],
            )
        )
