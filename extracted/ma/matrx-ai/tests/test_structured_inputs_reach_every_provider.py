"""A structured input part (input_remarks, input_notes, ...) reaches EVERY provider's wire request.

## The regression (LEGACY-3a fix round 1, 2026-10-30)

A person filled a questionnaire on the admin's default agent (GPT OSS 20B on Groq). The answers
were stored as an ``input_remarks`` part with the correct ``resolved_text`` and reached the
Anthropic request, but the Groq request held only the person's typed line: the model said
"I didn't receive any answers" and invented values. Every Chat Completions translator (Groq,
Cerebras, Together, generic OpenAI-compatible, xAI) built its user text from ``TextContent``
alone, so EVERY structured input (remarks, notes, tasks, tables, webpages ...) was dropped
without a trace on those wires. Anthropic, Google and OpenAI Responses delegate to the part's
own ``to_<provider>()`` and always carried it.

The guard: one user turn with typed text plus a resolved remarks part; every translator's wire
request must carry the remark text, after the typed text, in that same turn.

## Fix round 2 (2026-10-30): nothing hand-listed

The translator list and the part list were hand-written, and only remarks were covered. Now EVERY
translator is discovered from the code (the concrete ``BaseTranslator`` subclasses under
``matrx_ai.providers``) and EVERY part type a user message can carry is read from
``UnifiedContent`` itself: a new translator or part type is covered automatically (a new part type
that is none of structured / media / known-not-user fails until classified). A structured part's
text must reach the wire; a document, audio, video or YouTube part must either reach the wire or be
RECORDED as dropped on the request snapshot (``_record_serializer_drop``), never skipped silently.
"""


from __future__ import annotations

import base64
import importlib
import inspect
import json
import pkgutil
import re
import typing
from typing import Any

import pytest

import matrx_ai.providers as providers_pkg
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.media_config import AudioContent, DocumentContent, VideoContent, YouTubeVideoContent
from matrx_ai.config.speech_script_config import SpeechScriptContent
from matrx_ai.config.structured_input_config import RemarksInputContent, _StructuredInputBase
from matrx_ai.config.unified_content import UnifiedContent
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.groq.translator import GroqTranslator
from matrx_ai.testing.profile_factory import make_profile

TYPED = "Based on my answers, tell me my group size."
REMARK = '<!-- answers c1 to "Team Offsite Planning" in your previous reply -->\n- Group size: 17 people'


#: Modules under providers that are standalone scripts, not importable (they need a sibling that does not exist).
#: A NEW unimportable module is not in this set, so it fails ``test_every_provider_module_imports`` loudly.
KNOWN_UNIMPORTABLE_SCRIPTS = {"matrx_ai.providers.google.sample_podcast_direct"}
IMPORT_FAILURES: dict[str, str] = {}


def discover_translators(extra_base: type[BaseTranslator] = BaseTranslator) -> list[type[BaseTranslator]]:
    """Every concrete translator the code defines: imports EVERY module under ``matrx_ai.providers`` (not only
    ``.translator``), then walks all ``BaseTranslator`` subclasses. Only real abstractness (unimplemented
    abstract methods) excludes a class: never its name, its module or an empty ``PROVIDER``."""
    IMPORT_FAILURES.clear()
    for mod in pkgutil.walk_packages(providers_pkg.__path__, "matrx_ai.providers."):
        try:
            importlib.import_module(mod.name)
        except Exception as exc:  # noqa: BLE001 - recorded, asserted in test_every_provider_module_imports
            IMPORT_FAILURES[mod.name] = f"{type(exc).__name__}: {exc}"
    found: dict[str, type[BaseTranslator]] = {}
    todo = list(BaseTranslator.__subclasses__())
    while todo:
        cls = todo.pop()
        todo.extend(cls.__subclasses__())
        if not inspect.isabstract(cls) and (cls.__module__.startswith("matrx_ai.providers.") or cls.__module__ == __name__):
            found[f"{cls.__module__}.{cls.__qualname__}"] = cls
    return sorted(found.values(), key=lambda c: c.__name__)


TRANSLATORS = [t for t in discover_translators() if t.__module__ != __name__]

