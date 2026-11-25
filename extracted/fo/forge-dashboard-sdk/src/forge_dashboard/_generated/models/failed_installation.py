from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge_error_kind import ForgeErrorKind
from ..types import UNSET, Unset






T = TypeVar("T", bound="FailedInstallation")



@_attrs_define
class FailedInstallation:
    """ One GitHub App installation that did not answer a refresh.

        Attributes:
            installation_id (int): GitHub's ID for the installation.
            error_kind (ForgeErrorKind): Why a forge is unreachable, or why a write to it was rejected, as
                coarse as every forge this service talks to can agree on.
                "unreachable" is a request that got no response; "upstream_error" is
                the forge answering with a 5xx (a gateway timeout, say), and the
                status is in ForgeHealth.upstreamStatus. "unauthorized" covers both a
                bad token and a forbidden request; "not_found" usually means a wrong
                instance URL. "conflict" is only ever returned from a pull-request
                write — the forge reports the PR itself isn't currently mergeable. "unknown" covers a signal this
                service doesn't recognize, rather than a guessed-at specific cause.
            account (str | Unset): The account or org the App is installed on. Omitted when it was never recorded.
     """

    installation_id: int
    error_kind: ForgeErrorKind
    account: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        installation_id = self.installation_id

        error_kind = self.error_kind.value

        account = self.account


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "installationId": installation_id,
            "errorKind": error_kind,
        })
        if account is not UNSET:
            field_dict["account"] = account

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        installation_id = d.pop("installationId")

        error_kind = ForgeErrorKind(d.pop("errorKind"))




        account = d.pop("account", UNSET)

        failed_installation = cls(
            installation_id=installation_id,
            error_kind=error_kind,
            account=account,
        )


        failed_installation.additional_properties = d
        return failed_installation

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
