from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session_usage import ManagedAgentsSessionUsage





T = TypeVar("T", bound="ManagedAgentsSessionUsageListResponse")



@_attrs_define
class ManagedAgentsSessionUsageListResponse:
    """ Response body of GET /v1/sessions/usage: token and cost totals for an explicit batch of session ids, so a list view
    can show a cost per row without reading every session's events. session_ids is required and bounded; too many ids is
    rejected outright rather than truncated, because a silently short answer is indistinguishable from idle sessions.

        Example:
            {'session_usage': [{'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_micros': 1, 'event_count': 1,
                'input_tokens': 1, 'output_tokens': 1, 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}

        Attributes:
            session_usage (list[ManagedAgentsSessionUsage] | None): One roll-up row per requested session id that the caller
                can see. Null rather than an empty array when none of the requested ids resolved. Ids naming nothing visible are
                omitted, so the result may be shorter than session_ids and the order should not be assumed to match.
     """

    session_usage: list[ManagedAgentsSessionUsage] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_usage import ManagedAgentsSessionUsage # noqa: PLC0415
        session_usage: list[dict[str, Any]] | None
        if isinstance(self.session_usage, list):
            session_usage = []
            for session_usage_type_0_item_data in self.session_usage:
                session_usage_type_0_item = session_usage_type_0_item_data.to_dict()
                session_usage.append(session_usage_type_0_item)


        else:
            session_usage = self.session_usage


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "session_usage": session_usage,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_usage import ManagedAgentsSessionUsage # noqa: PLC0415
        d = dict(src_dict)
        def _parse_session_usage(data: object) -> list[ManagedAgentsSessionUsage] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                session_usage_type_0 = []
                _session_usage_type_0 = data
                for session_usage_type_0_item_data in (_session_usage_type_0):
                    session_usage_type_0_item = ManagedAgentsSessionUsage.from_dict(session_usage_type_0_item_data)



                    session_usage_type_0.append(session_usage_type_0_item)

                return session_usage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSessionUsage] | None, data)

        session_usage = _parse_session_usage(d.pop("session_usage"))


        managed_agents_session_usage_list_response = cls(
            session_usage=session_usage,
        )


        managed_agents_session_usage_list_response.additional_properties = d
        return managed_agents_session_usage_list_response

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
