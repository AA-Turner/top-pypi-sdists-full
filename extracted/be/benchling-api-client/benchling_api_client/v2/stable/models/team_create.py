from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="TeamCreate")


@attr.s(auto_attribs=True, repr=False)
class TeamCreate:
    """  """

    _description: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _organization_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("description={}".format(repr(self._description)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("organization_id={}".format(repr(self._organization_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "TeamCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        description = self._description
        name = self._name
        organization_id = self._organization_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_organization_id() -> Union[Unset, str]:
            organization_id = d.pop("organizationId")
            return organization_id

        try:
            organization_id = get_organization_id()
        except KeyError:
            if strict:
                raise
            organization_id = cast(Union[Unset, str], UNSET)

        team_create = cls(
            description=description,
            name=name,
            organization_id=organization_id,
        )

        team_create.additional_properties = d
        return team_create

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
    def description(self) -> str:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def organization_id(self) -> str:
        if isinstance(self._organization_id, Unset):
            raise NotPresentError(self, "organization_id")
        return self._organization_id

    @organization_id.setter
    def organization_id(self, value: str) -> None:
        self._organization_id = value

    @organization_id.deleter
    def organization_id(self) -> None:
        self._organization_id = UNSET
