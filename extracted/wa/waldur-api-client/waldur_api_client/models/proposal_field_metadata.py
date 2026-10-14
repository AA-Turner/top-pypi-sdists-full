from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.proposal_field_state_enum import ProposalFieldStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProposalFieldMetadata")


@_attrs_define
class ProposalFieldMetadata:
    """
    Attributes:
        field (Union[Unset, str]):
        state (Union[Unset, ProposalFieldStateEnum]):
        allowed_states (Union[Unset, list[str]]):
        locked_reason (Union[None, Unset, str]):
        usage (Union[Unset, list[str]]):
    """

    field: Union[Unset, str] = UNSET
    state: Union[Unset, ProposalFieldStateEnum] = UNSET
    allowed_states: Union[Unset, list[str]] = UNSET
    locked_reason: Union[None, Unset, str] = UNSET
    usage: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        allowed_states: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_states, Unset):
            allowed_states = self.allowed_states

        locked_reason: Union[None, Unset, str]
        if isinstance(self.locked_reason, Unset):
            locked_reason = UNSET
        else:
            locked_reason = self.locked_reason

        usage: Union[Unset, list[str]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field is not UNSET:
            field_dict["field"] = field
        if state is not UNSET:
            field_dict["state"] = state
        if allowed_states is not UNSET:
            field_dict["allowed_states"] = allowed_states
        if locked_reason is not UNSET:
            field_dict["locked_reason"] = locked_reason
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, ProposalFieldStateEnum]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = ProposalFieldStateEnum(_state)

        allowed_states = cast(list[str], d.pop("allowed_states", UNSET))

        def _parse_locked_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        locked_reason = _parse_locked_reason(d.pop("locked_reason", UNSET))

        usage = cast(list[str], d.pop("usage", UNSET))

        proposal_field_metadata = cls(
            field=field,
            state=state,
            allowed_states=allowed_states,
            locked_reason=locked_reason,
            usage=usage,
        )

        proposal_field_metadata.additional_properties = d
        return proposal_field_metadata

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
