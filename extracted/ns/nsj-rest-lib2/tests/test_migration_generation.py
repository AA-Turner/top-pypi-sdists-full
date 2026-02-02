import json
import os
import sys
import copy
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault("ESCOPO_RESTLIB2", "test-scope")

from nsj_rest_lib2.compiler.compiler import EDLCompiler
from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_root import EntityModelRoot
from nsj_rest_lib2.compiler.migration_compiler import MigrationCompiler
from nsj_rest_lib2.dto.escopo_dto import EscopoDTO


def _load_entity(path: Path) -> tuple[str, EntityModel]:
    with path.open("r") as fp:
        if path.suffix.lower() == ".json":
            edl_data = json.load(fp)
        else:
            edl_data = yaml.safe_load(fp)

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
        if path.suffix.lower() not in {".json", ".yaml", ".yml"}:
            continue
        key, model = _load_entity(path)
        models[key] = model
    return models


def test_migration_generation_for_pessoa():
    base_dir = Path(__file__).resolve().parents[1] / "@schemas_test"
    entity_models = _load_entity_models(base_dir)

    pessoa_model = entity_models["dados_mestre/pessoa"]

    compiler = EDLCompiler()
    migration_compiler = MigrationCompiler(compiler)

    sql = migration_compiler.compile(pessoa_model, entity_models)

    assert "DO $MIGRATION$" in sql
    assert "IF exists_table('ns.pessoas')" in sql
    assert "CREATE TABLE ns.pessoas" in sql
    assert "pessoa varchar(30)" in sql  # coluna mapeada de 'codigo'
    assert "nome varchar(200)" in sql
    assert "cnpj varchar(20)" in sql  # cpf_cnpj mapeia para coluna cnpj
    assert "ALTER TABLE ns.pessoas ALTER COLUMN nome SET NOT NULL" in sql
    assert "table_has_primary_key('ns.pessoas')" in sql
    # Enum checks gerados
    assert "qualificacao_enum_chk CHECK (qualificacao IN (" in sql
    assert "situacaopagamento_enum_chk CHECK (situacaopagamento IN (" in sql
    assert (
        "indicadorinscricaoestadual_enum_chk CHECK (indicadorinscricaoestadual IN ("
        in sql
    )
    # Comentários de coluna (usa COMMENT ON)
    assert "COMMENT ON COLUMN ns.pessoas" in sql
    # Garantia de uso das funções auxiliares de coluna
    assert "column_default_equals(" in sql
    assert "column_is_not_null(" in sql


def test_migration_generation_with_rename():
    base_dir = Path(__file__).resolve().parents[1] / "@schemas_test"
    entity_models = _load_entity_models(base_dir)

    pessoa_model = entity_models["dados_mestre/pessoa"]
    # Copiando e alterando o mapeamento da coluna 'codigo' de pessoa -> pessoa_new
    import copy

    pessoa_old = copy.deepcopy(pessoa_model)
    pessoa_old.repository.properties["codigo"].column = "pessoa"
    pessoa_new = copy.deepcopy(pessoa_model)
    pessoa_new.repository.properties["codigo"].column = "pessoa_new"

    compiler = EDLCompiler()
    migration_compiler = MigrationCompiler(compiler)

    sql = migration_compiler.compile(pessoa_new, entity_models, pessoa_old)

    assert "RENAME COLUMN pessoa TO pessoa_new" in sql
    assert "exists_column('ns.pessoas', 'pessoa')" in sql
    assert "exists_column('ns.pessoas', 'pessoa_new')" in sql


def test_migration_generation_with_fk():
    base_dir = Path(__file__).resolve().parents[1] / "@schemas_test"
    entity_models = _load_entity_models(base_dir)

    pessoa_model = entity_models["dados_mestre/pessoa"]
    compiler = EDLCompiler()
    migration_compiler = MigrationCompiler(compiler)

    # Simula que 'conta' usa coluna local id_conta apontando para financas/conta
    pessoa_model = copy.deepcopy(pessoa_model)
    pessoa_model.repository.properties["conta"].relation_column = "dados_mestre/pessoa/id_conta"

    sql = migration_compiler.compile(pessoa_model, entity_models)

    assert "id_conta uuid" in sql
    assert "FOREIGN KEY (id_conta)" in sql
    assert "financas.conta" in sql or "financas_conta" in sql


