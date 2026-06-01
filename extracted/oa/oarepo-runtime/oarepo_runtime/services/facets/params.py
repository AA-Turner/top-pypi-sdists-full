#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Facet params."""

from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, Any, cast

from flask import current_app
from invenio_access.permissions import system_user_id
from invenio_app.helpers import obj_or_import_string
from invenio_records_resources.services.records.facets import FacetsResponse
from invenio_records_resources.services.records.params import FacetsParam

if TYPE_CHECKING:
    from collections.abc import Callable

    from flask_principal import Identity
    from invenio_records_resources.services.records.config import SearchOptions
    from invenio_records_resources.services.records.facets.facets import TermsFacet
    from invenio_search.api import RecordsSearchV2


log = logging.getLogger(__name__)


class GroupedFacetsParam(FacetsParam):
    """Facet parameter class that supports grouping of facets."""

    def __init__(self, config: type[SearchOptions]):
        """Initialize the facets parameter with the given config."""
        super().__init__(config)
        self._facets = {**config.facets}

    @property
    def facets(self) -> dict[str, TermsFacet]:
        """Return the facets dictionary."""
        return self._facets

    def identity_facet_groups(self, identity: Identity) -> list[str]:
        """Return the facet groups for the given identity."""
        if "OAREPO_FACET_GROUP_NAME" in current_app.config:
            find_facet_groups_func = cast(
                "Callable[[Identity, type[SearchOptions], Any], list[str]]",
                obj_or_import_string(current_app.config["OAREPO_FACET_GROUP_NAME"]),
            )
            return find_facet_groups_func(identity, self.config, None)

        if hasattr(identity, "provides"):
            return [need.value for need in identity.provides if need.method == "role"]

        return []

    @property
    def facet_groups(self) -> dict[str, Any] | None:
        """Return facet groups."""
        groups = getattr(self.config, "facet_groups", None)
        if groups is None:
            return None

        facets = getattr(self.config, "facets", {})
        return {group: {name: facets[name] for name in names} for group, names in groups.items()}

    def identity_facets(self, identity: Identity) -> dict[str, TermsFacet]:
        """Return the facets for the given identity."""
        if not self.facet_groups:
            return self.facets

        has_system_user_id = identity.id == system_user_id
        has_system_process_need = any(need.method == "system_process" for need in identity.provides)
        if has_system_user_id or has_system_process_need:
            return self.facets

        return self._filter_user_facets(identity)

    def aggregate_with_user_facets(
        self, search: RecordsSearchV2, user_facets: dict[str, TermsFacet]
    ) -> RecordsSearchV2:
        """Add aggregations representing the user facets."""
        for name, facet in user_facets.items():
            agg = facet.get_aggregation()
            search.aggs.bucket(name, agg)

        return search

    def filter(self, search: RecordsSearchV2) -> RecordsSearchV2:
        """Apply a post filter on the search."""
        if not self._filters:
            return search

        filters = list(self._filters.values())

        _filter = filters[0]
        for f in filters[1:]:
            _filter &= f

        return search.filter(_filter).post_filter(_filter)

    def apply(self, identity: Identity, search: RecordsSearchV2, params: dict) -> RecordsSearchV2:
        """Evaluate the facets on the search."""
        facets_values = params.pop("facets", {})
        for name, values in facets_values.items():
            if name in self.facets:
                self.add_filter(name, values)

        user_facets = self.identity_facets(identity)
        self_copy = copy.copy(self)
        self_copy._facets = user_facets  # noqa: SLF001 - TODO: this looks like a hack
        search = search.response_class(FacetsResponse.create_response_cls(self_copy))

        search = self.aggregate_with_user_facets(search, user_facets)
        search = self.filter(search)

        params.update(self.selected_values)

        return search

    def _filter_user_facets(self, identity: Identity) -> dict[str, TermsFacet]:
        """Filter user facets based on the identity."""
        user_facets = {}
        if not self.facet_groups:
            user_facets.update(self.facets)  # pragma: no cover
        else:
            self.facets.clear()  # TODO: why is this needed?
            user_facets.update(self.facet_groups.get("default", {}))

        groups = self.identity_facet_groups(identity)
        for group in groups:
            user_facets.update((self.facet_groups or {}).get(group, {}))
        return user_facets
