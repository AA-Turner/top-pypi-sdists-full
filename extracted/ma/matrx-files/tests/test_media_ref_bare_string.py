"""Guard (2026-09-11): a bare string is a MediaRef.

The reverse-image node refused an Expert's image link with 'should be a valid
dictionary or instance of MediaRef' and the whole verification run died.
Workflow edges hand media around as plain strings; the record coerces them.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from matrx_files.cloud_sync.media_ref import MediaRef


class _Node(BaseModel):
    image: MediaRef


def test_https_link_becomes_url():
    ref = _Node.model_validate({"image": "https://example.com/a.jpg"}).image
    assert ref.url == "https://example.com/a.jpg"
    assert ref.file_id is None and ref.file_uri is None


def test_uuid_becomes_file_id():
    fid = "0f3b4c6a-1d2e-4f5a-8b9c-0d1e2f3a4b5c"
    ref = _Node.model_validate({"image": fid}).image
    assert ref.file_id == fid and ref.url is None


def test_cloud_uri_becomes_file_uri():
    ref = _Node.model_validate({"image": "s3://bucket/key.png"}).image
    assert ref.file_uri == "s3://bucket/key.png"


def test_dict_form_is_unchanged():
    ref = _Node.model_validate({"image": {"url": "https://example.com/b.jpg"}}).image
    assert ref.url == "https://example.com/b.jpg"


def test_two_identifiers_still_refused():
    with pytest.raises(ValueError):
        MediaRef(url="https://example.com/a.jpg", file_id="0f3b4c6a-1d2e-4f5a-8b9c-0d1e2f3a4b5c")
