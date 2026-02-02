from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Dict, Optional, Sequence

import black

from nsj_rest_lib2.compiler.compiler_structures import PropertiesCompilerStructure
from nsj_rest_lib2.compiler.edl_model.api_model import HandlerConfig, HandlerMapping
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.primitives import PrimitiveTypes
from nsj_rest_lib2.compiler.function_model import (
    FunctionBindingConfig,
    FunctionCompilationOutput,
    FunctionRelationBinding,
)
from nsj_rest_lib2.compiler.util.str_util import CompilerStrUtil
from nsj_rest_lib2.compiler.util.type_naming_util import compile_function_class_name
from nsj_rest_lib2.compiler.util.type_util import TypeUtil


@dataclass
class _MappingNode:
    attr: str
    python_name: str
    dto_field: Optional[str]
    children: list["_MappingNode"] = field(default_factory=list)
    pg_type: Optional[str] = None
    is_array: bool = False


@dataclass
class _FieldSpec:
    name: str
    annotation: str
    type_field_name: Optional[str]
    relation_class: Optional[str]
    is_relation: bool
    is_list: bool


@dataclass
class _ClassSpec:
    name: str
    type_name: str
    function_name: str
    fields: list[_FieldSpec]
    children: list["_ClassSpec"] = field(default_factory=list)


