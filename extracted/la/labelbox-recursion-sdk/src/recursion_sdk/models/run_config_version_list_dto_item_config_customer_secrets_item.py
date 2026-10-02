from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RunConfigVersionListDtoItemConfigCustomerSecretsItem")



@_attrs_define
class RunConfigVersionListDtoItemConfigCustomerSecretsItem:
    """ Declaration that a run-config payload expects an env-var-named customer secret to be injected at runtime. Carries
    only the name; credentials are resolved at submit time.

        Attributes:
            env_var_name (str): Env-var name (uppercase + digits + underscore, leading letter) the harness expects to
                receive at runtime; resolved against attached customer secrets at job-submit time.
     """

    env_var_name: str





    def to_dict(self) -> dict[str, Any]:
        env_var_name = self.env_var_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "envVarName": env_var_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        env_var_name = d.pop("envVarName")

        run_config_version_list_dto_item_config_customer_secrets_item = cls(
            env_var_name=env_var_name,
        )

        return run_config_version_list_dto_item_config_customer_secrets_item

