import os
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault("ESCOPO_RESTLIB2", "test-scope")

from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel


def _base_edl() -> dict:
    return {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para campo lut.",
        "id": "LutEntity",
        "version": "1.0",
        "required": ["id"],
        "properties": {
            "id": {"type": "uuid", "pk": True},
        },
        "repository": {
            "map": "test.lut_entities",
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


def test_entity_model_accepts_lut_boolean():
    edl = _base_edl()
    edl["lut"] = True

    model = EntityModel(**edl)

    assert model.lut is True


def test_entity_model_rejects_invalid_lut_value():
    edl = _base_edl()
    edl["lut"] = "talvez"

    with pytest.raises(ValidationError):
        EntityModel(**edl)
