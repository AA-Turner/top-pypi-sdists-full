"""Mixin models for corvic orm tables."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import datetime, timezone
from typing import Any, cast

import sqlalchemy as sa
from google.protobuf import timestamp_pb2
from sqlalchemy import event, exc
from sqlalchemy import orm as sa_orm
from sqlalchemy.ext.hybrid import hybrid_property
from typing_extensions import LiteralString

import corvic.context
from corvic.orm.base import EventBase, EventKey, OrgBase
from corvic.orm.errors import (
    DeletedObjectError,
    RequestedObjectsForNobodyError,
)
from corvic.orm.func import gen_uuid
from corvic.orm.ids import OrgID
from corvic.result import InvalidArgumentError
from corvic_generated.status.v1 import event_pb2


def _filter_org_objects(orm_execute_state: sa_orm.ORMExecuteState):
    if all(
        not issubclass(mapper.class_, BelongsToOrgMixin | OrgBase)
        for mapper in orm_execute_state.all_mappers
    ):
        # operation has nothing to do with models owned by org
        return
    if orm_execute_state.is_select:
        requester = corvic.context.get_requester()
        org_id = OrgID(requester.org_id)
        if org_id.is_super_user:
            return

        if org_id.is_nobody:
            raise RequestedObjectsForNobodyError(
                "requester org from context was nobody"
            )
        # we need the real value in in expression world and
        # because of sqlalchemys weird runtime parsing of this it
        # needs to be a real local with a name
        db_id = org_id.to_db().unwrap_or_raise()

        # this goofy syntax doesn't typecheck well, but is the documented way to apply
        # these operations to all subclasses (recursive). Sqlalchemy is inspecting the
        # lambda rather than just executing it so a function won't work.
        # https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria
        check_org_id_lambda: Callable[  # noqa: E731
            [type[BelongsToOrgMixin]], sa.ColumnElement[bool]
        ] = lambda cls: cls.org_id == db_id
        orm_execute_state.statement = orm_execute_state.statement.options(
            sa_orm.with_loader_criteria(
                BelongsToOrgMixin,
                cast(Any, check_org_id_lambda),
                include_aliases=True,
                track_closure_variables=False,
            ),
            sa_orm.with_loader_criteria(
                OrgBase,
                OrgBase.id == org_id,
                include_aliases=True,
                track_closure_variables=False,
            ),
        )


class BadDeleteError(DeletedObjectError):
    """Raised when deleting deleted objects."""

    def __init__(self):
        super().__init__(message="deleting an object that is already deleted")


def _filter_deleted_objects_when_orm_loading(
    execute_state: sa_orm.session.ORMExecuteState,
):
    # check if the orm operation was submitted with an option to force load despite
    # soft-load status and if so just skip this event
    if any(
        isinstance(opt, SoftDeleteMixin.ForceLoadOption)
        for opt in execute_state.user_defined_options
    ) or any(
        isinstance(opt, SoftDeleteMixin.ForceLoadOption)
        for opt in execute_state.local_execution_options.values()
    ):
        return

    def where_criteria(cls: type[SoftDeleteMixin]) -> sa.ColumnElement[bool]:
        return ~cls.is_deleted

    execute_state.statement = execute_state.statement.options(
        sa_orm.with_loader_criteria(
            entity_or_base=SoftDeleteMixin,
            # suppressing pyright is unfortunately required as there seems to be a
            # problem with sqlalchemy.orm.util::LoaderCriteriaOption which will
            # construct a 'DeferredLambdaElement' when `where_criteria` is callable.
            # However, the type annotations are not consistent with the implementation.
            # The implementation, on callables criteria, passes to the lambda the
            # mapping class for using in constructing the `ColumnElement[bool]` result
            # needed. For this reason we ignore the argument type.
            where_criteria=where_criteria,
            include_aliases=True,
        )
    )


class SoftDeleteMixin(sa_orm.MappedAsDataclass):
    """Mixin to make corvic orm models use soft-delete.

    Modifications to objects which are marked as deleted will result in
    an error.
    """

    class ForceLoadOption(sa_orm.UserDefinedOption):
        """Option for ignoring soft delete status when loading."""

    deleted_at: sa_orm.Mapped[datetime | None] = sa_orm.mapped_column(
        sa.DateTime(timezone=True),
        server_default=None,
        default=None,
    )
    is_live: sa_orm.Mapped[bool | None] = sa_orm.mapped_column(
        init=False,
        default=True,
    )

    @classmethod
    def _force_load_option(cls):
        return cls.ForceLoadOption()

    @classmethod
    def force_load_options(cls):
        """Options to force load soft-deleted objects when using session.get."""
        return [cls._force_load_option()]

    @classmethod
    def force_load_execution_options(cls):
        """Options to force load soft-deleted objects when using session.execute.

        Also works with session.scalars.
        """
        return {"ignored_option_name": cls._force_load_option()}

    def mark_deleted(self):
        """Updates soft-delete object.

        Note: users should not use this directly and instead should use
        `session.delete(obj)`.
        """
        if self.is_deleted:
            raise BadDeleteError()
        # set is_live to None instead of False so that orm objects can use it to
        # build uniqueness constraints that are only enforced on non-deleted objects
        self.is_live = None
        self.deleted_at = datetime.now(tz=timezone.utc)

    @hybrid_property
    def is_deleted(self) -> bool:
        """Useful when constructing queries for direct use (e.g via `session.execute`).

        ORM users can rely on the typical session interfaces for checking object
        persistence.
        """
        return not self.is_live

    @is_deleted.inplace.expression
    @classmethod
    def _is_deleted_expression(cls):
        return cls.is_live.is_not(True)

    @staticmethod
    def register_session_event_listeners(session: type[sa_orm.Session]):
        event.listen(
            session, "do_orm_execute", _filter_deleted_objects_when_orm_loading
        )


def live_unique_constraint(
    column_name: LiteralString, *other_column_names: LiteralString
) -> sa.UniqueConstraint:
    """Construct a unique constraint that only applies to live objects.

    Live objects are those that support soft deletion and have not been soft deleted.
    """
    return sa.UniqueConstraint(column_name, *other_column_names, "is_live")


class BelongsToOrgMixin(sa_orm.MappedAsDataclass):
    """Mark models that should be subject to org level access control."""

    @staticmethod
    def _current_org_id_from_context():
        requester = corvic.context.get_requester()
        return OrgID(requester.org_id)

    @staticmethod
    def _make_org_id_default() -> OrgID | None:
        org_id = BelongsToOrgMixin._current_org_id_from_context()

        if org_id.is_nobody:
            raise RequestedObjectsForNobodyError(
                "the nobody org cannot change orm objects"
            )

        if org_id.is_super_user:
            return None

        return org_id

    org_id: sa_orm.Mapped[OrgID | None] = sa_orm.mapped_column(
        OrgBase.foreign_key().make(ondelete="CASCADE"),
        nullable=False,
        default_factory=_make_org_id_default,
        init=False,
    )

    @sa_orm.validates("org_id")
    def validate_org_id(self, _key: str, orm_id: OrgID | None):
        expected_org_id = self._current_org_id_from_context()
        if expected_org_id.is_nobody:
            raise RequestedObjectsForNobodyError(
                "the nobody org cannot change orm objects"
            )

        if expected_org_id.is_super_user:
            return orm_id

        if orm_id != expected_org_id:
            raise InvalidArgumentError(
                "provided org_id must match the current org",
                provided=orm_id,
                expected=expected_org_id,
            )

        return orm_id

    @staticmethod
    def register_session_event_listeners(session: type[sa_orm.Session]):
        event.listen(session, "do_orm_execute", _filter_org_objects)


class Session(sa_orm.Session):
    """Wrapper around sqlalchemy.orm.Session."""

    _soft_deleted: dict[sa_orm.InstanceState[Any], Any] | None = None

    def _track_soft_deleted(self, instance: object):
        if self._soft_deleted is None:
            self._soft_deleted = {}
        self._soft_deleted[sa_orm.attributes.instance_state(instance)] = instance

    def _reset_soft_deleted(self):
        self._soft_deleted = {}

    def _ensure_persistence(self, instance: object):
        instance_state = sa_orm.attributes.instance_state(instance)
        if instance_state.key is None:
            raise exc.InvalidRequestError("Instance is not persisted")

    def _delete_soft_deleted(self, instance: SoftDeleteMixin):
        self._ensure_persistence(instance)

        instance.mark_deleted()

        # Soft deleted should be tracked so that way a deleted soft-delete instance is
        # correctly identified as being "deleted"
        self._track_soft_deleted(instance)

        # Flushing the objects being deleted is needed to ensure the 'soft-delete'
        # impact is spread. This is because sqlalchemy flush implementation is doing
        # the heavy lifting of updating deleted/modified state across dependencies
        # after flushing. Ensuring this is done necessary to ensure relationships with
        # cascades have valid state after a soft-delete. Otherwise divergence between
        # hard-delete and soft-delete will be seen here (and surprise the user).
        # Note: the cost is reduced by limiting the flush to the soft-delete instance.
        self.flush([instance])

        # Invalidate existing session references for expected get-after-delete behavior.
        if sa_orm.attributes.instance_state(instance).session_id is self.hash_key:
            self.expunge(instance)

    def commit(self):
        super().commit()
        if self._soft_deleted:
            self._reset_soft_deleted()

    def rollback(self):
        super().rollback()
        if self._soft_deleted:
            for obj in self._soft_deleted.values():
                if isinstance(obj, SoftDeleteMixin):
                    obj.deleted_at = None
                    obj.is_live = True
                    continue
                raise RuntimeError("non-soft delete object in soft deleted set")
            self._reset_soft_deleted()

    @property
    def deleted(self):
        deleted = super().deleted
        if self._soft_deleted:
            deleted.update(self._soft_deleted.values())
        return deleted

    def delete(self, instance: object, *, force_hard_delete=False):
        if isinstance(instance, SoftDeleteMixin) and not force_hard_delete:
            self._delete_soft_deleted(instance)
            return
        super().delete(instance)

    def recent_object_events(
        self,
        key_provider: EventKey.Provider,
        max_events: int | None = None,
    ) -> list[event_pb2.Event]:
        """Returns max_events (default=10) most recent events from the event log."""
        recent_events: Sequence[EventBase] = self.scalars(
            EventBase.select_latest_by_event_key(
                event_key=key_provider.event_key, limit=max_events or None
            )
        ).all()
        return [ev.as_event() for ev in recent_events]


def _timestamp_or_utc_now(timestamp: datetime | None = None):
    if timestamp is not None:
        return timestamp
    return datetime.now(tz=timezone.utc)


class EventLoggerMixin(sa_orm.MappedAsDataclass):
    """Mixin to add status event logging features to corvic orm models.

    This mixin will add a `log_src_id` uuid value to the ORM model. This value is set
    by the DB on initial object persistence. ORM users can then use `orm.log_X` method
    to add a status event to the corvic event log which will be associated with the
    `log_src_id` value for the object. Supported events include done, error,
    pending_system, and pending_user. The `latest_event` property can be used to read
    the latest event for the orm object from the event log.
    """

    def _get_latest_event(self, _: Any = None) -> event_pb2.Event:
        obj_session = sa_orm.object_session(self)
        if obj_session:
            query = EventBase.select_latest_by_event_key(
                event_key=self.event_key, limit=1
            )
            last_log_entry = obj_session.scalars(query).first()
            if last_log_entry is not None:
                timestamp = timestamp_pb2.Timestamp()
                timestamp.FromDatetime(dt=last_log_entry.timestamp)
                return event_pb2.Event(
                    timestamp=timestamp,
                    reason=last_log_entry.reason,
                    event_type=event_pb2.EventType.Name(last_log_entry.event),
                    regarding=last_log_entry.regarding,
                )
        return event_pb2.Event()

    def _set_latest_event(self, event: event_pb2.Event, _: Any = None):
        if event.SerializeToString():  # initially the event is b''
            obj_session = sa_orm.object_session(self)

            if obj_session is not None:
                # this can occur when an event is set on a new object
                if not self._event_src_id:
                    obj_session.flush()
                from datetime import timezone

                obj_session.add(
                    EventBase(
                        event=event.event_type,
                        timestamp=event.timestamp.ToDatetime(tzinfo=timezone.utc),
                        regarding=event.regarding,
                        reason=event.reason,
                        event_key=str(self.event_key),
                    )
                )
            else:
                raise sa_orm.exc.UnmappedInstanceError(
                    self, msg="cannot add event to unmapped instance"
                )

    @sa_orm.declared_attr
    def _latest_event(self):
        """Get or set the latest event for this orm object."""
        return sa_orm.synonym(
            "_latest_event",
            default_factory=event_pb2.Event,
            descriptor=property(self._get_latest_event, self._set_latest_event),
        )

    @property
    def latest_event(self):
        """Returns the latest event for this entity from the event log."""
        return self._get_latest_event()

    _event_src_id: sa_orm.Mapped[str] = sa_orm.mapped_column(
        sa.Text, init=False, server_default=gen_uuid()
    )

    @property
    def event_key(self) -> EventKey:
        return EventKey.from_str(id=self._event_src_id)

    def _log_event(
        self, event_type: event_pb2.EventType, reason: str, regarding: str, dt: datetime
    ):
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(dt=dt)
        return event_pb2.Event(
            event_type=event_type,
            reason=reason,
            regarding=regarding,
            timestamp=timestamp,
        )

    def notify_done(
        self, reason: str = "", regarding: str = "", timestamp: datetime | None = None
    ):
        """Add a finished event to the event log for this object."""
        self._latest_event = self._log_event(
            event_type=event_pb2.EVENT_TYPE_FINISHED,
            reason=reason,
            regarding=regarding,
            dt=_timestamp_or_utc_now(timestamp=timestamp),
        )

    def notify_error(
        self, reason: str = "", regarding: str = "", timestamp: datetime | None = None
    ):
        """Add an error event to the event log for this object."""
        self._latest_event = self._log_event(
            event_type=event_pb2.EVENT_TYPE_ERROR,
            reason=reason,
            regarding=regarding,
            dt=_timestamp_or_utc_now(timestamp=timestamp),
        )

    def notify_pending_system(
        self, reason: str = "", regarding: str = "", timestamp: datetime | None = None
    ):
        """Add a pending system event to the event log for this object."""
        self._latest_event = self._log_event(
            event_type=event_pb2.EVENT_TYPE_SYSTEM_PENDING,
            reason=reason,
            regarding=regarding,
            dt=_timestamp_or_utc_now(timestamp=timestamp),
        )

    def notify_pending_user(
        self, reason: str = "", regarding: str = "", timestamp: datetime | None = None
    ):
        """Add a pending user event to the event log for this object."""
        self._latest_event = self._log_event(
            event_type=event_pb2.EVENT_TYPE_USER_PENDING,
            reason=reason,
            regarding=regarding,
            dt=_timestamp_or_utc_now(timestamp=timestamp),
        )


SoftDeleteMixin.register_session_event_listeners(Session)
BelongsToOrgMixin.register_session_event_listeners(Session)
