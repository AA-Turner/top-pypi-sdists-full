#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Functionality for handling multilingual UI schemas using Marshmallow.

It includes dynamic schema generation based on
the provided language and value names, as well as specialized fields for
working with multilingual data and localized user interfaces.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from invenio_base.utils import obj_or_import_string
from marshmallow import Schema, fields


@lru_cache
def get_i18n_ui_schema(
    lang_name: str,
    value_name: str,
    value_field: str = "marshmallow_utils.fields.SanitizedHTML",
) -> type[Schema]:
    """Dynamically creates and returns I18n Schema class.

    Add custom serialization logic based on the provided `lang_name` and `value_name`.
    """
    value_field_class = obj_or_import_string(value_field)
    if value_field_class is None:
        raise ValueError(
            f"Invalid value field class provided: '{value_field}'. "
            "Expected a valid import string for a Marshmallow field class."
        )
    return type(
        f"I18nUISchema_{lang_name}_{value_name}",
        (Schema,),
        {
            lang_name: fields.String(required=True),
            value_name: value_field_class(required=True),
        },
    )


def MultilingualUIField(  # noqa NOSONAR
    *args: Any,
    lang_name: str = "lang",
    value_name: str = "value",
    value_field: str = "marshmallow_utils.fields.SanitizedHTML",
    **kwargs: Any,
):
    _ = args
    return fields.List(
        fields.Nested(get_i18n_ui_schema(lang_name, value_name, value_field)),
        **kwargs,
    )


def I18nStrUIField(  # noqa NOSONAR
    *args: Any,
    lang_name: str = "lang",
    value_name: str = "value",
    value_field: str = "marshmallow_utils.fields.SanitizedHTML",
    **kwargs: Any,
) -> fields.Field:
    return fields.Nested(
        get_i18n_ui_schema(lang_name, value_name, value_field),
        *args,
        **kwargs,
    )


@lru_cache
def get_i18n_localized_ui_schema(lang_name: str, value_name: str) -> type[Schema]:
    """Dynamically creates and returns Localized I18n Schema class.

    Add custom serialization logic based on the provided `lang_name` and `value_name`.
    """

    class I18nLocalizedUISchema(Schema):
        def _serialize(self, obj: Any, *, many: bool | None = None) -> Any:
            _ = many
            if not obj:
                return None
            language = self.context["locale"].language
            for v in obj:
                if language == v[lang_name]:
                    return v[value_name]
            return next(iter(obj))[value_name]

    # inherit to get a nice name for debugging
    return type(
        f"I18nLocalizedUISchema_{lang_name}_{value_name}",
        (I18nLocalizedUISchema,),
        {},
    )


def MultilingualLocalizedUIField(  # noqa NOSONAR
    *args: Any, lang_name: str = "lang", value_name: str = "value", **kwargs: Any
) -> fields.Field:
    return fields.Nested(get_i18n_localized_ui_schema(lang_name, value_name), *args, **kwargs)


def I18nStrLocalizedUIField(  # noqa NOSONAR
    *args: Any, lang_name: str = "lang", value_name: str = "value", **kwargs: Any
) -> fields.Field:
    _ = args
    return fields.Nested(
        get_i18n_ui_schema(lang_name, value_name),
        **kwargs,
    )
