from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DispatchRunRequest")


@_attrs_define
class DispatchRunRequest:
    """
    Attributes:
        run_authorization_jwt (str): Scheduler-signed RunAuthorizationJwt
    """

    run_authorization_jwt: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_authorization_jwt = self.run_authorization_jwt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "run_authorization_jwt": run_authorization_jwt,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_authorization_jwt = d.pop("run_authorization_jwt")

        dispatch_run_request = cls(
            run_authorization_jwt=run_authorization_jwt,
        )

        dispatch_run_request.additional_properties = d
        return dispatch_run_request

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
