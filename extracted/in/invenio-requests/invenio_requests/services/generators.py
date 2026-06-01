# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request permissions."""

import operator
from functools import reduce
from itertools import chain

from flask import current_app
from invenio_records_permissions.generators import ConditionalGenerator, Generator
from invenio_records_resources.references import EntityGrant
from invenio_search.engine import dsl

from invenio_requests.customizations.event_types import LogEventType
from invenio_requests.proxies import current_requests


class Status(Generator):
    """Generator to validate needs only for a given request status."""

    def __init__(self, statuses, generators):
        """Initialize need entity generator."""
        self._statuses = statuses
        self._generators = generators or []

    def needs(self, request=None, **kwargs):
        """Needs if status is in one of the provided ones."""
        if request.status in self._statuses:
            needs = [g.needs(request=request, **kwargs) for g in self._generators]
            return set(chain.from_iterable(needs))
        return []

    def query_filter(self, **kwargs):
        """Query filters for the current identity."""
        queries = [g.query_filter(**kwargs) for g in self._generators]
        queries = [q for q in queries if q]
        queries = reduce(operator.or_, queries) if queries else None

        if queries:
            return dsl.Q("terms", **{"status": self._statuses}) & queries
        return None


class EntityNeedsGenerator(Generator):
    """Allows the creator of the request."""

    entity_field = None
    grants_field = "grants"

    def __init__(self):
        """Initialize need entity generator."""
        assert self.entity_field is not None, "Subclass must define entity_field."

    def needs(self, request=None, **kwargs):
        """Needs for the given entity reference."""
        entity = getattr(request, self.entity_field)
        return request.type.entity_needs(entity)

    def query_filter(self, identity=None, **kwargs):
        """Query filters for the current identity."""
        grants = []
        for need in identity.provides:
            grants.append(EntityGrant(self.entity_field, need).token)
        if grants:
            return dsl.Q("terms", **{self.grants_field: grants})
        return None


class Creator(EntityNeedsGenerator):
    """Allows the creator of the request."""

    entity_field = "created_by"


class Receiver(EntityNeedsGenerator):
    """Allows the receiver of the request."""

    entity_field = "receiver"


class Topic(EntityNeedsGenerator):
    """Allows access control based on the request's topic.

    This generator grants permissions to users/entities associated with the topic
    of a request. The specific needs depend on whether the request type supports
    `resolve_topic_needs`.
    """

    entity_field = "topic"

    def needs(self, request=None, **kwargs):
        """Determine the access needs for the given request topic.

        If the request type defines `resolve_topic_needs`, it means the topic's
        permissions should be resolved dynamically based on the entity associated
        with it (e.g., a record, community, or another object).

        Otherwise, the topic is not involved in access control, and no additional
        permissions are granted.
        """
        entity = getattr(request, self.entity_field)

        if getattr(request.type, "resolve_topic_needs"):
            return request.type.entity_needs(entity)

        return []

    def query_filter(self, identity=None, **kwargs):
        """Construct a query filter to include only requests where the topic grants access.

        This filter ensures that only request types that support `resolve_topic_needs`
        contribute to permissions. Request types that do not define this attribute
        are explicitly excluded.

        Excluding request types without `resolve_topic_needs` prevents them from
        granting unintended access based on their topic, as they may not have
        the necessary logic to determine entity-specific permissions.
        """
        # Exclude request types that do NOT define `resolve_topic_needs`
        excluded_request_types = [
            ~dsl.Q("term", **{"type": _type.type_id})
            for _type in current_requests.request_type_registry
            if not getattr(_type, "resolve_topic_needs")
        ]

        # Generate grant tokens based on the user's identity
        grant_tokens = [
            EntityGrant(self.entity_field, need).token for need in identity.provides
        ]

        # If the user has no grant tokens, there is no need to proceed
        if not grant_tokens:
            return None

        # Build the final query
        query = dsl.Q(
            "bool",
            must=[
                dsl.Q("terms", **{self.grants_field: grant_tokens}),
                dsl.Q("bool", must=excluded_request_types),
            ],
        )

        return query


class Reviewers(EntityNeedsGenerator):
    """Allows the reviewer of the request."""

    entity_field = "reviewers"

    def _reviewers_enabled(self):
        """Check if reviewers are enabled."""
        return current_app.config.get("REQUESTS_REVIEWERS_ENABLED", False)

    def needs(self, request=None, **kwargs):
        """Needs for the given entity reference."""
        if not self._reviewers_enabled():
            return []

        entities = getattr(request, self.entity_field)
        _needs = []
        for entity in entities:
            _needs.extend(request.type.entity_needs(entity))
        return _needs

    def query_filter(self, identity=None, **kwargs):
        """Query filters for the current identity."""
        if not self._reviewers_enabled():
            return None

        grants = []
        for need in identity.provides:
            grants.append(EntityGrant(self.entity_field, need).token)
        if grants:
            return dsl.Q("terms", **{self.grants_field: grants})
        return None


class Commenter(Generator):
    """The user who created a specific comment."""

    def needs(self, event=None, request=None, **kwargs):
        """Enabling Needs."""
        if event.created_by is not None:
            return event.created_by.get_needs()
        return []

    def query_filter(self, identity=None, **kwargs):
        """Filters for current identity as creator."""
        raise RuntimeError("The generator cannot be used for searching.")


class IfLocked(ConditionalGenerator):
    """Disallows the action if the request is locked."""

    def _condition(self, request=None, **kwargs):
        """Condition to choose generators set."""
        return request is not None and request.get("is_locked", False)
