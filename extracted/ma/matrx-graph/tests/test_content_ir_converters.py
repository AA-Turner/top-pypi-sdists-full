"""The converter registry: one id one mapping, many-to-many, detection, chaining, provenance."""

from __future__ import annotations

import pytest

import importlib
import sys

from pydantic import BaseModel

from matrx_graph.content_ir.converters import (
    AmbiguousSource,
    Converter,
    ConverterError,
    ConverterRegistry,
    SourceFormat,
    Target,
    code_fingerprint,
)


class Post(BaseModel):
    id: str


def _reg() -> ConverterRegistry:
    reg = ConverterRegistry()
    reg.register_target(Target(id="capture", label="capture", kind="capture_kind"))
    reg.register_target(Target(id="post", label="post", contract=Post))
    reg.register_target(Target(id="profile", label="profile", kind="profile_kind"))
    reg.register_format(SourceFormat(id="acme.page", label="page",
                                     detect=lambda p, h: isinstance(p, dict) and "html" in p))
    reg.register_format(SourceFormat(id="acme.api", label="api",
                                     detect=lambda p, h: isinstance(p, dict) and "items" in p))
    return reg


def page_to_capture(p, h):
    return {"posts": [{"id": i} for i in p["html"].split(",")]}


def api_to_post(p, h):
    return [{"id": str(i)} for i in p["items"]]


def capture_to_post(p, h):
    return list(p["posts"])


def post_to_capture(p, h):
    if p["id"] == "boom":
        raise RuntimeError("bad item")
    return {"posts": [{"id": p["id"] + "!"}]}


def capture_to_profile(p, h):
    return {"handle": h["handle"]}


def _full() -> ConverterRegistry:
    reg = _reg()
    reg.register(Converter(id="acme.page->capture", source="acme.page", target="capture", version=1, fn=page_to_capture))
    reg.register(Converter(id="acme.api->post", source="acme.api", target="post", version=2, fn=api_to_post, many=True))
    reg.register(Converter(id="capture->post", source="capture", target="post", version=1, fn=capture_to_post, many=True))
    reg.register(Converter(id="capture->profile", source="capture", target="profile", version=1, fn=capture_to_profile))
    return reg


def test_many_to_many_and_detection():
    reg = _full()
    assert {c.id for c in reg.for_target("post")} == {"acme.api->post", "capture->post"}
    assert {c.id for c in reg.for_source("capture")} == {"capture->post", "capture->profile"}
    assert [c.id for c in reg.match({"items": [1]})] == ["acme.api->post"]
    assert [c.id for c in reg.match({"html": "a"}, target="capture")] == ["acme.page->capture"]
    assert reg.detect({"nothing": 1}) == []
    assert reg.detect({"items": []}, {"format": "acme.page"}) == ["acme.page"]  # a named format wins


def test_chain_runs_every_hop_with_provenance():
    reg = _full()
    steps = reg.convert_to({"html": "a,b"}, "post")
    assert [s.converter.id for s in steps] == ["acme.page->capture", "capture->post"]
    assert steps[-1].items == [{"id": "a"}, {"id": "b"}]  # validated against the contract, kept as returned
    prov = steps[0].provenance
    assert prov.converter == "acme.page->capture" and prov.version == 1 and len(prov.code_sha) == 12
    assert prov.input_sha256 and prov.stamp()["converter"] == "acme.page->capture"


def test_one_id_one_mapping():
    reg = _full()
    reg.register(Converter(id="capture->post", source="capture", target="post", version=1, fn=capture_to_post))
    with pytest.raises(ConverterError):
        reg.register(Converter(id="capture->post", source="capture", target="post", version=1, fn=capture_to_profile))


def test_unknown_source_and_missing_path_refuse():
    reg = _reg()
    with pytest.raises(ConverterError):
        reg.register(Converter(id="x", source="nope", target="post", version=1, fn=api_to_post))
    with pytest.raises(ConverterError):
        reg.path("acme.api", "profile")


def test_code_sha_follows_the_implementation():
    reg = _reg()
    a = reg.register(Converter(id="a", source="acme.api", target="post", version=1, fn=api_to_post))
    b = reg.register(Converter(id="b", source="acme.api", target="post", version=1, fn=lambda p, h: p,
                               impl=capture_to_post))
    assert a.code_sha != b.code_sha


def test_two_claimants_refuse_and_name_both():
    reg = _full()
    with pytest.raises(AmbiguousSource) as err:
        reg.convert_to({"html": "a", "items": ["1"]}, "post")
    assert err.value.claimants == ["acme.api", "acme.page"]
    steps = reg.convert_to({"html": "a", "items": ["1"]}, "post", {"format": "acme.api"})
    assert [s.converter.id for s in steps] == ["acme.api->post"]


def test_a_hop_after_many_runs_per_item_and_keeps_the_rest_when_one_fails():
    reg = _full()
    reg.register(Converter(id="post->capture", source="post", target="capture", version=1, fn=post_to_capture))
    steps = reg.convert_to({"items": ["a", "boom", "c"]}, "capture", source="acme.api")
    hop = steps[-1]
    assert hop.items == [{"posts": [{"id": "a!"}]}, {"posts": [{"id": "c!"}]}]
    assert hop.failures == [{"index": 1, "error": "RuntimeError: bad item"}] and hop.status == "partial"


def test_a_mapping_error_is_a_failed_conversion_not_an_exception():
    reg = _full()
    done = reg.convert("acme.api->post", {"nope": 1})
    assert done.status == "failed" and done.failures[0]["error"].startswith("KeyError")


def test_targets_are_declared_and_contracts_enforced():
    reg = _reg()
    with pytest.raises(ConverterError):
        reg.register(Converter(id="x", source="acme.api", target="nowhere", version=1, fn=api_to_post))
    with pytest.raises(ConverterError):
        reg.register_target(Target(id="loose", label="loose"))
    reg.register(Converter(id="bad", source="acme.api", target="post", version=1, many=True,
                           fn=lambda p, h: [{"wrong": 1}]))
    assert reg.convert("bad", {"items": []}).status == "failed"


def test_code_sha_moves_when_a_helper_beside_the_impl_changes(tmp_path, monkeypatch):
    mod = tmp_path / "p1_conv_mod.py"
    mod.write_text("def helper(x):\n    return x\n\ndef impl(p, h):\n    return helper(p)\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    m = importlib.import_module("p1_conv_mod")
    before = code_fingerprint(m.impl)
    mod.write_text("def helper(x):\n    return [x]\n\ndef impl(p, h):\n    return helper(p)\n")
    importlib.reload(m)
    assert code_fingerprint(m.impl) != before
    sys.modules.pop("p1_conv_mod", None)
