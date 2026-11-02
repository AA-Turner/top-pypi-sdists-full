from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cloud_agent_harness_request import CloudAgentHarnessRequest
    from ..models.cloud_agent_runtime_reference import CloudAgentRuntimeReference
    from ..models.managed_model_provider_reference import ManagedModelProviderReference
    from ..models.runtime_repository_selection import RuntimeRepositorySelection


T = TypeVar("T", bound="CreateCloudAgentRequest")


@_attrs_define
class CreateCloudAgentRequest:
    """
    Attributes:
        model_provider (ManagedModelProviderReference):
        name (str | Unset):
        system_prompt (str | Unset):
        initial_message (str | Unset):
        repositories (list[RuntimeRepositorySelection] | Unset): Ordered GitHub repositories to initialize for fresh or
            checkpoint runtimes. The first is the default workspace. Nonempty selections are not allowed for existing
            runtimes.
        runtime (CloudAgentRuntimeReference | Unset):
        harness (CloudAgentHarnessRequest | Unset):
    """

    model_provider: ManagedModelProviderReference
    name: str | Unset = UNSET
    system_prompt: str | Unset = UNSET
    initial_message: str | Unset = UNSET
    repositories: list[RuntimeRepositorySelection] | Unset = UNSET
    runtime: CloudAgentRuntimeReference | Unset = UNSET
    harness: CloudAgentHarnessRequest | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        model_provider = self.model_provider.to_dict()

        name = self.name

        system_prompt = self.system_prompt

        initial_message = self.initial_message

        repositories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.repositories, Unset):
            repositories = []
            for repositories_item_data in self.repositories:
                repositories_item = repositories_item_data.to_dict()
                repositories.append(repositories_item)

        runtime: dict[str, Any] | Unset = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.to_dict()

        harness: dict[str, Any] | Unset = UNSET
        if not isinstance(self.harness, Unset):
            harness = self.harness.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model_provider": model_provider,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if system_prompt is not UNSET:
            field_dict["system_prompt"] = system_prompt
        if initial_message is not UNSET:
            field_dict["initial_message"] = initial_message
        if repositories is not UNSET:
            field_dict["repositories"] = repositories
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if harness is not UNSET:
            field_dict["harness"] = harness

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_agent_harness_request import CloudAgentHarnessRequest
        from ..models.cloud_agent_runtime_reference import CloudAgentRuntimeReference
        from ..models.managed_model_provider_reference import (
            ManagedModelProviderReference,
        )
        from ..models.runtime_repository_selection import RuntimeRepositorySelection

        d = dict(src_dict)
        model_provider = ManagedModelProviderReference.from_dict(
            d.pop("model_provider")
        )

        name = d.pop("name", UNSET)

        system_prompt = d.pop("system_prompt", UNSET)

        initial_message = d.pop("initial_message", UNSET)

        _repositories = d.pop("repositories", UNSET)
        repositories: list[RuntimeRepositorySelection] | Unset = UNSET
        if _repositories is not UNSET:
            repositories = []
            for repositories_item_data in _repositories:
                repositories_item = RuntimeRepositorySelection.from_dict(
                    repositories_item_data
                )

                repositories.append(repositories_item)

        _runtime = d.pop("runtime", UNSET)
        runtime: CloudAgentRuntimeReference | Unset
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = CloudAgentRuntimeReference.from_dict(_runtime)

        _harness = d.pop("harness", UNSET)
        harness: CloudAgentHarnessRequest | Unset
        if isinstance(_harness, Unset):
            harness = UNSET
        else:
            harness = CloudAgentHarnessRequest.from_dict(_harness)

        create_cloud_agent_request = cls(
            model_provider=model_provider,
            name=name,
            system_prompt=system_prompt,
            initial_message=initial_message,
            repositories=repositories,
            runtime=runtime,
            harness=harness,
        )

        return create_cloud_agent_request