#: Parts a user message never carries onto a wire (assistant / tool / hosted-tool output), plus the
#: decision parts, which the unified client resolves before any translator runs. Anything else in
#: ``UnifiedContent`` is exercised below; a NEW part type fails ``test_every_part_type_is_classified``.
NOT_USER_WIRE_PARTS = {
    "TextContent",
    "ImageContent",
    "ToolCallContent",
    "ToolResultContent",
    "ThinkingContent",
    "CodeExecutionContent",
    "CodeExecutionResultContent",
    "WebSearchCallContent",
    "HostedToolContent",
    "DecisionQuestionsContent",
    "DecisionAnswersContent",
}

_B64 = base64.b64encode(b"%PDF-1.4 marker-bytes-7f3a").decode()
MEDIA_FACTORIES: dict[str, Any] = {
    "DocumentContent": lambda: DocumentContent(base64_data=_B64, mime_type="application/pdf"),
    "AudioContent": lambda: AudioContent(base64_data=_B64, mime_type="audio/wav"),
    "VideoContent": lambda: VideoContent(base64_data=_B64, mime_type="video/mp4"),
    "YouTubeVideoContent": lambda: YouTubeVideoContent(url="https://www.youtube.com/watch?v=marker7f3a"),
}
MEDIA_MARKERS = (_B64, "marker-bytes-7f3a", "marker7f3a")


def _part_types() -> list[type]:
    return list(typing.get_args(UnifiedContent))


def _structured_parts() -> list[type]:
    return [t for t in _part_types() if issubclass(t, _StructuredInputBase) or t is SpeechScriptContent]


def _structured_part(cls: type) -> tuple[Any, str]:
    """A part of ``cls`` carrying its own unique text, and that text."""
    mark = f"MARK[{cls.__name__}] group size is 17"
    if cls is SpeechScriptContent:
        return cls(turns=[{"speaker": "Host", "text": mark}]), mark
    if cls is RemarksInputContent:
        return cls(items=[], metadata={"resolved_text": mark}), mark
    return cls(metadata={"resolved_text": mark}), mark


def test_every_part_type_is_classified() -> None:
    names = {t.__name__ for t in _part_types()}
    classified = NOT_USER_WIRE_PARTS | set(MEDIA_FACTORIES) | {t.__name__ for t in _structured_parts()}
    assert names == classified, f"classify the new part type(s) {sorted(names - classified)} here"


def _config(model: str, part: Any, *, typed_first: bool = False) -> UnifiedConfig:
    return UnifiedConfig(
        model=model,
        system_instruction="You are helpful.",
        messages=MessageList(
            _messages=[
                UnifiedMessage(role="user", content=[TextContent(text="Ask me.")]),
                UnifiedMessage(role="assistant", content=[TextContent(text="Here you go.")]),
                UnifiedMessage(role="user", content=[part, TextContent(text=TYPED)]),
            ]
        ),
    )


def _wire(translator: BaseTranslator, config: UnifiedConfig) -> str:
    provider = translator.PROVIDER
    wire_format = f"{provider}_chat"
    profile = make_profile(model_name="m", wire_format=wire_format, vendor=provider)
    config.model = "m"
    return json.dumps(translator.build_request(config, profile), default=str)


@pytest.fixture
def notices(monkeypatch) -> list[dict]:
    """Every media notice a serializer stages on the request snapshot during the test."""
    from matrx_ai.processing.media_fallback import handler

    staged: list[dict] = []
    monkeypatch.setattr(handler, "stage_media_notice", staged.append)
    return staged


def check_structured_reaches_wire(translator_cls: type[BaseTranslator], part_cls: type) -> None:
    part, mark = _structured_part(part_cls)
    wire = _wire(translator_cls(), _config("m", part))
    assert mark in wire, f"{translator_cls.__name__} dropped {part_cls.__name__}: its text never reached the wire"
    assert wire.index(mark) < wire.index(TYPED), f"{translator_cls.__name__}: {part_cls.__name__} not before the typed text"


def check_media_arrives_or_is_recorded(translator_cls: type[BaseTranslator], name: str, staged: list[dict]) -> None:
    staged.clear()
    wire = _wire(translator_cls(), _config("m", MEDIA_FACTORIES[name]()))
    sent = any(marker in wire for marker in MEDIA_MARKERS)
    recorded = any(n.get("action") == "dropped" for n in staged)
    assert sent or recorded, f"{translator_cls.__name__} silently dropped {name}: not on the wire, no recorded drop"


