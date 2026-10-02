from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupWarning")



@_attrs_define
class ManagedAgentsEnvironmentSetupWarning:
    """ An advisory finding about a setup script line. Warnings never block a save.

        Example:
            {'code': 'example', 'line': 1, 'message': 'example'}

        Attributes:
            code (str): Stable identifier: bash_lc_wrapper, curl_pipe_sh, unpinned_install, rm_rf_root (line findings);
                verify_not_started (line 0: the save succeeded but the run requested with verify=true could not be started; call
                createEnvironmentSetupRun); or legacy_setup_discarded (line 0: the stored setup predates setup.script and does
                not run; re-enter it as a script).
            line (int): 1-based script line the finding is on; 0 when the finding is about the save rather than a line.
            message (str): What was found and the recommended change.
     """

    code: str
    line: int
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        line = self.line

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "line": line,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        line = d.pop("line")

        message = d.pop("message")

        managed_agents_environment_setup_warning = cls(
            code=code,
            line=line,
            message=message,
        )


        managed_agents_environment_setup_warning.additional_properties = d
        return managed_agents_environment_setup_warning

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
