from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_container_size import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigContainerSize
from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_gpu_type import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigGpuType
from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_installed_package_managers_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigInstalledPackageManagersItem
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_compute_env import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigComputeEnv
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_customer_secrets_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_env_vars import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigEnvVars
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_mcp_tools_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMcpToolsItem
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_mounts_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMountsItem
  from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_retry_policy import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigRetryPolicy





T = TypeVar("T", bound="CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig")



@_attrs_define
class CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfig:
    """ Run-config payload shared by agent-harness and snapshot types. Container, invocation, and limit primitives the
    platform passes through verbatim without inspecting the harness shape.

        Attributes:
            harness_image_url (str | Unset): Fully qualified container image URL for the harness. Omit to inherit the
                platform default. Example: us-central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3.
            grader_image_url (str | Unset): Fully qualified grader image URL paired with this harness. When set, new
                programmatic and mcp_tool_call grading configs pre-fill their grader image from it (the solver's companion
                grader image). Omit to use the platform default grader image. Example: us-central1-docker.pkg.dev/lb-ml-dev/dev-
                agent-service/runner-worldsim-mcp-verify@sha256:….
            container_size (CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigContainerSize | Unset): Container resource
                preset (CPU + memory). Omit to inherit the platform default.
            gpu_type (CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigGpuType | Unset): GPU type attached to the
                container. Omit to run without GPU acceleration.
            privileged (bool | Unset): When true, the container runs with elevated privileges. Required by harnesses that
                need Docker-in-Docker or raw block-device access.
            nested_virt (bool | Unset): When true, requests KVM-backed nested virtualization. Requires privileged=true and a
                GKE launcher.
            machine_type (str | Unset): Explicit GKE node machine type (e.g. "e2-standard-16"), overriding the platform
                default. Not validated against a fixed set here — an invalid value is rejected by agent-service/GKE at
                submission. Takes priority over the machine type implied by nestedVirt when both are set.
            port (int | Unset): HTTP port the container exposes (snapshot/compute-only). Ignored by job submission and
                absent from the effective invocation. Example: 8080.
            installed_package_managers
                (list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigInstalledPackageManagersItem] | Unset): Package
                managers preinstalled in the harness image, used to drive setup snippets in the editor.
            args (str | Unset): Extra CLI arguments appended to the harness command. Tokenized by whitespace split at
                submission time; quoted strings are not supported.
            env_vars (CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigEnvVars | Unset): Env vars injected into the
                container. Null values permitted for backward compatibility; the editor strips them on save.
            mounts (list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMountsItem] | Unset): External file mounts
                referencing previously uploaded objects. Valid only on snapshot-type configs; agent-harness configs attach files
                via the run_config_files join table instead and the server rejects this field on save.
            customer_secrets (list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem] | Unset): Env-
                var names this config expects the runner to inject. Resolved against the version's attached customer secrets at
                submit time.
            allowed_domains (list[str] | None | Unset): Egress allowlist for the container. An empty list denies general
                outbound traffic; hosts independently authorized by attached proxy credentials remain reachable. Any list
                containing the exact '*' entry permits everything, and a nonempty list without '*' restricts general egress to
                those domains. Null explicitly selects no run-config egress policy and overrides an inherited problem-version
                allowlist; omission defers to the consuming context.
            timeout_seconds (int | Unset): Wall-clock timeout for the harness invocation (seconds). Example: 600.
            mcp_tools (list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMcpToolsItem] | Unset): MCP tools the
                harness exposes, as returned by the MCP service list_tools(). Metadata only — persisted for future grader-UI use
                and not consumed at submit time.
            mcp_tools_bake_ref (str | Unset): The WORLDSIM_BAKE_REF the mcpTools catalogue was discovered against. Server-
                owned: set during MCP tool discovery. On other writes a client-supplied value is ignored, and the stored tag is
                carried forward while mcpTools is unchanged (a changed WORLDSIM_BAKE_REF keeps it, so worldsim validation
                detects the mismatch) and cleared when mcpTools changes. Used when submitting problem versions to reject an MCP
                allowlist that would be materialized from a catalogue stale relative to the dispatch-time parent bake.
            mcp_tools_probe_context (str | Unset): Seeded-entity overrides for the worldsim MCP functional tool checks, as
                an opaque JSON-object string with the runner's snake_case keys (e.g.
                {"erpnext_company":"Northline","keycloak_realm":"northline"}). Emitted as the probe_context block of the mounted
                mcp-tools.yaml when a run forks the worldsim solver child from this config. Ignored when the problem version
                inherits the solver's MCP tools: the runner then reads the probe_context block of the file this config names in
                WORLDSIM_MCP_TOOLS_FILE. Only read by runs that set WORLDSIM_RUN_MCP_TOOL_CHECKS=true.
            compute_env (CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigComputeEnv | Unset): Declared execution
                environment for a snapshot run config's persistent compute (container ref, shared/grade dirs, and image-supplied
                solver verbs). Omit to inherit the platform defaults.
            retry_policy (CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigRetryPolicy | Unset): Infra-retry policy
                override for runs launched from this run-config. Omit to use the platform default; an eval-level override
                (EvaluationMetadataSchema.retryPolicy) takes precedence over this when both are set.
     """

    harness_image_url: str | Unset = UNSET
    grader_image_url: str | Unset = UNSET
    container_size: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigContainerSize | Unset = UNSET
    gpu_type: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigGpuType | Unset = UNSET
    privileged: bool | Unset = UNSET
    nested_virt: bool | Unset = UNSET
    machine_type: str | Unset = UNSET
    port: int | Unset = UNSET
    installed_package_managers: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigInstalledPackageManagersItem] | Unset = UNSET
    args: str | Unset = UNSET
    env_vars: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigEnvVars | Unset = UNSET
    mounts: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMountsItem] | Unset = UNSET
    customer_secrets: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem] | Unset = UNSET
    allowed_domains: list[str] | None | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    mcp_tools: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMcpToolsItem] | Unset = UNSET
    mcp_tools_bake_ref: str | Unset = UNSET
    mcp_tools_probe_context: str | Unset = UNSET
    compute_env: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigComputeEnv | Unset = UNSET
    retry_policy: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigRetryPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_compute_env import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigComputeEnv # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_customer_secrets_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_env_vars import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigEnvVars # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_mcp_tools_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMcpToolsItem # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_mounts_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMountsItem # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_retry_policy import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigRetryPolicy # noqa: PLC0415
        harness_image_url = self.harness_image_url

        grader_image_url = self.grader_image_url

        container_size: str | Unset = UNSET
        if not isinstance(self.container_size, Unset):
            container_size = self.container_size.value


        gpu_type: str | Unset = UNSET
        if not isinstance(self.gpu_type, Unset):
            gpu_type = self.gpu_type.value


        privileged = self.privileged

        nested_virt = self.nested_virt

        machine_type = self.machine_type

        port = self.port

        installed_package_managers: list[str] | Unset = UNSET
        if not isinstance(self.installed_package_managers, Unset):
            installed_package_managers = []
            for installed_package_managers_item_data in self.installed_package_managers:
                installed_package_managers_item = installed_package_managers_item_data.value
                installed_package_managers.append(installed_package_managers_item)



        args = self.args

        env_vars: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = self.env_vars.to_dict()

        mounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.mounts, Unset):
            mounts = []
            for mounts_item_data in self.mounts:
                mounts_item = mounts_item_data.to_dict()
                mounts.append(mounts_item)



        customer_secrets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.customer_secrets, Unset):
            customer_secrets = []
            for customer_secrets_item_data in self.customer_secrets:
                customer_secrets_item = customer_secrets_item_data.to_dict()
                customer_secrets.append(customer_secrets_item)



        allowed_domains: list[str] | None | Unset
        if isinstance(self.allowed_domains, Unset):
            allowed_domains = UNSET
        elif isinstance(self.allowed_domains, list):
            allowed_domains = self.allowed_domains


        else:
            allowed_domains = self.allowed_domains

        timeout_seconds = self.timeout_seconds

        mcp_tools: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.mcp_tools, Unset):
            mcp_tools = []
            for mcp_tools_item_data in self.mcp_tools:
                mcp_tools_item = mcp_tools_item_data.to_dict()
                mcp_tools.append(mcp_tools_item)



        mcp_tools_bake_ref = self.mcp_tools_bake_ref

        mcp_tools_probe_context = self.mcp_tools_probe_context

        compute_env: dict[str, Any] | Unset = UNSET
        if not isinstance(self.compute_env, Unset):
            compute_env = self.compute_env.to_dict()

        retry_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.retry_policy, Unset):
            retry_policy = self.retry_policy.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if harness_image_url is not UNSET:
            field_dict["harnessImageUrl"] = harness_image_url
        if grader_image_url is not UNSET:
            field_dict["graderImageUrl"] = grader_image_url
        if container_size is not UNSET:
            field_dict["containerSize"] = container_size
        if gpu_type is not UNSET:
            field_dict["gpuType"] = gpu_type
        if privileged is not UNSET:
            field_dict["privileged"] = privileged
        if nested_virt is not UNSET:
            field_dict["nestedVirt"] = nested_virt
        if machine_type is not UNSET:
            field_dict["machineType"] = machine_type
        if port is not UNSET:
            field_dict["port"] = port
        if installed_package_managers is not UNSET:
            field_dict["installedPackageManagers"] = installed_package_managers
        if args is not UNSET:
            field_dict["args"] = args
        if env_vars is not UNSET:
            field_dict["envVars"] = env_vars
        if mounts is not UNSET:
            field_dict["mounts"] = mounts
        if customer_secrets is not UNSET:
            field_dict["customerSecrets"] = customer_secrets
        if allowed_domains is not UNSET:
            field_dict["allowedDomains"] = allowed_domains
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if mcp_tools is not UNSET:
            field_dict["mcpTools"] = mcp_tools
        if mcp_tools_bake_ref is not UNSET:
            field_dict["mcpToolsBakeRef"] = mcp_tools_bake_ref
        if mcp_tools_probe_context is not UNSET:
            field_dict["mcpToolsProbeContext"] = mcp_tools_probe_context
        if compute_env is not UNSET:
            field_dict["computeEnv"] = compute_env
        if retry_policy is not UNSET:
            field_dict["retryPolicy"] = retry_policy

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_compute_env import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigComputeEnv # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_customer_secrets_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_env_vars import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigEnvVars # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_mcp_tools_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMcpToolsItem # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_mounts_item import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMountsItem # noqa: PLC0415
        from ..models.create_rollout_batch_dto_properties_agents_items_inline_config_retry_policy import CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigRetryPolicy # noqa: PLC0415
        d = dict(src_dict)
        harness_image_url = d.pop("harnessImageUrl", UNSET)

        grader_image_url = d.pop("graderImageUrl", UNSET)

        _container_size = d.pop("containerSize", UNSET)
        container_size: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigContainerSize | Unset
        if isinstance(_container_size,  Unset):
            container_size = UNSET
        else:
            container_size = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigContainerSize(_container_size)




        _gpu_type = d.pop("gpuType", UNSET)
        gpu_type: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigGpuType | Unset
        if isinstance(_gpu_type,  Unset):
            gpu_type = UNSET
        else:
            gpu_type = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigGpuType(_gpu_type)




        privileged = d.pop("privileged", UNSET)

        nested_virt = d.pop("nestedVirt", UNSET)

        machine_type = d.pop("machineType", UNSET)

        port = d.pop("port", UNSET)

        _installed_package_managers = d.pop("installedPackageManagers", UNSET)
        installed_package_managers: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigInstalledPackageManagersItem] | Unset = UNSET
        if _installed_package_managers is not UNSET:
            installed_package_managers = []
            for installed_package_managers_item_data in _installed_package_managers:
                installed_package_managers_item = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigInstalledPackageManagersItem(installed_package_managers_item_data)



                installed_package_managers.append(installed_package_managers_item)


        args = d.pop("args", UNSET)

        _env_vars = d.pop("envVars", UNSET)
        env_vars: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigEnvVars | Unset
        if isinstance(_env_vars,  Unset):
            env_vars = UNSET
        else:
            env_vars = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigEnvVars.from_dict(_env_vars)




        _mounts = d.pop("mounts", UNSET)
        mounts: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMountsItem] | Unset = UNSET
        if _mounts is not UNSET:
            mounts = []
            for mounts_item_data in _mounts:
                mounts_item = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMountsItem.from_dict(mounts_item_data)



                mounts.append(mounts_item)


        _customer_secrets = d.pop("customerSecrets", UNSET)
        customer_secrets: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem] | Unset = UNSET
        if _customer_secrets is not UNSET:
            customer_secrets = []
            for customer_secrets_item_data in _customer_secrets:
                customer_secrets_item = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigCustomerSecretsItem.from_dict(customer_secrets_item_data)



                customer_secrets.append(customer_secrets_item)


        def _parse_allowed_domains(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_domains_type_0 = cast(list[str], data)

                return allowed_domains_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        allowed_domains = _parse_allowed_domains(d.pop("allowedDomains", UNSET))


        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        _mcp_tools = d.pop("mcpTools", UNSET)
        mcp_tools: list[CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMcpToolsItem] | Unset = UNSET
        if _mcp_tools is not UNSET:
            mcp_tools = []
            for mcp_tools_item_data in _mcp_tools:
                mcp_tools_item = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigMcpToolsItem.from_dict(mcp_tools_item_data)



                mcp_tools.append(mcp_tools_item)


        mcp_tools_bake_ref = d.pop("mcpToolsBakeRef", UNSET)

        mcp_tools_probe_context = d.pop("mcpToolsProbeContext", UNSET)

        _compute_env = d.pop("computeEnv", UNSET)
        compute_env: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigComputeEnv | Unset
        if isinstance(_compute_env,  Unset):
            compute_env = UNSET
        else:
            compute_env = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigComputeEnv.from_dict(_compute_env)




        _retry_policy = d.pop("retryPolicy", UNSET)
        retry_policy: CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigRetryPolicy | Unset
        if isinstance(_retry_policy,  Unset):
            retry_policy = UNSET
        else:
            retry_policy = CreateRolloutBatchDtoPropertiesAgentsItemsInlineConfigRetryPolicy.from_dict(_retry_policy)




        create_rollout_batch_dto_properties_agents_items_inline_config = cls(
            harness_image_url=harness_image_url,
            grader_image_url=grader_image_url,
            container_size=container_size,
            gpu_type=gpu_type,
            privileged=privileged,
            nested_virt=nested_virt,
            machine_type=machine_type,
            port=port,
            installed_package_managers=installed_package_managers,
            args=args,
            env_vars=env_vars,
            mounts=mounts,
            customer_secrets=customer_secrets,
            allowed_domains=allowed_domains,
            timeout_seconds=timeout_seconds,
            mcp_tools=mcp_tools,
            mcp_tools_bake_ref=mcp_tools_bake_ref,
            mcp_tools_probe_context=mcp_tools_probe_context,
            compute_env=compute_env,
            retry_policy=retry_policy,
        )


        create_rollout_batch_dto_properties_agents_items_inline_config.additional_properties = d
        return create_rollout_batch_dto_properties_agents_items_inline_config

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
