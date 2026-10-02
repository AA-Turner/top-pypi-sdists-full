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
  from ..models.managed_agents_environment_config import ManagedAgentsEnvironmentConfig
  from ..models.managed_agents_environment_env_vars import ManagedAgentsEnvironmentEnvVars
  from ..models.managed_agents_environment_metadata import ManagedAgentsEnvironmentMetadata
  from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount
  from ..models.managed_agents_environment_network_policy import ManagedAgentsEnvironmentNetworkPolicy
  from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources
  from ..models.managed_agents_environment_secrets import ManagedAgentsEnvironmentSecrets
  from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup
  from ..models.managed_agents_environment_setup_verification import ManagedAgentsEnvironmentSetupVerification
  from ..models.managed_agents_environment_setup_warning import ManagedAgentsEnvironmentSetupWarning





T = TypeVar("T", bound="ManagedAgentsEnvironment")



@_attrs_define
class ManagedAgentsEnvironment:
    """ A sandbox environment a session executes in: its provider, resources, mounts, setup steps and idle/delete lifecycle.
    Created and started independently of any session.

        Example:
            {'computer_use': True, 'config': {'key': 'example'}, 'created_at': '2026-02-18T09:30:00Z', 'description':
                'example', 'env_vars': {'key': 'example'}, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key': 'example'}, 'mounts':
                [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-name', 'network_policy': {'key': 'example'},
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
            computer_use (bool): Whether this environment boots the shared interactive Chromium display used by the computer
                and human-handoff tools. The server projects this to http_port 6901.
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the environment was created.
            environment_id (str): Server-assigned id of the environment; pass it when starting a session that should run in
                this sandbox.
            name (str): Human-readable label shown wherever environments are listed.
            organization_id (str): Organization that owns the environment. Server-assigned from the caller's credentials; a
                value sent in a request body is ignored.
            provider (str): Sandbox runtime that executes the session, chosen from the sandbox providers catalog.
            resources (ManagedAgentsEnvironmentResources): Compute sizing and lifetime for an environment's sandbox. CPU
                environments accept caller-selected CPU and memory. GPU environments accept an exclusive accelerator plus
                optional lifetime and placement constraints, but use service-owned limits of 8,000 millicores (8 vCPU) and
                32,768 MiB (32 GiB) of memory. Example: {'accelerator': {'count': 1, 'name': 'example-name', 'type': 'example'},
                'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True, 'max_price_per_hour_usd': 1.5,
                'min_accelerator_vram_gb': 1, 'providers': ['example'], 'regions': ['example']}, 'timeout_seconds': 1}.
            scope (str): Who may use the environment. Defaults to organization, meaning it is shared across the owning
                organization.
            setup (ManagedAgentsEnvironmentSetup): Post-provision customization of a sandbox: a bash script run before the
                agent starts. Set it when the agent needs packages, tools, or state the runner image does not ship; leave it
                empty to start from the image as is. Verify it with a setup run before sessions use the environment. Example:
                {'script': 'example', 'timeout_seconds': 1}.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent update to the environment.
            config (ManagedAgentsEnvironmentConfig | Unset): Provider-specific overflow settings this schema does not model.
                Passed to the provider unchanged.
            description (str | Unset): Free-text note about what this environment provides.
            env_vars (ManagedAgentsEnvironmentEnvVars | Unset): Plaintext environment variables exported in the sandbox.
                They become the whole container environment, including the runner entrypoint's, so PATH is refused
                (env_vars.PATH): managed images select /workspace/.venv themselves. A Runs session using one-time setup after
                its runner changes also refuses startup-hook names such as BASH_ENV, HOME, PYTHONPATH, and LD_PRELOAD; re-test
                to capture a compatible image instead. Never put secrets here; use secrets instead. On update, omit to keep the
                current variables; send {} to clear them.
            http_port (int | Unset): Port inside the sandbox to expose over HTTP for services the agent starts; 0 exposes
                nothing.
            idle_stop_after_seconds (int | Unset): Seconds of inactivity after which a running sandbox is stopped; 0 uses
                the provider default. A computer-enabled environment requires 0 or at least 600 seconds so its five-minute
                handoff heartbeat arrives before idle-stop.
            image (str | Unset): Container image the sandbox boots. Omit to use the provider's default image. For the Agent
                runner provider only the deployment's own runner repository or a sibling published beside it (for example rma-
                runner-recursion) is accepted, and it must be omitted when an accelerator is requested, which always boots the
                platform's GPU runner. Customize the sandbox itself with setup.script.
            metadata (ManagedAgentsEnvironmentMetadata | Unset): Caller-owned key/value data stored with the environment and
                returned unchanged.
            mounts (list[ManagedAgentsEnvironmentMount] | Unset): Files or objects staged into the sandbox workspace when it
                is created. On update, omit to keep the current mounts; send [] to clear them.
            network_policy (ManagedAgentsEnvironmentNetworkPolicy | Unset): Runs egress rules. On update, omission keeps the
                stored policy. Changing from a non-Runs provider to Runs with an absent or {} stored policy requires an explicit
                network_policy: {"version":"v1","rules":[]} for deny-all or {} for unrestricted egress. A nonempty policy
                requires GKE; with explicit non-GKE placement, send {} for unrestricted egress or change placement to GKE. Send
                {} to clear a policy. Runs responses always include network_policy; {} means unrestricted.
            privileged (bool | Unset): Whether a Runs sandbox may use privileged Docker. Independent of network_policy; omit
                on update to retain the saved value, or send false to disable it. New Runs environments and transitions from
                another provider default to false. Existing Runs environments retain their earlier effective setting until
                edited. Compute creation fails closed unless Agent Service can enforce the requested combination.
            pvc_size_gi (int | Unset): Size in GiB of the persistent workspace volume; 0 uses the provider default.
            secrets (ManagedAgentsEnvironmentSecrets | Unset): Environment variable name to secret-manager reference.
                References only, never plaintext values; the runtime resolves them at start. The one-time Runs setup fallback
                applies the same startup-hook name restriction to secrets and vault-injected variables. On update, omit to keep
                the current references; send {} to clear them.
            setup_updated_at (datetime.datetime | Unset): RFC 3339 timestamp of the last setup script change. Server-
                assigned.
            setup_updated_by_user_id (str | Unset): User who last changed the setup script. Server-assigned.
            setup_verification (ManagedAgentsEnvironmentSetupVerification | Unset): Whether an environment's setup script
                has been proven to run on real compute. Server-owned: it is written by manual setup runs and never accepted from
                a request body. Example: {'active_setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at':
                '2026-02-18T09:30:00Z', 'fingerprint': 'example', 'image': {'baseImageDigest': 'example', 'capturedAt':
                '2026-02-18T09:30:00Z', 'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
                'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1, 'usable': True,
                'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture': {'at': '2026-02-18T09:30:00Z', 'message':
                'example', 'reason': 'example', 'setupRunId': 'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1,
                'exit_code': 1, 'failed_command': 'example', 'failed_line': 1, 'hint': 'example', 'hint_code': 'example',
                'message': 'example', 'phase': 'example', 'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status':
                'example', 'stderr_tail': 'example'}, 'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True,
                'status': 'example', 'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            setup_warnings (list[ManagedAgentsEnvironmentSetupWarning] | Unset): Advisory findings about the setup script
                (bash -lc wrapping, curl | sh, unpinned installs, ambiguous system Python, PATH replacement, or non-persistent
                shell activation), plus legacy_setup_discarded when the stored setup predates setup.script and is not run. Never
                block a save; computed on read.
            stopped_delete_after_seconds (int | Unset): Seconds a stopped sandbox is retained before it is deleted along
                with its volume; 0 uses the provider default.
     """

    computer_use: bool
    created_at: datetime.datetime
    environment_id: str
    name: str
    organization_id: str
    provider: str
    resources: ManagedAgentsEnvironmentResources
    scope: str
    setup: ManagedAgentsEnvironmentSetup
    updated_at: datetime.datetime
    config: ManagedAgentsEnvironmentConfig | Unset = UNSET
    description: str | Unset = UNSET
    env_vars: ManagedAgentsEnvironmentEnvVars | Unset = UNSET
    http_port: int | Unset = UNSET
    idle_stop_after_seconds: int | Unset = UNSET
    image: str | Unset = UNSET
    metadata: ManagedAgentsEnvironmentMetadata | Unset = UNSET
    mounts: list[ManagedAgentsEnvironmentMount] | Unset = UNSET
    network_policy: ManagedAgentsEnvironmentNetworkPolicy | Unset = UNSET
    privileged: bool | Unset = UNSET
    pvc_size_gi: int | Unset = UNSET
    secrets: ManagedAgentsEnvironmentSecrets | Unset = UNSET
    setup_updated_at: datetime.datetime | Unset = UNSET
    setup_updated_by_user_id: str | Unset = UNSET
    setup_verification: ManagedAgentsEnvironmentSetupVerification | Unset = UNSET
    setup_warnings: list[ManagedAgentsEnvironmentSetupWarning] | Unset = UNSET
    stopped_delete_after_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_config import ManagedAgentsEnvironmentConfig # noqa: PLC0415
        from ..models.managed_agents_environment_env_vars import ManagedAgentsEnvironmentEnvVars # noqa: PLC0415
        from ..models.managed_agents_environment_metadata import ManagedAgentsEnvironmentMetadata # noqa: PLC0415
        from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount # noqa: PLC0415
        from ..models.managed_agents_environment_network_policy import ManagedAgentsEnvironmentNetworkPolicy # noqa: PLC0415
        from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources # noqa: PLC0415
        from ..models.managed_agents_environment_secrets import ManagedAgentsEnvironmentSecrets # noqa: PLC0415
        from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup # noqa: PLC0415
        from ..models.managed_agents_environment_setup_verification import ManagedAgentsEnvironmentSetupVerification # noqa: PLC0415
        from ..models.managed_agents_environment_setup_warning import ManagedAgentsEnvironmentSetupWarning # noqa: PLC0415
        computer_use = self.computer_use

        created_at = self.created_at.isoformat()

        environment_id = self.environment_id

        name = self.name

        organization_id = self.organization_id

        provider = self.provider

        resources = self.resources.to_dict()

        scope = self.scope

        setup = self.setup.to_dict()

        updated_at = self.updated_at.isoformat()

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        description = self.description

        env_vars: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = self.env_vars.to_dict()

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



        network_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.network_policy, Unset):
            network_policy = self.network_policy.to_dict()

        privileged = self.privileged

        pvc_size_gi = self.pvc_size_gi

        secrets: dict[str, Any] | Unset = UNSET
        if not isinstance(self.secrets, Unset):
            secrets = self.secrets.to_dict()

        setup_updated_at: str | Unset = UNSET
        if not isinstance(self.setup_updated_at, Unset):
            setup_updated_at = self.setup_updated_at.isoformat()

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


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "computer_use": computer_use,
            "created_at": created_at,
            "environment_id": environment_id,
            "name": name,
            "organization_id": organization_id,
            "provider": provider,
            "resources": resources,
            "scope": scope,
            "setup": setup,
            "updated_at": updated_at,
        })
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
        if secrets is not UNSET:
            field_dict["secrets"] = secrets
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

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_config import ManagedAgentsEnvironmentConfig # noqa: PLC0415
        from ..models.managed_agents_environment_env_vars import ManagedAgentsEnvironmentEnvVars # noqa: PLC0415
        from ..models.managed_agents_environment_metadata import ManagedAgentsEnvironmentMetadata # noqa: PLC0415
        from ..models.managed_agents_environment_mount import ManagedAgentsEnvironmentMount # noqa: PLC0415
        from ..models.managed_agents_environment_network_policy import ManagedAgentsEnvironmentNetworkPolicy # noqa: PLC0415
        from ..models.managed_agents_environment_resources import ManagedAgentsEnvironmentResources # noqa: PLC0415
        from ..models.managed_agents_environment_secrets import ManagedAgentsEnvironmentSecrets # noqa: PLC0415
        from ..models.managed_agents_environment_setup import ManagedAgentsEnvironmentSetup # noqa: PLC0415
        from ..models.managed_agents_environment_setup_verification import ManagedAgentsEnvironmentSetupVerification # noqa: PLC0415
        from ..models.managed_agents_environment_setup_warning import ManagedAgentsEnvironmentSetupWarning # noqa: PLC0415
        d = dict(src_dict)
        computer_use = d.pop("computer_use")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        environment_id = d.pop("environment_id")

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        provider = d.pop("provider")

        resources = ManagedAgentsEnvironmentResources.from_dict(d.pop("resources"))




        scope = d.pop("scope")

        setup = ManagedAgentsEnvironmentSetup.from_dict(d.pop("setup"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _config = d.pop("config", UNSET)
        config: ManagedAgentsEnvironmentConfig | Unset
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = ManagedAgentsEnvironmentConfig.from_dict(_config)




        description = d.pop("description", UNSET)

        _env_vars = d.pop("env_vars", UNSET)
        env_vars: ManagedAgentsEnvironmentEnvVars | Unset
        if isinstance(_env_vars,  Unset):
            env_vars = UNSET
        else:
            env_vars = ManagedAgentsEnvironmentEnvVars.from_dict(_env_vars)




        http_port = d.pop("http_port", UNSET)

        idle_stop_after_seconds = d.pop("idle_stop_after_seconds", UNSET)

        image = d.pop("image", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsEnvironmentMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsEnvironmentMetadata.from_dict(_metadata)




        _mounts = d.pop("mounts", UNSET)
        mounts: list[ManagedAgentsEnvironmentMount] | Unset = UNSET
        if _mounts is not UNSET:
            mounts = []
            for mounts_item_data in _mounts:
                mounts_item = ManagedAgentsEnvironmentMount.from_dict(mounts_item_data)



                mounts.append(mounts_item)


        _network_policy = d.pop("network_policy", UNSET)
        network_policy: ManagedAgentsEnvironmentNetworkPolicy | Unset
        if isinstance(_network_policy,  Unset):
            network_policy = UNSET
        else:
            network_policy = ManagedAgentsEnvironmentNetworkPolicy.from_dict(_network_policy)




        privileged = d.pop("privileged", UNSET)

        pvc_size_gi = d.pop("pvc_size_gi", UNSET)

        _secrets = d.pop("secrets", UNSET)
        secrets: ManagedAgentsEnvironmentSecrets | Unset
        if isinstance(_secrets,  Unset):
            secrets = UNSET
        else:
            secrets = ManagedAgentsEnvironmentSecrets.from_dict(_secrets)




        _setup_updated_at = d.pop("setup_updated_at", UNSET)
        setup_updated_at: datetime.datetime | Unset
        if isinstance(_setup_updated_at,  Unset):
            setup_updated_at = UNSET
        else:
            setup_updated_at = datetime.datetime.fromisoformat(_setup_updated_at)




        setup_updated_by_user_id = d.pop("setup_updated_by_user_id", UNSET)

        _setup_verification = d.pop("setup_verification", UNSET)
        setup_verification: ManagedAgentsEnvironmentSetupVerification | Unset
        if isinstance(_setup_verification,  Unset):
            setup_verification = UNSET
        else:
            setup_verification = ManagedAgentsEnvironmentSetupVerification.from_dict(_setup_verification)




        _setup_warnings = d.pop("setup_warnings", UNSET)
        setup_warnings: list[ManagedAgentsEnvironmentSetupWarning] | Unset = UNSET
        if _setup_warnings is not UNSET:
            setup_warnings = []
            for setup_warnings_item_data in _setup_warnings:
                setup_warnings_item = ManagedAgentsEnvironmentSetupWarning.from_dict(setup_warnings_item_data)



                setup_warnings.append(setup_warnings_item)


        stopped_delete_after_seconds = d.pop("stopped_delete_after_seconds", UNSET)

        managed_agents_environment = cls(
            computer_use=computer_use,
            created_at=created_at,
            environment_id=environment_id,
            name=name,
            organization_id=organization_id,
            provider=provider,
            resources=resources,
            scope=scope,
            setup=setup,
            updated_at=updated_at,
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
            secrets=secrets,
            setup_updated_at=setup_updated_at,
            setup_updated_by_user_id=setup_updated_by_user_id,
            setup_verification=setup_verification,
            setup_warnings=setup_warnings,
            stopped_delete_after_seconds=stopped_delete_after_seconds,
        )


        managed_agents_environment.additional_properties = d
        return managed_agents_environment

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
