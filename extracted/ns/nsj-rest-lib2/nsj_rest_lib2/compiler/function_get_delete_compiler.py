from __future__ import annotations

from typing import Optional

from nsj_rest_lib2.compiler.compiler_structures import PropertiesCompilerStructure
from nsj_rest_lib2.compiler.edl_model.api_model import HandlerConfig, HandlerMapping
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.primitives import PrimitiveTypes
from nsj_rest_lib2.compiler.function_model import FunctionCompilationOutput
from nsj_rest_lib2.compiler.util.str_util import CompilerStrUtil
from nsj_rest_lib2.compiler.util.type_naming_util import compile_function_class_name
from nsj_rest_lib2.compiler.util.type_util import TypeUtil


class FunctionGetDeleteCompiler:
    """
    Responsável por gerar FunctionTypes (Get/List/Delete) baseados no
    binding de pg_function declarado no EDL.
    """

    def compile(
        self,
        entity_model: EntityModelBase,
        properties_structure: PropertiesCompilerStructure,
        handler_config: Optional[HandlerConfig],
        prefx_class_name: str,
        verb: str,
    ) -> FunctionCompilationOutput:
        if not isinstance(handler_config, HandlerConfig):
            return FunctionCompilationOutput()
        if handler_config.impl != "pg_function":
            return FunctionCompilationOutput()
        if not handler_config.call or not handler_config.call.arg_binding:
            return FunctionCompilationOutput()

        arg_binding = handler_config.call.arg_binding
        if not arg_binding.mapping or not arg_binding.type_name:
            return FunctionCompilationOutput()

        function_name = handler_config.function_ref
        if not function_name:
            return FunctionCompilationOutput()

        class_name = compile_function_class_name(
            entity_model.id,
            prefx_class_name,
            [],
            verb,
        )

        fields = self._build_fields(arg_binding.mapping, properties_structure)
        if not fields:
            return FunctionCompilationOutput()

        code = self._build_code(class_name, arg_binding.type_name, fields, verb)

        return FunctionCompilationOutput(
            class_name=class_name,
            code=code,
            function_name=function_name,
        )

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _build_fields(
        self,
        mappings: list[HandlerMapping],
        properties_structure: PropertiesCompilerStructure,
    ) -> list[tuple[str, str, Optional[str], bool]]:
        """
        Retorna lista de tuplas:
        (python_name, annotation, type_field_name, is_pk)
        """
        fields: list[tuple[str, str, Optional[str], bool]] = []
        used: set[str] = set()

        for entry in mappings or []:
            attr = (entry.attr or "").strip()
            if not attr:
                continue

            python_name = self._sanitize_identifier(attr)
            if python_name in used:
                continue
            used.add(python_name)

            type_field_name = attr if python_name != attr else None
            source = (entry.from_ or "").strip()
            is_pk = source.startswith("path.")

            annotation = self._resolve_annotation(entry, properties_structure)

            fields.append(
                (
                    python_name,
                    annotation,
                    type_field_name,
                    is_pk,
                )
            )

        return fields

    def _resolve_annotation(
        self,
        entry: HandlerMapping,
        properties_structure: PropertiesCompilerStructure,
    ) -> str:
        """
        Tenta inferir o tipo a partir das propriedades da entidade.
        Prioriza:
        - campos referenciados como body.<campo>;
        - ou, se o último segmento de 'from' (após o '.') existir como
          property do EDL, usa esse nome para lookup.
        """
        dto_field = self._extract_dto_field(entry.from_)

        # Se não veio de body.*, tenta casar o último segmento de 'from'
        # com o nome de alguma propriedade do EDL.
        if not dto_field:
            candidate = CompilerStrUtil.to_snake_case(
                (entry.from_ or "").split(".")[-1]
            )
            if candidate and properties_structure and candidate in properties_structure.properties:
                dto_field = candidate

        if not dto_field:
            return "Any"

        prop = (
            properties_structure.properties.get(dto_field)
            if properties_structure
            else None
        )
        if not prop or not isinstance(prop.type, PrimitiveTypes):
            return "Any"

        return TypeUtil.property_type_to_python_type(prop.type)

    def _build_code(
        self,
        class_name: str,
        type_name: str,
        fields: list[tuple[str, str, Optional[str], bool]],
        verb: str,
    ) -> str:
        needs_any = any(annotation == "Any" for _, annotation, _, _ in fields)
        needs_uuid = any(annotation == "uuid.UUID" for _, annotation, _, _ in fields)
        needs_datetime = any(
            annotation == "datetime.datetime" for _, annotation, _, _ in fields
        )

        lines: list[str] = []
        if needs_uuid:
            lines.append("import uuid")
        if needs_datetime:
            lines.append("import datetime")
        if needs_any:
            lines.append("from typing import Any")

        decorator_module, decorator_name, base_class = self._resolve_decorator(verb)
        lines.extend(
            [
                f"from {decorator_module} import {decorator_name}",
                f"from nsj_rest_lib.entity.function_type_base import {base_class}",
                "from nsj_rest_lib.descriptor.function_field import FunctionField",
                "",
                f"@{decorator_name}(type_name=\"{type_name}\")",
                f"class {class_name}({base_class}):",
            ]
        )

        for name, annotation, type_field_name, is_pk in fields:
            kwargs: list[str] = []
            if type_field_name:
                kwargs.append(f'type_field_name="{type_field_name}"')
            if is_pk:
                kwargs.append("pk=True")
            kwargs_str = ", ".join(kwargs)
            if kwargs_str:
                kwargs_str = ", " + kwargs_str
            lines.append(
                f"    {name}: {annotation} = FunctionField({kwargs_str.lstrip(', ')})"
            )

        if not fields:
            lines.append("    pass")

        lines.append("")  # newline final
        return "\n".join(lines)

    def _resolve_decorator(self, verb: str) -> tuple[str, str, str]:
        verb = (verb or "").lower()
        if verb == "get":
            return (
                "nsj_rest_lib.decorator.get_function_type",
                "GetFunctionType",
                "GetFunctionTypeBase",
            )
        if verb == "list":
            return (
                "nsj_rest_lib.decorator.list_function_type",
                "ListFunctionType",
                "ListFunctionTypeBase",
            )
        if verb == "delete":
            return (
                "nsj_rest_lib.decorator.delete_function_type",
                "DeleteFunctionType",
                "DeleteFunctionTypeBase",
            )
        # fallback genérico
        return (
            "nsj_rest_lib.decorator.function_type",
            "FunctionType",
            "FunctionTypeBase",
        )

    def _sanitize_identifier(self, name: str) -> str:
        candidate = CompilerStrUtil.to_snake_case(name)
        candidate = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in candidate)
        if not candidate:
            candidate = "field"
        if candidate[0].isdigit():
            candidate = f"_{candidate}"
        return candidate

    def _extract_dto_field(self, source: Optional[str]) -> Optional[str]:
        if not source:
            return None

        if source.startswith("body."):
            segment = source[5:].split(".", 1)[0]
            return CompilerStrUtil.to_snake_case(segment)

        return None
