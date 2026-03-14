import pathlib
import sys

import pytest
from pydantic import ValidationError


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_root import EntityModelRoot


def _mixin_edl():
    return {
        "edl_version": "1.0",
        "escopo": "core",
        "id": "auditoria",
        "description": "Mixin de auditoria",
        "mixin": True,
        "properties": {
            "atualizado_em": {
                "type": "datetime",
            }
        },
        "repository": {
            "properties": {
                "atualizado_em": {"column": "lastupdate"},
            }
        },
    }


def _entity_edl():
    return {
        "edl_version": "1.0",
        "escopo": "core",
        "id": "empresa",
        "description": "Entidade real",
        "properties": {
            "id": {"type": "uuid", "pk": True},
        },
        "required": ["id"],
        "repository": {
            "properties": {
                "id": {"column": "id"},
            }
        },
        "api": {
            "resource": "empresas",
            "verbs": ["GET"],
            "expose": True,
        },
    }


def test_entity_model_root_accepts_mixin_without_repository_map():
    model = EntityModelRoot(**_mixin_edl())

    assert model.mixin is True
    assert model.repository.map is None


def test_entity_model_root_rejects_mixin_with_repository_map():
    edl = _mixin_edl()
    edl["repository"]["map"] = "core.auditoria"

    with pytest.raises(ValidationError, match="Mixins não devem definir"):
        EntityModelRoot(**edl)


def test_entity_model_rejects_non_mixin_without_repository_map():
    with pytest.raises(ValidationError, match="repository\\.map"):
        EntityModel(**_entity_edl())


def test_entity_model_accepts_external_reference_with_hierarchical_scope():
    edl = _entity_edl()
    edl["properties"]["departamento"] = {
        "type": "RH.EST.ORG/departamento",
        "cardinality": "1_1",
    }
    edl["repository"]["properties"]["departamento"] = {
        "relation_column": "RH.EST.ADM/empresa/departamento",
    }

    model = EntityModel(**edl)

    assert model.properties["departamento"].type == "RH.EST.ORG/departamento"
