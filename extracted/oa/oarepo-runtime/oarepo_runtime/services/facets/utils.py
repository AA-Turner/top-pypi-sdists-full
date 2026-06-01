#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Runtime utils for facets management."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from invenio_app.helpers import obj_or_import_string
from invenio_i18n import lazy_gettext as _

if TYPE_CHECKING:
    from collections.abc import Iterable


class I18nLabel:
    """Lazy multilingual label that resolves to the current locale at str() time."""

    def __init__(self, labels: dict[str, str]) -> None:
        """Initialize with a dict of locale -> label mappings."""
        self._labels = labels

    def __str__(self) -> str:
        """Resolve label for the current locale."""
        from flask_babel import get_locale

        babel_locale = get_locale()
        locale = babel_locale.language if babel_locale else "en"
        return self._labels.get(locale, self._labels.get("en", next(iter(self._labels.values()), "")))


def get_basic_facet(  # noqa: PLR0913
    facets: dict,
    facet_def: dict | None,
    facet_name: str,
    facet_path: str,
    content: list,
    facet_class: str,
    facet_kwargs: dict[str, Any] | None = None,
    label: dict[str, str] | str | None = None,
) -> dict[str, list]:
    """Get basic leaf facet definition."""
    if facet_def is not None:
        if isinstance(facet_def.get("label"), dict):
            facet_def = {**facet_def, "label": I18nLabel(facet_def["label"])}
        facets[facet_name] = [*content, {**(facet_kwargs or {}), **facet_def}]
    else:
        if label:
            resolved_label = I18nLabel(label) if isinstance(label, dict) else label
        else:
            resolved_label = _label_for_field(facet_name)

        facets[facet_name] = [
            *content,
            {
                "facet": facet_class,
                "field": facet_path,
                "label": resolved_label,
                **(facet_kwargs or {}),
            },
        ]
    return facets


def _label_for_field(field: str) -> Any:
    """Create label for facet based on field name."""
    base = field.removesuffix(".keyword")
    base = base.replace(".", "/")
    return _(
        f"{base}.label"  # noqa: INT001 # this is correct, we want to translate blah/abc.label
    )


def build_facet(specs: Iterable[dict[str, str | object]]) -> Any:
    """Build runtime facet definition."""
    items: list[dict[str, str | object]] = list(specs)

    leaf_facet_definition = items[-1]

    leaf_facet_cls = obj_or_import_string(leaf_facet_definition["facet"])
    if leaf_facet_cls is None:
        raise ValueError("Facet class can not be None.")
    params = {k: v for k, v in leaf_facet_definition.items() if k != "facet"}

    terms = leaf_facet_cls(**params)  # type: ignore[reportCallIssue]

    current = terms
    for entry in reversed(items[:-1]):
        nested_cls = obj_or_import_string(entry["facet"])
        if nested_cls is None:
            raise ValueError("Facet class can not be None.")
        params = {k: v for k, v in entry.items() if k != "facet"}

        current = nested_cls(**params, nested_facet=current, label=leaf_facet_definition.get("label", ""))  # type: ignore[reportCallIssue]

    return current
