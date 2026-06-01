#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Nested facets with label."""

from __future__ import annotations

from typing import Any, override

from invenio_search.engine import dsl


class NestedLabeledFacet(dsl.Facet):
    """Create nested facet with label."""

    agg_type = "nested"

    def __init__(self, path: str, nested_facet: Any, label: str = ""):
        """Initialize labeled nested facet."""
        self._path = path
        self._inner = nested_facet
        self._label = label
        super(NestedLabeledFacet, self).__init__(  # noqa UP008
            path=path,
            aggs={
                "inner": nested_facet.get_aggregation(),
            },
        )

    def get_values(self, data: Any, filter_values: list) -> Any:
        """Extract facet values from the inner facet."""
        return self._inner.get_values(data.inner, filter_values)  # type: ignore[attr-defined]

    @override
    def add_filter(self, filter_values: list) -> dsl.Nested | None:  # type: ignore[override, reportIncompatibleMethodOverride]
        """Build nested query filter for facet."""
        inner_q = self._inner.add_filter(filter_values)
        if inner_q:
            return dsl.Nested(path=self._path, query=inner_q)
        return None

    def get_labelled_values(self, data: dict, filter_values: list) -> dict:
        """Get a labelled version of a bucket."""
        _ = filter_values
        try:
            out = data["buckets"]
        except KeyError:
            out = []
        return {"buckets": out, "label": str(self._label)}
