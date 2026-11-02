from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allowlist_egress_policy import AllowlistEgressPolicy
    from ..models.denylist_egress_policy import DenylistEgressPolicy
    from ..models.disabled_idle_policy import DisabledIdlePolicy
    from ..models.patch_llm_token_saving_policy import PatchLlmTokenSavingPolicy
    from ..models.patch_runtime_request_environment_variables import (
        PatchRuntimeRequestEnvironmentVariables,
    )
    from ..models.patch_runtime_resources import PatchRuntimeResources
    from ..models.public_ingress_spec import PublicIngressSpec
    from ..models.runtime_secret_configuration import RuntimeSecretConfiguration
    from ..models.suspend_and_wakeup_idle_policy import SuspendAndWakeupIdlePolicy
    from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy
    from ..models.timeout_policy import TimeoutPolicy


T = TypeVar("T", bound="PatchRuntimeRequest")


@_attrs_define
class PatchRuntimeRequest:
    """Runtime patch request.

    Attributes:
        environment_variables (PatchRuntimeRequestEnvironmentVariables | Unset): Complete replacement of the runtime's
            non-secret environment variables. An empty object removes every variable; omit to leave unchanged. The same
            name, value, and reservation rules as creation apply.
        display_name (str | Unset): New user-facing runtime name. The runtime UUID and data-plane identity remain
            unchanged.
        egress_policy (AllowlistEgressPolicy | DenylistEgressPolicy | Unset): Per-runtime egress gateway policy.
        ingress_specs (list[PublicIngressSpec] | Unset): Complete replacement ingress configuration. Omit to leave
            unchanged.
        idle_policy (DisabledIdlePolicy | SuspendAndWakeupIdlePolicy | SuspendOnlyIdlePolicy | Unset): Runtime idle
            suspension and automatic wakeup policy.
        auto_shutdown_policy (TimeoutPolicy | Unset):
        auto_delete_policy (TimeoutPolicy | Unset):
        llm_tool_io_capture_enabled (bool | Unset): Whether official LLM HTTP API tool input/output capture is enabled.
            Omit to leave unchanged.
        llm_session_content_capture_enabled (bool | Unset): Explicitly opt in to user, assistant, and tool conversation
            content capture. Disabled by default; independent from tool-only capture. Omit to leave unchanged.
        tls_passthrough_hosts (list[str] | Unset): Complete replacement HTTPS passthrough host configuration. Matching
            TLS connections bypass secret injection, LLM capture, token saving, and model routing and connect to the
            original destination. Omit to leave unchanged.
        tcp_allowlist (list[str] | Unset): Complete replacement raw TCP allowlist. Each entry is an exact FQDN:port.
            Omit to leave unchanged.
        vnc_enabled (bool | Unset): Enable or disable the on-demand shared VNC desktop. Omit to leave unchanged.
        llm_token_saving_policy (PatchLlmTokenSavingPolicy | Unset): Per-method LLM tool-output compression patch.
            Omitted fields remain unchanged.
        resources (PatchRuntimeResources | Unset): Resource requests and limits for runtime patching.
        secret_configuration (list[RuntimeSecretConfiguration] | Unset): Complete replacement inline secret
            configuration. Omit to leave unchanged.
    """

    environment_variables: PatchRuntimeRequestEnvironmentVariables | Unset = UNSET
    display_name: str | Unset = UNSET
    egress_policy: AllowlistEgressPolicy | DenylistEgressPolicy | Unset = UNSET
    ingress_specs: list[PublicIngressSpec] | Unset = UNSET
    idle_policy: (
        DisabledIdlePolicy | SuspendAndWakeupIdlePolicy | SuspendOnlyIdlePolicy | Unset
    ) = UNSET
    auto_shutdown_policy: TimeoutPolicy | Unset = UNSET
    auto_delete_policy: TimeoutPolicy | Unset = UNSET
    llm_tool_io_capture_enabled: bool | Unset = UNSET
    llm_session_content_capture_enabled: bool | Unset = UNSET
    tls_passthrough_hosts: list[str] | Unset = UNSET
    tcp_allowlist: list[str] | Unset = UNSET
    vnc_enabled: bool | Unset = UNSET
    llm_token_saving_policy: PatchLlmTokenSavingPolicy | Unset = UNSET
    resources: PatchRuntimeResources | Unset = UNSET
    secret_configuration: list[RuntimeSecretConfiguration] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.denylist_egress_policy import DenylistEgressPolicy
        from ..models.disabled_idle_policy import DisabledIdlePolicy
        from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy

        environment_variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environment_variables, Unset):
            environment_variables = self.environment_variables.to_dict()

        display_name = self.display_name

        egress_policy: dict[str, Any] | Unset
        if isinstance(self.egress_policy, Unset):
            egress_policy = UNSET
        elif isinstance(self.egress_policy, DenylistEgressPolicy):
            egress_policy = self.egress_policy.to_dict()
        else:
            egress_policy = self.egress_policy.to_dict()

        ingress_specs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ingress_specs, Unset):
            ingress_specs = []
            for ingress_specs_item_data in self.ingress_specs:
                ingress_specs_item = ingress_specs_item_data.to_dict()
                ingress_specs.append(ingress_specs_item)

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

        llm_tool_io_capture_enabled = self.llm_tool_io_capture_enabled

        llm_session_content_capture_enabled = self.llm_session_content_capture_enabled

        tls_passthrough_hosts: list[str] | Unset = UNSET
        if not isinstance(self.tls_passthrough_hosts, Unset):
            tls_passthrough_hosts = self.tls_passthrough_hosts

        tcp_allowlist: list[str] | Unset = UNSET
        if not isinstance(self.tcp_allowlist, Unset):
            tcp_allowlist = self.tcp_allowlist

        vnc_enabled = self.vnc_enabled

        llm_token_saving_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.llm_token_saving_policy, Unset):
            llm_token_saving_policy = self.llm_token_saving_policy.to_dict()

        resources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources.to_dict()

        secret_configuration: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.secret_configuration, Unset):
            secret_configuration = []
            for secret_configuration_item_data in self.secret_configuration:
                secret_configuration_item = secret_configuration_item_data.to_dict()
                secret_configuration.append(secret_configuration_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if environment_variables is not UNSET:
            field_dict["environment_variables"] = environment_variables
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if egress_policy is not UNSET:
            field_dict["egress_policy"] = egress_policy
        if ingress_specs is not UNSET:
            field_dict["ingress_specs"] = ingress_specs
        if idle_policy is not UNSET:
            field_dict["idle_policy"] = idle_policy
        if auto_shutdown_policy is not UNSET:
            field_dict["auto_shutdown_policy"] = auto_shutdown_policy
        if auto_delete_policy is not UNSET:
            field_dict["auto_delete_policy"] = auto_delete_policy
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
        if vnc_enabled is not UNSET:
            field_dict["vnc_enabled"] = vnc_enabled
        if llm_token_saving_policy is not UNSET:
            field_dict["llm_token_saving_policy"] = llm_token_saving_policy
        if resources is not UNSET:
            field_dict["resources"] = resources
        if secret_configuration is not UNSET:
            field_dict["secret_configuration"] = secret_configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowlist_egress_policy import AllowlistEgressPolicy
        from ..models.denylist_egress_policy import DenylistEgressPolicy
        from ..models.disabled_idle_policy import DisabledIdlePolicy
        from ..models.patch_llm_token_saving_policy import PatchLlmTokenSavingPolicy
        from ..models.patch_runtime_request_environment_variables import (
            PatchRuntimeRequestEnvironmentVariables,
        )
        from ..models.patch_runtime_resources import PatchRuntimeResources
        from ..models.public_ingress_spec import PublicIngressSpec
        from ..models.runtime_secret_configuration import RuntimeSecretConfiguration
        from ..models.suspend_and_wakeup_idle_policy import SuspendAndWakeupIdlePolicy
        from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy
        from ..models.timeout_policy import TimeoutPolicy

        d = dict(src_dict)
        _environment_variables = d.pop("environment_variables", UNSET)
        environment_variables: PatchRuntimeRequestEnvironmentVariables | Unset
        if isinstance(_environment_variables, Unset):
            environment_variables = UNSET
        else:
            environment_variables = PatchRuntimeRequestEnvironmentVariables.from_dict(
                _environment_variables
            )

        display_name = d.pop("display_name", UNSET)

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

        _ingress_specs = d.pop("ingress_specs", UNSET)
        ingress_specs: list[PublicIngressSpec] | Unset = UNSET
        if _ingress_specs is not UNSET:
            ingress_specs = []
            for ingress_specs_item_data in _ingress_specs:
                ingress_specs_item = PublicIngressSpec.from_dict(
                    ingress_specs_item_data
                )

                ingress_specs.append(ingress_specs_item)

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

        llm_tool_io_capture_enabled = d.pop("llm_tool_io_capture_enabled", UNSET)

        llm_session_content_capture_enabled = d.pop(
            "llm_session_content_capture_enabled", UNSET
        )

        tls_passthrough_hosts = cast(list[str], d.pop("tls_passthrough_hosts", UNSET))

        tcp_allowlist = cast(list[str], d.pop("tcp_allowlist", UNSET))

        vnc_enabled = d.pop("vnc_enabled", UNSET)

        _llm_token_saving_policy = d.pop("llm_token_saving_policy", UNSET)
        llm_token_saving_policy: PatchLlmTokenSavingPolicy | Unset
        if isinstance(_llm_token_saving_policy, Unset):
            llm_token_saving_policy = UNSET
        else:
            llm_token_saving_policy = PatchLlmTokenSavingPolicy.from_dict(
                _llm_token_saving_policy
            )

        _resources = d.pop("resources", UNSET)
        resources: PatchRuntimeResources | Unset
        if isinstance(_resources, Unset):
            resources = UNSET
        else:
            resources = PatchRuntimeResources.from_dict(_resources)

        _secret_configuration = d.pop("secret_configuration", UNSET)
        secret_configuration: list[RuntimeSecretConfiguration] | Unset = UNSET
        if _secret_configuration is not UNSET:
            secret_configuration = []
            for secret_configuration_item_data in _secret_configuration:
                secret_configuration_item = RuntimeSecretConfiguration.from_dict(
                    secret_configuration_item_data
                )

                secret_configuration.append(secret_configuration_item)

        patch_runtime_request = cls(
            environment_variables=environment_variables,
            display_name=display_name,
            egress_policy=egress_policy,
            ingress_specs=ingress_specs,
            idle_policy=idle_policy,
            auto_shutdown_policy=auto_shutdown_policy,
            auto_delete_policy=auto_delete_policy,
            llm_tool_io_capture_enabled=llm_tool_io_capture_enabled,
            llm_session_content_capture_enabled=llm_session_content_capture_enabled,
            tls_passthrough_hosts=tls_passthrough_hosts,
            tcp_allowlist=tcp_allowlist,
            vnc_enabled=vnc_enabled,
            llm_token_saving_policy=llm_token_saving_policy,
            resources=resources,
            secret_configuration=secret_configuration,
        )

        return patch_runtime_request
