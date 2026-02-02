import ast

import black

from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.util.str_util import CompilerStrUtil
from nsj_rest_lib2.compiler.util.type_naming_util import compile_entity_class_name


class EntityCompiler:
    def __init__(self):
        pass

    def compile(
        self,
        entity_model: EntityModelBase,
        ast_entity_attributes: list[ast.stmt],
        props_pk: list[str],
        prefix_class_name: str,
        partial_metadata: dict[str, str] | None,
    ) -> tuple[str, str]:
        # Imports
        imports = [
            # import datetime
            ast.Import(names=[ast.alias(name="datetime", asname=None)]),
            # import dateutil
            ast.ImportFrom(module="dateutil.relativedelta", 
                           names=[ast.alias(name="relativedelta")], 
                           level=0),
            # import uuid
            ast.Import(names=[ast.alias(name="uuid", asname=None)]),
            # from nsj_rest_lib.entity.entity_base import EntityBase
            ast.ImportFrom(
                module="nsj_rest_lib.entity.entity_base",
                names=[ast.alias(name="EntityBase", asname=None)],
                level=0,
            ),
            # from nsj_rest_lib.decorator.entity import Entity
            ast.ImportFrom(
                module="nsj_rest_lib.decorator.entity",
                names=[ast.alias(name="Entity", asname=None)],
                level=0,
            ),
        ]

        if partial_metadata:
            imports.append(
                ast.ImportFrom(
                    module=f"dynamic.{partial_metadata['module']}",
                    names=[
                        ast.alias(name=partial_metadata["entity_class"], asname=None)
                    ],
                    level=0,
                )
            )

        # Entity
        if len(props_pk) > 1:
            raise Exception(
                f"Entidade '{entity_model.id}' possui mais de uma chave primária (ainda não suportado): {props_pk}"
            )

        if len(props_pk) == 0 and not partial_metadata:
            raise Exception(
                f"Entidade '{entity_model.id}' não possui nenhuma chave primária (ainda não suportado)."
            )

        default_order_props = []

        # Resolvendo o nome da coluna da chave primária
        if len(props_pk) == 1:
            key_field_property = props_pk[0]
        else:
            key_field_property = (
                partial_metadata["relation_field"] if partial_metadata else None
            )

        key_field = key_field_property
        if (
            len(props_pk) == 1
            and entity_model.repository.properties
            and key_field_property in entity_model.repository.properties
            and entity_model.repository.properties[key_field_property].column
        ):
            key_field = entity_model.repository.properties[key_field_property].column
        elif partial_metadata and partial_metadata.get("relation_field"):
            key_field = partial_metadata["relation_field"]

        if key_field is None:
            raise Exception(
                f"Não foi possível determinar a chave primária para a entidade '{entity_model.id}'."
            )

        if (
            isinstance(entity_model, EntityModel)
            and entity_model.api
            and entity_model.api.default_sort
        ):
            default_order_props = entity_model.api.default_sort

        default_order_fields = []
        for prop in default_order_props:
            if (
                entity_model.repository.properties
                and prop in entity_model.repository.properties
            ):
                field = entity_model.repository.properties[prop].column
            else:
                field = prop

            default_order_fields.append(CompilerStrUtil.to_snake_case(field))

        if CompilerStrUtil.to_snake_case(key_field) not in default_order_fields:
            default_order_fields.append(CompilerStrUtil.to_snake_case(key_field))

        class_name = compile_entity_class_name(entity_model.id, prefix_class_name)
        ast_class = ast.ClassDef(
            name=class_name,
            bases=[ast.Name(id="EntityBase", ctx=ast.Load())],
            keywords=[],
            decorator_list=[
                ast.Call(
                    func=ast.Name(id="Entity", ctx=ast.Load()),
                    args=[],
                    keywords=self._build_entity_decorator_keywords(
                        entity_model, key_field, default_order_fields, partial_metadata
                    ),
                )
            ],
            body=ast_entity_attributes,
        )

        # Definindo o módulo
        module = ast.Module(
            body=imports + [ast_class],
            type_ignores=[],
        )
        module = ast.fix_missing_locations(module)

        # Compilando o AST do DTO para o código Python
        code = ast.unparse(module)

        # Chamando o black para formatar o código Python do DTO
        code = black.format_str(code, mode=black.FileMode())

        return (class_name, code)

    def _build_entity_decorator_keywords(
        self,
        entity_model: EntityModelBase,
        key_field: str,
        default_order_fields: list[str],
        partial_metadata: dict[str, str] | None,
    ) -> list[ast.keyword]:
        keywords = [
            ast.keyword(
                arg="table_name",
                value=ast.Constant(value=entity_model.repository.map),
            ),
        ]

        if not partial_metadata:
            keywords.extend(
                [
                    ast.keyword(
                        arg="pk_field",
                        value=ast.Constant(
                            value=CompilerStrUtil.to_snake_case(key_field)
                        ),
                    ),
                    ast.keyword(
                        arg="default_order_fields",
                        value=ast.List(
                            elts=[
                                ast.Constant(value=field)
                                for field in default_order_fields
                            ],
                            ctx=ast.Load(),
                        ),
                    ),
                ]
            )

        if partial_metadata:
            keywords.insert(
                0,
                ast.keyword(
                    arg="partial_of",
                    value=ast.Name(id=partial_metadata["entity_class"], ctx=ast.Load()),
                ),
            )

        return keywords
