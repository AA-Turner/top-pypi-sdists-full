from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plan_datatable_acl_json_body_change_type_0 import PlanDatatableAclJsonBodyChangeType0
    from ..models.plan_datatable_acl_json_body_change_type_1 import PlanDatatableAclJsonBodyChangeType1
    from ..models.plan_datatable_acl_json_body_change_type_2 import PlanDatatableAclJsonBodyChangeType2
    from ..models.plan_datatable_acl_json_body_target_type_0 import PlanDatatableAclJsonBodyTargetType0
    from ..models.plan_datatable_acl_json_body_target_type_1 import PlanDatatableAclJsonBodyTargetType1
    from ..models.plan_datatable_acl_json_body_target_type_2 import PlanDatatableAclJsonBodyTargetType2


T = TypeVar("T", bound="PlanDatatableAclJsonBody")


@_attrs_define
class PlanDatatableAclJsonBody:
    """
    Attributes:
        target (Union['PlanDatatableAclJsonBodyTargetType0', 'PlanDatatableAclJsonBodyTargetType1',
            'PlanDatatableAclJsonBodyTargetType2']): what access is read or changed on
        change (Union['PlanDatatableAclJsonBodyChangeType0', 'PlanDatatableAclJsonBodyChangeType1',
            'PlanDatatableAclJsonBodyChangeType2']): one change to plan or apply
        statements (Union[Unset, List[str]]): The statements the plan showed. Required to apply, which plans again and
            refuses if the result differs.
    """

    target: Union[
        "PlanDatatableAclJsonBodyTargetType0",
        "PlanDatatableAclJsonBodyTargetType1",
        "PlanDatatableAclJsonBodyTargetType2",
    ]
    change: Union[
        "PlanDatatableAclJsonBodyChangeType0",
        "PlanDatatableAclJsonBodyChangeType1",
        "PlanDatatableAclJsonBodyChangeType2",
    ]
    statements: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.plan_datatable_acl_json_body_change_type_0 import PlanDatatableAclJsonBodyChangeType0
        from ..models.plan_datatable_acl_json_body_change_type_1 import PlanDatatableAclJsonBodyChangeType1
        from ..models.plan_datatable_acl_json_body_target_type_0 import PlanDatatableAclJsonBodyTargetType0
        from ..models.plan_datatable_acl_json_body_target_type_1 import PlanDatatableAclJsonBodyTargetType1

        target: Dict[str, Any]

        if isinstance(self.target, PlanDatatableAclJsonBodyTargetType0):
            target = self.target.to_dict()

        elif isinstance(self.target, PlanDatatableAclJsonBodyTargetType1):
            target = self.target.to_dict()

        else:
            target = self.target.to_dict()

        change: Dict[str, Any]

        if isinstance(self.change, PlanDatatableAclJsonBodyChangeType0):
            change = self.change.to_dict()

        elif isinstance(self.change, PlanDatatableAclJsonBodyChangeType1):
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
        from ..models.plan_datatable_acl_json_body_change_type_0 import PlanDatatableAclJsonBodyChangeType0
        from ..models.plan_datatable_acl_json_body_change_type_1 import PlanDatatableAclJsonBodyChangeType1
        from ..models.plan_datatable_acl_json_body_change_type_2 import PlanDatatableAclJsonBodyChangeType2
        from ..models.plan_datatable_acl_json_body_target_type_0 import PlanDatatableAclJsonBodyTargetType0
        from ..models.plan_datatable_acl_json_body_target_type_1 import PlanDatatableAclJsonBodyTargetType1
        from ..models.plan_datatable_acl_json_body_target_type_2 import PlanDatatableAclJsonBodyTargetType2

        d = src_dict.copy()

        def _parse_target(
            data: object,
        ) -> Union[
            "PlanDatatableAclJsonBodyTargetType0",
            "PlanDatatableAclJsonBodyTargetType1",
            "PlanDatatableAclJsonBodyTargetType2",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                target_type_0 = PlanDatatableAclJsonBodyTargetType0.from_dict(data)

                return target_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                target_type_1 = PlanDatatableAclJsonBodyTargetType1.from_dict(data)

                return target_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            target_type_2 = PlanDatatableAclJsonBodyTargetType2.from_dict(data)

            return target_type_2

        target = _parse_target(d.pop("target"))

        def _parse_change(
            data: object,
        ) -> Union[
            "PlanDatatableAclJsonBodyChangeType0",
            "PlanDatatableAclJsonBodyChangeType1",
            "PlanDatatableAclJsonBodyChangeType2",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                change_type_0 = PlanDatatableAclJsonBodyChangeType0.from_dict(data)

                return change_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                change_type_1 = PlanDatatableAclJsonBodyChangeType1.from_dict(data)

                return change_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            change_type_2 = PlanDatatableAclJsonBodyChangeType2.from_dict(data)

            return change_type_2

        change = _parse_change(d.pop("change"))

        statements = cast(List[str], d.pop("statements", UNSET))

        plan_datatable_acl_json_body = cls(
            target=target,
            change=change,
            statements=statements,
        )

        plan_datatable_acl_json_body.additional_properties = d
        return plan_datatable_acl_json_body

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
