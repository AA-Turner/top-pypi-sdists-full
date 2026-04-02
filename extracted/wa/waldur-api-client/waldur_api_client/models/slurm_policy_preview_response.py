import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.current_qos_status_enum import CurrentQosStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.slurm_command import SlurmCommand
    from ..models.slurm_command_history import SlurmCommandHistory
    from ..models.slurm_policy_carryover import SlurmPolicyCarryover
    from ..models.slurm_policy_date_projections import SlurmPolicyDateProjections
    from ..models.slurm_policy_thresholds import SlurmPolicyThresholds


T = TypeVar("T", bound="SlurmPolicyPreviewResponse")


@_attrs_define
class SlurmPolicyPreviewResponse:
    """
    Attributes:
        base_allocation (float):
        effective_allocation (float):
        carryover_enabled (bool):
        carryover (Union['SlurmPolicyCarryover', None]):
        thresholds (SlurmPolicyThresholds):
        grace_ratio (float):
        carryover_factor (int):
        current_usage (Union[Unset, float]):
        daily_usage_rate (Union[Unset, float]):
        usage_percentage (Union[Unset, float]):
        current_qos_status (Union[Unset, CurrentQosStatusEnum]):
        date_projections (Union[Unset, SlurmPolicyDateProjections]):
        preview_commands (Union[Unset, list['SlurmCommand']]):
        command_history (Union[Unset, list['SlurmCommandHistory']]):
        billing_period_start (Union[Unset, datetime.date]):
        billing_period_end (Union[Unset, datetime.date]):
    """

    base_allocation: float
    effective_allocation: float
    carryover_enabled: bool
    carryover: Union["SlurmPolicyCarryover", None]
    thresholds: "SlurmPolicyThresholds"
    grace_ratio: float
    carryover_factor: int
    current_usage: Union[Unset, float] = UNSET
    daily_usage_rate: Union[Unset, float] = UNSET
    usage_percentage: Union[Unset, float] = UNSET
    current_qos_status: Union[Unset, CurrentQosStatusEnum] = UNSET
    date_projections: Union[Unset, "SlurmPolicyDateProjections"] = UNSET
    preview_commands: Union[Unset, list["SlurmCommand"]] = UNSET
    command_history: Union[Unset, list["SlurmCommandHistory"]] = UNSET
    billing_period_start: Union[Unset, datetime.date] = UNSET
    billing_period_end: Union[Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.slurm_policy_carryover import SlurmPolicyCarryover

        base_allocation = self.base_allocation

        effective_allocation = self.effective_allocation

        carryover_enabled = self.carryover_enabled

        carryover: Union[None, dict[str, Any]]
        if isinstance(self.carryover, SlurmPolicyCarryover):
            carryover = self.carryover.to_dict()
        else:
            carryover = self.carryover

        thresholds = self.thresholds.to_dict()

        grace_ratio = self.grace_ratio

        carryover_factor = self.carryover_factor

        current_usage = self.current_usage

        daily_usage_rate = self.daily_usage_rate

        usage_percentage = self.usage_percentage

        current_qos_status: Union[Unset, str] = UNSET
        if not isinstance(self.current_qos_status, Unset):
            current_qos_status = self.current_qos_status.value

        date_projections: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.date_projections, Unset):
            date_projections = self.date_projections.to_dict()

        preview_commands: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.preview_commands, Unset):
            preview_commands = []
            for preview_commands_item_data in self.preview_commands:
                preview_commands_item = preview_commands_item_data.to_dict()
                preview_commands.append(preview_commands_item)

        command_history: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.command_history, Unset):
            command_history = []
            for command_history_item_data in self.command_history:
                command_history_item = command_history_item_data.to_dict()
                command_history.append(command_history_item)

        billing_period_start: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period_start, Unset):
            billing_period_start = self.billing_period_start.isoformat()

        billing_period_end: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period_end, Unset):
            billing_period_end = self.billing_period_end.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_allocation": base_allocation,
                "effective_allocation": effective_allocation,
                "carryover_enabled": carryover_enabled,
                "carryover": carryover,
                "thresholds": thresholds,
                "grace_ratio": grace_ratio,
                "carryover_factor": carryover_factor,
            }
        )
        if current_usage is not UNSET:
            field_dict["current_usage"] = current_usage
        if daily_usage_rate is not UNSET:
            field_dict["daily_usage_rate"] = daily_usage_rate
        if usage_percentage is not UNSET:
            field_dict["usage_percentage"] = usage_percentage
        if current_qos_status is not UNSET:
            field_dict["current_qos_status"] = current_qos_status
        if date_projections is not UNSET:
            field_dict["date_projections"] = date_projections
        if preview_commands is not UNSET:
            field_dict["preview_commands"] = preview_commands
        if command_history is not UNSET:
            field_dict["command_history"] = command_history
        if billing_period_start is not UNSET:
            field_dict["billing_period_start"] = billing_period_start
        if billing_period_end is not UNSET:
            field_dict["billing_period_end"] = billing_period_end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slurm_command import SlurmCommand
        from ..models.slurm_command_history import SlurmCommandHistory
        from ..models.slurm_policy_carryover import SlurmPolicyCarryover
        from ..models.slurm_policy_date_projections import SlurmPolicyDateProjections
        from ..models.slurm_policy_thresholds import SlurmPolicyThresholds

        d = dict(src_dict)
        base_allocation = d.pop("base_allocation")

        effective_allocation = d.pop("effective_allocation")

        carryover_enabled = d.pop("carryover_enabled")

        def _parse_carryover(data: object) -> Union["SlurmPolicyCarryover", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                carryover_type_1 = SlurmPolicyCarryover.from_dict(data)

                return carryover_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SlurmPolicyCarryover", None], data)

        carryover = _parse_carryover(d.pop("carryover"))

        thresholds = SlurmPolicyThresholds.from_dict(d.pop("thresholds"))

        grace_ratio = d.pop("grace_ratio")

        carryover_factor = d.pop("carryover_factor")

        current_usage = d.pop("current_usage", UNSET)

        daily_usage_rate = d.pop("daily_usage_rate", UNSET)

        usage_percentage = d.pop("usage_percentage", UNSET)

        _current_qos_status = d.pop("current_qos_status", UNSET)
        current_qos_status: Union[Unset, CurrentQosStatusEnum]
        if isinstance(_current_qos_status, Unset):
            current_qos_status = UNSET
        else:
            current_qos_status = CurrentQosStatusEnum(_current_qos_status)

        _date_projections = d.pop("date_projections", UNSET)
        date_projections: Union[Unset, SlurmPolicyDateProjections]
        if isinstance(_date_projections, Unset):
            date_projections = UNSET
        else:
            date_projections = SlurmPolicyDateProjections.from_dict(_date_projections)

        preview_commands = []
        _preview_commands = d.pop("preview_commands", UNSET)
        for preview_commands_item_data in _preview_commands or []:
            preview_commands_item = SlurmCommand.from_dict(preview_commands_item_data)

            preview_commands.append(preview_commands_item)

        command_history = []
        _command_history = d.pop("command_history", UNSET)
        for command_history_item_data in _command_history or []:
            command_history_item = SlurmCommandHistory.from_dict(command_history_item_data)

            command_history.append(command_history_item)

        _billing_period_start = d.pop("billing_period_start", UNSET)
        billing_period_start: Union[Unset, datetime.date]
        if isinstance(_billing_period_start, Unset):
            billing_period_start = UNSET
        else:
            billing_period_start = isoparse(_billing_period_start).date()

        _billing_period_end = d.pop("billing_period_end", UNSET)
        billing_period_end: Union[Unset, datetime.date]
        if isinstance(_billing_period_end, Unset):
            billing_period_end = UNSET
        else:
            billing_period_end = isoparse(_billing_period_end).date()

        slurm_policy_preview_response = cls(
            base_allocation=base_allocation,
            effective_allocation=effective_allocation,
            carryover_enabled=carryover_enabled,
            carryover=carryover,
            thresholds=thresholds,
            grace_ratio=grace_ratio,
            carryover_factor=carryover_factor,
            current_usage=current_usage,
            daily_usage_rate=daily_usage_rate,
            usage_percentage=usage_percentage,
            current_qos_status=current_qos_status,
            date_projections=date_projections,
            preview_commands=preview_commands,
            command_history=command_history,
            billing_period_start=billing_period_start,
            billing_period_end=billing_period_end,
        )

        slurm_policy_preview_response.additional_properties = d
        return slurm_policy_preview_response

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
