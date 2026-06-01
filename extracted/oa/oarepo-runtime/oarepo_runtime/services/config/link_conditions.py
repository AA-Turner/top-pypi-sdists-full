#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Link conditions module."""

from __future__ import annotations

from abc import abstractmethod
from logging import getLogger
from typing import TYPE_CHECKING, Any

from invenio_pidstore.errors import PIDDoesNotExistError, PIDUnregistered
from invenio_records_resources.records.api import FileRecord

from oarepo_runtime.proxies import current_runtime
from oarepo_runtime.records.drafts import get_draft

if TYPE_CHECKING:
    from invenio_records.api import Record as RecordBase

log = getLogger(__name__)


class Condition:
    """Base class for defining conditions with callable logic."""

    @abstractmethod
    def __call__(self, obj: RecordBase, ctx: dict):
        """Abstract method to be implemented in subclasses to define a condition."""
        raise NotImplementedError  # pragma: no cover

    def __and__(self, other: Any):
        """Combine two conditions using a logical AND."""
        return type(
            "And",
            (Condition,),
            {"__call__": lambda _, obj, ctx: self(obj, ctx) and other(obj, ctx)},
        )()

    def __or__(self, other: Any):
        """Combine two conditions using a logical OR."""
        return type(
            "Or",
            (Condition,),
            {"__call__": lambda _, obj, ctx: self(obj, ctx) or other(obj, ctx)},
        )()

    def __invert__(self):
        """Negate the condition using a logical NOT."""
        return type(
            "Not",
            (Condition,),
            {"__call__": lambda _, obj, ctx: not self(obj, ctx)},
        )()


class has_permission(Condition):  # noqa: N801
    """A condition to check if a user has the specified permission for a given record."""

    def __init__(self, action_name: str):
        """Initialize the condition with the specified action name."""
        self.action_name = action_name

    def __call__(self, obj: RecordBase, ctx: dict):
        """Evaluate the condition by checking the permission for a given record."""
        if isinstance(obj, FileRecord):
            obj = obj.record
        service = current_runtime.get_record_service_for_record(obj)
        try:
            return service.check_permission(action_name=self.action_name, record=obj, **ctx)
        except Exception:  # pragma: no cover
            log.exception("Unexpected exception.")


class has_draft_permission(Condition):  # noqa: N801
    """A condition to check if a user has the specified permission for a draft record."""

    def __init__(self, action_name: str):
        """Initialize the condition with the specified action name."""
        self.action_name = action_name

    def __call__(self, obj: RecordBase, ctx: dict):
        """Valuates the condition by checking the permission for a draft record."""
        _ = ctx
        draft_record = get_draft(obj)
        if not draft_record:
            return False
        service = current_runtime.get_record_service_for_record(obj)
        try:
            return service.check_permission(action_name=self.action_name, record=draft_record, **ctx)
        except Exception:  # pragma: no cover
            log.exception("Unexpected exception.")
            return False


class has_draft(Condition):  # noqa: N801
    """Shortcut for links to determine if record is either a draft or a published one with a draft associated."""

    def __call__(self, obj: RecordBase, ctx: dict):
        """Check if the given record has draft."""
        _ = ctx
        return bool(getattr(obj, "is_draft", False)) or bool(getattr(obj, "has_draft", False))


class has_published_record(Condition):  # noqa: N801
    """Shortcut for links to determine if the given record has a published PID."""

    def __call__(self, obj: RecordBase, ctx: dict):
        """Check if the given record has a published PID."""
        _ = ctx
        service = current_runtime.get_record_service_for_record(obj)
        try:
            service.record_cls.pid.resolve(obj["id"])
        except PIDUnregistered, PIDDoesNotExistError:
            return False
        return True


class is_published_record(Condition):  # noqa: N801
    """Shortcut for links to determine if record is a published record."""

    def __call__(self, obj: RecordBase, ctx: dict):
        """Check if the given record is draft."""
        _ = ctx
        return not getattr(obj, "is_draft", False)


class is_draft(Condition):  # noqa: N801
    """Shortcut for links to determine if record is a draft."""

    def __call__(self, obj: RecordBase, ctx: dict):
        """Check if the given record is draft."""
        _ = ctx
        return getattr(obj, "is_draft", False)
