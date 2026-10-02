import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.slurm_policy_evaluation_log_new_state import SlurmPolicyEvaluationLogNewState
    from ..models.slurm_policy_evaluation_log_previous_state import SlurmPolicyEvaluationLogPreviousState
    from ..models.slurm_policy_evaluation_log_site_agent_response_type_0 import (
        SlurmPolicyEvaluationLogSiteAgentResponseType0,
    )


T = TypeVar("T", bound="SlurmPolicyEvaluationLog")


@_attrs_define
class SlurmPolicyEvaluationLog:
    """
    Attributes:
        uuid (UUID):
        resource_uuid (UUID):
        resource_name (str):
        billing_period (str): Billing period identifier, e.g. '2026-Q1'
        usage_percentage (float): Resource usage percentage at the time of evaluation
        grace_limit_percentage (float): Grace limit percentage threshold (e.g. 120 for 20% grace)
        actions_taken (list[str]):
        evaluated_at (datetime.datetime): When this evaluation was performed
        previous_state (Union[Unset, SlurmPolicyEvaluationLogPreviousState]): Resource state before evaluation: {paused:
            bool, downscaled: bool}
        new_state (Union[Unset, SlurmPolicyEvaluationLogNewState]): Resource state after evaluation: {paused: bool,
            downscaled: bool}
        stomp_message_sent (Union[Unset, bool]): Whether a STOMP message was sent to the site agent
        site_agent_confirmed (Union[None, Unset, bool]): Whether the site agent confirmed command execution (null = no
            response yet)
        site_agent_response (Union['SlurmPolicyEvaluationLogSiteAgentResponseType0', None, Unset]): Response payload
            from the site agent
    """

    uuid: UUID
    resource_uuid: UUID
    resource_name: str
    billing_period: str
    usage_percentage: float
    grace_limit_percentage: float
    actions_taken: list[str]
    evaluated_at: datetime.datetime
    previous_state: Union[Unset, "SlurmPolicyEvaluationLogPreviousState"] = UNSET
    new_state: Union[Unset, "SlurmPolicyEvaluationLogNewState"] = UNSET
    stomp_message_sent: Union[Unset, bool] = UNSET
    site_agent_confirmed: Union[None, Unset, bool] = UNSET
    site_agent_response: Union["SlurmPolicyEvaluationLogSiteAgentResponseType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.slurm_policy_evaluation_log_site_agent_response_type_0 import (
            SlurmPolicyEvaluationLogSiteAgentResponseType0,
        )

        uuid = str(self.uuid)

        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        billing_period = self.billing_period

        usage_percentage = self.usage_percentage

        grace_limit_percentage = self.grace_limit_percentage

        actions_taken = self.actions_taken

        evaluated_at = self.evaluated_at.isoformat()

        previous_state: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.previous_state, Unset):
            previous_state = self.previous_state.to_dict()

        new_state: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.new_state, Unset):
            new_state = self.new_state.to_dict()

        stomp_message_sent = self.stomp_message_sent

        site_agent_confirmed: Union[None, Unset, bool]
        if isinstance(self.site_agent_confirmed, Unset):
            site_agent_confirmed = UNSET
        else:
            site_agent_confirmed = self.site_agent_confirmed

        site_agent_response: Union[None, Unset, dict[str, Any]]
        if isinstance(self.site_agent_response, Unset):
            site_agent_response = UNSET
        elif isinstance(self.site_agent_response, SlurmPolicyEvaluationLogSiteAgentResponseType0):
            site_agent_response = self.site_agent_response.to_dict()
        else:
            site_agent_response = self.site_agent_response

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "billing_period": billing_period,
                "usage_percentage": usage_percentage,
                "grace_limit_percentage": grace_limit_percentage,
                "actions_taken": actions_taken,
                "evaluated_at": evaluated_at,
            }
        )
        if previous_state is not UNSET:
            field_dict["previous_state"] = previous_state
        if new_state is not UNSET:
            field_dict["new_state"] = new_state
        if stomp_message_sent is not UNSET:
            field_dict["stomp_message_sent"] = stomp_message_sent
        if site_agent_confirmed is not UNSET:
            field_dict["site_agent_confirmed"] = site_agent_confirmed
        if site_agent_response is not UNSET:
            field_dict["site_agent_response"] = site_agent_response

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slurm_policy_evaluation_log_new_state import SlurmPolicyEvaluationLogNewState
        from ..models.slurm_policy_evaluation_log_previous_state import SlurmPolicyEvaluationLogPreviousState
        from ..models.slurm_policy_evaluation_log_site_agent_response_type_0 import (
            SlurmPolicyEvaluationLogSiteAgentResponseType0,
        )

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        billing_period = d.pop("billing_period")

        usage_percentage = d.pop("usage_percentage")

        grace_limit_percentage = d.pop("grace_limit_percentage")

        actions_taken = cast(list[str], d.pop("actions_taken"))

        evaluated_at = isoparse(d.pop("evaluated_at"))

        _previous_state = d.pop("previous_state", UNSET)
        previous_state: Union[Unset, SlurmPolicyEvaluationLogPreviousState]
        if isinstance(_previous_state, Unset):
            previous_state = UNSET
        else:
            previous_state = SlurmPolicyEvaluationLogPreviousState.from_dict(_previous_state)

        _new_state = d.pop("new_state", UNSET)
        new_state: Union[Unset, SlurmPolicyEvaluationLogNewState]
        if isinstance(_new_state, Unset):
            new_state = UNSET
        else:
            new_state = SlurmPolicyEvaluationLogNewState.from_dict(_new_state)

        stomp_message_sent = d.pop("stomp_message_sent", UNSET)

        def _parse_site_agent_confirmed(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        site_agent_confirmed = _parse_site_agent_confirmed(d.pop("site_agent_confirmed", UNSET))

        def _parse_site_agent_response(
            data: object,
        ) -> Union["SlurmPolicyEvaluationLogSiteAgentResponseType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                site_agent_response_type_0 = SlurmPolicyEvaluationLogSiteAgentResponseType0.from_dict(data)

                return site_agent_response_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SlurmPolicyEvaluationLogSiteAgentResponseType0", None, Unset], data)

        site_agent_response = _parse_site_agent_response(d.pop("site_agent_response", UNSET))

        slurm_policy_evaluation_log = cls(
            uuid=uuid,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            billing_period=billing_period,
            usage_percentage=usage_percentage,
            grace_limit_percentage=grace_limit_percentage,
            actions_taken=actions_taken,
            evaluated_at=evaluated_at,
            previous_state=previous_state,
            new_state=new_state,
            stomp_message_sent=stomp_message_sent,
            site_agent_confirmed=site_agent_confirmed,
            site_agent_response=site_agent_response,
        )

        slurm_policy_evaluation_log.additional_properties = d
        return slurm_policy_evaluation_log

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
