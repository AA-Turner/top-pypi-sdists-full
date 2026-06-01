#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see https://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Typed invenio generators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import chain
from typing import TYPE_CHECKING, Any, Literal, override

from invenio_access.models import ActionRoles, ActionUsers
from invenio_administration.generators import (
    Administration,
    administration_access_action,
)
from invenio_records_permissions.generators import (
    ConditionalGenerator as InvenioConditionalGenerator,
)
from invenio_records_permissions.generators import (
    Disable,
)
from invenio_records_permissions.generators import Generator as InvenioGenerator
from invenio_search.engine import dsl

if TYPE_CHECKING:
    from collections.abc import Collection, Sequence

    from flask_principal import Need
    from invenio_rdm_records.records.api import RDMRecord
    from invenio_records.api import Record


class Generator(InvenioGenerator):
    """Custom generator for the service.

    This class will be removed when invenio has proper type stubs.
    """

    @override
    def needs(self, **kwargs: Any) -> Collection[Need]:
        return super().needs(**kwargs)  # type: ignore[no-any-return] # mypy bug

    @override
    def excludes(self, **kwargs: Any) -> Collection[Need]:
        return super().excludes(**kwargs)  # type: ignore[no-any-return] # mypy bug

    @override
    def query_filter(self, **kwargs: Any) -> dsl.query.Query:
        return super().query_filter(**kwargs)  # type: ignore[no-any-return] # mypy bug


class ConditionalGenerator(InvenioConditionalGenerator, ABC):
    """Typed conditional generator.

    This class will be removed when invenio has proper type stubs.
    """

    def __init__(self, then_: Sequence[InvenioGenerator], else_: Sequence[InvenioGenerator]) -> None:
        """Initialize the conditional generator."""
        super().__init__(then_=then_, else_=else_)

    @abstractmethod
    def _condition(self, **kwargs: Any) -> bool:
        """Condition to choose generators set."""
        raise NotImplementedError  # pragma: no cover

    def _generators(self, record: Record | None = None, **kwargs: Any) -> Sequence[InvenioGenerator]:
        """Get the "then" or "else" generators."""
        return super()._generators(record=record, **kwargs)  # type: ignore[no-any-return]  # mypy bug ?

    @override
    def needs(self, record: Record | None = None, **kwargs: Any) -> Collection[Need]:
        return super().needs(record=record, **kwargs)  # type: ignore[no-any-return]  # mypy bug ?

    @override
    def excludes(self, record: Record | None = None, **kwargs: Any) -> Collection[Need]:
        return super().excludes(record=record, **kwargs)  # type: ignore[no-any-return]  # mypy bug ?

    @abstractmethod
    def _query_instate(self, **context: Any) -> dsl.query.Query:
        raise NotImplementedError  # pragma: no cover

    @override
    def query_filter(self, **context: Any) -> dsl.query.Query:
        """Apply then or else filter."""
        then_query = super()._make_query(self.then_, **context)
        else_query = super()._make_query(self.else_, **context)

        q_instate = self._query_instate(**context)
        q_outstate = ~q_instate

        if then_query and else_query:
            ret = (q_instate & then_query) | (q_outstate & else_query)
        elif then_query:
            ret = q_instate & then_query
        elif else_query:
            ret = q_outstate & else_query
        else:
            ret = dsl.Q("match_none")

        return ret


class AggregateGenerator(Generator, ABC):
    """Superclass for generators aggregating multiple generators."""

    @abstractmethod
    def _generators(self, **context: Any) -> Sequence[InvenioGenerator]:
        """Return the generators."""
        raise NotImplementedError  # pragma: no cover

    @override
    def needs(self, **context: Any) -> Collection[Need]:
        """Get the needs from the policy."""
        needs = [generator.needs(**context) for generator in self._generators(**context)]
        return list(chain.from_iterable(needs))

    @override
    def excludes(self, **context: Any) -> Collection[Need]:
        """Get the excludes from the policy."""
        excludes = [generator.excludes(**context) for generator in self._generators(**context)]
        return list(chain.from_iterable(excludes))

    @override
    def query_filter(self, **context: Any) -> dsl.query.Query:
        """Search filters."""
        ret = ConditionalGenerator._make_query(  # noqa: SLF001
            self._generators(**context), **context
        )
        if ret is None:
            return dsl.Q("match_none")
        return ret


