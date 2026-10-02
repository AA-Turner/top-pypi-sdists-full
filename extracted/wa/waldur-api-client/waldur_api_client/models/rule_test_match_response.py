from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.customer_candidate import CustomerCandidate
    from ..models.filter_check_result import FilterCheckResult


T = TypeVar("T", bound="RuleTestMatchResponse")


@_attrs_define
class RuleTestMatchResponse:
    """
    Attributes:
        would_provision (bool):
        block_reason (str):
        user_username (str):
        user_email (str):
        user_organization (str):
        user_registration_method (str):
        user_identity_source (str):
        user_affiliations (list[str]):
        user_is_protected (bool):
        filter_results (list['FilterCheckResult']):
        customer_lookup_performed (bool):
        customer_candidates (list['CustomerCandidate']):
        customer_lookup_ambiguous (bool):
        resolved_project_name (Union[None, str]):
    """

    would_provision: bool
    block_reason: str
    user_username: str
    user_email: str
    user_organization: str
    user_registration_method: str
    user_identity_source: str
    user_affiliations: list[str]
    user_is_protected: bool
    filter_results: list["FilterCheckResult"]
    customer_lookup_performed: bool
    customer_candidates: list["CustomerCandidate"]
    customer_lookup_ambiguous: bool
    resolved_project_name: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        would_provision = self.would_provision

        block_reason = self.block_reason

        user_username = self.user_username

        user_email = self.user_email

        user_organization = self.user_organization

        user_registration_method = self.user_registration_method

        user_identity_source = self.user_identity_source

        user_affiliations = self.user_affiliations

        user_is_protected = self.user_is_protected

        filter_results = []
        for filter_results_item_data in self.filter_results:
            filter_results_item = filter_results_item_data.to_dict()
            filter_results.append(filter_results_item)

        customer_lookup_performed = self.customer_lookup_performed

        customer_candidates = []
        for customer_candidates_item_data in self.customer_candidates:
            customer_candidates_item = customer_candidates_item_data.to_dict()
            customer_candidates.append(customer_candidates_item)

        customer_lookup_ambiguous = self.customer_lookup_ambiguous

        resolved_project_name: Union[None, str]
        resolved_project_name = self.resolved_project_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "would_provision": would_provision,
                "block_reason": block_reason,
                "user_username": user_username,
                "user_email": user_email,
                "user_organization": user_organization,
                "user_registration_method": user_registration_method,
                "user_identity_source": user_identity_source,
                "user_affiliations": user_affiliations,
                "user_is_protected": user_is_protected,
                "filter_results": filter_results,
                "customer_lookup_performed": customer_lookup_performed,
                "customer_candidates": customer_candidates,
                "customer_lookup_ambiguous": customer_lookup_ambiguous,
                "resolved_project_name": resolved_project_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customer_candidate import CustomerCandidate
        from ..models.filter_check_result import FilterCheckResult

        d = dict(src_dict)
        would_provision = d.pop("would_provision")

        block_reason = d.pop("block_reason")

        user_username = d.pop("user_username")

        user_email = d.pop("user_email")

        user_organization = d.pop("user_organization")

        user_registration_method = d.pop("user_registration_method")

        user_identity_source = d.pop("user_identity_source")

        user_affiliations = cast(list[str], d.pop("user_affiliations"))

        user_is_protected = d.pop("user_is_protected")

        filter_results = []
        _filter_results = d.pop("filter_results")
        for filter_results_item_data in _filter_results:
            filter_results_item = FilterCheckResult.from_dict(filter_results_item_data)

            filter_results.append(filter_results_item)

        customer_lookup_performed = d.pop("customer_lookup_performed")

        customer_candidates = []
        _customer_candidates = d.pop("customer_candidates")
        for customer_candidates_item_data in _customer_candidates:
            customer_candidates_item = CustomerCandidate.from_dict(customer_candidates_item_data)

            customer_candidates.append(customer_candidates_item)

        customer_lookup_ambiguous = d.pop("customer_lookup_ambiguous")

        def _parse_resolved_project_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resolved_project_name = _parse_resolved_project_name(d.pop("resolved_project_name"))

        rule_test_match_response = cls(
            would_provision=would_provision,
            block_reason=block_reason,
            user_username=user_username,
            user_email=user_email,
            user_organization=user_organization,
            user_registration_method=user_registration_method,
            user_identity_source=user_identity_source,
            user_affiliations=user_affiliations,
            user_is_protected=user_is_protected,
            filter_results=filter_results,
            customer_lookup_performed=customer_lookup_performed,
            customer_candidates=customer_candidates,
            customer_lookup_ambiguous=customer_lookup_ambiguous,
            resolved_project_name=resolved_project_name,
        )

        rule_test_match_response.additional_properties = d
        return rule_test_match_response

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
