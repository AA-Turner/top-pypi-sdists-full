from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_compliance_overview_checklist_type_0 import CallComplianceOverviewChecklistType0


T = TypeVar("T", bound="CallComplianceOverview")


@_attrs_define
class CallComplianceOverview:
    """
    Attributes:
        checklist (Union['CallComplianceOverviewChecklistType0', None]):
        proposals (list[Any]):
    """

    checklist: Union["CallComplianceOverviewChecklistType0", None]
    proposals: list[Any]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_compliance_overview_checklist_type_0 import CallComplianceOverviewChecklistType0

        checklist: Union[None, dict[str, Any]]
        if isinstance(self.checklist, CallComplianceOverviewChecklistType0):
            checklist = self.checklist.to_dict()
        else:
            checklist = self.checklist

        proposals = self.proposals

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checklist": checklist,
                "proposals": proposals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_compliance_overview_checklist_type_0 import CallComplianceOverviewChecklistType0

        d = dict(src_dict)

        def _parse_checklist(data: object) -> Union["CallComplianceOverviewChecklistType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                checklist_type_0 = CallComplianceOverviewChecklistType0.from_dict(data)

                return checklist_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CallComplianceOverviewChecklistType0", None], data)

        checklist = _parse_checklist(d.pop("checklist"))

        proposals = cast(list[Any], d.pop("proposals"))

        call_compliance_overview = cls(
            checklist=checklist,
            proposals=proposals,
        )

        call_compliance_overview.additional_properties = d
        return call_compliance_overview

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
