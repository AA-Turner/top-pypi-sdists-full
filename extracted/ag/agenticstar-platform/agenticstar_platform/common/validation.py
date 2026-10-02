"""
AGENTICSTAR Platform SDK - Validation Utilities
識別子検証などの共通バリデーション機能
"""

import re
from typing import List


# SQL識別子の検証パターン（英数字、アンダースコア、ドットのみ許可）
_IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$')

# ORDER BY句の検証パターン（カラム名 + オプションのASC/DESC）
_ORDER_BY_PATTERN = re.compile(
    r'^[a-zA-Z_][a-zA-Z0-9_]*(\s+(ASC|DESC|asc|desc))?'
    r'(\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*(\s+(ASC|DESC|asc|desc))?)*$'
)


class IdentifierValidationError(Exception):
    """識別子検証エラー

    SQL Injection対策として不正な識別子が検出された場合に発生
    """

    def __init__(self, identifier: str, identifier_type: str = "identifier"):
        self.identifier = identifier
        self.identifier_type = identifier_type
        super().__init__(
            f"Invalid {identifier_type}: '{identifier}'. "
            f"Only alphanumeric characters, underscores, and dots are allowed."
        )


def validate_identifier(identifier: str, identifier_type: str = "identifier") -> str:
    """SQL識別子（テーブル名・カラム名）を検証

    Args:
        identifier: 検証する識別子
        identifier_type: エラーメッセージ用の識別子タイプ

    Returns:
        検証済みの識別子

    Raises:
        IdentifierValidationError: 不正な識別子の場合

    Example:
        safe_table = validate_identifier("users", "table")  # OK
        validate_identifier("users; DROP TABLE users;", "table")  # IdentifierValidationError
    """
    if not identifier or not _IDENTIFIER_PATTERN.match(identifier):
        raise IdentifierValidationError(identifier, identifier_type)
    return identifier


def validate_identifiers(identifiers: List[str], identifier_type: str = "column") -> List[str]:
    """複数のSQL識別子を検証

    Args:
        identifiers: 検証する識別子のリスト
        identifier_type: エラーメッセージ用の識別子タイプ

    Returns:
        検証済みの識別子リスト

    Raises:
        IdentifierValidationError: 不正な識別子が含まれる場合
    """
    return [validate_identifier(ident, identifier_type) for ident in identifiers]


def validate_order_by(order_by: str) -> str:
    """ORDER BY句を検証

    Args:
        order_by: ORDER BY句（例: "created_at DESC"）

    Returns:
        検証済みのORDER BY句

    Raises:
        IdentifierValidationError: 不正なORDER BY句の場合

    Example:
        validate_order_by("created_at DESC")  # OK
        validate_order_by("name ASC, id DESC")  # OK
        validate_order_by("name; DROP TABLE users;")  # IdentifierValidationError
    """
    if not order_by or not _ORDER_BY_PATTERN.match(order_by.strip()):
        raise IdentifierValidationError(order_by, "ORDER BY clause")
    return order_by
