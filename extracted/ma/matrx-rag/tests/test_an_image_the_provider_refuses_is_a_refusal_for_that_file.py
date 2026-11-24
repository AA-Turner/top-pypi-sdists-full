"""An image the vision provider refuses is a typed refusal for that one file, not a platform failure.

Live 2026-11-07 (workflow.in_organization): Google answered one image with 400 "Unable to process
input image" and stopped two others on RECITATION mid-answer. Each landed as a
``rag_vision_analysis_failed`` system error. The host raises ``LLMInputRefused`` for a refusal; the
pipeline names it ``VisionInputRefused`` and ``ingest_image`` writes it on the file's result
(``vision_refused: ...``) without filing it. Any other failure still files, as before.
"""

from __future__ import annotations

import pytest

import matrx_rag
from matrx_rag import image_pipeline
from matrx_rag._ext import LLMInputRefused


class _RefusingProvider:
    async def chat(self, messages, **kwargs):
        raise LLMInputRefused("the provider could not read this image")

    async def chat_stream(self, messages, **kwargs):
        raise LLMInputRefused("never reached")


class _BrokenProvider:
    async def chat(self, messages, **kwargs):
        raise RuntimeError("provider outage")

    async def chat_stream(self, messages, **kwargs):
        raise RuntimeError("never reached")


@pytest.fixture
def captured(monkeypatch, tmp_path):
    seen: list[dict] = []

    async def _capture(exc, *, kind, **fields):
        seen.append({"kind": kind, "error": str(exc)})

    monkeypatch.setattr("matrx_utils.capture_error", _capture)
    matrx_rag._ext._reset_for_tests()
    yield seen
    matrx_rag._ext._reset_for_tests()


def _image(tmp_path) -> str:
    path = tmp_path / "picture.png"
    path.write_bytes(b"\x89PNG not really an image")
    return str(path)


async def _ingest(tmp_path):
    return await image_pipeline.ingest_image(
        cld_file_id="00000000-0000-0000-0000-000000000001",
        organization_id="00000000-0000-0000-0000-000000000002",
        owner_id="00000000-0000-0000-0000-000000000003",
        local_path=_image(tmp_path),
        force=True,
    )


async def test_a_refused_image_raises_the_typed_refusal(captured) -> None:
    matrx_rag.configure(llm_provider=_RefusingProvider())
    with pytest.raises(image_pipeline.VisionInputRefused, match="could not read this image"):
        await image_pipeline.analyze_image_unified(bytes_b64="aGVsbG8=", mime_type="image/png", model="any")


async def test_a_refused_image_is_written_on_the_files_result_and_not_filed(captured, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("matrx_rag._ext.get_default_vision_model", lambda: "any", raising=False)
    matrx_rag.configure(llm_provider=_RefusingProvider())
    result = await _ingest(tmp_path)
    assert result.error and result.error.startswith("vision_refused:")
    assert result.chunks_written == 0
    assert captured == []


async def test_any_other_vision_failure_is_still_filed(captured, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("matrx_rag._ext.get_default_vision_model", lambda: "any", raising=False)
    matrx_rag.configure(llm_provider=_BrokenProvider())
    result = await _ingest(tmp_path)
    assert result.error and result.error.startswith("vision_analysis_failed:")
    assert [row["kind"] for row in captured] == ["rag_vision_analysis_failed"]
