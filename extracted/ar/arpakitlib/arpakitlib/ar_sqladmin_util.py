from __future__ import annotations

from sqladmin import ModelView


def get_string_info_from_model_view(class_: type[ModelView]):
    res = f"Model Views: {len(class_.__subclasses__())}"
    for i, cls in enumerate(class_.__subclasses__()):
        res += f"\n{i + 1}. {cls.__name__}"
    return res
