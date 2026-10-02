from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_rollout_batch_dto_properties_agents_items_inline_customer_secrets_item_injection_mode import CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItemInjectionMode
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem")



@_attrs_define
class CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem:
    """ 
        Attributes:
            customer_secret_id (UUID): Existing customer secret (already created via POST /customer-secrets) to attach to
                this agent's ephemeral version.
            injection_mode (CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItemInjectionMode | Unset):
                Injection mode for this attachment. Must match the secret: 'proxy' if it has an upstream host and header, else
                'direct'. Omit to use the secret's mode.
     """

    customer_secret_id: UUID
    injection_mode: CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItemInjectionMode | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        customer_secret_id = str(self.customer_secret_id)

        injection_mode: str | Unset = UNSET
        if not isinstance(self.injection_mode, Unset):
            injection_mode = self.injection_mode.value



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "customerSecretId": customer_secret_id,
        })
        if injection_mode is not UNSET:
            field_dict["injectionMode"] = injection_mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        customer_secret_id = UUID(d.pop("customerSecretId"))




        _injection_mode = d.pop("injectionMode", UNSET)
        injection_mode: CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItemInjectionMode | Unset
        if isinstance(_injection_mode,  Unset):
            injection_mode = UNSET
        else:
            injection_mode = CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItemInjectionMode(_injection_mode)




        create_rollout_batch_dto_properties_agents_items_inline_customer_secrets_item = cls(
            customer_secret_id=customer_secret_id,
            injection_mode=injection_mode,
        )

        return create_rollout_batch_dto_properties_agents_items_inline_customer_secrets_item

