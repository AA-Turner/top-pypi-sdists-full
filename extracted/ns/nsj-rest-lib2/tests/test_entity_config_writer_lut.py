import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault("ESCOPO_RESTLIB2", "test-scope")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")

from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.model import CompilerResult
from nsj_rest_lib2.service.entity_config_writer import EntityConfigWriter


def _base_edl() -> dict:
    return {
        "edl_version": "1.0",
        "escopo": "folha",
        "description": "Entidade de teste para payload de entity_config.",
        "id": "LutEntity",
        "version": "1.0",
        "required": ["id"],
        "properties": {
            "id": {"type": "uuid", "pk": True},
        },
        "repository": {
            "map": "lookuptables.lut_entities",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "lut-entities",
            "expose": True,
            "verbs": ["GET"],
        },
    }


def test_build_payload_includes_lut_true():
    edl = _base_edl()
    edl["lut"] = True
    model = EntityModel(**edl)
    result = CompilerResult()

    payload = EntityConfigWriter("folha").build_payload(model, result)

    assert payload["lut"] is True


def test_build_payload_includes_lut_false_by_default():
    model = EntityModel(**_base_edl())
    result = CompilerResult()

    payload = EntityConfigWriter("folha").build_payload(model, result)

    assert payload["lut"] is False
