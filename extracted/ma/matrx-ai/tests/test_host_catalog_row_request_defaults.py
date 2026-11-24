"""A host catalog row's request_defaults reach the wire (parity walk 2026-11-10, W05).

Matrx 2's on-device service registers its llama-server model with
``request_defaults={"stream_options": {"include_usage": True}}``: llama-server streams its terminal usage block
only when asked. ``build_catalog_call_profile`` dropped the row's value (``request_defaults={}``), so no usage
arrived, the completion's ``total_usage.by_model`` was empty and the answer could not name the model that wrote
it. Red before the fix: the profile carried {} and the request had no stream_options.
"""

from __future__ import annotations

from matrx_ai.catalog.host_catalog import CatalogModel, build_catalog_call_profile

ROW = {
    "id": "local/smollm2-135m",
    "name": "local/smollm2-135m",
    "api_class": "generic_openai_standard",
    "provider": "local",
    "is_active": True,
    "endpoints": ["generic_openai_chat"],
    "request_defaults": {"stream_options": {"include_usage": True}},
}


def test_the_profile_carries_the_rows_request_defaults() -> None:
    profile = build_catalog_call_profile(CatalogModel(dict(ROW)))
    assert profile.request_defaults == {"stream_options": {"include_usage": True}}


def test_the_profile_owns_a_copy_never_the_row() -> None:
    row = dict(ROW, request_defaults={"stream_options": {"include_usage": True}})
    profile = build_catalog_call_profile(CatalogModel(row))
    profile.request_defaults["stream_options"]["include_usage"] = False
    assert row["request_defaults"]["stream_options"]["include_usage"] is True


def test_a_row_without_request_defaults_gets_none() -> None:
    row = {k: v for k, v in ROW.items() if k != "request_defaults"}
    assert build_catalog_call_profile(CatalogModel(row)).request_defaults == {}
