from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateRunConfigDtoConfigComputeEnvRunVerbs")



@_attrs_define
class CreateRunConfigDtoConfigComputeEnvRunVerbs:
    """ Image-supplied solver-lifecycle verb scripts. Omit to use the platform default verbs.

        Attributes:
            reset (str): Terminate any in-flight agent and clear prior-run state (idempotent).
            submit (str): Launch the agent on $PROMPT, detached; the platform polls status afterward.
            status (str): Print exactly one ComputeRunPhase token to stdout.
            result (str): Print the successful run result to stdout (read on completed).
            error (str): Print failure diagnostics to stdout (read on failed).
            readiness (str | Unset): Optional child-container readiness probe; prints a verdict token before launch.
     """

    reset: str
    submit: str
    status: str
    result: str
    error: str
    readiness: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        reset = self.reset

        submit = self.submit

        status = self.status

        result = self.result

        error = self.error

        readiness = self.readiness


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "reset": reset,
            "submit": submit,
            "status": status,
            "result": result,
            "error": error,
        })
        if readiness is not UNSET:
            field_dict["readiness"] = readiness

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reset = d.pop("reset")

        submit = d.pop("submit")

        status = d.pop("status")

        result = d.pop("result")

        error = d.pop("error")

        readiness = d.pop("readiness", UNSET)

        create_run_config_dto_config_compute_env_run_verbs = cls(
            reset=reset,
            submit=submit,
            status=status,
            result=result,
            error=error,
            readiness=readiness,
        )


        create_run_config_dto_config_compute_env_run_verbs.additional_properties = d
        return create_run_config_dto_config_compute_env_run_verbs

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