def test_migration_generation_with_remote_fk():
    base_dir = Path(__file__).resolve().parents[1] / "@schemas_test"
    entity_models = _load_entity_models(base_dir)

    endereco_model = entity_models["dados_mestre/endereco"]
    compiler = EDLCompiler()
    migration_compiler = MigrationCompiler(compiler)

    # relation_column de 'enderecos' (em pessoa) aponta coluna id_pessoa na tabela de enderecos
    sql = migration_compiler.compile(endereco_model, entity_models)

    assert "ALTER TABLE ns.enderecos" in sql
    assert "FOREIGN KEY (id_pessoa)" in sql
    assert "REFERENCES ns.pessoas" in sql


def test_compile_external_component_relation():
    base_dir = Path(__file__).resolve().parents[1] / "@schemas_test"
    entity_models = _load_entity_models(base_dir)

    pedido_edl = {
        "edl_version": "1.0",
        "escopo": "vendas",
        "description": "Pedido com relação a componente externa",
        "id": "pedido",
        "version": "1.0",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "numero": {"type": "string"},
            "contatos": {
                "type": "dados_mestre/pessoa/#/components/contato",
                "label": "Contatos",
                "cardinality": "1_N",
            },
        },
        "repository": {
            "map": "ns.pedidos",
            "table_owner": True,
            "properties": {
                "id": {"column": "id"},
                "numero": {"column": "numero"},
                "contatos": {
                    "relation_column": "dados_mestre/pessoa/#/components/contato/id_pedido"
                },
            },
            "indexes": [],
        },
        "api": {
            "resource": "pedidos",
            "expose": True,
            "verbs": ["GET"],
        },
    }

    pedido_model = EntityModel(**pedido_edl)

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo=pedido_model.escopo, service_account=None)
    result = compiler.compile_model(
        pedido_model,
        list(entity_models.items()),
        escopo=escopo,
    )

    assert result is not None
    assert "PessoaContatoDTO" in (result.dto_code or "")

    relation_resources = [
        rd.entity_resource for rd in (result.relations_dependencies or [])
    ]
    assert "pessoas" in relation_resources


def test_compile_deep_component_relation():
    pessoa_nested = {
        "edl_version": "1.0",
        "escopo": "dados_mestre",
        "description": "Pessoa com contato e telefone",
        "id": "pessoa",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "contatos": {
                "type": "#/components/contato",
                "cardinality": "1_N",
                "label": "Contatos",
            },
        },
        "components": {
            "contato": {
                "id": "contato",
                "description": "Contato de pessoa",
                "properties": {
                    "id": {"type": "uuid", "pk": True},
                    "id_pessoa": {"type": "uuid"},
                    "telefones": {
                        "type": "#/components/telefone",
                        "cardinality": "1_N",
                    },
                },
                "components": {
                    "telefone": {
                        "id": "telefone",
                        "description": "Telefone do contato",
                        "properties": {
                            "id": {"type": "uuid", "pk": True},
                            "id_contato": {"type": "uuid"},
                            "numero": {"type": "string"},
                        },
                        "repository": {
                            "map": "ns.telefones",
                            "table_owner": True,
                            "sharedTable": True,
                            "properties": {
                                "id": {"column": "id"},
                                "id_contato": {"column": "id_contato"},
                                "numero": {"column": "numero"},
                            },
                            "indexes": [],
                        },
                    }
                },
                "repository": {
                    "map": "ns.contatos",
                    "table_owner": True,
                    "sharedTable": True,
                    "properties": {
                        "id": {"column": "id"},
                        "id_pessoa": {"column": "id_pessoa"},
                        "telefones": {
                            "relation_column": "dados_mestre/pessoa/#/components/contato/#/components/telefone/id_contato"
                        },
                    },
                    "indexes": [],
                },
            },
        },
        "repository": {
            "map": "ns.pessoas",
            "table_owner": True,
            "properties": {
                "id": {"column": "id"},
                "contatos": {
                    "relation_column": "dados_mestre/pessoa/#/components/contato/id_pessoa"
                },
            },
            "indexes": [],
        },
        "api": {
            "resource": "pessoas",
            "expose": True,
            "verbs": ["GET"],
        },
    }

    followup_edl = {
        "edl_version": "1.0",
        "escopo": "crm",
        "description": "Followup ligado a telefone de contato de pessoa",
        "id": "followup",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "descricao": {"type": "string"},
            "telefones": {
                "type": "dados_mestre/pessoa/#/components/contato/#/components/telefone",
                "cardinality": "1_N",
            },
        },
        "repository": {
            "map": "ns.followups",
            "table_owner": True,
            "properties": {
                "id": {"column": "id"},
                "descricao": {"column": "descricao"},
                "telefones": {
                    "relation_column": "dados_mestre/pessoa/#/components/contato/#/components/telefone/id_followup"
                },
            },
            "indexes": [],
        },
        "api": {
            "resource": "followups",
            "expose": True,
            "verbs": ["GET"],
        },
    }

    pessoa_model = EntityModel(**pessoa_nested)
    followup_model = EntityModel(**followup_edl)

    entity_models = {
        "dados_mestre/pessoa": pessoa_model,
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo=followup_model.escopo, service_account=None)
    result = compiler.compile_model(
        followup_model,
        list(entity_models.items()),
        escopo=escopo,
    )

    assert result is not None
    assert "PessoaContatoTelefoneDTO" in (result.dto_code or "")
    assert any(
        rd.entity_resource == "pessoas" for rd in (result.relations_dependencies or [])
    )


