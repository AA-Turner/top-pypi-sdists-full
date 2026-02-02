from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class FunctionRelationBinding:
    """
    Representa o vínculo entre um campo do DTO e um campo declarado
    no FunctionType correspondente.
    """

    field_name: str
    function_type_class: Optional[str] = None


@dataclass
class FunctionBindingConfig:
    """
    Estrutura usada pelo PropertyCompiler para aplicar metadados de
    binding entre DTOs e FunctionTypes (insert/update).
    """

    insert_fields: Dict[str, str] = field(default_factory=dict)
    update_fields: Dict[str, str] = field(default_factory=dict)
    insert_relations: Dict[str, FunctionRelationBinding] = field(
        default_factory=dict
    )
    update_relations: Dict[str, FunctionRelationBinding] = field(
        default_factory=dict
    )

    def merge_insert_field(self, dto_field: str, function_field: str) -> None:
        if not dto_field or not function_field:
            return
        self.insert_fields[dto_field] = function_field

    def merge_update_field(self, dto_field: str, function_field: str) -> None:
        if not dto_field or not function_field:
            return
        self.update_fields[dto_field] = function_field

    def merge_insert_relation(
        self, dto_field: str, binding: FunctionRelationBinding
    ) -> None:
        if not dto_field or not binding:
            return
        self.insert_relations[dto_field] = binding

    def merge_update_relation(
        self, dto_field: str, binding: FunctionRelationBinding
    ) -> None:
        if not dto_field or not binding:
            return
        self.update_relations[dto_field] = binding


@dataclass
class FunctionCompilationOutput:
    """
    Resultado da compilação de um FunctionType (insert/update).
    """

    class_name: Optional[str] = None
    code: Optional[str] = None
    function_name: Optional[str] = None
    field_bindings: Dict[str, str] = field(default_factory=dict)
    relation_bindings: Dict[str, FunctionRelationBinding] = field(
        default_factory=dict
    )
