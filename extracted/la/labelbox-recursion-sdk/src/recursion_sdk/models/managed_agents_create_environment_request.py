from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_create_environment_request_config import ManagedAgentsCreateEnvironmentRequestConfig
  from ..models.managed_agents_create_environment_request_env_vars import ManagedAgentsCreateEnvironmentRequestEnvVars
  from ..models.managed_agents_create_environment_request_metadata import ManagedAgentsCreateEnvironmentRequestMetadata
  from ..models.managed_agents_create_environment_request_network_policy_type_0 import ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0
  from ..models.managed_agents_create_environment_request_secrets import ManagedAgentsCreateEnvironmentRequestSecrets
  from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount
  from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources
  from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup





T = TypeVar("T", bound="ManagedAgentsCreateEnvironmentRequest")



@_attrs_define
class ManagedAgentsCreateEnvironmentRequest:
    """ Request body for creating an environment: the sandbox image, setup, compute sizing, networking, and lifecycle a
    session's sandbox is provisioned from. Server-managed fields are not accepted.

        Example:
            {'computer_use': True, 'config': {'key': 'example'}, 'description': 'example', 'env_vars': {'key': 'example'},
                'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key': 'example'}, 'mounts':
                [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-name', 'network_policy': {'key': 'example'},
                'privileged': True, 'provider': 'example', 'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name':
                'example-name', 'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
                'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'], 'regions': ['example']},
                'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key': 'example'}, 'setup': {'script': 'example',
                'timeout_seconds': 1}, 'stopped_delete_after_seconds': 1}

        Attributes:
            name (str): Human-readable label for the environment. Required.
            provider (str): Environment runtime: runs (managed agent runner) or docker (local development). Any other value
                is rejected, including the retired self_hosted and rma names.
            computer_use (bool | None | Unset): Enable the shared interactive browser display. The server sets http_port to
                6901; false disables it.
            config (ManagedAgentsCreateEnvironmentRequestConfig | Unset): Provider-specific overflow config.
            description (str | Unset): Optional free-text note about what this environment is for.
            env_vars (ManagedAgentsCreateEnvironmentRequestEnvVars | Unset): Environment variables injected into the
                sandbox.
            http_port (int | None | Unset): TCP port inside the sandbox that the provider exposes for HTTP traffic. Omit or
                send 0 if the workload serves nothing.
            idle_stop_after_seconds (int | Unset): Seconds of inactivity after which the sandbox is stopped. Omit or send 0
                to use the provider's lifecycle policy instead of a per-environment one. Computer use requires 0 or at least 600
                seconds.
            image (str | Unset): Container/sandbox image the runtime runs in.
            metadata (ManagedAgentsCreateEnvironmentRequestMetadata | Unset): Free-form caller-owned JSON stored with the
                environment and returned on reads. Not interpreted by the service.
            mounts (list[ManagedAgentsEnvironmentMount] | Unset): Files staged into the sandbox workspace on create.
            network_policy (ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0 | None | Unset): Runs egress policy.
                Omit or send null to derive deny-all. A nonempty policy requires GKE: the runtime selects GKE when placement is
                omitted, or accepts explicit GKE placement. With explicit non-GKE placement, send {} for unrestricted egress or
                change placement to GKE.
            privileged (bool | None | Unset): Whether the Runs sandbox may use privileged Docker. Defaults to false
                independently of network_policy. Compute creation fails closed unless Agent Service can enforce the requested
                combination.
            pvc_size_gi (int | Unset): Size in gibibytes of the persistent volume attached to the sandbox workspace. Omit or
                send 0 to let the sandbox provider choose.
            resources (ManagedAgentsEnvironmentResources | Unset): Compute sizing and lifetime for an environment's sandbox.
                CPU environments accept caller-selected CPU and memory. GPU environments accept an exclusive accelerator plus
                optional lifetime and placement constraints, but use service-owned limits of 8,000 millicores (8 vCPU) and
                32,768 MiB (32 GiB) of memory. Example: {'accelerator': {'count': 1, 'name': 'example-name', 'type': 'example'},
                'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True, 'max_price_per_hour_usd': 1.5,
                'min_accelerator_vram_gb': 1, 'providers': ['example'], 'regions': ['example']}, 'timeout_seconds': 1}.
            scope (str | Unset): Visibility of the environment record within the organization. Defaults to organization when
                omitted.
            secrets (ManagedAgentsCreateEnvironmentRequestSecrets | Unset): Env-var name -> secret-manager reference (never
                plaintext).
            setup (ManagedAgentsEnvironmentSetup | Unset): Post-provision customization of a sandbox: a bash script run
                before the agent starts. Set it when the agent needs packages, tools, or state the runner image does not ship;
                leave it empty to start from the image as is. Verify it with a setup run before sessions use the environment.
                Example: {'script': 'example', 'timeout_seconds': 1}.
            stopped_delete_after_seconds (int | Unset): Seconds a stopped sandbox is retained before deletion, after which
                its workspace is gone. Omit or send 0 to use the provider's lifecycle policy.
     """

    name: str
    provider: str
    computer_use: bool | None | Unset = UNSET
    config: ManagedAgentsCreateEnvironmentRequestConfig | Unset = UNSET
    description: str | Unset = UNSET
    env_vars: ManagedAgentsCreateEnvironmentRequestEnvVars | Unset = UNSET
    http_port: int | None | Unset = UNSET
    idle_stop_after_seconds: int | Unset = UNSET
    image: str | Unset = UNSET
    metadata: ManagedAgentsCreateEnvironmentRequestMetadata | Unset = UNSET
    mounts: list[ManagedAgentsEnvironmentMount] | Unset = UNSET
    network_policy: ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0 | None | Unset = UNSET
    privileged: bool | None | Unset = UNSET
    pvc_size_gi: int | Unset = UNSET
    resources: ManagedAgentsEnvironmentResources | Unset = UNSET
    scope: str | Unset = UNSET
    secrets: ManagedAgentsCreateEnvironmentRequestSecrets | Unset = UNSET
    setup: ManagedAgentsEnvironmentSetup | Unset = UNSET
    stopped_delete_after_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_create_environment_request_config import ManagedAgentsCreateEnvironmentRequestConfig # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_env_vars import ManagedAgentsCreateEnvironmentRequestEnvVars # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_metadata import ManagedAgentsCreateEnvironmentRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_network_policy_type_0 import ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0 # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_secrets import ManagedAgentsCreateEnvironmentRequestSecrets # noqa: PLC0415
        from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount # noqa: PLC0415
        from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources # noqa: PLC0415
        from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup # noqa: PLC0415
        name = self.name

        provider = self.provider

        computer_use: bool | None | Unset
        if isinstance(self.computer_use, Unset):
            computer_use = UNSET
        else:
            computer_use = self.computer_use

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        description = self.description

        env_vars: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = self.env_vars.to_dict()

        http_port: int | None | Unset
        if isinstance(self.http_port, Unset):
            http_port = UNSET
        else:
            http_port = self.http_port

        idle_stop_after_seconds = self.idle_stop_after_seconds

        image = self.image

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        mounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.mounts, Unset):
            mounts = []
            for mounts_item_data in self.mounts:
                mounts_item = mounts_item_data.to_dict()
                mounts.append(mounts_item)



        network_policy: dict[str, Any] | None | Unset
        if isinstance(self.network_policy, Unset):
            network_policy = UNSET
        elif isinstance(self.network_policy, ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0):
            network_policy = self.network_policy.to_dict()
        else:
            network_policy = self.network_policy

        privileged: bool | None | Unset
        if isinstance(self.privileged, Unset):
            privileged = UNSET
        else:
            privileged = self.privileged

        pvc_size_gi = self.pvc_size_gi

        resources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources.to_dict()

        scope = self.scope

        secrets: dict[str, Any] | Unset = UNSET
        if not isinstance(self.secrets, Unset):
            secrets = self.secrets.to_dict()

        setup: dict[str, Any] | Unset = UNSET
        if not isinstance(self.setup, Unset):
            setup = self.setup.to_dict()

        stopped_delete_after_seconds = self.stopped_delete_after_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "provider": provider,
        })
        if computer_use is not UNSET:
            field_dict["computer_use"] = computer_use
        if config is not UNSET:
            field_dict["config"] = config
        if description is not UNSET:
            field_dict["description"] = description
        if env_vars is not UNSET:
            field_dict["env_vars"] = env_vars
        if http_port is not UNSET:
            field_dict["http_port"] = http_port
        if idle_stop_after_seconds is not UNSET:
            field_dict["idle_stop_after_seconds"] = idle_stop_after_seconds
        if image is not UNSET:
            field_dict["image"] = image
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if mounts is not UNSET:
            field_dict["mounts"] = mounts
        if network_policy is not UNSET:
            field_dict["network_policy"] = network_policy
        if privileged is not UNSET:
            field_dict["privileged"] = privileged
        if pvc_size_gi is not UNSET:
            field_dict["pvc_size_gi"] = pvc_size_gi
        if resources is not UNSET:
            field_dict["resources"] = resources
        if scope is not UNSET:
            field_dict["scope"] = scope
        if secrets is not UNSET:
            field_dict["secrets"] = secrets
        if setup is not UNSET:
            field_dict["setup"] = setup
        if stopped_delete_after_seconds is not UNSET:
            field_dict["stopped_delete_after_seconds"] = stopped_delete_after_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_create_environment_request_config import ManagedAgentsCreateEnvironmentRequestConfig # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_env_vars import ManagedAgentsCreateEnvironmentRequestEnvVars # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_metadata import ManagedAgentsCreateEnvironmentRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_network_policy_type_0 import ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0 # noqa: PLC0415
        from ..models.managed_agents_create_environment_request_secrets import ManagedAgentsCreateEnvironmentRequestSecrets # noqa: PLC0415
        from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount # noqa: PLC0415
        from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources # noqa: PLC0415
        from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        provider = d.pop("provider")

        def _parse_computer_use(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        computer_use = _parse_computer_use(d.pop("computer_use", UNSET))


        _config = d.pop("config", UNSET)
        config: ManagedAgentsCreateEnvironmentRequestConfig | Unset
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = ManagedAgentsCreateEnvironmentRequestConfig.from_dict(_config)




        description = d.pop("description", UNSET)

        _env_vars = d.pop("env_vars", UNSET)
        env_vars: ManagedAgentsCreateEnvironmentRequestEnvVars | Unset
        if isinstance(_env_vars,  Unset):
            env_vars = UNSET
        else:
            env_vars = ManagedAgentsCreateEnvironmentRequestEnvVars.from_dict(_env_vars)




        def _parse_http_port(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        http_port = _parse_http_port(d.pop("http_port", UNSET))


        idle_stop_after_seconds = d.pop("idle_stop_after_seconds", UNSET)

        image = d.pop("image", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsCreateEnvironmentRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsCreateEnvironmentRequestMetadata.from_dict(_metadata)




        _mounts = d.pop("mounts", UNSET)
        mounts: list[ManagedAgentsEnvironmentMount] | Unset = UNSET
        if _mounts is not UNSET:
            mounts = []
            for mounts_item_data in _mounts:
                mounts_item = ManagedAgentsEnvironmentMount.from_dict(mounts_item_data)



                mounts.append(mounts_item)


        def _parse_network_policy(data: object) -> ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                network_policy_type_0 = ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0.from_dict(data)



                return network_policy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsCreateEnvironmentRequestNetworkPolicyType0 | None | Unset, data)

        network_policy = _parse_network_policy(d.pop("network_policy", UNSET))


        def _parse_privileged(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        privileged = _parse_privileged(d.pop("privileged", UNSET))


        pvc_size_gi = d.pop("pvc_size_gi", UNSET)

        _resources = d.pop("resources", UNSET)
        resources: ManagedAgentsEnvironmentResources | Unset
        if isinstance(_resources,  Unset):
            resources = UNSET
        else:
            resources = ManagedAgentsEnvironmentResources.from_dict(_resources)




        scope = d.pop("scope", UNSET)

        _secrets = d.pop("secrets", UNSET)
        secrets: ManagedAgentsCreateEnvironmentRequestSecrets | Unset
        if isinstance(_secrets,  Unset):
            secrets = UNSET
        else:
            secrets = ManagedAgentsCreateEnvironmentRequestSecrets.from_dict(_secrets)




        _setup = d.pop("setup", UNSET)
        setup: ManagedAgentsEnvironmentSetup | Unset
        if isinstance(_setup,  Unset):
            setup = UNSET
        else:
            setup = ManagedAgentsEnvironmentSetup.from_dict(_setup)




        stopped_delete_after_seconds = d.pop("stopped_delete_after_seconds", UNSET)

        managed_agents_create_environment_request = cls(
            name=name,
            provider=provider,
            computer_use=computer_use,
            config=config,
            description=description,
            env_vars=env_vars,
            http_port=http_port,
            idle_stop_after_seconds=idle_stop_after_seconds,
            image=image,
            metadata=metadata,
            mounts=mounts,
            network_policy=network_policy,
            privileged=privileged,
            pvc_size_gi=pvc_size_gi,
            resources=resources,
            scope=scope,
            secrets=secrets,
            setup=setup,
            stopped_delete_after_seconds=stopped_delete_after_seconds,
        )


        managed_agents_create_environment_request.additional_properties = d
        return managed_agents_create_environment_request

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
