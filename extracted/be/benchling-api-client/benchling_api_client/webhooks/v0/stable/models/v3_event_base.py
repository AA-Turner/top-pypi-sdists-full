import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.v3_event_base_stability import V3EventBaseStability
from ..types import UNSET, Unset

T = TypeVar("T", bound="V3EventBase")


@attr.s(auto_attribs=True, repr=False)
class V3EventBase:
    """  """

    _created_at: datetime.datetime
    _id: str
    _resource_id: str
    _stability: V3EventBaseStability
    _type: str
    _deprecated: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("stability={}".format(repr(self._stability)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "V3EventBase({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        created_at = self._created_at.isoformat()

        id = self._id
        resource_id = self._resource_id
        stability = self._stability.value

        type = self._type
        deprecated = self._deprecated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if stability is not UNSET:
            field_dict["stability"] = stability
        if type is not UNSET:
            field_dict["type"] = type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_created_at() -> datetime.datetime:
            created_at = isoparse(d.pop("createdAt"))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(datetime.datetime, UNSET)

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_resource_id() -> str:
            resource_id = d.pop("resourceId")
            return resource_id

        try:
            resource_id = get_resource_id()
        except KeyError:
            if strict:
                raise
            resource_id = cast(str, UNSET)

        def get_stability() -> V3EventBaseStability:
            _stability = d.pop("stability")
            try:
                stability = V3EventBaseStability(_stability)
            except ValueError:
                stability = V3EventBaseStability.of_unknown(_stability)

            return stability

        try:
            stability = get_stability()
        except KeyError:
            if strict:
                raise
            stability = cast(V3EventBaseStability, UNSET)

        def get_type() -> str:
            type = d.pop("type")
            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(str, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        v3_event_base = cls(
            created_at=created_at,
            id=id,
            resource_id=resource_id,
            stability=stability,
            type=type,
            deprecated=deprecated,
        )

        v3_event_base.additional_properties = d
        return v3_event_base

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
    def created_at(self) -> datetime.datetime:
        """ ISO 8601 date-time string when the event was created """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @property
    def id(self) -> str:
        """ Unique identifier for the event """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def resource_id(self) -> str:
        """ Unique identifier for the resource that triggered the event """
        if isinstance(self._resource_id, Unset):
            raise NotPresentError(self, "resource_id")
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str) -> None:
        self._resource_id = value

    @property
    def stability(self) -> V3EventBaseStability:
        """ Stability level of the resource type """
        if isinstance(self._stability, Unset):
            raise NotPresentError(self, "stability")
        return self._stability

    @stability.setter
    def stability(self, value: V3EventBaseStability) -> None:
        self._stability = value

    @property
    def type(self) -> str:
        """ The event type """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value
