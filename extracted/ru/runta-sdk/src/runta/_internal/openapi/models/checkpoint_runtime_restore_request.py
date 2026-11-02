from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allowlist_egress_policy import AllowlistEgressPolicy
    from ..models.cold_restore_resources import ColdRestoreResources
    from ..models.create_llm_token_saving_policy import CreateLlmTokenSavingPolicy
    from ..models.denylist_egress_policy import DenylistEgressPolicy
    from ..models.disabled_idle_policy import DisabledIdlePolicy
    from ..models.public_ingress_spec import PublicIngressSpec
    from ..models.runtime_repository_selection import RuntimeRepositorySelection
    from ..models.runtime_secret_configuration import RuntimeSecretConfiguration
    from ..models.suspend_and_wakeup_idle_policy import SuspendAndWakeupIdlePolicy
    from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy
    from ..models.timeout_policy import TimeoutPolicy


T = TypeVar("T", bound="CheckpointRuntimeRestoreRequest")


@_attrs_define
class CheckpointRuntimeRestoreRequest:
    """Restore a runtime from a checkpoint. Runtime Image identity and disk size stay fixed to the checkpoint. A live
    checkpoint restores guest memory and running processes, so CPU and memory stay fixed. A cold checkpoint stores only
    the disk and boots fresh, so resources may rechoose CPU and memory; omit resources to keep the values recorded on
    the checkpoint.

        Attributes:
            checkpoint_id (str): Checkpoint UUID to restore from.
            resources (ColdRestoreResources | Unset): CPU and memory for a cold checkpoint restore. Omit the object to keep
                the CPU and memory recorded on the checkpoint. A cold checkpoint stores only the disk and boots fresh, so these
                values may be smaller or larger. A live checkpoint restores guest memory and running processes, so CPU and
                memory stay fixed and this object is rejected.
            egress_policy (AllowlistEgressPolicy | DenylistEgressPolicy | Unset): Per-runtime egress gateway policy.
            idle_policy (DisabledIdlePolicy | SuspendAndWakeupIdlePolicy | SuspendOnlyIdlePolicy | Unset): Runtime idle
                suspension and automatic wakeup policy.
            auto_shutdown_policy (TimeoutPolicy | Unset):
            auto_delete_policy (TimeoutPolicy | Unset):
            ingress_specs (list[PublicIngressSpec] | Unset): Optional ingress specs.
            name (None | str | Unset): Human-readable runtime name.
            secret_configuration (list[RuntimeSecretConfiguration] | Unset): Complete inline secret injection configuration
                override. Omit or pass an empty array to inherit the checkpoint snapshot.
            ssh_key_ids (list[str] | Unset): Personal SSH key UUIDs to attach atomically.
            vnc_enabled (bool | Unset): Start the shared VNC desktop whenever the runtime is running. Default: False.
            repositories (list[RuntimeRepositorySelection] | Unset): GitHub repository override in checkout order. Omit or
                pass an empty array to inherit the checkpoint snapshot. The first repository becomes the default workspace.
            llm_tool_io_capture_enabled (bool | Unset): Opt in to official LLM HTTP API tool input/output capture. Default:
                False.
            llm_session_content_capture_enabled (bool | Unset): Explicitly opt in to user, assistant, and tool conversation
                content capture. Disabled by default; independent from tool-only capture. Default: False.
            tls_passthrough_hosts (list[str] | Unset): Complete HTTPS passthrough host override. Matching TLS connections
                bypass secret injection, LLM capture, token saving, and model routing and connect to the original destination.
                Omit or pass an empty array to inherit the checkpoint snapshot.
            tcp_allowlist (list[str] | Unset): Complete raw TCP allowlist override. Each entry is an exact FQDN:port. Omit
                or pass an empty array to inherit the checkpoint snapshot.
            llm_token_saving_policy (CreateLlmTokenSavingPolicy | Unset): Initial per-runtime LLM tool-output compression
                settings. Omitted fields default to false.
    """

    checkpoint_id: str
    resources: ColdRestoreResources | Unset = UNSET
    egress_policy: AllowlistEgressPolicy | DenylistEgressPolicy | Unset = UNSET
    idle_policy: (
        DisabledIdlePolicy | SuspendAndWakeupIdlePolicy | SuspendOnlyIdlePolicy | Unset
    ) = UNSET
    auto_shutdown_policy: TimeoutPolicy | Unset = UNSET
    auto_delete_policy: TimeoutPolicy | Unset = UNSET
    ingress_specs: list[PublicIngressSpec] | Unset = UNSET
    name: None | str | Unset = UNSET
    secret_configuration: list[RuntimeSecretConfiguration] | Unset = UNSET
    ssh_key_ids: list[str] | Unset = UNSET
    vnc_enabled: bool | Unset = False
    repositories: list[RuntimeRepositorySelection] | Unset = UNSET
    llm_tool_io_capture_enabled: bool | Unset = False
    llm_session_content_capture_enabled: bool | Unset = False
    tls_passthrough_hosts: list[str] | Unset = UNSET
    tcp_allowlist: list[str] | Unset = UNSET
    llm_token_saving_policy: CreateLlmTokenSavingPolicy | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.denylist_egress_policy import DenylistEgressPolicy
        from ..models.disabled_idle_policy import DisabledIdlePolicy
        from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy

        checkpoint_id = self.checkpoint_id

        resources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources.to_dict()

        egress_policy: dict[str, Any] | Unset
        if isinstance(self.egress_policy, Unset):
            egress_policy = UNSET
        elif isinstance(self.egress_policy, DenylistEgressPolicy):
            egress_policy = self.egress_policy.to_dict()
        else:
            egress_policy = self.egress_policy.to_dict()

        idle_policy: dict[str, Any] | Unset
        if isinstance(self.idle_policy, Unset):
            idle_policy = UNSET
        elif isinstance(self.idle_policy, DisabledIdlePolicy):
            idle_policy = self.idle_policy.to_dict()
        elif isinstance(self.idle_policy, SuspendOnlyIdlePolicy):
            idle_policy = self.idle_policy.to_dict()
        else:
            idle_policy = self.idle_policy.to_dict()

        auto_shutdown_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_shutdown_policy, Unset):
            auto_shutdown_policy = self.auto_shutdown_policy.to_dict()

        auto_delete_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_delete_policy, Unset):
            auto_delete_policy = self.auto_delete_policy.to_dict()

        ingress_specs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ingress_specs, Unset):
            ingress_specs = []
            for ingress_specs_item_data in self.ingress_specs:
                ingress_specs_item = ingress_specs_item_data.to_dict()
                ingress_specs.append(ingress_specs_item)

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        secret_configuration: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.secret_configuration, Unset):
            secret_configuration = []
            for secret_configuration_item_data in self.secret_configuration:
                secret_configuration_item = secret_configuration_item_data.to_dict()
                secret_configuration.append(secret_configuration_item)

        ssh_key_ids: list[str] | Unset = UNSET
        if not isinstance(self.ssh_key_ids, Unset):
            ssh_key_ids = self.ssh_key_ids

        vnc_enabled = self.vnc_enabled

        repositories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.repositories, Unset):
            repositories = []
            for repositories_item_data in self.repositories:
                repositories_item = repositories_item_data.to_dict()
                repositories.append(repositories_item)

        llm_tool_io_capture_enabled = self.llm_tool_io_capture_enabled

        llm_session_content_capture_enabled = self.llm_session_content_capture_enabled

        tls_passthrough_hosts: list[str] | Unset = UNSET
        if not isinstance(self.tls_passthrough_hosts, Unset):
            tls_passthrough_hosts = self.tls_passthrough_hosts

        tcp_allowlist: list[str] | Unset = UNSET
        if not isinstance(self.tcp_allowlist, Unset):
            tcp_allowlist = self.tcp_allowlist

        llm_token_saving_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.llm_token_saving_policy, Unset):
            llm_token_saving_policy = self.llm_token_saving_policy.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "checkpoint_id": checkpoint_id,
            }
        )
        if resources is not UNSET:
            field_dict["resources"] = resources
        if egress_policy is not UNSET:
            field_dict["egress_policy"] = egress_policy
        if idle_policy is not UNSET:
            field_dict["idle_policy"] = idle_policy
        if auto_shutdown_policy is not UNSET:
            field_dict["auto_shutdown_policy"] = auto_shutdown_policy
        if auto_delete_policy is not UNSET:
            field_dict["auto_delete_policy"] = auto_delete_policy
        if ingress_specs is not UNSET:
            field_dict["ingress_specs"] = ingress_specs
        if name is not UNSET:
            field_dict["name"] = name
        if secret_configuration is not UNSET:
            field_dict["secret_configuration"] = secret_configuration
        if ssh_key_ids is not UNSET:
            field_dict["ssh_key_ids"] = ssh_key_ids
        if vnc_enabled is not UNSET:
            field_dict["vnc_enabled"] = vnc_enabled
        if repositories is not UNSET:
            field_dict["repositories"] = repositories
        if llm_tool_io_capture_enabled is not UNSET:
            field_dict["llm_tool_io_capture_enabled"] = llm_tool_io_capture_enabled
        if llm_session_content_capture_enabled is not UNSET:
            field_dict["llm_session_content_capture_enabled"] = (
                llm_session_content_capture_enabled
            )
        if tls_passthrough_hosts is not UNSET:
            field_dict["tls_passthrough_hosts"] = tls_passthrough_hosts
        if tcp_allowlist is not UNSET:
            field_dict["tcp_allowlist"] = tcp_allowlist
        if llm_token_saving_policy is not UNSET:
            field_dict["llm_token_saving_policy"] = llm_token_saving_policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowlist_egress_policy import AllowlistEgressPolicy
        from ..models.cold_restore_resources import ColdRestoreResources
        from ..models.create_llm_token_saving_policy import CreateLlmTokenSavingPolicy
        from ..models.denylist_egress_policy import DenylistEgressPolicy
        from ..models.disabled_idle_policy import DisabledIdlePolicy
        from ..models.public_ingress_spec import PublicIngressSpec
        from ..models.runtime_repository_selection import RuntimeRepositorySelection
        from ..models.runtime_secret_configuration import RuntimeSecretConfiguration
        from ..models.suspend_and_wakeup_idle_policy import SuspendAndWakeupIdlePolicy
        from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy
        from ..models.timeout_policy import TimeoutPolicy

        d = dict(src_dict)
        checkpoint_id = d.pop("checkpoint_id")

        _resources = d.pop("resources", UNSET)
        resources: ColdRestoreResources | Unset
        if isinstance(_resources, Unset):
            resources = UNSET
        else:
            resources = ColdRestoreResources.from_dict(_resources)

        def _parse_egress_policy(
            data: object,
        ) -> AllowlistEgressPolicy | DenylistEgressPolicy | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_public_egress_policy_type_0 = (
                    DenylistEgressPolicy.from_dict(data)
                )

                return componentsschemas_public_egress_policy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_public_egress_policy_type_1 = (
                AllowlistEgressPolicy.from_dict(data)
            )

            return componentsschemas_public_egress_policy_type_1

        egress_policy = _parse_egress_policy(d.pop("egress_policy", UNSET))

        def _parse_idle_policy(
            data: object,
        ) -> (
            DisabledIdlePolicy
            | SuspendAndWakeupIdlePolicy
            | SuspendOnlyIdlePolicy
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_idle_policy_type_0 = DisabledIdlePolicy.from_dict(
                    data
                )

                return componentsschemas_idle_policy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_idle_policy_type_1 = SuspendOnlyIdlePolicy.from_dict(
                    data
                )

                return componentsschemas_idle_policy_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_idle_policy_type_2 = SuspendAndWakeupIdlePolicy.from_dict(
                data
            )

            return componentsschemas_idle_policy_type_2

        idle_policy = _parse_idle_policy(d.pop("idle_policy", UNSET))

        _auto_shutdown_policy = d.pop("auto_shutdown_policy", UNSET)
        auto_shutdown_policy: TimeoutPolicy | Unset
        if isinstance(_auto_shutdown_policy, Unset):
            auto_shutdown_policy = UNSET
        else:
            auto_shutdown_policy = TimeoutPolicy.from_dict(_auto_shutdown_policy)

        _auto_delete_policy = d.pop("auto_delete_policy", UNSET)
        auto_delete_policy: TimeoutPolicy | Unset
        if isinstance(_auto_delete_policy, Unset):
            auto_delete_policy = UNSET
        else:
            auto_delete_policy = TimeoutPolicy.from_dict(_auto_delete_policy)

        _ingress_specs = d.pop("ingress_specs", UNSET)
        ingress_specs: list[PublicIngressSpec] | Unset = UNSET
        if _ingress_specs is not UNSET:
            ingress_specs = []
            for ingress_specs_item_data in _ingress_specs:
                ingress_specs_item = PublicIngressSpec.from_dict(
                    ingress_specs_item_data
                )

                ingress_specs.append(ingress_specs_item)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        _secret_configuration = d.pop("secret_configuration", UNSET)
        secret_configuration: list[RuntimeSecretConfiguration] | Unset = UNSET
        if _secret_configuration is not UNSET:
            secret_configuration = []
            for secret_configuration_item_data in _secret_configuration:
                secret_configuration_item = RuntimeSecretConfiguration.from_dict(
                    secret_configuration_item_data
                )

                secret_configuration.append(secret_configuration_item)

        ssh_key_ids = cast(list[str], d.pop("ssh_key_ids", UNSET))

        vnc_enabled = d.pop("vnc_enabled", UNSET)

        _repositories = d.pop("repositories", UNSET)
        repositories: list[RuntimeRepositorySelection] | Unset = UNSET
        if _repositories is not UNSET:
            repositories = []
            for repositories_item_data in _repositories:
                repositories_item = RuntimeRepositorySelection.from_dict(
                    repositories_item_data
                )

                repositories.append(repositories_item)

        llm_tool_io_capture_enabled = d.pop("llm_tool_io_capture_enabled", UNSET)

        llm_session_content_capture_enabled = d.pop(
            "llm_session_content_capture_enabled", UNSET
        )

        tls_passthrough_hosts = cast(list[str], d.pop("tls_passthrough_hosts", UNSET))

        tcp_allowlist = cast(list[str], d.pop("tcp_allowlist", UNSET))

        _llm_token_saving_policy = d.pop("llm_token_saving_policy", UNSET)
        llm_token_saving_policy: CreateLlmTokenSavingPolicy | Unset
        if isinstance(_llm_token_saving_policy, Unset):
            llm_token_saving_policy = UNSET
        else:
            llm_token_saving_policy = CreateLlmTokenSavingPolicy.from_dict(
                _llm_token_saving_policy
            )

        checkpoint_runtime_restore_request = cls(
            checkpoint_id=checkpoint_id,
            resources=resources,
            egress_policy=egress_policy,
            idle_policy=idle_policy,
            auto_shutdown_policy=auto_shutdown_policy,
            auto_delete_policy=auto_delete_policy,
            ingress_specs=ingress_specs,
            name=name,
            secret_configuration=secret_configuration,
            ssh_key_ids=ssh_key_ids,
            vnc_enabled=vnc_enabled,
            repositories=repositories,
            llm_tool_io_capture_enabled=llm_tool_io_capture_enabled,
            llm_session_content_capture_enabled=llm_session_content_capture_enabled,
            tls_passthrough_hosts=tls_passthrough_hosts,
            tcp_allowlist=tcp_allowlist,
            llm_token_saving_policy=llm_token_saving_policy,
        )

        return checkpoint_runtime_restore_request
