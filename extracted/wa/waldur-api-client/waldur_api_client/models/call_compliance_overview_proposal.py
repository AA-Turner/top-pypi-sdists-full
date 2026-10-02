from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_compliance_overview_proposal_compliance import CallComplianceOverviewProposalCompliance


T = TypeVar("T", bound="CallComplianceOverviewProposal")


@_attrs_define
class CallComplianceOverviewProposal:
    """
    Attributes:
        uuid (UUID):
        name (str):
        state (str):
        created_by (Union[None, str]):
        created_by_uuid (Union[None, UUID]):
        compliance (Union['CallComplianceOverviewProposalCompliance', None]):
    """

    uuid: UUID
    name: str
    state: str
    created_by: Union[None, str]
    created_by_uuid: Union[None, UUID]
    compliance: Union["CallComplianceOverviewProposalCompliance", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_compliance_overview_proposal_compliance import CallComplianceOverviewProposalCompliance

        uuid = str(self.uuid)

        name = self.name

        state = self.state

        created_by: Union[None, str]
        created_by = self.created_by

        created_by_uuid: Union[None, str]
        if isinstance(self.created_by_uuid, UUID):
            created_by_uuid = str(self.created_by_uuid)
        else:
            created_by_uuid = self.created_by_uuid

        compliance: Union[None, dict[str, Any]]
        if isinstance(self.compliance, CallComplianceOverviewProposalCompliance):
            compliance = self.compliance.to_dict()
        else:
            compliance = self.compliance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "state": state,
                "created_by": created_by,
                "created_by_uuid": created_by_uuid,
                "compliance": compliance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_compliance_overview_proposal_compliance import CallComplianceOverviewProposalCompliance

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        state = d.pop("state")

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        def _parse_created_by_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_uuid_type_0 = UUID(data)

                return created_by_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        created_by_uuid = _parse_created_by_uuid(d.pop("created_by_uuid"))

        def _parse_compliance(data: object) -> Union["CallComplianceOverviewProposalCompliance", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                compliance_type_1 = CallComplianceOverviewProposalCompliance.from_dict(data)

                return compliance_type_1
            except:  # noqa: E722
                pass
            return cast(Union["CallComplianceOverviewProposalCompliance", None], data)

        compliance = _parse_compliance(d.pop("compliance"))

        call_compliance_overview_proposal = cls(
            uuid=uuid,
            name=name,
            state=state,
            created_by=created_by,
            created_by_uuid=created_by_uuid,
            compliance=compliance,
        )

        call_compliance_overview_proposal.additional_properties = d
        return call_compliance_overview_proposal

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
