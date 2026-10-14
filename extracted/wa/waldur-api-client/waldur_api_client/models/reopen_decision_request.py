import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReopenDecisionRequest")


@_attrs_define
class ReopenDecisionRequest:
    """
    Attributes:
        reason (str): Why the held decision is taken back, e.g. the board changed the outcome when adopting the list.
            Never sent to the applicant and kept out of the proposal's event feed, which the applicant team reads; recorded
            in the server log.
        deadline (Union[None, Unset, datetime.datetime]): New deadline for the decision. Without one, a deadline that
            has passed is cleared and one still ahead is kept.
    """

    reason: str
    deadline: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        deadline: Union[None, Unset, str]
        if isinstance(self.deadline, Unset):
            deadline = UNSET
        elif isinstance(self.deadline, datetime.datetime):
            deadline = self.deadline.isoformat()
        else:
            deadline = self.deadline

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
            }
        )
        if deadline is not UNSET:
            field_dict["deadline"] = deadline

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        def _parse_deadline(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deadline_type_0 = isoparse(data)

                return deadline_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        deadline = _parse_deadline(d.pop("deadline", UNSET))

        reopen_decision_request = cls(
            reason=reason,
            deadline=deadline,
        )

        reopen_decision_request.additional_properties = d
        return reopen_decision_request

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
