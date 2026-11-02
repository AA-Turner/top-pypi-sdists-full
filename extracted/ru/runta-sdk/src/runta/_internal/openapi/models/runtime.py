from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.public_runtime_status import PublicRuntimeStatus
from ..models.runtime_desired_status import RuntimeDesiredStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allowlist_egress_policy import AllowlistEgressPolicy
    from ..models.denylist_egress_policy import DenylistEgressPolicy
    from ..models.disabled_idle_policy import DisabledIdlePolicy
    from ..models.llm_token_saving_policy import LlmTokenSavingPolicy
    from ..models.public_ingress_spec import PublicIngressSpec
    from ..models.runtime_environment_variables import RuntimeEnvironmentVariables
    from ..models.runtime_resources import RuntimeResources
    from ..models.runtime_secret_configuration import RuntimeSecretConfiguration
    from ..models.suspend_and_wakeup_idle_policy import SuspendAndWakeupIdlePolicy
    from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy
    from ..models.timeout_policy import TimeoutPolicy
    from ..models.vnc_gateway_connection import VncGatewayConnection


T = TypeVar("T", bound="Runtime")


@_attrs_define
class Runtime:
    """Runtime response object.

    Attributes:
        display_name (str): User-chosen display name.
        egress_policy (AllowlistEgressPolicy | DenylistEgressPolicy): Per-runtime egress gateway policy.
        llm_tool_io_capture_enabled (bool): Whether official LLM HTTP API tool input/output capture is enabled.
        llm_session_content_capture_enabled (bool): Explicitly opt in to user, assistant, and tool conversation content
            capture. Disabled by default; independent from tool-only capture.
        llm_token_saving_policy (LlmTokenSavingPolicy): Canonical per-runtime LLM tool-output compression settings.
        idle_policy (DisabledIdlePolicy | SuspendAndWakeupIdlePolicy | SuspendOnlyIdlePolicy): Runtime idle suspension
            and automatic wakeup policy.
        id (str): Stable runtime UUID.
        created_at (str): RFC3339 timestamp when the control-plane runtime row was created.
        updated_at (str): RFC3339 timestamp of the last control-plane runtime row mutation.
        ingress_specs (list[PublicIngressSpec]): Active ingress specs.
        resources (RuntimeResources): Runtime resource requests and limits.
        image_id (str): Stable Runtime Image variant identifier.
        status (PublicRuntimeStatus): Runtime state of a runtime.
        degraded (bool): Whether a running runtime has lacked a new successful heartbeat for at least 60 seconds.
        desired_status (RuntimeDesiredStatus): Control-plane target lifecycle state.
        ssh_enabled (bool): Whether this runtime supports SSH access.
        vnc_enabled (bool): Whether the shared VNC desktop is configured to run with this runtime.
        vnc_ready (bool): Whether the current Worker assignment has published a ready VNC mapping.
        vnc_connection (VncGatewayConnection): Fixed native VNC gateway connection parameters for runtimes in this zone.
        owner_user_id (str): Organization member who owns the runtime.
        can_manage (bool): Whether the current caller may perform control operations on this runtime.
        revision (int): Monotonic runtime aggregate revision.
        secret_configuration (list[RuntimeSecretConfiguration]): Canonical inline secret injection configuration.
        auto_shutdown_at (datetime.datetime | Unset): Current session deadline, absent until running or when disabled.
        auto_delete_at (datetime.datetime | Unset): Deletion deadline, absent until shutdown or when disabled.
        environment_variables (RuntimeEnvironmentVariables | Unset): Non-secret environment variables the runtime
            carries.
        tls_passthrough_hosts (list[str] | Unset): HTTPS host patterns using opaque TLS tunnels to the original
            destination, bypassing secret injection, LLM capture, token saving, and model routing.
        tcp_allowlist (list[str] | Unset): Exact FQDN:port destinations that may receive raw TCP from the runtime. Empty
            denies raw TCP.
        auto_shutdown_policy (TimeoutPolicy | Unset):
        auto_delete_policy (TimeoutPolicy | Unset):
        vnc_error_code (None | str | Unset): Bounded machine-readable VNC startup failure code.
        error_code (None | str | Unset): Bounded machine-readable provisioning failure code.
        error_message (None | str | Unset): Current runtime failure reason, bounded to 4096 UTF-8 bytes. Cleared when
            the failure recovers.
    """

    display_name: str
    egress_policy: AllowlistEgressPolicy | DenylistEgressPolicy
    llm_tool_io_capture_enabled: bool
    llm_session_content_capture_enabled: bool
    llm_token_saving_policy: LlmTokenSavingPolicy
    idle_policy: DisabledIdlePolicy | SuspendAndWakeupIdlePolicy | SuspendOnlyIdlePolicy
    id: str
    created_at: str
    updated_at: str
    ingress_specs: list[PublicIngressSpec]
    resources: RuntimeResources
    image_id: str
    status: PublicRuntimeStatus
    degraded: bool
    desired_status: RuntimeDesiredStatus
    ssh_enabled: bool
    vnc_enabled: bool
    vnc_ready: bool
    vnc_connection: VncGatewayConnection
    owner_user_id: str
    can_manage: bool
    revision: int
    secret_configuration: list[RuntimeSecretConfiguration]
    auto_shutdown_at: datetime.datetime | Unset = UNSET
    auto_delete_at: datetime.datetime | Unset = UNSET
    environment_variables: RuntimeEnvironmentVariables | Unset = UNSET
    tls_passthrough_hosts: list[str] | Unset = UNSET
    tcp_allowlist: list[str] | Unset = UNSET
    auto_shutdown_policy: TimeoutPolicy | Unset = UNSET
    auto_delete_policy: TimeoutPolicy | Unset = UNSET
    vnc_error_code: None | str | Unset = UNSET
    error_code: None | str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.denylist_egress_policy import DenylistEgressPolicy
        from ..models.disabled_idle_policy import DisabledIdlePolicy
        from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy

        display_name = self.display_name

        egress_policy: dict[str, Any]
        if isinstance(self.egress_policy, DenylistEgressPolicy):
            egress_policy = self.egress_policy.to_dict()
        else:
            egress_policy = self.egress_policy.to_dict()

        llm_tool_io_capture_enabled = self.llm_tool_io_capture_enabled

        llm_session_content_capture_enabled = self.llm_session_content_capture_enabled

        llm_token_saving_policy = self.llm_token_saving_policy.to_dict()

        idle_policy: dict[str, Any]
        if isinstance(self.idle_policy, DisabledIdlePolicy):
            idle_policy = self.idle_policy.to_dict()
        elif isinstance(self.idle_policy, SuspendOnlyIdlePolicy):
            idle_policy = self.idle_policy.to_dict()
        else:
            idle_policy = self.idle_policy.to_dict()

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        ingress_specs = []
        for ingress_specs_item_data in self.ingress_specs:
            ingress_specs_item = ingress_specs_item_data.to_dict()
            ingress_specs.append(ingress_specs_item)

        resources = self.resources.to_dict()

        image_id = self.image_id

        status = self.status.value

        degraded = self.degraded

        desired_status = self.desired_status.value

        ssh_enabled = self.ssh_enabled

        vnc_enabled = self.vnc_enabled

        vnc_ready = self.vnc_ready

        vnc_connection = self.vnc_connection.to_dict()

        owner_user_id = self.owner_user_id

        can_manage = self.can_manage

        revision = self.revision

        secret_configuration = []
        for secret_configuration_item_data in self.secret_configuration:
            secret_configuration_item = secret_configuration_item_data.to_dict()
            secret_configuration.append(secret_configuration_item)

        auto_shutdown_at: str | Unset = UNSET
        if not isinstance(self.auto_shutdown_at, Unset):
            auto_shutdown_at = self.auto_shutdown_at.isoformat()

        auto_delete_at: str | Unset = UNSET
        if not isinstance(self.auto_delete_at, Unset):
            auto_delete_at = self.auto_delete_at.isoformat()

        environment_variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environment_variables, Unset):
            environment_variables = self.environment_variables.to_dict()

        tls_passthrough_hosts: list[str] | Unset = UNSET
        if not isinstance(self.tls_passthrough_hosts, Unset):
            tls_passthrough_hosts = self.tls_passthrough_hosts

        tcp_allowlist: list[str] | Unset = UNSET
        if not isinstance(self.tcp_allowlist, Unset):
            tcp_allowlist = self.tcp_allowlist

        auto_shutdown_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_shutdown_policy, Unset):
            auto_shutdown_policy = self.auto_shutdown_policy.to_dict()

        auto_delete_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_delete_policy, Unset):
            auto_delete_policy = self.auto_delete_policy.to_dict()

        vnc_error_code: None | str | Unset
        if isinstance(self.vnc_error_code, Unset):
            vnc_error_code = UNSET
        else:
            vnc_error_code = self.vnc_error_code

        error_code: None | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
                "egress_policy": egress_policy,
                "llm_tool_io_capture_enabled": llm_tool_io_capture_enabled,
                "llm_session_content_capture_enabled": llm_session_content_capture_enabled,
                "llm_token_saving_policy": llm_token_saving_policy,
                "idle_policy": idle_policy,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "ingress_specs": ingress_specs,
                "resources": resources,
                "image_id": image_id,
                "status": status,
                "degraded": degraded,
                "desired_status": desired_status,
                "ssh_enabled": ssh_enabled,
                "vnc_enabled": vnc_enabled,
                "vnc_ready": vnc_ready,
                "vnc_connection": vnc_connection,
                "owner_user_id": owner_user_id,
                "can_manage": can_manage,
                "revision": revision,
                "secret_configuration": secret_configuration,
            }
        )
        if auto_shutdown_at is not UNSET:
            field_dict["auto_shutdown_at"] = auto_shutdown_at
        if auto_delete_at is not UNSET:
            field_dict["auto_delete_at"] = auto_delete_at
        if environment_variables is not UNSET:
            field_dict["environment_variables"] = environment_variables
        if tls_passthrough_hosts is not UNSET:
            field_dict["tls_passthrough_hosts"] = tls_passthrough_hosts
        if tcp_allowlist is not UNSET:
            field_dict["tcp_allowlist"] = tcp_allowlist
        if auto_shutdown_policy is not UNSET:
            field_dict["auto_shutdown_policy"] = auto_shutdown_policy
        if auto_delete_policy is not UNSET:
            field_dict["auto_delete_policy"] = auto_delete_policy
        if vnc_error_code is not UNSET:
            field_dict["vnc_error_code"] = vnc_error_code
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowlist_egress_policy import AllowlistEgressPolicy
        from ..models.denylist_egress_policy import DenylistEgressPolicy
        from ..models.disabled_idle_policy import DisabledIdlePolicy
        from ..models.llm_token_saving_policy import LlmTokenSavingPolicy
        from ..models.public_ingress_spec import PublicIngressSpec
        from ..models.runtime_environment_variables import RuntimeEnvironmentVariables
        from ..models.runtime_resources import RuntimeResources
        from ..models.runtime_secret_configuration import RuntimeSecretConfiguration
        from ..models.suspend_and_wakeup_idle_policy import SuspendAndWakeupIdlePolicy
        from ..models.suspend_only_idle_policy import SuspendOnlyIdlePolicy
        from ..models.timeout_policy import TimeoutPolicy
        from ..models.vnc_gateway_connection import VncGatewayConnection

        d = dict(src_dict)
        display_name = d.pop("display_name")

        def _parse_egress_policy(
            data: object,
        ) -> AllowlistEgressPolicy | DenylistEgressPolicy:
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

        egress_policy = _parse_egress_policy(d.pop("egress_policy"))

        llm_tool_io_capture_enabled = d.pop("llm_tool_io_capture_enabled")

        llm_session_content_capture_enabled = d.pop(
            "llm_session_content_capture_enabled"
        )

        llm_token_saving_policy = LlmTokenSavingPolicy.from_dict(
            d.pop("llm_token_saving_policy")
        )

        def _parse_idle_policy(
            data: object,
        ) -> DisabledIdlePolicy | SuspendAndWakeupIdlePolicy | SuspendOnlyIdlePolicy:
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

        idle_policy = _parse_idle_policy(d.pop("idle_policy"))

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        ingress_specs = []
        _ingress_specs = d.pop("ingress_specs")
        for ingress_specs_item_data in _ingress_specs:
            ingress_specs_item = PublicIngressSpec.from_dict(ingress_specs_item_data)

            ingress_specs.append(ingress_specs_item)

        resources = RuntimeResources.from_dict(d.pop("resources"))

        image_id = d.pop("image_id")

        status = PublicRuntimeStatus(d.pop("status"))

        degraded = d.pop("degraded")

        desired_status = RuntimeDesiredStatus(d.pop("desired_status"))

        ssh_enabled = d.pop("ssh_enabled")

        vnc_enabled = d.pop("vnc_enabled")

        vnc_ready = d.pop("vnc_ready")

        vnc_connection = VncGatewayConnection.from_dict(d.pop("vnc_connection"))

        owner_user_id = d.pop("owner_user_id")

        can_manage = d.pop("can_manage")

        revision = d.pop("revision")

        secret_configuration = []
        _secret_configuration = d.pop("secret_configuration")
        for secret_configuration_item_data in _secret_configuration:
            secret_configuration_item = RuntimeSecretConfiguration.from_dict(
                secret_configuration_item_data
            )

            secret_configuration.append(secret_configuration_item)

        _auto_shutdown_at = d.pop("auto_shutdown_at", UNSET)
        auto_shutdown_at: datetime.datetime | Unset
        if isinstance(_auto_shutdown_at, Unset):
            auto_shutdown_at = UNSET
        else:
            auto_shutdown_at = datetime.datetime.fromisoformat(
                _auto_shutdown_at.replace("Z", "+00:00")
            )

        _auto_delete_at = d.pop("auto_delete_at", UNSET)
        auto_delete_at: datetime.datetime | Unset
        if isinstance(_auto_delete_at, Unset):
            auto_delete_at = UNSET
        else:
            auto_delete_at = datetime.datetime.fromisoformat(
                _auto_delete_at.replace("Z", "+00:00")
            )

        _environment_variables = d.pop("environment_variables", UNSET)
        environment_variables: RuntimeEnvironmentVariables | Unset
        if isinstance(_environment_variables, Unset):
            environment_variables = UNSET
        else:
            environment_variables = RuntimeEnvironmentVariables.from_dict(
                _environment_variables
            )

        tls_passthrough_hosts = cast(list[str], d.pop("tls_passthrough_hosts", UNSET))

        tcp_allowlist = cast(list[str], d.pop("tcp_allowlist", UNSET))

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

        def _parse_vnc_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vnc_error_code = _parse_vnc_error_code(d.pop("vnc_error_code", UNSET))

        def _parse_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        runtime = cls(
            display_name=display_name,
            egress_policy=egress_policy,
            llm_tool_io_capture_enabled=llm_tool_io_capture_enabled,
            llm_session_content_capture_enabled=llm_session_content_capture_enabled,
            llm_token_saving_policy=llm_token_saving_policy,
            idle_policy=idle_policy,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            ingress_specs=ingress_specs,
            resources=resources,
            image_id=image_id,
            status=status,
            degraded=degraded,
            desired_status=desired_status,
            ssh_enabled=ssh_enabled,
            vnc_enabled=vnc_enabled,
            vnc_ready=vnc_ready,
            vnc_connection=vnc_connection,
            owner_user_id=owner_user_id,
            can_manage=can_manage,
            revision=revision,
            secret_configuration=secret_configuration,
            auto_shutdown_at=auto_shutdown_at,
            auto_delete_at=auto_delete_at,
            environment_variables=environment_variables,
            tls_passthrough_hosts=tls_passthrough_hosts,
            tcp_allowlist=tcp_allowlist,
            auto_shutdown_policy=auto_shutdown_policy,
            auto_delete_policy=auto_delete_policy,
            vnc_error_code=vnc_error_code,
            error_code=error_code,
            error_message=error_message,
        )

        runtime.additional_properties = d
        return runtime

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
