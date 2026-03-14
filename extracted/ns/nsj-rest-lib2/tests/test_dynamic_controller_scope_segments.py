import os
import sys
from pathlib import Path

from flask import Flask

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault("ESCOPO_RESTLIB2", "test-scope")

from nsj_rest_lib2.controller import dynamic_controller


class DummyDTO:
    pass


class DummyEntity:
    pass


class FakeListRoute:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def internal_handle_request(self, *args, **kwargs):
        return ({"ok": True}, 200, {})


def test_dynamic_route_rebuilds_escopo_from_three_url_segments(monkeypatch):
    captured: dict[str, str | None] = {}

    def fake_load_entity_source(
        self,
        entity_resource,
        tenant,
        grupo_empresarial,
        escopo="",
        force_reload=False,
    ):
        captured["entity_resource"] = entity_resource
        captured["tenant"] = tenant
        captured["grupo_empresarial"] = grupo_empresarial
        captured["escopo"] = escopo
        captured["force_reload"] = force_reload
        return (
            "DummyDTO",
            "DummyEntity",
            {"DummyDTO": DummyDTO, "DummyEntity": DummyEntity},
            True,
            ["GET"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            False,
            False,
        )

    monkeypatch.setattr(dynamic_controller, "ListRoute", FakeListRoute)
    monkeypatch.setattr(
        dynamic_controller.EntityLoader,
        "load_entity_source",
        fake_load_entity_source,
    )

    app = Flask(__name__)
    dynamic_controller.setup_dynamic_routes(
        app,
        multidb=False,
        dynamic_root_path="edl1",
        escopo_in_url=True,
    )

    response = app.test_client().get(
        f"/{dynamic_controller.APP_NAME}/edl1/gvn/inf/mdg/tomadores?tenant=47"
    )

    assert response.status_code == 200
    assert captured["entity_resource"] == "tomadores"
    assert captured["tenant"] == "47"
    assert captured["grupo_empresarial"] is None
    assert captured["escopo"] == "GVN.INF.MDG"


def test_dynamic_route_keeps_legacy_single_scope_segment(monkeypatch):
    captured: dict[str, str | None] = {}

    def fake_load_entity_source(
        self,
        entity_resource,
        tenant,
        grupo_empresarial,
        escopo="",
        force_reload=False,
    ):
        captured["entity_resource"] = entity_resource
        captured["tenant"] = tenant
        captured["grupo_empresarial"] = grupo_empresarial
        captured["escopo"] = escopo
        captured["force_reload"] = force_reload
        return (
            "DummyDTO",
            "DummyEntity",
            {"DummyDTO": DummyDTO, "DummyEntity": DummyEntity},
            True,
            ["GET"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            False,
            False,
        )

    monkeypatch.setattr(dynamic_controller, "ListRoute", FakeListRoute)
    monkeypatch.setattr(
        dynamic_controller.EntityLoader,
        "load_entity_source",
        fake_load_entity_source,
    )

    app = Flask(__name__)
    dynamic_controller.setup_dynamic_routes(
        app,
        multidb=False,
        dynamic_root_path="edl1",
        escopo_in_url=True,
    )

    response = app.test_client().get(
        f"/{dynamic_controller.APP_NAME}/edl1/folha/trabalhadores?tenant=47"
    )

    assert response.status_code == 200
    assert captured["entity_resource"] == "trabalhadores"
    assert captured["tenant"] == "47"
    assert captured["grupo_empresarial"] is None
    assert captured["escopo"] == "folha"
