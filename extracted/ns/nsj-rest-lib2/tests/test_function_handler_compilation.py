import json
import os
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault("ESCOPO_RESTLIB2", "test-scope")

from nsj_rest_lib2.compiler.compiler import EDLCompiler
from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_root import EntityModelRoot
from nsj_rest_lib2.compiler.util.type_naming_util import (
    compile_function_class_name,
)
from nsj_rest_lib2.dto.escopo_dto import EscopoDTO


def _load_entity(path: Path):
    with path.open("r") as fp:
        edl_data = json.load(fp)

    model = (
        EntityModelRoot(**edl_data)
        if edl_data.get("mixin", False)
        else EntityModel(**edl_data)
    )
    complete_id = f"{model.escopo}/{model.id}"
    return complete_id, model


def _load_entity_models(base_dir: Path) -> dict[str, EntityModel]:
    models: dict[str, EntityModel] = {}
    for path in base_dir.iterdir():
        if path.suffix.lower() != ".json":
            continue
        key, model = _load_entity(path)
        models[key] = model
    return models


def test_compile_handlers_for_classificacao_financeira_generates_delete_function_type():
    base_dir = ROOT_DIR / "@schemas_test"
    entity_models = _load_entity_models(base_dir)

    model_key = "financas/ClassificacaoFinanceira"
    entity_model = entity_models[model_key]

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo=entity_model.escopo, service_account=None)
    result = compiler.compile_model(
        entity_model,
        list(entity_models.items()),
        escopo=escopo,
    )

    assert result is not None

    # Nomes das funções de banco para post/put/delete
    assert result.insert_function_name == "financas.api_classificacaofinanceiranovo"
    assert result.update_function_name == "financas.api_classificacaofinanceiraalterar"
    assert result.delete_function_name == "financas.api_classificacaofinanceiraexcluir"
    assert result.retrieve_after_insert is True
    assert result.retrieve_after_update is True
    assert result.retrieve_after_partial_update is False
    assert result.post_response_dto_class_name is None
    assert result.custom_json_post_response is False
    assert result.custom_json_put_response is False
    assert result.custom_json_patch_response is False

    # FunctionType para delete
    delete_code = result.source_delete_function_type
    assert delete_code is not None

    expected_class = compile_function_class_name(entity_model.id, "", [], "delete")
    assert result.delete_function_type_class_name == expected_class
    assert f"class {expected_class}" in delete_code
    # Campos esperados (derivados do mapping do handler de delete)
    assert "classificacao: uuid.UUID = FunctionField(" in delete_code
    assert "grupoempresarial: uuid.UUID = FunctionField(" in delete_code


