from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_rollout_batch_dto_properties_agents_items_inline_kind import CreateRolloutBatchDtoPropertiesAgentsItemsInlineKind
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_config import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_customer_secrets_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem





T = TypeVar("T", bound="CreateRolloutBatchDtoPropertiesAgentsItemsInline")



@_attrs_define
class CreateRolloutBatchDtoPropertiesAgentsItemsInline:
    """ 
        Attributes:
            kind (CreateRolloutBatchDtoPropertiesAgentsItemsInlineKind): Materialize an ephemeral locked run-config version.
            name (str): Name for the ephemeral run-config identity.
            config (CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig): Run-config payload shared by agent-harness and
                snapshot types. Container, invocation, and limit primitives the platform passes through verbatim without
                inspecting the harness shape.
            timeout_seconds (int | Unset): Per-agent container timeout override. Omit to use the batch-level timeoutSeconds,
                then the run-config version default.
            customer_secrets (list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem] | Unset): Existing
                customer secrets to attach to this agent's ephemeral run-config version at dispatch time, referenced by id — no
                secret value is ever accepted here. Resolved by the run_config_run leaf at submit time via the same mechanism a
                versionRef agent already gets automatically.
     """

    kind: CreateRolloutBatchDtoPropertiesAgentsItemsInlineKind
    name: str
    config: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig
    timeout_seconds: int | Unset = UNSET
    customer_secrets: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_customer_secrets_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem # noqa: PLC0415
        kind = self.kind.value

        name = self.name

        config = self.config.to_dict()

        timeout_seconds = self.timeout_seconds

        customer_secrets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.customer_secrets, Unset):
            customer_secrets = []
            for customer_secrets_item_data in self.customer_secrets:
                customer_secrets_item = customer_secrets_item_data.to_dict()
                customer_secrets.append(customer_secrets_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "name": name,
            "config": config,
        })
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if customer_secrets is not UNSET:
            field_dict["customerSecrets"] = customer_secrets

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_customer_secrets_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem # noqa: PLC0415
        d = dict(src_dict)
        kind = CreateRolloutBatchDtoPropertiesAgentsItemsInlineKind(d.pop("kind"))




        name = d.pop("name")

        config = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig.from_dict(d.pop("config"))




        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        _customer_secrets = d.pop("customerSecrets", UNSET)
        customer_secrets: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem] | Unset = UNSET
        if _customer_secrets is not UNSET:
            customer_secrets = []
            for customer_secrets_item_data in _customer_secrets:
                customer_secrets_item = CreateRolloutBatchDtoPropertiesAgentsItemsInlineCustomerSecretsItem.from_dict(customer_secrets_item_data)



                customer_secrets.append(customer_secrets_item)


        create_rollout_batch_dto_properties_agents_items_inline = cls(
            kind=kind,
            name=name,
            config=config,
            timeout_seconds=timeout_seconds,
            customer_secrets=customer_secrets,
        )

        return create_rollout_batch_dto_properties_agents_items_inline

