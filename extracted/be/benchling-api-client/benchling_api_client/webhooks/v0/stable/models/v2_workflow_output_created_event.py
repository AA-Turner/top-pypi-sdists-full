import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.event_resource_schema import EventResourceSchema
from ..models.v2_workflow_output_created_event_event_type import V2WorkflowOutputCreatedEventEventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="V2WorkflowOutputCreatedEvent")


@attr.s(auto_attribs=True, repr=False)
class V2WorkflowOutputCreatedEvent:
    """  """

    _event_type: V2WorkflowOutputCreatedEventEventType
    _deprecated: bool
    _schema: Union[Unset, None, EventResourceSchema] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _id: Union[Unset, str] = UNSET
    _resource_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("event_type={}".format(repr(self._event_type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "V2WorkflowOutputCreatedEvent({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        event_type = self._event_type.value

        deprecated = self._deprecated
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._schema, Unset):
            schema = self._schema.to_dict() if self._schema else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        id = self._id
        resource_id = self._resource_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if event_type is not UNSET:
            field_dict["eventType"] = event_type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if schema is not UNSET:
            field_dict["schema"] = schema
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_event_type() -> V2WorkflowOutputCreatedEventEventType:
            _event_type = d.pop("eventType")
            try:
                event_type = V2WorkflowOutputCreatedEventEventType(_event_type)
            except ValueError:
                event_type = V2WorkflowOutputCreatedEventEventType.of_unknown(_event_type)

            return event_type

        try:
            event_type = get_event_type()
        except KeyError:
            if strict:
                raise
            event_type = cast(V2WorkflowOutputCreatedEventEventType, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        def get_schema() -> Union[Unset, None, EventResourceSchema]:
            schema = None
            _schema = d.pop("schema")

            if _schema is not None and not isinstance(_schema, Unset):
                schema = EventResourceSchema.from_dict(_schema)

            return schema

        try:
            schema = get_schema()
        except KeyError:
            if strict:
                raise
            schema = cast(Union[Unset, None, EventResourceSchema], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_resource_id() -> Union[Unset, str]:
            resource_id = d.pop("resourceId")
            return resource_id

        try:
            resource_id = get_resource_id()
        except KeyError:
            if strict:
                raise
            resource_id = cast(Union[Unset, str], UNSET)

        v2_workflow_output_created_event = cls(
            event_type=event_type,
            deprecated=deprecated,
            schema=schema,
            created_at=created_at,
            id=id,
            resource_id=resource_id,
        )

        v2_workflow_output_created_event.additional_properties = d
        return v2_workflow_output_created_event

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def event_type(self) -> V2WorkflowOutputCreatedEventEventType:
        if isinstance(self._event_type, Unset):
            raise NotPresentError(self, "event_type")
        return self._event_type

    @event_type.setter
    def event_type(self, value: V2WorkflowOutputCreatedEventEventType) -> None:
        self._event_type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value

    @property
    def schema(self) -> Optional[EventResourceSchema]:
        """ The schema of the associated resource """
        if isinstance(self._schema, Unset):
            raise NotPresentError(self, "schema")
        return self._schema

    @schema.setter
    def schema(self, value: Optional[EventResourceSchema]) -> None:
        self._schema = value

    @schema.deleter
    def schema(self) -> None:
        self._schema = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        """ISO 8601 date-time string. The time at which the event was created."""
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def id(self) -> str:
        """ Unique identifier for the event """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def resource_id(self) -> str:
        """ Unique identifier for the resource that the event is associated with """
        if isinstance(self._resource_id, Unset):
            raise NotPresentError(self, "resource_id")
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str) -> None:
        self._resource_id = value

    @resource_id.deleter
    def resource_id(self) -> None:
        self._resource_id = UNSET
