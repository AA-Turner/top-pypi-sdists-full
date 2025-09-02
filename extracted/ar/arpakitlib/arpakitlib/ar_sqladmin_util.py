from __future__ import annotations

from typing import Any

from sqladmin import ModelView
from sqlalchemy.orm.attributes import InstrumentedAttribute


def get_string_info_from_model_view(class_: type[ModelView]):
    lines = [f"ModelViews: {len(class_.__subclasses__())}"]
    for i, cls in enumerate(class_.__subclasses__()):
        if hasattr(cls, "__name__"):
            lines.append(f"{i + 1}. ModelView: {cls.__name__}, (columns={len(cls.column_list)})")
            for v in cls.column_list:
                v: str | InstrumentedAttribute | Any
                if isinstance(v, str):
                    lines.append(f"   - {v}")
                elif isinstance(v, InstrumentedAttribute):
                    lines.append(f"   - {v}")
                else:
                    raise TypeError(f"unknown type, {type(v)=}")

    return "\n".join(lines)
