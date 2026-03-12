from __future__ import annotations

from typing import Any

from nsj_rest_lib2.compiler.edl_model.primitives import PrimitiveTypes, STR_BASED_TYPES


def parse_primitive_type(property_type: Any) -> PrimitiveTypes | None:
    """
    Converte valor de tipo para `PrimitiveTypes` quando aplicavel.

    Args:
        property_type: Valor bruto do campo `type`.

    Returns:
        Enum `PrimitiveTypes` quando reconhecido; caso contrario, None.
    """
    if isinstance(property_type, PrimitiveTypes):
        return property_type
    if not isinstance(property_type, str):
        return None
    normalized = property_type.strip().lower()
    if not normalized:
        return None
    try:
        return PrimitiveTypes(normalized)
    except Exception:
        return None


def is_primitive_property_type(property_type: Any) -> bool:
    """
    Indica se o tipo representa um primitivo canonico do EDL.

    Args:
        property_type: Valor do campo `type`.

    Returns:
        True quando `property_type` pertence a `PrimitiveTypes`.
    """
    return parse_primitive_type(property_type) is not None


def is_relation_property_type(property_type: Any) -> bool:
    """
    Indica se o tipo representa relacionamento (interno ou externo).

    Args:
        property_type: Valor do campo `type`.

    Returns:
        True para tipos de relacao (ex.: `escopo/recurso`, `#/components/...`).
    """
    if is_primitive_property_type(property_type):
        return False
    if not isinstance(property_type, str):
        return False
    normalized = property_type.strip()
    if not normalized:
        return False
    return "/" in normalized or normalized.startswith("#/")


def is_textual_primitive_type(property_type: Any) -> bool:
    """
    Indica se o tipo primitivo possui semantica textual.

    Args:
        property_type: Valor do campo `type`.

    Returns:
        True para tipos definidos em `STR_BASED_TYPES`.
    """
    primitive_type = parse_primitive_type(property_type)
    if primitive_type is None:
        return False
    return primitive_type in STR_BASED_TYPES


def resolve_effective_repository_column(
    prop_name: str,
    prop_meta: Any,
    repo_prop_meta: Any,
) -> str | None:
    """
    Resolve coluna fisica efetiva para uma propriedade de EDL.

    Args:
        prop_name: Nome logico da propriedade.
        prop_meta: Metadados da propriedade no schema.
        repo_prop_meta: Metadados em `repository.properties.<prop>`.

    Returns:
        Nome da coluna local quando aplicavel; None para relacoes sem coluna
        explicita.
    """
    if isinstance(repo_prop_meta, dict):
        column = repo_prop_meta.get("column")
    else:
        column = getattr(repo_prop_meta, "column", None)

    if column is not None and str(column).strip():
        return str(column).strip()

    if isinstance(prop_meta, dict):
        property_type = prop_meta.get("type")
    else:
        property_type = getattr(prop_meta, "type", None)

    if is_relation_property_type(property_type):
        return None

    return prop_name