def test_translators_are_discovered_from_the_code() -> None:
    names = {t.__name__ for t in TRANSLATORS}
    assert {"GroqTranslator", "CerebrasTranslator", "TogetherTranslator", "GenericOpenAITranslator",
            "XAITranslator", "AnthropicTranslator", "OpenAITranslator", "GoogleTranslator"} <= names


def test_every_provider_module_imports() -> None:
    assert set(IMPORT_FAILURES) <= KNOWN_UNIMPORTABLE_SCRIPTS, {
        k: v for k, v in IMPORT_FAILURES.items() if k not in KNOWN_UNIMPORTABLE_SCRIPTS
    }


def test_discovery_catches_a_subclass_with_an_empty_provider() -> None:
    """A concrete subclass with PROVIDER == "" (and a non-translator module) is discovered, not skipped."""

    class NoProvider(GroqTranslator):
        PROVIDER = ""

    try:
        assert NoProvider in discover_translators()
    finally:
        del NoProvider
        import gc

        gc.collect()


def test_every_discovered_translator_has_a_provider() -> None:
    assert all(t.PROVIDER for t in TRANSLATORS), [t.__name__ for t in TRANSLATORS if not t.PROVIDER]


@pytest.mark.parametrize("translator_cls", TRANSLATORS, ids=lambda c: c.__name__)
@pytest.mark.parametrize("part_cls", _structured_parts(), ids=lambda c: c.__name__)
def test_structured_part_reaches_every_wire(translator_cls, part_cls) -> None:
    check_structured_reaches_wire(translator_cls, part_cls)


@pytest.mark.parametrize("translator_cls", TRANSLATORS, ids=lambda c: c.__name__)
@pytest.mark.parametrize("name", list(MEDIA_FACTORIES))
def test_media_part_arrives_or_is_recorded_on_every_wire(translator_cls, name, notices) -> None:
    check_media_arrives_or_is_recorded(translator_cls, name, notices)


@pytest.mark.parametrize("translator_cls", [t for t in TRANSLATORS if t.PROVIDER not in ("anthropic", "openai", "google")], ids=lambda c: c.__name__)
def test_a_remark_that_ends_the_message_leaves_no_trailing_blank_lines(translator_cls) -> None:
    """Chat Completions text: the remark's blank-line boundary must not dangle when it is the last part."""
    config = _config("m", RemarksInputContent(items=[], metadata={"resolved_text": REMARK}))
    last = config.messages._messages[-1]
    last.content = [last.content[1], last.content[0]]  # typed text first, remark last
    wire = _wire(translator_cls(), config)
    assert REMARK.splitlines()[-1] in wire
    assert "17 people\\n\\n" not in wire, wire
    assert "17 people" in wire


@pytest.mark.parametrize("translator_cls", [t for t in TRANSLATORS if t.PROVIDER not in ("anthropic", "openai", "google")], ids=lambda c: c.__name__)
def test_plain_typed_text_ending_in_blank_lines_is_sent_byte_identical(translator_cls) -> None:
    """Only a rendered structured part is trimmed; the person's own trailing newlines are theirs."""
    typed = "keep my spacing\n\n"
    config = _config("m", RemarksInputContent(items=[], metadata={"resolved_text": REMARK}))
    config.messages._messages[-1].content = [TextContent(text=typed)]
    tail = re.search(r"keep my spacing((?:\\+n)*)", _wire(translator_cls(), config))  # wire escaping depth varies
    assert tail and tail.group(1).count("n") == 2, tail


def test_the_guard_fails_when_one_translator_drops_one_part_type(notices) -> None:
    """Prove the loops can fail: a Groq stand-in that drops remarks, one that drops documents silently."""
    class DropsRemarks(GroqTranslator):
        def build_request(self, config, route_ctx=""):
            for m in config.messages._messages:
                m.content = [c for c in m.content if not isinstance(c, RemarksInputContent)]
            return super().build_request(config, route_ctx)

    class DropsDocumentsSilently(GroqTranslator):
        def build_request(self, config, route_ctx=""):
            for m in config.messages._messages:
                m.content = [c for c in m.content if not isinstance(c, DocumentContent)]
            return super().build_request(config, route_ctx)

    with pytest.raises(AssertionError, match="dropped RemarksInputContent"):
        check_structured_reaches_wire(DropsRemarks, RemarksInputContent)
    with pytest.raises(AssertionError, match="silently dropped DocumentContent"):
        check_media_arrives_or_is_recorded(DropsDocumentsSilently, "DocumentContent", notices)
