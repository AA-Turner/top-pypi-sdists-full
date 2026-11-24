"""A STORED FILE SAYS WHERE IT CAME FROM (CGU-10 AND-IMG13 #6, 2026-11-11).

Live (AND-V IMG12): every stored file's ``metadata.source`` was ``ai_media`` — the handler wrote its base
``source`` first and merged the caller's ``extra_metadata`` with ``setdefault``, so a person's attachment
(``inline_media_part`` / ``confidential_inline_attachment``) and a tool's blob (``tool_output_blob``) never
said what they were. SUT: ``AIMediaHandler.save_response_media_envelope_async`` up to the upload, with the
metadata it hands ``FileService.upload_simple`` captured. Put ``setdefault`` back → red.
"""

from __future__ import annotations

import base64
from types import SimpleNamespace
from typing import Any

import pytest


class _Stop(Exception):
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("source", ["inline_media_part", "confidential_inline_attachment", "tool_output_blob"])
async def test_the_callers_source_is_the_files_source(monkeypatch, source: str) -> None:
    import matrx_files
    import matrx_ai.media.media_persistence as mp

    sent: list[dict[str, Any]] = []

    class _FileService:
        @classmethod
        def for_file_manager(cls, _fm: Any) -> _FileService:
            return cls()

        async def upload_simple(self, _body: Any, **kw: Any) -> Any:
            sent.append(kw["metadata"])
            raise _Stop()

    handler = mp.AIMediaHandler.get_instance()
    monkeypatch.setattr(handler, "_get_cloud_fm", lambda: SimpleNamespace(sync_engine=None))
    monkeypatch.setattr(mp, "resolve_media_owner", lambda _fm, _feature: "owner-1")
    monkeypatch.setattr(matrx_files, "FileService", _FileService)
    png = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\0" * 32).decode()
    with pytest.raises(_Stop):
        await mp.save_media_envelope_async(png, "image/png", feature="ai_images", extra_metadata={"source": source})
    assert sent and sent[0]["source"] == source, sent
