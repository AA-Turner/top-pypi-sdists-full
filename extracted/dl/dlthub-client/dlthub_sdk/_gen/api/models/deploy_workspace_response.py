from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jobs_deploy_receipt import JobsDeployReceipt


T = TypeVar("T", bound="DeployWorkspaceResponse")


@_attrs_define
class DeployWorkspaceResponse:
    """
    Attributes:
        job_receipt (JobsDeployReceipt): What the deploy did to jobs.
        warnings (list[str]): Validation warnings.
        deployment_module (None | str | Unset): The deployment module the deploy was scoped to.
    """

    job_receipt: JobsDeployReceipt
    warnings: list[str]
    deployment_module: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_receipt = self.job_receipt.to_dict()

        warnings = self.warnings

        deployment_module: None | str | Unset
        if isinstance(self.deployment_module, Unset):
            deployment_module = UNSET
        else:
            deployment_module = self.deployment_module

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_receipt": job_receipt,
                "warnings": warnings,
            }
        )
        if deployment_module is not UNSET:
            field_dict["deployment_module"] = deployment_module

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.jobs_deploy_receipt import JobsDeployReceipt

        d = dict(src_dict)
        job_receipt = JobsDeployReceipt.from_dict(d.pop("job_receipt"))

        warnings = cast(list[str], d.pop("warnings"))

        def _parse_deployment_module(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        deployment_module = _parse_deployment_module(d.pop("deployment_module", UNSET))

        deploy_workspace_response = cls(
            job_receipt=job_receipt,
            warnings=warnings,
            deployment_module=deployment_module,
        )

        deploy_workspace_response.additional_properties = d
        return deploy_workspace_response

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
