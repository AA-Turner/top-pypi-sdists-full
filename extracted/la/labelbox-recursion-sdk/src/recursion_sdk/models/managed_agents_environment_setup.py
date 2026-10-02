from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsEnvironmentSetup")



@_attrs_define
class ManagedAgentsEnvironmentSetup:
    """ Post-provision customization of a sandbox: a bash script run before the agent starts. Set it when the agent needs
    packages, tools, or state the runner image does not ship; leave it empty to start from the image as is. Verify it
    with a setup run before sessions use the environment.

        Example:
            {'script': 'example', 'timeout_seconds': 1}

        Attributes:
            script (str | Unset): Bash script run after the sandbox is provisioned and before the agent starts. When a Runs
                session's verified captured image has an older runner base, setup runs once on that session's compute. It does
                not rerun after a container restart or move; a changed container generation prevents further sandbox work in
                that session. Re-test the environment to capture a compatible image, then start a new session. Executed as a
                separate login shell with set -eo pipefail, so the first failing line fails the run and is reported by line
                number; exports and activation do not persist into agent commands. Managed images automatically select a
                /workspace/.venv created here: install through its explicit interpreter and preserve the existing PATH. Do not
                wrap lines in bash -lc; the script already runs under bash. Empty means no setup. At most 64 KiB.
            timeout_seconds (int | Unset): Wall-clock bound in seconds on the whole script; 0 uses the default of 600.
                Between 10 and 3600 when set. A run that exceeds it fails with exit code 124.
     """

    script: str | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        script = self.script

        timeout_seconds = self.timeout_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if script is not UNSET:
            field_dict["script"] = script
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        script = d.pop("script", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        managed_agents_environment_setup = cls(
            script=script,
            timeout_seconds=timeout_seconds,
        )


        managed_agents_environment_setup.additional_properties = d
        return managed_agents_environment_setup

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