class FunctionInsertUpdateCompiler:
    """
    Responsável por compilar tipos usados por funções de banco (Insert/Update)
    com base na configuração declarada no EDL.
    """

    def compile_insert(
        self,
        entity_model: EntityModelBase,
        properties_structure: PropertiesCompilerStructure,
        handler_config: Optional[HandlerConfig],
        prefx_class_name: str,
    ) -> FunctionCompilationOutput:
        return self._compile(
            entity_model,
            properties_structure,
            handler_config,
            prefx_class_name,
            operation="insert",
        )

    def compile_update(
        self,
        entity_model: EntityModelBase,
        properties_structure: PropertiesCompilerStructure,
        handler_config: Optional[HandlerConfig],
        prefx_class_name: str,
    ) -> FunctionCompilationOutput:
        return self._compile(
            entity_model,
            properties_structure,
            handler_config,
            prefx_class_name,
            operation="update",
        )

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _compile(
        self,
        entity_model: EntityModelBase,
        properties_structure: PropertiesCompilerStructure,
        handler_config: Optional[HandlerConfig],
        prefx_class_name: str,
        operation: str,
    ) -> FunctionCompilationOutput:
        if not handler_config or handler_config.impl != "pg_function":
            return FunctionCompilationOutput()

        if not handler_config.call or not handler_config.call.arg_binding:
            return FunctionCompilationOutput()

        arg_binding = handler_config.call.arg_binding
        if not arg_binding.mapping or not arg_binding.type_name:
            return FunctionCompilationOutput()

        function_name = handler_config.function_ref
        if not function_name:
            return FunctionCompilationOutput()

        mapping_nodes = self._build_nodes(arg_binding.mapping)
        if not mapping_nodes:
            return FunctionCompilationOutput()

        class_name = compile_function_class_name(
            entity_model.id,
            prefx_class_name,
            [],
            operation,
        )

        field_bindings: Dict[str, str] = {}
        relation_bindings: Dict[str, FunctionRelationBinding] = {}

        class_spec = self._build_class_spec(
            mapping_nodes,
            entity_model,
            properties_structure,
            function_name,
            class_name,
            arg_binding.type_name,
            path=[],
            operation=operation,
            field_bindings=field_bindings,
            relation_bindings=relation_bindings,
            prefx_class_name=prefx_class_name,
        )

        module_ast, has_relations, needs_any = self._build_module_ast(
            class_spec, operation
        )

        if not module_ast:
            return FunctionCompilationOutput()

        imports = self._build_imports(operation, has_relations, needs_any)
        module = ast.Module(body=imports + module_ast, type_ignores=[])
        module = ast.fix_missing_locations(module)
        code = ast.unparse(module)
        code = black.format_str(code, mode=black.FileMode())

        return FunctionCompilationOutput(
            class_name=class_name,
            code=code,
            function_name=function_name,
            field_bindings=field_bindings,
            relation_bindings=relation_bindings,
        )

    def _build_nodes(self, mappings: Sequence[HandlerMapping]) -> list[_MappingNode]:
        nodes: list[_MappingNode] = []
        used_names: Dict[str, int] = {}

        for entry in mappings or []:
            if not entry.attr:
                continue

            python_name = self._sanitize_identifier(entry.attr)
            python_name = self._ensure_unique_name(python_name, used_names)
            dto_field = self._extract_dto_field(entry.from_)

            node = _MappingNode(
                attr=entry.attr,
                python_name=python_name,
                dto_field=dto_field,
            )

            if entry.mapping:
                pg_type, is_array = self._parse_type_declaration(entry.as_)
                node.pg_type = pg_type
                node.is_array = is_array
                node.children = self._build_nodes(entry.mapping)

            nodes.append(node)

        return nodes

    def _build_class_spec(
        self,
        nodes: Sequence[_MappingNode],
        entity_model: EntityModelBase,
        properties_structure: PropertiesCompilerStructure,
        function_name: str,
        class_name: str,
        type_name: str,
        path: list[str],
        operation: str,
        field_bindings: Dict[str, str],
        relation_bindings: Dict[str, FunctionRelationBinding],
        prefx_class_name: str,
    ) -> _ClassSpec:
        fields: list[_FieldSpec] = []
        children_specs: list[_ClassSpec] = []

        for node in nodes:
            if node.children:
                if not node.pg_type:
                    raise ValueError(
                        f"O campo '{node.attr}' possui sub-mapeamento, porém o tipo Postgres não foi informado em 'as'."
                    )

                child_class_name = compile_function_class_name(
                    entity_model.id,
                    prefx_class_name,
                    path + [node.python_name],
                    operation,
                )

                child_spec = self._build_class_spec(
                    node.children,
                    entity_model,
                    properties_structure,
                    function_name,
                    child_class_name,
                    node.pg_type,
                    path + [node.python_name],
                    operation,
                    field_bindings,
                    relation_bindings,
                    prefx_class_name,
                )

                children_specs.append(child_spec)
                fields.append(
                    _FieldSpec(
                        name=node.python_name,
                        annotation=self._relation_annotation(
                            child_class_name, node.is_array
                        ),
                        type_field_name=(
                            node.attr if node.python_name != node.attr else None
                        ),
                        relation_class=child_class_name,
                        is_relation=True,
                        is_list=node.is_array,
                    )
                )

                if node.dto_field:
                    relation_bindings[node.dto_field] = FunctionRelationBinding(
                        field_name=node.python_name,
                        function_type_class=child_class_name,
                    )

                continue

            annotation = self._resolve_annotation(node, properties_structure)
            fields.append(
                _FieldSpec(
                    name=node.python_name,
                    annotation=annotation,
                    type_field_name=(
                        node.attr if node.python_name != node.attr else None
                    ),
                    relation_class=None,
                    is_relation=False,
                    is_list=False,
                )
            )

            if node.dto_field and node.dto_field != node.python_name:
                field_bindings[node.dto_field] = node.python_name

        return _ClassSpec(
            name=class_name,
            type_name=type_name,
            function_name=function_name,
            fields=fields,
            children=children_specs,
        )

    def _build_module_ast(
        self,
        spec: _ClassSpec,
        operation: str,
    ) -> tuple[list[ast.stmt], bool, bool]:
        class_defs: list[ast.stmt] = []
        has_relation = False
        needs_any = False

        for child in spec.children:
            child_defs, child_has_relation, child_needs_any = self._build_module_ast(
                child, operation
            )
            class_defs.extend(child_defs)
            has_relation = has_relation or child_has_relation
            needs_any = needs_any or child_needs_any

        body: list[ast.stmt] = []
        for field in spec.fields:
            annotation_expr = self._build_annotation_expr(field.annotation, field)
            descriptor_call = self._build_descriptor_call(field)
            body.append(
                ast.AnnAssign(
                    target=ast.Name(id=field.name, ctx=ast.Store()),
                    annotation=annotation_expr,
                    value=descriptor_call,
                    simple=1,
                )
            )
            if field.is_relation:
                has_relation = True
            if field.annotation == "Any":
                needs_any = True

        if not body:
            body = [ast.Pass()]

        decorator_name = (
            "InsertFunctionType" if operation == "insert" else "UpdateFunctionType"
        )
        base_class = (
            "InsertFunctionTypeBase"
            if operation == "insert"
            else "UpdateFunctionTypeBase"
        )

        decorator = ast.Call(
            func=ast.Name(id=decorator_name, ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="type_name", value=ast.Constant(value=spec.type_name)),
            ],
        )

        class_defs.append(
            ast.ClassDef(
                name=spec.name,
                bases=[ast.Name(id=base_class, ctx=ast.Load())],
                keywords=[],
                decorator_list=[decorator],
                body=body,
            )
        )

        return class_defs, has_relation, needs_any

    def _build_imports(
        self, operation: str, has_relation_fields: bool, needs_any: bool
    ) -> list[ast.stmt]:
        imports: list[ast.stmt] = [
            ast.Import(names=[ast.alias(name="datetime", asname=None)]),
            ast.Import(names=[ast.alias(name="uuid", asname=None)]),
        ]

        if needs_any:
            imports.append(
                ast.ImportFrom(
                    module="typing",
                    names=[ast.alias(name="Any", asname=None)],
                    level=0,
                )
            )

        decorator_module = (
            "nsj_rest_lib.decorator.insert_function_type"
            if operation == "insert"
            else "nsj_rest_lib.decorator.update_function_type"
        )
        decorator_name = (
            "InsertFunctionType" if operation == "insert" else "UpdateFunctionType"
        )

        base_module = "nsj_rest_lib.entity.function_type_base"
        base_name = (
            "InsertFunctionTypeBase"
            if operation == "insert"
            else "UpdateFunctionTypeBase"
        )

        imports.extend(
            [
                ast.ImportFrom(
                    module=decorator_module,
                    names=[ast.alias(name=decorator_name, asname=None)],
                    level=0,
                ),
                ast.ImportFrom(
                    module="nsj_rest_lib.descriptor.function_field",
                    names=[ast.alias(name="FunctionField", asname=None)],
                    level=0,
                ),
                ast.ImportFrom(
                    module=base_module,
                    names=[ast.alias(name=base_name, asname=None)],
                    level=0,
                ),
            ]
        )

        if has_relation_fields:
            imports.append(
                ast.ImportFrom(
                    module="nsj_rest_lib.descriptor.function_relation_field",
                    names=[ast.alias(name="FunctionRelationField", asname=None)],
                    level=0,
                )
            )

        return imports

    def _build_annotation_expr(
        self, annotation: str, field: _FieldSpec
    ) -> ast.expr:
        if field.is_relation and field.is_list:
            return ast.Subscript(
                value=ast.Name(id="list", ctx=ast.Load()),
                slice=ast.Name(id=field.relation_class, ctx=ast.Load()),
                ctx=ast.Load(),
            )

        if field.is_relation:
            return ast.Name(id=field.relation_class, ctx=ast.Load())

        if annotation == "Any":
            return ast.Name(id="Any", ctx=ast.Load())

        if "." in annotation:
            parts = annotation.split(".")
            expr = ast.Name(id=parts[0], ctx=ast.Load())
            for part in parts[1:]:
                expr = ast.Attribute(value=expr, attr=part, ctx=ast.Load())
            return expr

        return ast.Name(id=annotation, ctx=ast.Load())

    def _build_descriptor_call(self, field: _FieldSpec) -> ast.Call:
        descriptor_cls = (
            "FunctionRelationField" if field.is_relation else "FunctionField"
        )
        keywords: list[ast.keyword] = []
        if field.type_field_name:
            keywords.append(
                ast.keyword(
                    arg="type_field_name",
                    value=ast.Constant(value=field.type_field_name),
                )
            )
        return ast.Call(
            func=ast.Name(id=descriptor_cls, ctx=ast.Load()),
            args=[],
            keywords=keywords,
        )

    def _resolve_annotation(
        self,
        node: _MappingNode,
        properties_structure: PropertiesCompilerStructure,
    ) -> str:
        dto_field = node.dto_field
        if not dto_field:
            return "Any"

        prop = properties_structure.properties.get(dto_field) if properties_structure else None
        if not prop or not isinstance(prop.type, PrimitiveTypes):
            return "Any"

        return TypeUtil.property_type_to_python_type(prop.type)

    # ------------------------------------------------------------------ #
    # Utility helpers
    # ------------------------------------------------------------------ #

    def _sanitize_identifier(self, name: str) -> str:
        candidate = CompilerStrUtil.to_snake_case(name)
        candidate = re.sub(r"\W+", "_", candidate)
        if not candidate:
            candidate = "field"
        if candidate[0].isdigit():
            candidate = f"_{candidate}"
        return candidate

    def _ensure_unique_name(self, name: str, used: Dict[str, int]) -> str:
        counter = used.setdefault(name, 0)
        if counter == 0:
            used[name] = 1
            return name

        while True:
            candidate = f"{name}_{counter}"
            counter += 1
            if candidate not in used:
                used[name] = counter
                used[candidate] = 1
                return candidate

    def _extract_dto_field(self, source: Optional[str]) -> Optional[str]:
        if not source:
            return None

        if source.startswith("body."):
            segment = source[5:].split(".", 1)[0]
            return CompilerStrUtil.to_snake_case(segment)

        return None

    def _parse_type_declaration(self, declaration: Optional[str]) -> tuple[str, bool]:
        if not declaration:
            return (None, False)

        declaration = declaration.strip()
        if declaration.endswith("[]"):
            return (declaration[:-2], True)
        return (declaration, False)

    def _relation_annotation(self, class_name: str, is_array: bool) -> str:
        if is_array:
            return f"list[{class_name}]"
        return class_name


def inject_function_bindings(
    target_config: FunctionBindingConfig,
    insert_output: FunctionCompilationOutput,
    update_output: FunctionCompilationOutput,
) -> FunctionBindingConfig:
    """
    Popula um FunctionBindingConfig a partir dos resultados de compilação das
    funções de insert/update.
    """

    for dto_field, function_field in insert_output.field_bindings.items():
        target_config.insert_fields[dto_field] = function_field

    for dto_field, relation in insert_output.relation_bindings.items():
        target_config.insert_relations[dto_field] = relation

    for dto_field, function_field in update_output.field_bindings.items():
        target_config.update_fields[dto_field] = function_field

    for dto_field, relation in update_output.relation_bindings.items():
        target_config.update_relations[dto_field] = relation

    return target_config