def test_compile_handlers_generates_get_and_list_function_types_from_edl():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para funções GET/LIST.",
        "id": "Foo",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "codigo": {"type": "string"},
        },
        "repository": {
            "map": "test.foo",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
                "codigo": {"column": "codigo"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "foos",
            "expose": True,
            "verbs": ["GET"],
            "handlers": {
                "get": {
                    "impl": "pg_function",
                    "function_ref": "test.fn_foo_get",
                    "call": {
                        "arg_binding": {
                            "type_name": "test.tfoo_get",
                            "mapping": [
                                {"attr": "id_func", "from": "path.id"},
                                {"attr": "tenant", "from": "args.tenant"},
                            ],
                        }
                    },
                    "result": {"expected": "entity_row"},
                },
                "list": {
                    "impl": "pg_function",
                    "function_ref": "test.fn_foo_list",
                    "call": {
                        "arg_binding": {
                            "type_name": "test.tfoo_list",
                            "mapping": [
                                {"attr": "tenant", "from": "args.tenant"},
                                {"attr": "search", "from": "args.search"},
                            ],
                        }
                    },
                    "result": {"expected": "entity_row"},
                },
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)
    result = compiler.compile_model_from_edl(edl_json, [], escopo=escopo)

    assert result is not None
    assert result.get_function_name == "test.fn_foo_get"
    assert result.list_function_name == "test.fn_foo_list"

    get_code = result.source_get_function_type
    list_code = result.source_list_function_type
    assert get_code is not None
    assert list_code is not None

    expected_get_class = compile_function_class_name("Foo", "", [], "get")
    expected_list_class = compile_function_class_name("Foo", "", [], "list")

    assert result.get_function_type_class_name == expected_get_class
    assert result.list_function_type_class_name == expected_list_class
    assert f"class {expected_get_class}" in get_code
    assert "id_func: uuid.UUID = FunctionField(" in get_code
    assert "tenant: Any = FunctionField(" in get_code

    assert f"class {expected_list_class}" in list_code
    assert "tenant: Any = FunctionField(" in list_code
    assert "search: Any = FunctionField(" in list_code
    assert result.custom_json_get_response is False
    assert result.custom_json_list_response is False


def test_compile_handlers_generates_partial_row_response_dto():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para partial_row.",
        "id": "Bar",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "codigo": {"type": "string"},
            "descricao": {"type": "string"},
        },
        "repository": {
            "map": "test.bar",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
                "codigo": {"column": "codigo"},
                "descricao": {"column": "descricao"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "bars",
            "expose": True,
            "verbs": ["POST"],
            "handlers": {
                "post": {
                    "impl": "pg_function",
                    "function_ref": "test.fn_bar",
                    "call": {
                        "arg_binding": {
                            "type_name": "test.tbar",
                            "mapping": [{"attr": "codigo", "from": "body.codigo"}],
                        }
                    },
                    "result": {"expected": "partial_row", "properties": ["codigo"]},
                }
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)
    result = compiler.compile_model_from_edl(edl_json, [], escopo=escopo)

    assert result is not None
    assert result.post_response_dto_class_name == "BarPostResponseDTO"
    assert "class BarPostResponseDTO" in result.dto_code
    response_section = result.dto_code.split("class BarPostResponseDTO")[1]
    assert "codigo: str = DTOField" in response_section
    assert "id: uuid.UUID = DTOField" not in response_section
    assert result.retrieve_after_insert is False
    assert result.custom_json_post_response is False


def test_compile_handlers_sets_custom_json_flag_without_impl():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para custom_json.",
        "id": "Baz",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
        },
        "repository": {
            "map": "test.baz",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "baz",
            "expose": True,
            "verbs": ["POST"],
            "handlers": {
                "post": {
                    "result": {"expected": "custom_json"},
                }
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)
    result = compiler.compile_model_from_edl(edl_json, [], escopo=escopo)

    assert result is not None
    assert result.custom_json_post_response is True
    assert result.retrieve_after_insert is False
    assert result.post_response_dto_class_name is None


def test_compile_handlers_sets_custom_json_for_get_and_list():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para custom_json em GET/LIST.",
        "id": "FooBar",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
        },
        "repository": {
            "map": "test.foobar",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "foobars",
            "expose": True,
            "verbs": ["GET"],
            "handlers": {
                "get": {
                    "result": {"expected": "custom_json"},
                },
                "list": {
                    "result": {"expected": "custom_json"},
                },
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)
    result = compiler.compile_model_from_edl(edl_json, [], escopo=escopo)

    assert result is not None
    assert result.custom_json_get_response is True
    assert result.custom_json_list_response is True


def test_compile_handlers_sets_custom_json_for_delete():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para custom_json em DELETE.",
        "id": "FooDelete",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
        },
        "repository": {
            "map": "test.foodelete",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "foodeletes",
            "expose": True,
            "verbs": ["DELETE"],
            "handlers": {
                "delete": {
                    "result": {"expected": "custom_json"},
                }
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)
    result = compiler.compile_model_from_edl(edl_json, [], escopo=escopo)

    assert result is not None
    assert result.custom_json_delete_response is True


def test_compile_handlers_retrieve_after_update_and_partial_update_flags():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para flags de retrieve em PUT/PATCH.",
        "id": "RetrieveFlags",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "codigo": {"type": "string"},
        },
        "repository": {
            "map": "test.retrieve_flags",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
                "codigo": {"column": "codigo"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "retrieve-flags",
            "expose": True,
            "verbs": ["PUT", "PATCH"],
            "handlers": {
                "put": {
                    "result": {"expected": "entity_row"},
                },
                "patch": {
                    "result": {"expected": "entity_row"},
                },
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)
    result = compiler.compile_model_from_edl(edl_json, [], escopo=escopo)

    assert result is not None
    assert result.retrieve_after_update is True
    assert result.retrieve_after_partial_update is True


def test_compile_handlers_disable_retrieve_after_update_for_partial_row():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade de teste para partial_row em PUT/PATCH.",
        "id": "PartialRetrieveFlags",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "codigo": {"type": "string"},
        },
        "repository": {
            "map": "test.partial_retrieve_flags",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
                "codigo": {"column": "codigo"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "partial-retrieve-flags",
            "expose": True,
            "verbs": ["PUT", "PATCH"],
            "handlers": {
                "put": {
                    "result": {"expected": "partial_row", "properties": ["codigo"]},
                },
                "patch": {
                    "result": {"expected": "partial_row", "properties": ["codigo"]},
                },
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)
    result = compiler.compile_model_from_edl(edl_json, [], escopo=escopo)

    assert result is not None
    assert result.retrieve_after_update is False
    assert result.retrieve_after_partial_update is False


def test_compile_handlers_partial_row_requires_properties():
    edl_json = {
        "edl_version": "1.0",
        "escopo": "test",
        "description": "Entidade inválida para partial_row.",
        "id": "Qux",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
        },
        "repository": {
            "map": "test.qux",
            "shared_table": False,
            "properties": {
                "id": {"column": "id"},
            },
            "indexes": [],
        },
        "api": {
            "resource": "qux",
            "expose": True,
            "verbs": ["POST"],
            "handlers": {
                "post": {
                    "result": {"expected": "partial_row"},
                }
            },
        },
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo="test", service_account=None)

    with pytest.raises(ValidationError):
        compiler.compile_model_from_edl(edl_json, [], escopo=escopo)
