from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_rollout_batch_dto_properties_agents_items_inline import CreateRolloutBatchDtoPropertiesAgentsItemsInline
  from ..models.create_rollout_batch_dto_properties_agents_items_version_ref import CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef
  from ..models.create_rollout_batch_dto_properties_dataset_file_ref import CreateRolloutBatchDtoPropertiesDatasetFileRef
  from ..models.create_rollout_batch_dto_properties_dataset_inline import CreateRolloutBatchDtoPropertiesDatasetInline





T = TypeVar("T", bound="CreateRolloutBatchDto")



@_attrs_define
class CreateRolloutBatchDto:
    """ Create-request body for a rollout_batch: dataset (M items) x agents (N specs). organizationId is stamped from the
    route.

        Example:
            {'runName': 'ci-nightly-rollouts', 'dataset': {'kind': 'inline', 'items': [{'prompt': 'hello world'}]},
                'agents': [{'kind': 'versionRef', 'runConfigVersionId': '11111111-1111-4111-8111-111111111111'}]}

        Attributes:
            run_name (str): Human-readable name for the batch.
            dataset (CreateRolloutBatchDtoPropertiesDatasetFileRef | CreateRolloutBatchDtoPropertiesDatasetInline): The
                dataset (M items) to run every agent against.
            agents (list[CreateRolloutBatchDtoPropertiesAgentsItemsInline |
                CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef]): Agent specs under test (N). Every item × every agent is
                run.
            timeout_seconds (int | Unset): Batch-level container timeout override, applied to every child unless overridden
                per-agent (inline agents only).
            concurrency (int | Unset): Maximum rollouts this batch keeps alive on the agent service at once (1-75). Omitted
                means the platform default applies.
     """

    run_name: str
    dataset: CreateRolloutBatchDtoPropertiesDatasetFileRef | CreateRolloutBatchDtoPropertiesDatasetInline
    agents: list[CreateRolloutBatchDtoPropertiesAgentsItemsInline | CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef]
    timeout_seconds: int | Unset = UNSET
    concurrency: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_rollout_batch_dto_properties_agents_items_inline import CreateRolloutBatchDtoPropertiesAgentsItemsInline # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_version_ref import CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_dataset_file_ref import CreateRolloutBatchDtoPropertiesDatasetFileRef # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_dataset_inline import CreateRolloutBatchDtoPropertiesDatasetInline # noqa: PLC0415
        run_name = self.run_name

        dataset: dict[str, Any]
        if isinstance(self.dataset, CreateRolloutBatchDtoPropertiesDatasetInline):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset.to_dict()


        agents = []
        for agents_item_data in self.agents:
            agents_item: dict[str, Any]
            if isinstance(agents_item_data, CreateRolloutBatchDtoPropertiesAgentsItemsInline):
                agents_item = agents_item_data.to_dict()
            else:
                agents_item = agents_item_data.to_dict()

            agents.append(agents_item)



        timeout_seconds = self.timeout_seconds

        concurrency = self.concurrency


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runName": run_name,
            "dataset": dataset,
            "agents": agents,
        })
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if concurrency is not UNSET:
            field_dict["concurrency"] = concurrency

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_rollout_batch_dto_properties_agents_items_inline import CreateRolloutBatchDtoPropertiesAgentsItemsInline # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_version_ref import CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_dataset_file_ref import CreateRolloutBatchDtoPropertiesDatasetFileRef # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_dataset_inline import CreateRolloutBatchDtoPropertiesDatasetInline # noqa: PLC0415
        d = dict(src_dict)
        run_name = d.pop("runName")

        def _parse_dataset(data: object) -> CreateRolloutBatchDtoPropertiesDatasetFileRef | CreateRolloutBatchDtoPropertiesDatasetInline:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_type_0 = CreateRolloutBatchDtoPropertiesDatasetInline.from_dict(data)



                return dataset_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            dataset_type_1 = CreateRolloutBatchDtoPropertiesDatasetFileRef.from_dict(data)



            return dataset_type_1

        dataset = _parse_dataset(d.pop("dataset"))


        agents = []
        _agents = d.pop("agents")
        for agents_item_data in (_agents):
            def _parse_agents_item(data: object) -> CreateRolloutBatchDtoPropertiesAgentsItemsInline | CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    agents_item_type_0 = CreateRolloutBatchDtoPropertiesAgentsItemsInline.from_dict(data)



                    return agents_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                agents_item_type_1 = CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef.from_dict(data)



                return agents_item_type_1

            agents_item = _parse_agents_item(agents_item_data)

            agents.append(agents_item)


        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        concurrency = d.pop("concurrency", UNSET)

        create_rollout_batch_dto = cls(
            run_name=run_name,
            dataset=dataset,
            agents=agents,
            timeout_seconds=timeout_seconds,
            concurrency=concurrency,
        )

        return create_rollout_batch_dto

