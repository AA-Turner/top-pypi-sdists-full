# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Search parameter interpreters for requests."""

from functools import partial

from invenio_records_resources.references import EntityGrant
from invenio_records_resources.services.records.params import (
    FilterParam,
    ParamInterpreter,
)
from invenio_search.engine import dsl

from ...resolvers.registry import ResolverRegistry


class ReferenceFilterParam(FilterParam):
    """Filter for reference dictionaries."""

    def __init__(self, param_name, field_name, config):
        """Constructor."""
        super().__init__(param_name, field_name, config)
        self._match_cache = {}

    def _is_valid(self, ref_type, ref_id):
        """Check if the reference dict is potentially resolvable."""
        if ref_type in self._match_cache:
            return self._match_cache[ref_type]

        # check if there's any resolver registered for the dict
        is_valid = any(
            (
                res.matches_reference_dict({ref_type: ref_id})
                for res in ResolverRegistry().get_registered_resolvers()
            )
        )
        self._match_cache[ref_type] = is_valid
        return is_valid

    def apply(self, identity, search, params):
        """Apply filter for a potentially resolvable reference dict."""
        if self.param_name not in params:
            return search

        ref_dict = params.pop(self.param_name, None)
        ref_type, ref_id = list(ref_dict.items())[0]

        # only apply the filter if it is potentially resolvable
        if self._is_valid(ref_type, ref_id):
            field_name = f"{self.field_name}.{ref_type}"
            if isinstance(ref_id, str):
                search = search.filter("term", **{field_name: ref_id})
            else:
                search = search.filter("terms", **{field_name: ref_id})

        return search


class IsOpenParam(ParamInterpreter):
    """Evaluates the 'is_open' parameter."""

    def __init__(self, field_name, config):
        """Construct."""
        self.field_name = field_name
        super().__init__(config)

    @classmethod
    def factory(cls, field):
        """Create a new filter parameter."""
        return partial(cls, field)

    def apply(self, identity, search, params):
        """Evaluate the is_open parameter on the search."""
        if params.get("is_open") is True:
            search = search.filter("term", **{self.field_name: True})
        elif params.get("is_open") is False:
            search = search.filter("term", **{self.field_name: False})
        return search


class SharedOrMyRequestsParam(ParamInterpreter):
    """Evaluates the 'shared_with_me' parameter for requests."""

    def _generate_my_requests_query(self, identity):
        """Generate the query for my requests.

        The query will return requests created by the user or requests where the user is the receiver.
        """
        created_by = "created_by.user"
        receiver = "receiver.user"
        return dsl.Q(
            "bool",
            should=[
                dsl.Q("term", **{created_by: identity.id}),
                dsl.Q("term", **{receiver: identity.id}),
            ],
        )

    def _generate_shared_with_me_query(self, identity):
        """Generate the query for shared_with_me.

        The query will return requests shared with the user via the topic grants (only via user or group).
        """
        allowed_need_methods = {"id", "role"}
        topic_grants = [
            EntityGrant("topic", need).token
            for need in identity.provides
            if need.method in allowed_need_methods
        ]
        reviewer_grants = [
            EntityGrant("reviewers", need).token
            for need in identity.provides
            if need.method in allowed_need_methods
        ]
        my_requests_query = self._generate_my_requests_query(identity)
        # Topic grants include requests created by the user or the user is the receiver,
        # so we need to exclude them
        return (
            dsl.Q("terms", **{"grants": topic_grants + reviewer_grants})
            & ~my_requests_query
        )

    def apply(self, identity, search, params):
        """Evaluate the shared_with_me parameter on the search.

        If shared_with_me is True, the search will return requests shared with the user via the topic grants (only via user or group).
        If shared_with_me is False, the search will return requests created by the user or requests where the user is the receiver.
        """
        if params.get("shared_with_me") is True:
            # Shared with me
            shared_with_me_query = self._generate_shared_with_me_query(identity)
            search = search.filter(shared_with_me_query)
        else:
            # My requests
            my_requests_query = self._generate_my_requests_query(identity)
            search = search.filter(my_requests_query)

        return search
