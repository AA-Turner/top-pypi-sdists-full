from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.inaccessible_resource_resource_type import InaccessibleResourceResourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InaccessibleResource")


@attr.s(auto_attribs=True, repr=False)
class InaccessibleResource:
    """  """

    _inaccessible_id: Union[Unset, str] = UNSET
    _resource_type: Union[Unset, InaccessibleResourceResourceType] = UNSET
    _type: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("inaccessible_id={}".format(repr(self._inaccessible_id)))
        fields.append("resource_type={}".format(repr(self._resource_type)))
        fields.append("type={}".format(repr(self._type)))
        return "InaccessibleResource({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        inaccessible_id = self._inaccessible_id
        resource_type: Union[Unset, int] = UNSET
        if not isinstance(self._resource_type, Unset):
            resource_type = self._resource_type.value

        type = self._type

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if inaccessible_id is not UNSET:
            field_dict["inaccessibleId"] = inaccessible_id
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_inaccessible_id() -> Union[Unset, str]:
            inaccessible_id = d.pop("inaccessibleId")
            return inaccessible_id

        try:
            inaccessible_id = get_inaccessible_id()
        except KeyError:
            if strict:
                raise
            inaccessible_id = cast(Union[Unset, str], UNSET)

        def get_resource_type() -> Union[Unset, InaccessibleResourceResourceType]:
            resource_type = UNSET
            _resource_type = d.pop("resourceType")
            if _resource_type is not None and _resource_type is not UNSET:
                try:
                    resource_type = InaccessibleResourceResourceType(_resource_type)
                except ValueError:
                    resource_type = InaccessibleResourceResourceType.of_unknown(_resource_type)

            return resource_type

        try:
            resource_type = get_resource_type()
        except KeyError:
            if strict:
                raise
            resource_type = cast(Union[Unset, InaccessibleResourceResourceType], UNSET)

        def get_type() -> Union[Unset, str]:
            type = d.pop("type")
            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, str], UNSET)

        inaccessible_resource = cls(
            inaccessible_id=inaccessible_id,
            resource_type=resource_type,
            type=type,
        )

        return inaccessible_resource

    @property
    def inaccessible_id(self) -> str:
        if isinstance(self._inaccessible_id, Unset):
            raise NotPresentError(self, "inaccessible_id")
        return self._inaccessible_id

    @inaccessible_id.setter
    def inaccessible_id(self, value: str) -> None:
        self._inaccessible_id = value

    @inaccessible_id.deleter
    def inaccessible_id(self) -> None:
        self._inaccessible_id = UNSET

    @property
    def resource_type(self) -> InaccessibleResourceResourceType:
        if isinstance(self._resource_type, Unset):
            raise NotPresentError(self, "resource_type")
        return self._resource_type

    @resource_type.setter
    def resource_type(self, value: InaccessibleResourceResourceType) -> None:
        self._resource_type = value

    @resource_type.deleter
    def resource_type(self) -> None:
        self._resource_type = UNSET

    @property
    def type(self) -> str:
        """The type of this inaccessible item. Example values: "custom_entity", "container", "plate", "dna_sequence" """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
