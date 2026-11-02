from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.secret_egress_injection import SecretEgressInjection
    from ..models.secret_environment_injection import SecretEnvironmentInjection
    from ..models.secret_file_injection import SecretFileInjection


T = TypeVar("T", bound="RuntimeSecretConfiguration")


@_attrs_define
class RuntimeSecretConfiguration:
    """Inline injection configuration for one tenant secret.

    Attributes:
        secret_id (str):
        environment (list[SecretEnvironmentInjection] | Unset):
        egress_rules (list[SecretEgressInjection] | Unset):
        files (list[SecretFileInjection] | Unset):
    """

    secret_id: str
    environment: list[SecretEnvironmentInjection] | Unset = UNSET
    egress_rules: list[SecretEgressInjection] | Unset = UNSET
    files: list[SecretFileInjection] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        secret_id = self.secret_id

        environment: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.environment, Unset):
            environment = []
            for environment_item_data in self.environment:
                environment_item = environment_item_data.to_dict()
                environment.append(environment_item)

        egress_rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.egress_rules, Unset):
            egress_rules = []
            for egress_rules_item_data in self.egress_rules:
                egress_rules_item = egress_rules_item_data.to_dict()
                egress_rules.append(egress_rules_item)

        files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "secret_id": secret_id,
            }
        )
        if environment is not UNSET:
            field_dict["environment"] = environment
        if egress_rules is not UNSET:
            field_dict["egress_rules"] = egress_rules
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.secret_egress_injection import SecretEgressInjection
        from ..models.secret_environment_injection import SecretEnvironmentInjection
        from ..models.secret_file_injection import SecretFileInjection

        d = dict(src_dict)
        secret_id = d.pop("secret_id")

        _environment = d.pop("environment", UNSET)
        environment: list[SecretEnvironmentInjection] | Unset = UNSET
        if _environment is not UNSET:
            environment = []
            for environment_item_data in _environment:
                environment_item = SecretEnvironmentInjection.from_dict(
                    environment_item_data
                )

                environment.append(environment_item)

        _egress_rules = d.pop("egress_rules", UNSET)
        egress_rules: list[SecretEgressInjection] | Unset = UNSET
        if _egress_rules is not UNSET:
            egress_rules = []
            for egress_rules_item_data in _egress_rules:
                egress_rules_item = SecretEgressInjection.from_dict(
                    egress_rules_item_data
                )

                egress_rules.append(egress_rules_item)

        _files = d.pop("files", UNSET)
        files: list[SecretFileInjection] | Unset = UNSET
        if _files is not UNSET:
            files = []
            for files_item_data in _files:
                files_item = SecretFileInjection.from_dict(files_item_data)

                files.append(files_item)

        runtime_secret_configuration = cls(
            secret_id=secret_id,
            environment=environment,
            egress_rules=egress_rules,
            files=files,
        )

        return runtime_secret_configuration
