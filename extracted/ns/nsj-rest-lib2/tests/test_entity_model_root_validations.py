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
        "description": "Entidade de teste para validacoes estruturais.",
        "id": "ValidationEntity",
        "version": "1.0",
        "required": ["id"],
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "codigo": {"type": "string"},
            "nome": {"type": "string"},
        },
        "repository": {
            "map": "test.validation_entities",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
                "codigo": {"column": "codigo"},
                "nome": {"column": "nome"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "validation-entities",
            "expose": True,
            "verbs": ["GET"],
        },
    }


def test_pk_property_must_be_required():
    edl = _base_edl()
    edl["required"] = []

    with pytest.raises(ValidationError) as exc:
        EntityModel(**edl)

    errors = exc.value.errors()
    assert any(
        error.get("type") == "pk_not_required" and error.get("loc") == ("required",)
        for error in errors
    )


def test_repository_column_collision_raises_validation_error():
    edl = _base_edl()
    edl["repository"]["properties"]["nome"]["column"] = "codigo"

    with pytest.raises(ValidationError) as exc:
        EntityModel(**edl)

    errors = exc.value.errors()
    assert any(
        error.get("type") == "duplicate_repository_column"
        and error.get("loc") == ("repository", "properties")
        for error in errors
    )


def test_relation_without_local_column_does_not_collide():
    edl = _base_edl()
    edl["properties"]["categoria"] = {
        "type": "custom/categoria_profissional",
        "cardinality": "1_1",
    }
    edl["repository"]["properties"]["categoria"] = {
        "relation_column": "custom/categoria_profissional/id"
    }

    model = EntityModel(**edl)

    assert "categoria" in model.properties
