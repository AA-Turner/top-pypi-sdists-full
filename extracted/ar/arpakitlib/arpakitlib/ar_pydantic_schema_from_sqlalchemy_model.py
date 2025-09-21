# arpakit
import datetime as dt
from typing import Any, Optional

from pydantic import BaseModel, Field
from sqlalchemy import inspect
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.sql.sqltypes import (
    Boolean, Integer, BigInteger, SmallInteger,
    String, Text, Unicode, UnicodeText,
    DateTime, Date, Time,
    Float, Numeric, DECIMAL, LargeBinary, JSON
)
_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_SQLA_TYPE_MAP = {
    Boolean: bool,
    Integer: int,
    BigInteger: int,
    SmallInteger: int,
    Float: float,
    Numeric: float,
    DECIMAL: float,
    String: str,
    Unicode: str,
    Text: str,
    UnicodeText: str,
    LargeBinary: bytes,
    JSON: dict,
    DateTime: dt.datetime,
    Date: dt.date,
    Time: dt.time,
}


def _python_type_from_col(col) -> type | str:
    try:
        return col.type.python_type
    except Exception:
        for sa_t, py_t in _SQLA_TYPE_MAP.items():
            if isinstance(col.type, sa_t):
                return py_t
        return Any


def pydantic_schema_from_sqlalchemy_model(
        sqlalchemy_model: type,
        *,
        name: str | None = None,
        base_model: type[BaseModel] = BaseModel,
        include_defaults: bool = False,
        exclude_column_names: list[str] | None = None,
) -> type[BaseModel]:
    """
    Генерирует Pydantic-модель только из колонок SQLAlchemy-модели.
    - include_defaults: добавлять ли default/server_default.
    - exclude_column_names: список имён колонок, которые нужно пропустить.
    """
    mapper = inspect(sqlalchemy_model).mapper
    model_name = name or f"{sqlalchemy_model.__name__}Schema"

    annotations: dict[str, Any] = {}
    attrs: dict[str, Any] = {}
    exclude_column_names = set(exclude_column_names or [])

    for prop in mapper.attrs:
        if not isinstance(prop, ColumnProperty):
            continue
        if prop.key in exclude_column_names:
            continue

        col = prop.columns[0]
        py_t = _python_type_from_col(col)

        # Аннотация типа
        if col.nullable:
            annotations[prop.key] = Optional[py_t]  # type: ignore[name-defined]
        else:
            annotations[prop.key] = py_t

        # Если нужно — добавляем дефолт
        if include_defaults:
            default_value = None
            if col.default is not None and col.default.is_scalar:
                default_value = col.default.arg
            elif col.server_default is not None and getattr(col.server_default.arg, "text", None):
                default_value = col.server_default.arg.text

            if default_value is not None:
                attrs[prop.key] = Field(default=default_value)

    attrs["__annotations__"] = annotations
    return type(model_name, (base_model,), attrs)
