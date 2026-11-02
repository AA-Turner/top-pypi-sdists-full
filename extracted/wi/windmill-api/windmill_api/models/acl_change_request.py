from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.acl_change_request_change_type_0 import AclChangeRequestChangeType0
    from ..models.acl_change_request_change_type_1 import AclChangeRequestChangeType1
    from ..models.acl_change_request_change_type_2 import AclChangeRequestChangeType2
    from ..models.acl_change_request_target_type_0 import AclChangeRequestTargetType0
    from ..models.acl_change_request_target_type_1 import AclChangeRequestTargetType1
    from ..models.acl_change_request_target_type_2 import AclChangeRequestTargetType2


T = TypeVar("T", bound="AclChangeRequest")


@_attrs_define
class AclChangeRequest:
    """
    Attributes:
        target (Union['AclChangeRequestTargetType0', 'AclChangeRequestTargetType1', 'AclChangeRequestTargetType2']):
            what access is read or changed on
        change (Union['AclChangeRequestChangeType0', 'AclChangeRequestChangeType1', 'AclChangeRequestChangeType2']): one
            change to plan or apply
        statements (Union[Unset, List[str]]): The statements the plan showed. Required to apply, which plans again and
            refuses if the result differs.
    """

    target: Union["AclChangeRequestTargetType0", "AclChangeRequestTargetType1", "AclChangeRequestTargetType2"]
    change: Union["AclChangeRequestChangeType0", "AclChangeRequestChangeType1", "AclChangeRequestChangeType2"]
    statements: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.acl_change_request_change_type_0 import AclChangeRequestChangeType0
        from ..models.acl_change_request_change_type_1 import AclChangeRequestChangeType1
        from ..models.acl_change_request_target_type_0 import AclChangeRequestTargetType0
        from ..models.acl_change_request_target_type_1 import AclChangeRequestTargetType1

        target: Dict[str, Any]

        if isinstance(self.target, AclChangeRequestTargetType0):
            target = self.target.to_dict()

        elif isinstance(self.target, AclChangeRequestTargetType1):
            target = self.target.to_dict()

        else:
            target = self.target.to_dict()

        change: Dict[str, Any]

        if isinstance(self.change, AclChangeRequestChangeType0):
            change = self.change.to_dict()

        elif isinstance(self.change, AclChangeRequestChangeType1):
            change = self.change.to_dict()

        else:
            change = self.change.to_dict()

        statements: Union[Unset, List[str]] = UNSET
        if not isinstance(self.statements, Unset):
            statements = self.statements

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target": target,
                "change": change,
            }
        )
        if statements is not UNSET:
            field_dict["statements"] = statements

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.acl_change_request_change_type_0 import AclChangeRequestChangeType0
        from ..models.acl_change_request_change_type_1 import AclChangeRequestChangeType1
        from ..models.acl_change_request_change_type_2 import AclChangeRequestChangeType2
        from ..models.acl_change_request_target_type_0 import AclChangeRequestTargetType0
        from ..models.acl_change_request_target_type_1 import AclChangeRequestTargetType1
        from ..models.acl_change_request_target_type_2 import AclChangeRequestTargetType2

        d = src_dict.copy()

        def _parse_target(
            data: object,
        ) -> Union["AclChangeRequestTargetType0", "AclChangeRequestTargetType1", "AclChangeRequestTargetType2"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                target_type_0 = AclChangeRequestTargetType0.from_dict(data)

                return target_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                target_type_1 = AclChangeRequestTargetType1.from_dict(data)

                return target_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            target_type_2 = AclChangeRequestTargetType2.from_dict(data)

            return target_type_2

        target = _parse_target(d.pop("target"))

        def _parse_change(
            data: object,
        ) -> Union["AclChangeRequestChangeType0", "AclChangeRequestChangeType1", "AclChangeRequestChangeType2"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                change_type_0 = AclChangeRequestChangeType0.from_dict(data)

                return change_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                change_type_1 = AclChangeRequestChangeType1.from_dict(data)

                return change_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            change_type_2 = AclChangeRequestChangeType2.from_dict(data)

            return change_type_2

        change = _parse_change(d.pop("change"))

        statements = cast(List[str], d.pop("statements", UNSET))

        acl_change_request = cls(
            target=target,
            change=change,
            statements=statements,
        )

        acl_change_request.additional_properties = d
        return acl_change_request

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
