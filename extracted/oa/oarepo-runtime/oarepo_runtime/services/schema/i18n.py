#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Marshmallow schema for multilingual strings."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import langcodes
import langcodes.tag_parser
from invenio_base.utils import obj_or_import_string
from invenio_i18n import gettext as _
from marshmallow import Schema, ValidationError, fields, pre_load, validates


@lru_cache
def get_i18n_schema(
    lang_name: str,
    value_name: str,
    value_field: str = "marshmallow_utils.fields.SanitizedHTML",
) -> type[Schema]:
    """Dynamically creates and returns I18n Schema class.

    Add custom serialization logic based on the provided `lang_name` and `value_name`.
    """

    class I18nMixin:
        @validates(lang_name)
        def validate_lang(self, value: str) -> None:
            try:
                if value != "_" and not langcodes.Language.get(value).is_valid():
                    raise ValidationError("Invalid language code")
            except langcodes.tag_parser.LanguageTagError as e:
                raise ValidationError("Invalid language code") from e

        @pre_load
        def pre_load_func(self, data: dict[str, Any], **_kwargs: Any) -> dict[str, Any]:
            errors = {}
            if not data.get(lang_name) or not data.get(value_name):
                errors[lang_name] = [_("Both language and text must be provided.")]
                errors[value_name] = [_("Both language and text must be provided.")]

                if errors:
                    raise ValidationError(errors)
            return data

    value_field_class = obj_or_import_string(value_field)
    if value_field_class is None:
        raise ValueError(  # pragma: no cover
            f"Invalid value field class provided: '{value_field}'. "
            "Expected a valid import string for a Marshmallow field class."
        )
    return type(
        f"I18nSchema_{lang_name}_{value_name}",
        (
            I18nMixin,
            Schema,
        ),
        {
            lang_name: fields.String(required=True),
            value_name: value_field_class(required=True),
        },
    )


def MultilingualField(  # noqa NOSONAR
    *args: Any,
    lang_name: str = "lang",
    value_name: str = "value",
    value_field: str = "marshmallow_utils.fields.SanitizedHTML",
    **kwargs: Any,
):
    # TODO: args are not used but oarepo-model-builder-multilingual generates them
    # should be fixed there and subsequently removed here
    _ = args
    return fields.List(
        fields.Nested(get_i18n_schema(lang_name, value_name, value_field)),
        **kwargs,
    )


def I18nStrField(  # noqa NOSONAR
    *args: Any,
    lang_name: str = "lang",
    value_name: str = "value",
    value_field: str = "marshmallow_utils.fields.SanitizedHTML",
    **kwargs: Any,
):
    return fields.Nested(
        get_i18n_schema(lang_name, value_name, value_field),
        *args,
        **kwargs,
    )
