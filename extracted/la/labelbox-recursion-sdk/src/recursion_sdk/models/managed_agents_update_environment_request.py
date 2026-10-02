from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_environment_access_expectation import ManagedAgentsEnvironmentAccessExpectation
  from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount
  from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources
  from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup
  from ..models.managed_agents_environment_setup_verification_request import ManagedAgentsEnvironmentSetupVerificationRequest
  from ..models.managed_agents_environment_setup_warning_request import ManagedAgentsEnvironmentSetupWarningRequest
  from ..models.managed_agents_update_environment_request_config import ManagedAgentsUpdateEnvironmentRequestConfig
  from ..models.managed_agents_update_environment_request_env_vars import ManagedAgentsUpdateEnvironmentRequestEnvVars
  from ..models.managed_agents_update_environment_request_metadata import ManagedAgentsUpdateEnvironmentRequestMetadata
  from ..models.managed_agents_update_environment_request_network_policy import ManagedAgentsUpdateEnvironmentRequestNetworkPolicy
  from ..models.managed_agents_update_environment_request_secrets import ManagedAgentsUpdateEnvironmentRequestSecrets





T = TypeVar("T", bound="ManagedAgentsUpdateEnvironmentRequest")



@_attrs_define
class ManagedAgentsUpdateEnvironmentRequest:
    """ A sandbox environment a session executes in: its provider, resources, mounts, setup steps and idle/delete lifecycle.
    Created and started independently of any session.

        Example:
            {'computer_use': True, 'config': {'key': 'example'}, 'created_at': '2026-02-18T09:30:00Z', 'description':
                'example', 'env_vars': {'key': 'example'}, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'expected_access': {'network_policy': {'key': 'example'}, 'privileged': True}, 'http_port': 1,
                'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key': 'example'}, 'mounts': [{'mount_path':
                'example', 'source': 'example'}], 'name': 'example-name', 'network_policy': {'key': 'example'},
                'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'privileged': True, 'provider': 'example',
                'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name', 'type': 'example'},
                'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True, 'max_price_per_hour_usd': 1.5,
                'min_accelerator_vram_gb': 1, 'providers': ['example'], 'regions': ['example']}, 'timeout_seconds': 1}, 'scope':
                'example', 'secrets': {'key': 'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1},
                'setup_updated_at': '2026-02-18T09:30:00Z', 'setup_updated_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'setup_verification': {'active_setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at':
                '2026-02-18T09:30:00Z', 'fingerprint': 'example', 'image': {'baseImageDigest': 'example', 'capturedAt':
                '2026-02-18T09:30:00Z', 'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
                'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1, 'usable': True,
                'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture': {'at': '2026-02-18T09:30:00Z', 'message':
                'example', 'reason': 'example', 'setupRunId': 'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1,
                'exit_code': 1, 'failed_command': 'example', 'failed_line': 1, 'hint': 'example', 'hint_code': 'example',
                'message': 'example', 'phase': 'example', 'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status':
                'example', 'stderr_tail': 'example'}, 'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True,
                'status': 'example', 'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'setup_warnings': [{'code':
                'example', 'line': 1, 'message': 'example'}], 'stopped_delete_after_seconds': 1, 'updated_at':
                '2026-02-18T09:30:00Z'}

        Attributes:
            computer_use (bool | Unset): Whether this environment boots the shared interactive Chromium display used by the
                computer and human-handoff tools. The server projects this to http_port 6901.
            config (ManagedAgentsUpdateEnvironmentRequestConfig | Unset): Provider-specific overflow settings this schema
                does not model. Passed to the provider unchanged.
            created_at (datetime.datetime | Unset): Server-assigned RFC 3339 timestamp of when the environment was created.
            description (str | Unset): Free-text note about what this environment provides.
            env_vars (ManagedAgentsUpdateEnvironmentRequestEnvVars | Unset): Plaintext environment variables exported in the
                sandbox. They become the whole container environment, including the runner entrypoint's, so PATH is refused
                (env_vars.PATH): managed images select /workspace/.venv themselves. A Runs session using one-time setup after
                its runner changes also refuses startup-hook names such as BASH_ENV, HOME, PYTHONPATH, and LD_PRELOAD; re-test
                to capture a compatible image instead. Never put secrets here; use secrets instead. On update, omit to keep the
                current variables; send {} to clear them.
            environment_id (str | Unset): Server-assigned id of the environment; pass it when starting a session that should
                run in this sandbox.
            expected_access (ManagedAgentsEnvironmentAccessExpectation | Unset): Request-only precondition for changing an
                environment's access settings. Supply the network policy and effective privileged value from the last
                environment read; a stale snapshot is rejected. Example: {'network_policy': {'key': 'example'}, 'privileged':
                True}.
            http_port (int | Unset): Port inside the sandbox to expose over HTTP for services the agent starts; 0 exposes
                nothing.
            idle_stop_after_seconds (int | Unset): Seconds of inactivity after which a running sandbox is stopped; 0 uses
                the provider default. A computer-enabled environment requires 0 or at least 600 seconds so its five-minute
                handoff heartbeat arrives before idle-stop.
            image (str | Unset): Container image the sandbox boots. Omit to use the provider's default image. For the Agent
                runner provider only the deployment's own runner repository or a sibling published beside it (for example rma-
                runner-recursion) is accepted, and it must be omitted when an accelerator is requested, which always boots the
                platform's GPU runner. Customize the sandbox itself with setup.script.
            metadata (ManagedAgentsUpdateEnvironmentRequestMetadata | Unset): Caller-owned key/value data stored with the
                environment and returned unchanged.
            mounts (list[ManagedAgentsEnvironmentMount] | Unset): Files or objects staged into the sandbox workspace when it
                is created. On update, omit to keep the current mounts; send [] to clear them.
            name (str | Unset): Human-readable label shown wherever environments are listed.
            network_policy (ManagedAgentsUpdateEnvironmentRequestNetworkPolicy | Unset): Runs egress rules. On update,
                omission keeps the stored policy. Changing from a non-Runs provider to Runs with an absent or {} stored policy
                requires an explicit network_policy: {"version":"v1","rules":[]} for deny-all or {} for unrestricted egress. A
                nonempty policy requires GKE; with explicit non-GKE placement, send {} for unrestricted egress or change
                placement to GKE. Send {} to clear a policy. Runs responses always include network_policy; {} means
                unrestricted.
            organization_id (str | Unset): Organization that owns the environment. Server-assigned from the caller's
                credentials; a value sent in a request body is ignored.
            privileged (bool | None | Unset): Whether a Runs sandbox may use privileged Docker. Independent of
                network_policy; omit on update to retain the saved value, or send false to disable it. New Runs environments and
                transitions from another provider default to false. Existing Runs environments retain their earlier effective
                setting until edited. Compute creation fails closed unless Agent Service can enforce the requested combination.
            provider (str | Unset): Sandbox runtime that executes the session, chosen from the sandbox providers catalog.
            pvc_size_gi (int | Unset): Size in GiB of the persistent workspace volume; 0 uses the provider default.
            resources (ManagedAgentsEnvironmentResources | Unset): Compute sizing and lifetime for an environment's sandbox.
                CPU environments accept caller-selected CPU and memory. GPU environments accept an exclusive accelerator plus
                optional lifetime and placement constraints, but use service-owned limits of 8,000 millicores (8 vCPU) and
                32,768 MiB (32 GiB) of memory. Example: {'accelerator': {'count': 1, 'name': 'example-name', 'type': 'example'},
                'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True, 'max_price_per_hour_usd': 1.5,
                'min_accelerator_vram_gb': 1, 'providers': ['example'], 'regions': ['example']}, 'timeout_seconds': 1}.
            scope (str | Unset): Who may use the environment. Defaults to organization, meaning it is shared across the
                owning organization.
            secrets (ManagedAgentsUpdateEnvironmentRequestSecrets | Unset): Environment variable name to secret-manager
                reference. References only, never plaintext values; the runtime resolves them at start. The one-time Runs setup
                fallback applies the same startup-hook name restriction to secrets and vault-injected variables. On update, omit
                to keep the current references; send {} to clear them.
            setup (ManagedAgentsEnvironmentSetup | Unset): Post-provision customization of a sandbox: a bash script run
                before the agent starts. Set it when the agent needs packages, tools, or state the runner image does not ship;
                leave it empty to start from the image as is. Verify it with a setup run before sessions use the environment.
                Example: {'script': 'example', 'timeout_seconds': 1}.
            setup_updated_at (datetime.datetime | None | Unset): RFC 3339 timestamp of the last setup script change. Server-
                assigned.
            setup_updated_by_user_id (str | Unset): User who last changed the setup script. Server-assigned.
            setup_verification (ManagedAgentsEnvironmentSetupVerificationRequest | Unset): Whether an environment's setup
                script has been proven to run on real compute. Server-owned: it is written by manual setup runs and never
                accepted from a request body. Example: {'active_setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at':
                '2026-02-18T09:30:00Z', 'fingerprint': 'example', 'image': {'baseImageDigest': 'example', 'capturedAt':
                '2026-02-18T09:30:00Z', 'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
                'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1, 'usable': True,
                'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture': {'at': '2026-02-18T09:30:00Z', 'message':
                'example', 'reason': 'example', 'setupRunId': 'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1,
                'exit_code': 1, 'failed_command': 'example', 'failed_line': 1, 'hint': 'example', 'hint_code': 'example',
                'message': 'example', 'phase': 'example', 'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status':
                'example', 'stderr_tail': 'example'}, 'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True,
                'status': 'example', 'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            setup_warnings (list[ManagedAgentsEnvironmentSetupWarningRequest] | Unset): Advisory findings about the setup
                script (bash -lc wrapping, curl | sh, unpinned installs, ambiguous system Python, PATH replacement, or non-
                persistent shell activation), plus legacy_setup_discarded when the stored setup predates setup.script and is not
                run. Never block a save; computed on read.
            stopped_delete_after_seconds (int | Unset): Seconds a stopped sandbox is retained before it is deleted along
                with its volume; 0 uses the provider default.
            updated_at (datetime.datetime | Unset): Server-assigned RFC 3339 timestamp of the most recent update to the
                environment.
     """

    computer_use: bool | Unset = UNSET
    config: ManagedAgentsUpdateEnvironmentRequestConfig | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    description: str | Unset = UNSET
    env_vars: ManagedAgentsUpdateEnvironmentRequestEnvVars | Unset = UNSET
    environment_id: str | Unset = UNSET
    expected_access: ManagedAgentsEnvironmentAccessExpectation | Unset = UNSET
    http_port: int | Unset = UNSET
    idle_stop_after_seconds: int | Unset = UNSET
    image: str | Unset = UNSET
    metadata: ManagedAgentsUpdateEnvironmentRequestMetadata | Unset = UNSET
    mounts: list[ManagedAgentsEnvironmentMount] | Unset = UNSET
    name: str | Unset = UNSET
    network_policy: ManagedAgentsUpdateEnvironmentRequestNetworkPolicy | Unset = UNSET
    organization_id: str | Unset = UNSET
    privileged: bool | None | Unset = UNSET
    provider: str | Unset = UNSET
    pvc_size_gi: int | Unset = UNSET
    resources: ManagedAgentsEnvironmentResources | Unset = UNSET
    scope: str | Unset = UNSET
    secrets: ManagedAgentsUpdateEnvironmentRequestSecrets | Unset = UNSET
    setup: ManagedAgentsEnvironmentSetup | Unset = UNSET
    setup_updated_at: datetime.datetime | None | Unset = UNSET
    setup_updated_by_user_id: str | Unset = UNSET
    setup_verification: ManagedAgentsEnvironmentSetupVerificationRequest | Unset = UNSET
    setup_warnings: list[ManagedAgentsEnvironmentSetupWarningRequest] | Unset = UNSET
    stopped_delete_after_seconds: int | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_access_expectation import ManagedAgentsEnvironmentAccessExpectation # noqa: PLC0415
        from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount # noqa: PLC0415
        from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources # noqa: PLC0415
        from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup # noqa: PLC0415
        from ..models.managed_agents_environment_setup_verification_request import ManagedAgentsEnvironmentSetupVerificationRequest # noqa: PLC0415
        from ..models.managed_agents_environment_setup_warning_request import ManagedAgentsEnvironmentSetupWarningRequest # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_config import ManagedAgentsUpdateEnvironmentRequestConfig # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_env_vars import ManagedAgentsUpdateEnvironmentRequestEnvVars # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_metadata import ManagedAgentsUpdateEnvironmentRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_network_policy import ManagedAgentsUpdateEnvironmentRequestNetworkPolicy # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_secrets import ManagedAgentsUpdateEnvironmentRequestSecrets # noqa: PLC0415
        computer_use = self.computer_use

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        description = self.description

        env_vars: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = self.env_vars.to_dict()

        environment_id = self.environment_id

        expected_access: dict[str, Any] | Unset = UNSET
        if not isinstance(self.expected_access, Unset):
            expected_access = self.expected_access.to_dict()

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



        name = self.name

        network_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.network_policy, Unset):
            network_policy = self.network_policy.to_dict()

        organization_id = self.organization_id

        privileged: bool | None | Unset
        if isinstance(self.privileged, Unset):
            privileged = UNSET
        else:
            privileged = self.privileged

        provider = self.provider

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

        setup_updated_at: None | str | Unset
        if isinstance(self.setup_updated_at, Unset):
            setup_updated_at = UNSET
        elif isinstance(self.setup_updated_at, datetime.datetime):
            setup_updated_at = self.setup_updated_at.isoformat()
        else:
            setup_updated_at = self.setup_updated_at

        setup_updated_by_user_id = self.setup_updated_by_user_id

        setup_verification: dict[str, Any] | Unset = UNSET
        if not isinstance(self.setup_verification, Unset):
            setup_verification = self.setup_verification.to_dict()

        setup_warnings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.setup_warnings, Unset):
            setup_warnings = []
            for setup_warnings_item_data in self.setup_warnings:
                setup_warnings_item = setup_warnings_item_data.to_dict()
                setup_warnings.append(setup_warnings_item)



        stopped_delete_after_seconds = self.stopped_delete_after_seconds

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if computer_use is not UNSET:
            field_dict["computer_use"] = computer_use
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if description is not UNSET:
            field_dict["description"] = description
        if env_vars is not UNSET:
            field_dict["env_vars"] = env_vars
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if expected_access is not UNSET:
            field_dict["expected_access"] = expected_access
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
        if name is not UNSET:
            field_dict["name"] = name
        if network_policy is not UNSET:
            field_dict["network_policy"] = network_policy
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if privileged is not UNSET:
            field_dict["privileged"] = privileged
        if provider is not UNSET:
            field_dict["provider"] = provider
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
        if setup_updated_at is not UNSET:
            field_dict["setup_updated_at"] = setup_updated_at
        if setup_updated_by_user_id is not UNSET:
            field_dict["setup_updated_by_user_id"] = setup_updated_by_user_id
        if setup_verification is not UNSET:
            field_dict["setup_verification"] = setup_verification
        if setup_warnings is not UNSET:
            field_dict["setup_warnings"] = setup_warnings
        if stopped_delete_after_seconds is not UNSET:
            field_dict["stopped_delete_after_seconds"] = stopped_delete_after_seconds
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_access_expectation import ManagedAgentsEnvironmentAccessExpectation # noqa: PLC0415
        from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount # noqa: PLC0415
        from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources # noqa: PLC0415
        from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup # noqa: PLC0415
        from ..models.managed_agents_environment_setup_verification_request import ManagedAgentsEnvironmentSetupVerificationRequest # noqa: PLC0415
        from ..models.managed_agents_environment_setup_warning_request import ManagedAgentsEnvironmentSetupWarningRequest # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_config import ManagedAgentsUpdateEnvironmentRequestConfig # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_env_vars import ManagedAgentsUpdateEnvironmentRequestEnvVars # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_metadata import ManagedAgentsUpdateEnvironmentRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_network_policy import ManagedAgentsUpdateEnvironmentRequestNetworkPolicy # noqa: PLC0415
        from ..models.managed_agents_update_environment_request_secrets import ManagedAgentsUpdateEnvironmentRequestSecrets # noqa: PLC0415
        d = dict(src_dict)
        computer_use = d.pop("computer_use", UNSET)

        _config = d.pop("config", UNSET)
        config: ManagedAgentsUpdateEnvironmentRequestConfig | Unset
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = ManagedAgentsUpdateEnvironmentRequestConfig.from_dict(_config)




        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        description = d.pop("description", UNSET)

        _env_vars = d.pop("env_vars", UNSET)
        env_vars: ManagedAgentsUpdateEnvironmentRequestEnvVars | Unset
        if isinstance(_env_vars,  Unset):
            env_vars = UNSET
        else:
            env_vars = ManagedAgentsUpdateEnvironmentRequestEnvVars.from_dict(_env_vars)




        environment_id = d.pop("environment_id", UNSET)

        _expected_access = d.pop("expected_access", UNSET)
        expected_access: ManagedAgentsEnvironmentAccessExpectation | Unset
        if isinstance(_expected_access,  Unset):
            expected_access = UNSET
        else:
            expected_access = ManagedAgentsEnvironmentAccessExpectation.from_dict(_expected_access)




        http_port = d.pop("http_port", UNSET)

        idle_stop_after_seconds = d.pop("idle_stop_after_seconds", UNSET)

        image = d.pop("image", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsUpdateEnvironmentRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsUpdateEnvironmentRequestMetadata.from_dict(_metadata)




        _mounts = d.pop("mounts", UNSET)
        mounts: list[ManagedAgentsEnvironmentMount] | Unset = UNSET
        if _mounts is not UNSET:
            mounts = []
            for mounts_item_data in _mounts:
                mounts_item = ManagedAgentsEnvironmentMount.from_dict(mounts_item_data)



                mounts.append(mounts_item)


        name = d.pop("name", UNSET)

        _network_policy = d.pop("network_policy", UNSET)
        network_policy: ManagedAgentsUpdateEnvironmentRequestNetworkPolicy | Unset
        if isinstance(_network_policy,  Unset):
            network_policy = UNSET
        else:
            network_policy = ManagedAgentsUpdateEnvironmentRequestNetworkPolicy.from_dict(_network_policy)




        organization_id = d.pop("organization_id", UNSET)

        def _parse_privileged(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        privileged = _parse_privileged(d.pop("privileged", UNSET))


        provider = d.pop("provider", UNSET)

        pvc_size_gi = d.pop("pvc_size_gi", UNSET)

        _resources = d.pop("resources", UNSET)
        resources: ManagedAgentsEnvironmentResources | Unset
        if isinstance(_resources,  Unset):
            resources = UNSET
        else:
            resources = ManagedAgentsEnvironmentResources.from_dict(_resources)




        scope = d.pop("scope", UNSET)

        _secrets = d.pop("secrets", UNSET)
        secrets: ManagedAgentsUpdateEnvironmentRequestSecrets | Unset
        if isinstance(_secrets,  Unset):
            secrets = UNSET
        else:
            secrets = ManagedAgentsUpdateEnvironmentRequestSecrets.from_dict(_secrets)




        _setup = d.pop("setup", UNSET)
        setup: ManagedAgentsEnvironmentSetup | Unset
        if isinstance(_setup,  Unset):
            setup = UNSET
        else:
            setup = ManagedAgentsEnvironmentSetup.from_dict(_setup)




        def _parse_setup_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                setup_updated_at_type_1 = datetime.datetime.fromisoformat(data)



                return setup_updated_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        setup_updated_at = _parse_setup_updated_at(d.pop("setup_updated_at", UNSET))


        setup_updated_by_user_id = d.pop("setup_updated_by_user_id", UNSET)

        _setup_verification = d.pop("setup_verification", UNSET)
        setup_verification: ManagedAgentsEnvironmentSetupVerificationRequest | Unset
        if isinstance(_setup_verification,  Unset):
            setup_verification = UNSET
        else:
            setup_verification = ManagedAgentsEnvironmentSetupVerificationRequest.from_dict(_setup_verification)




        _setup_warnings = d.pop("setup_warnings", UNSET)
        setup_warnings: list[ManagedAgentsEnvironmentSetupWarningRequest] | Unset = UNSET
        if _setup_warnings is not UNSET:
            setup_warnings = []
            for setup_warnings_item_data in _setup_warnings:
                setup_warnings_item = ManagedAgentsEnvironmentSetupWarningRequest.from_dict(setup_warnings_item_data)



                setup_warnings.append(setup_warnings_item)


        stopped_delete_after_seconds = d.pop("stopped_delete_after_seconds", UNSET)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = datetime.datetime.fromisoformat(_updated_at)




        managed_agents_update_environment_request = cls(
            computer_use=computer_use,
            config=config,
            created_at=created_at,
            description=description,
            env_vars=env_vars,
            environment_id=environment_id,
            expected_access=expected_access,
            http_port=http_port,
            idle_stop_after_seconds=idle_stop_after_seconds,
            image=image,
            metadata=metadata,
            mounts=mounts,
            name=name,
            network_policy=network_policy,
            organization_id=organization_id,
            privileged=privileged,
            provider=provider,
            pvc_size_gi=pvc_size_gi,
            resources=resources,
            scope=scope,
            secrets=secrets,
            setup=setup,
            setup_updated_at=setup_updated_at,
            setup_updated_by_user_id=setup_updated_by_user_id,
            setup_verification=setup_verification,
            setup_warnings=setup_warnings,
            stopped_delete_after_seconds=stopped_delete_after_seconds,
            updated_at=updated_at,
        )


        managed_agents_update_environment_request.additional_properties = d
        return managed_agents_update_environment_request

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