def test_compile_deep_component_relation_without_markers():
    pessoa_nested = {
        "edl_version": "1.0",
        "escopo": "dados_mestre",
        "description": "Pessoa com contato e telefone",
        "id": "pessoa",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "contatos": {
                "type": "#/components/contato",
                "cardinality": "1_N",
                "label": "Contatos",
            },
        },
        "components": {
            "contato": {
                "id": "contato",
                "description": "Contato de pessoa",
                "properties": {
                    "id": {"type": "uuid", "pk": True},
                    "id_pessoa": {"type": "uuid"},
                    "telefones": {
                        "type": "#/components/telefone",
                        "cardinality": "1_N",
                    },
                },
                "components": {
                    "telefone": {
                        "id": "telefone",
                        "description": "Telefone do contato",
                        "properties": {
                            "id": {"type": "uuid", "pk": True},
                            "id_contato": {"type": "uuid"},
                            "numero": {"type": "string"},
                        },
                        "repository": {
                            "map": "ns.telefones",
                            "table_owner": True,
                            "sharedTable": True,
                            "properties": {
                                "id": {"column": "id"},
                                "id_contato": {"column": "id_contato"},
                                "numero": {"column": "numero"},
                            },
                            "indexes": [],
                        },
                    }
                },
                "repository": {
                    "map": "ns.contatos",
                    "table_owner": True,
                    "sharedTable": True,
                    "properties": {
                        "id": {"column": "id"},
                        "id_pessoa": {"column": "id_pessoa"},
                        "telefones": {
                            "relation_column": "dados_mestre/pessoa/contato/telefone/id_contato"
                        },
                    },
                    "indexes": [],
                },
            },
        },
        "repository": {
            "map": "ns.pessoas",
            "table_owner": True,
            "properties": {
                "id": {"column": "id"},
                "contatos": {
                    "relation_column": "dados_mestre/pessoa/contato/id_pessoa"
                },
            },
            "indexes": [],
        },
        "api": {
            "resource": "pessoas",
            "expose": True,
            "verbs": ["GET"],
        },
    }

    followup_edl = {
        "edl_version": "1.0",
        "escopo": "crm",
        "description": "Followup ligado a telefone de contato de pessoa",
        "id": "followup",
        "properties": {
            "id": {"type": "uuid", "pk": True},
            "descricao": {"type": "string"},
            "telefones": {
                "type": "dados_mestre/pessoa/contato/telefone",
                "cardinality": "1_N",
            },
        },
        "repository": {
            "map": "ns.followups",
            "table_owner": True,
            "properties": {
                "id": {"column": "id"},
                "descricao": {"column": "descricao"},
                "telefones": {
                    "relation_column": "dados_mestre/pessoa/contato/telefone/id_followup"
                },
            },
            "indexes": [],
        },
        "api": {
            "resource": "followups",
            "expose": True,
            "verbs": ["GET"],
        },
    }

    pessoa_model = EntityModel(**pessoa_nested)
    followup_model = EntityModel(**followup_edl)

    entity_models = {
        "dados_mestre/pessoa": pessoa_model,
    }

    compiler = EDLCompiler()
    escopo = EscopoDTO(codigo=followup_model.escopo, service_account=None)
    result = compiler.compile_model(
        followup_model,
        list(entity_models.items()),
        escopo=escopo,
    )

    assert result is not None
    assert "PessoaContatoTelefoneDTO" in (result.dto_code or "")
    assert any(
        rd.entity_resource == "pessoas" for rd in (result.relations_dependencies or [])
    )