class IfDraftType(ConditionalGenerator):
    """Match if record is a draft of specified type(s)."""

    def __init__(
        self,
        draft_types: (
            Literal["initial", "metadata", "new_version"] | list[Literal["initial", "metadata", "new_version"]]
        ),
        then_: (InvenioGenerator | list[InvenioGenerator] | tuple[InvenioGenerator] | None) = None,
        else_: (InvenioGenerator | list[InvenioGenerator] | tuple[InvenioGenerator] | None) = None,
    ):
        """Create the generator.

        :param draft_types: One or more of 'initial', 'metadata', 'new_version'.
        :param then_: Generators to use if condition matches.
        :param else_: Generators to use if condition does not match.
        """
        if not isinstance(draft_types, (list, tuple)):
            draft_types = [draft_types]
        self._draft_types = draft_types
        if not then_:
            then_ = [Disable()]
        if not else_:
            else_ = [Disable()]
        if not isinstance(then_, (list, tuple)):
            then_ = [then_]
        if not isinstance(else_, (list, tuple)):
            else_ = [else_]
        super().__init__(then_, else_)

    @override
    def _condition(self, record: RDMRecord | None = None, **kwargs: Any) -> bool:
        """Check if record is draft of specified type."""
        if not record:
            return False

        index = record.versions.index
        is_latest = record.versions.is_latest
        is_draft = record.is_draft

        if not is_draft:
            return False

        if index == 1 and not is_latest:
            draft_type = "initial"
        elif index > 1 and not is_latest:
            draft_type = "new_version"
        else:
            draft_type = "metadata"

        return draft_type in self._draft_types

    @override
    def _query_instate(self, **_context: Any) -> dsl.query.Query:
        queries = []
        if "initial" in self._draft_types:
            queries.append(dsl.Q("term", **{"versions.index": 1}) & dsl.Q("term", **{"metadata.is_latest_draft": True}))
        if "metadata" in self._draft_types:
            # unknown how the "edit_metadata" type of draft could be differentiated from new_version
            queries.append(dsl.Q("match_none"))
        if "new_version" in self._draft_types:
            # unknown how the "new_version" type of draft could be differentiated from edit_metadata
            queries.append(dsl.Q("match_none"))
        if not queries:
            # No recognized draft types; match no documents explicitly
            queries.append(dsl.Q("match_none"))
        return dsl.Q("bool", should=queries, minimum_should_match=1)


class ActionQueryFilterMixin:
    """Administration mixin that filters users based on action access."""

    access_action: Any

    def query_filter(self, **kwargs: Any) -> dsl.query.Query | list[dsl.query.Query] | None:
        """Return search filter that allows all in case user (or one of the roles the user belongs to) has access."""
        identity = kwargs["identity"]
        user_ids = [need.value for need in identity.provides if need.method == "id"]

        if user_ids:
            has_direct_access = ActionUsers.query.filter(
                ActionUsers.user_id == user_ids[0],
                ActionUsers.action == self.access_action.value,
                ActionUsers.exclude.is_(False),
            ).count()
            if has_direct_access:
                return dsl.query.MatchAll()

        user_roles = [need.value for need in identity.provides if need.method == "role"]
        if user_roles:
            has_access_through_roles = ActionRoles.query.filter(
                ActionRoles.role_id.in_(user_roles),
                ActionRoles.action == self.access_action.value,
                ActionRoles.exclude.is_(False),
            ).count()
            if has_access_through_roles:
                return dsl.query.MatchAll()

        # If no direct access or roles, return no match
        return dsl.query.MatchNone()


class AdministrationWithQueryFilter(ActionQueryFilterMixin, Administration):
    """Administration generator which matches people with administration-access permission."""

    access_action = administration_access_action
