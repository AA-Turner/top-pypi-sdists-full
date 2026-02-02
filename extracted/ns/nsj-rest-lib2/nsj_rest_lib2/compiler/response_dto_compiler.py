from __future__ import annotations

import ast
from typing import Any, Optional

from nsj_rest_lib2.compiler.dto_compiler import DTOCompiler
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.primitives import BasicTypes
from nsj_rest_lib2.compiler.util.str_util import CompilerStrUtil
from nsj_rest_lib2.compiler.util.type_naming_util import (
    compile_response_dto_class_name,
)


class ResponseDTOCompiler:
    def __init__(
        self,
        dto_compiler: DTOCompiler,
        entity_model: EntityModelBase,
        prefx_class_name: str,
        ast_dto_attributes: list[ast.stmt],
        aux_classes: list[ast.stmt],
        related_imports: list[tuple[str, str, str]],
        fixed_filters: list[tuple[str, BasicTypes]],
    ) -> None:
        self._dto_compiler = dto_compiler
        self._entity_model = entity_model
        self._prefx_class_name = prefx_class_name
        self._aux_classes = aux_classes
        self._related_imports = related_imports
        self._fixed_filters = fixed_filters
        self._dto_attr_map = self._build_attr_map(ast_dto_attributes)

    @staticmethod
    def handler_result_details(handler: Any) -> tuple[str, list[str] | None]:
        expected = "empty"
        properties = None
        if handler and getattr(handler, "result", None):
            expected = handler.result.expected or "empty"
            properties = handler.result.properties
        return (expected, properties)

    def compile_partial_response_dto(
        self, verb: str, properties: list[str]
    ) -> tuple[str, str]:
        if not properties:
            raise Exception(
                f"result.properties não pode ser vazio para '{verb}' na entidade '{self._entity_model.id}'."
            )

        normalized = [
            CompilerStrUtil.to_snake_case(prop) for prop in properties
        ]
        missing = [
            properties[idx]
            for idx, norm in enumerate(normalized)
            if norm not in self._dto_attr_map
        ]
        if missing:
            raise Exception(
                f"As propriedades {missing} não foram encontradas na entidade '{self._entity_model.id}'."
            )

        filtered_attrs = [self._dto_attr_map[name] for name in normalized]
        filtered_fixed_filters = [
            item for item in self._fixed_filters if item[0] in normalized
        ]

        class_name = compile_response_dto_class_name(
            self._entity_model.id,
            self._prefx_class_name,
            verb,
        )

        return self._dto_compiler.compile(
            self._entity_model,
            filtered_attrs,
            self._aux_classes,
            self._related_imports,
            filtered_fixed_filters,
            self._prefx_class_name,
            None,
            class_name_override=class_name,
        )

    @staticmethod
    def _extract_attr_name(stmt: ast.stmt) -> Optional[str]:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            return stmt.target.id
        if isinstance(stmt, ast.Assign) and stmt.targets:
            target = stmt.targets[0]
            if isinstance(target, ast.Name):
                return target.id
        return None

    def _build_attr_map(
        self, ast_dto_attributes: list[ast.stmt]
    ) -> dict[str, ast.stmt]:
        dto_attr_map: dict[str, ast.stmt] = {}
        for stmt in ast_dto_attributes:
            name = self._extract_attr_name(stmt)
            if name:
                dto_attr_map[name] = stmt
        return dto_attr_map
