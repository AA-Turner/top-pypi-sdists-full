import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.event_resource_schema import EventResourceSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="V2EventBaseSchematized")


@attr.s(auto_attribs=True, repr=False)
class V2EventBaseSchematized:
    """  """

    _schema: EventResourceSchema
    _deprecated: bool
    _excluded_properties: List[str]
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _id: Union[Unset, str] = UNSET
    _resource_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("excluded_properties={}".format(repr(self._excluded_properties)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "V2EventBaseSchematized({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        schema = self._schema.to_dict()

        deprecated = self._deprecated
        excluded_properties = self._excluded_properties

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        id = self._id
        resource_id = self._resource_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if schema is not UNSET:
            field_dict["schema"] = schema
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if excluded_properties is not UNSET:
            field_dict["excludedProperties"] = excluded_properties
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

        def get_schema() -> EventResourceSchema:
            schema = EventResourceSchema.from_dict(d.pop("schema"), strict=False)

            return schema

        try:
            schema = get_schema()
        except KeyError:
            if strict:
                raise
            schema = cast(EventResourceSchema, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        def get_excluded_properties() -> List[str]:
            excluded_properties = cast(List[str], d.pop("excludedProperties"))

            return excluded_properties

        try:
            excluded_properties = get_excluded_properties()
        except KeyError:
            if strict:
                raise
            excluded_properties = cast(List[str], UNSET)

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

        v2_event_base_schematized = cls(
            schema=schema,
            deprecated=deprecated,
            excluded_properties=excluded_properties,
            created_at=created_at,
            id=id,
            resource_id=resource_id,
        )

        v2_event_base_schematized.additional_properties = d
        return v2_event_base_schematized

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
    def schema(self) -> EventResourceSchema:
        """ The schema of the associated resource """
        if isinstance(self._schema, Unset):
            raise NotPresentError(self, "schema")
        return self._schema

    @schema.setter
    def schema(self, value: EventResourceSchema) -> None:
        self._schema = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value

    @property
    def excluded_properties(self) -> List[str]:
        """These properties have been dropped from the payload due to size."""
        if isinstance(self._excluded_properties, Unset):
            raise NotPresentError(self, "excluded_properties")
        return self._excluded_properties

    @excluded_properties.setter
    def excluded_properties(self, value: List[str]) -> None:
        self._excluded_properties = value

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
