"""Live DealCloud integration tests for the example project."""

from __future__ import annotations

import pytest

from dealcloud_sdk_example.main import TEST_OBJECT_API_NAME, build_client

pytestmark = pytest.mark.integration


def test_schema_lists_objects() -> None:
    dc = build_client()
    objects = dc.get_objects()
    assert len(objects) >= 1


def test_site_has_configured_test_object() -> None:
    dc = build_client()
    names = {o.apiName for o in dc.get_objects()}
    assert TEST_OBJECT_API_NAME in names, (
        f"Expected object {TEST_OBJECT_API_NAME!r} in site schema. "
        "Create it or change TEST_OBJECT_API_NAME in dealcloud_sdk_example."
    )


def test_read_test_object_top_rows() -> None:
    dc = build_client()
    rows: list = []
    for batch in dc.read_data_streaming(TEST_OBJECT_API_NAME, page_size=3):
        rows = batch
        break
    assert isinstance(rows, list)
