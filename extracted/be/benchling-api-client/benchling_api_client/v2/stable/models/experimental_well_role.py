from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.experimental_well_role_primary_role import ExperimentalWellRolePrimaryRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentalWellRole")


@attr.s(auto_attribs=True, repr=False)
class ExperimentalWellRole:
    """  """

    _group: Union[Unset, int] = UNSET
    _primary_role: Union[Unset, ExperimentalWellRolePrimaryRole] = UNSET
    _subrole: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("group={}".format(repr(self._group)))
        fields.append("primary_role={}".format(repr(self._primary_role)))
        fields.append("subrole={}".format(repr(self._subrole)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ExperimentalWellRole({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        group = self._group
        primary_role: Union[Unset, int] = UNSET
        if not isinstance(self._primary_role, Unset):
            primary_role = self._primary_role.value

        subrole = self._subrole

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if group is not UNSET:
            field_dict["group"] = group
        if primary_role is not UNSET:
            field_dict["primaryRole"] = primary_role
        if subrole is not UNSET:
            field_dict["subrole"] = subrole

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_group() -> Union[Unset, int]:
            group = d.pop("group")
            return group

        try:
            group = get_group()
        except KeyError:
            if strict:
                raise
            group = cast(Union[Unset, int], UNSET)

        def get_primary_role() -> Union[Unset, ExperimentalWellRolePrimaryRole]:
            primary_role = UNSET
            _primary_role = d.pop("primaryRole")
            if _primary_role is not None and _primary_role is not UNSET:
                try:
                    primary_role = ExperimentalWellRolePrimaryRole(_primary_role)
                except ValueError:
                    primary_role = ExperimentalWellRolePrimaryRole.of_unknown(_primary_role)

            return primary_role

        try:
            primary_role = get_primary_role()
        except KeyError:
            if strict:
                raise
            primary_role = cast(Union[Unset, ExperimentalWellRolePrimaryRole], UNSET)

        def get_subrole() -> Union[Unset, None, str]:
            subrole = d.pop("subrole")
            return subrole

        try:
            subrole = get_subrole()
        except KeyError:
            if strict:
                raise
            subrole = cast(Union[Unset, None, str], UNSET)

        experimental_well_role = cls(
            group=group,
            primary_role=primary_role,
            subrole=subrole,
        )

        experimental_well_role.additional_properties = d
        return experimental_well_role

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
    def group(self) -> int:
        if isinstance(self._group, Unset):
            raise NotPresentError(self, "group")
        return self._group

    @group.setter
    def group(self, value: int) -> None:
        self._group = value

    @group.deleter
    def group(self) -> None:
        self._group = UNSET

    @property
    def primary_role(self) -> ExperimentalWellRolePrimaryRole:
        if isinstance(self._primary_role, Unset):
            raise NotPresentError(self, "primary_role")
        return self._primary_role

    @primary_role.setter
    def primary_role(self, value: ExperimentalWellRolePrimaryRole) -> None:
        self._primary_role = value

    @primary_role.deleter
    def primary_role(self) -> None:
        self._primary_role = UNSET

    @property
    def subrole(self) -> Optional[str]:
        if isinstance(self._subrole, Unset):
            raise NotPresentError(self, "subrole")
        return self._subrole

    @subrole.setter
    def subrole(self, value: Optional[str]) -> None:
        self._subrole = value

    @subrole.deleter
    def subrole(self) -> None:
        self._subrole = UNSET
