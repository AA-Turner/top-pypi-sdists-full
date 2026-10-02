from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_compliance_checklist_info import CallComplianceChecklistInfo
    from ..models.call_compliance_overview_proposal import CallComplianceOverviewProposal


T = TypeVar("T", bound="CallComplianceOverview")


@_attrs_define
class CallComplianceOverview:
    """
    Attributes:
        checklist (Union['CallComplianceChecklistInfo', None]):
        proposals (list['CallComplianceOverviewProposal']):
    """

    checklist: Union["CallComplianceChecklistInfo", None]
    proposals: list["CallComplianceOverviewProposal"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_compliance_checklist_info import CallComplianceChecklistInfo

        checklist: Union[None, dict[str, Any]]
        if isinstance(self.checklist, CallComplianceChecklistInfo):
            checklist = self.checklist.to_dict()
        else:
            checklist = self.checklist

        proposals = []
        for proposals_item_data in self.proposals:
            proposals_item = proposals_item_data.to_dict()
            proposals.append(proposals_item)

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
        from ..models.call_compliance_checklist_info import CallComplianceChecklistInfo
        from ..models.call_compliance_overview_proposal import CallComplianceOverviewProposal

        d = dict(src_dict)

        def _parse_checklist(data: object) -> Union["CallComplianceChecklistInfo", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                checklist_type_1 = CallComplianceChecklistInfo.from_dict(data)

                return checklist_type_1
            except:  # noqa: E722
                pass
            return cast(Union["CallComplianceChecklistInfo", None], data)

        checklist = _parse_checklist(d.pop("checklist"))

        proposals = []
        _proposals = d.pop("proposals")
        for proposals_item_data in _proposals:
            proposals_item = CallComplianceOverviewProposal.from_dict(proposals_item_data)

            proposals.append(proposals_item)

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
