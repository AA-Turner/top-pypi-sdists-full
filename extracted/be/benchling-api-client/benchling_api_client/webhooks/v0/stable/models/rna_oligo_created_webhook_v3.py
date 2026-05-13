import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.rna_oligo_created_webhook_v3_type import RnaOligoCreatedWebhookV3Type
from ..models.v3_event_base_stability import V3EventBaseStability
from ..types import UNSET, Unset

T = TypeVar("T", bound="RnaOligoCreatedWebhookV3")


@attr.s(auto_attribs=True, repr=False)
class RnaOligoCreatedWebhookV3:
    """  """

    _type: RnaOligoCreatedWebhookV3Type
    _deprecated: bool
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _id: Union[Unset, str] = UNSET
    _resource_id: Union[Unset, str] = UNSET
    _stability: Union[Unset, V3EventBaseStability] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("stability={}".format(repr(self._stability)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "RnaOligoCreatedWebhookV3({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        deprecated = self._deprecated
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        id = self._id
        resource_id = self._resource_id
        stability: Union[Unset, int] = UNSET
        if not isinstance(self._stability, Unset):
            stability = self._stability.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if stability is not UNSET:
            field_dict["stability"] = stability

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> RnaOligoCreatedWebhookV3Type:
            _type = d.pop("type")
            try:
                type = RnaOligoCreatedWebhookV3Type(_type)
            except ValueError:
                type = RnaOligoCreatedWebhookV3Type.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(RnaOligoCreatedWebhookV3Type, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

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

        def get_stability() -> Union[Unset, V3EventBaseStability]:
            stability = UNSET
            _stability = d.pop("stability")
            if _stability is not None and _stability is not UNSET:
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
            stability = cast(Union[Unset, V3EventBaseStability], UNSET)

        rna_oligo_created_webhook_v3 = cls(
            type=type,
            deprecated=deprecated,
            created_at=created_at,
            id=id,
            resource_id=resource_id,
            stability=stability,
        )

        rna_oligo_created_webhook_v3.additional_properties = d
        return rna_oligo_created_webhook_v3

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
    def type(self) -> RnaOligoCreatedWebhookV3Type:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: RnaOligoCreatedWebhookV3Type) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value

    @property
    def created_at(self) -> datetime.datetime:
        """ ISO 8601 date-time string when the event was created """
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
        """ Unique identifier for the resource that triggered the event """
        if isinstance(self._resource_id, Unset):
            raise NotPresentError(self, "resource_id")
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str) -> None:
        self._resource_id = value

    @resource_id.deleter
    def resource_id(self) -> None:
        self._resource_id = UNSET

    @property
    def stability(self) -> V3EventBaseStability:
        """ Stability level of the resource type """
        if isinstance(self._stability, Unset):
            raise NotPresentError(self, "stability")
        return self._stability

    @stability.setter
    def stability(self, value: V3EventBaseStability) -> None:
        self._stability = value

    @stability.deleter
    def stability(self) -> None:
        self._stability = UNSET
