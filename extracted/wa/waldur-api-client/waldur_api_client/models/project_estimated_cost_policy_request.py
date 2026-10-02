from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_period_enum import PolicyPeriodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_estimated_cost_policy_request_options import ProjectEstimatedCostPolicyRequestOptions


T = TypeVar("T", bound="ProjectEstimatedCostPolicyRequest")


@_attrs_define
class ProjectEstimatedCostPolicyRequest:
    """
    Attributes:
        scope (str):
        actions (str):
        limit_cost (int):
        options (Union[Unset, ProjectEstimatedCostPolicyRequestOptions]): Fields for saving actions extra data. Keys are
            name of actions.
        period (Union[Unset, PolicyPeriodEnum]):
        resource (Union[None, UUID, Unset]):
        use_credit (Union[Unset, bool]):
    """

    scope: str
    actions: str
    limit_cost: int
    options: Union[Unset, "ProjectEstimatedCostPolicyRequestOptions"] = UNSET
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    resource: Union[None, UUID, Unset] = UNSET
    use_credit: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope

        actions = self.actions

        limit_cost = self.limit_cost

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        resource: Union[None, Unset, str]
        if isinstance(self.resource, Unset):
            resource = UNSET
        elif isinstance(self.resource, UUID):
            resource = str(self.resource)
        else:
            resource = self.resource

        use_credit = self.use_credit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
                "actions": actions,
                "limit_cost": limit_cost,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if period is not UNSET:
            field_dict["period"] = period
        if resource is not UNSET:
            field_dict["resource"] = resource
        if use_credit is not UNSET:
            field_dict["use_credit"] = use_credit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_estimated_cost_policy_request_options import ProjectEstimatedCostPolicyRequestOptions

        d = dict(src_dict)
        scope = d.pop("scope")

        actions = d.pop("actions")

        limit_cost = d.pop("limit_cost")

        _options = d.pop("options", UNSET)
        options: Union[Unset, ProjectEstimatedCostPolicyRequestOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = ProjectEstimatedCostPolicyRequestOptions.from_dict(_options)

        _period = d.pop("period", UNSET)
        period: Union[Unset, PolicyPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PolicyPeriodEnum(_period)

        def _parse_resource(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_type_0 = UUID(data)

                return resource_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        resource = _parse_resource(d.pop("resource", UNSET))

        use_credit = d.pop("use_credit", UNSET)

        project_estimated_cost_policy_request = cls(
            scope=scope,
            actions=actions,
            limit_cost=limit_cost,
            options=options,
            period=period,
            resource=resource,
            use_credit=use_credit,
        )

        project_estimated_cost_policy_request.additional_properties = d
        return project_estimated_cost_policy_request

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
