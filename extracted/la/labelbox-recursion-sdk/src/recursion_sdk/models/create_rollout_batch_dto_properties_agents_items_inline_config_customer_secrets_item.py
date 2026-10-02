from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem")



@_attrs_define
class CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem:
    """ Declaration that a run-config payload expects an env-var-named customer secret to be injected at runtime. Carries
    only the name; credentials are resolved at submit time.

        Attributes:
            env_var_name (str): Env-var name (uppercase + digits + underscore, leading letter) the harness expects to
                receive at runtime; resolved against attached customer secrets at job-submit time.
     """

    env_var_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        env_var_name = self.env_var_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "envVarName": env_var_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        env_var_name = d.pop("envVarName")

        create_rollout_batch_dto_properties_agents_items_inline_config_customer_secrets_item = cls(
            env_var_name=env_var_name,
        )


        create_rollout_batch_dto_properties_agents_items_inline_config_customer_secrets_item.additional_properties = d
        return create_rollout_batch_dto_properties_agents_items_inline_config_customer_secrets_item

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
