from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_access_policy import ManagedAgentsSessionAccessPolicy
from ..models.managed_agents_session_execution_state import ManagedAgentsSessionExecutionState
from ..models.managed_agents_session_kind import ManagedAgentsSessionKind
from ..models.managed_agents_session_status import ManagedAgentsSessionStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_active_handoff import ManagedAgentsActiveHandoff
  from ..models.managed_agents_session_agent_snapshot import ManagedAgentsSessionAgentSnapshot
  from ..models.managed_agents_session_config_type_0 import ManagedAgentsSessionConfigType0
  from ..models.managed_agents_session_failure import ManagedAgentsSessionFailure
  from ..models.managed_agents_session_metadata import ManagedAgentsSessionMetadata
  from ..models.managed_agents_session_model_snapshot import ManagedAgentsSessionModelSnapshot
  from ..models.managed_agents_session_source_refs import ManagedAgentsSessionSourceRefs
  from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef





T = TypeVar("T", bound="ManagedAgentsSession")



@_attrs_define
class ManagedAgentsSession:
    """ One durable agent run: its lifecycle status (active, awaiting_human, completed, failed, cancelled), the agent
    version, environment, model, and credentials it was pinned to, and its place in a multi-agent tree. Returned when
    starting, reading, or listing sessions; imported RL rollouts appear as sessions too and run no agent loop.

        Example:
            {'access_policy': 'admin_only', 'active_handoff': {'access_expires_at': '2026-02-18T09:30:00Z', 'deadline_at':
                '2026-02-18T09:30:00Z', 'handoff_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example',
                'requested_at': '2026-02-18T09:30:00Z', 'state': 'awaiting_user', 'wake_cause': 'example'}, 'agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_snapshot': {'key': 'example'}, 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'computer_use': True, 'concurrency_slot_held': True, 'config': {'key':
                'example'}, 'created_at': '2026-02-18T09:30:00Z', 'credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}],
                'credential_refs_configured': True, 'effective_model': 'example', 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'execution_state': 'provisioning', 'external_source_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'failure': {'at':
                '2026-02-18T09:30:00Z', 'category': 'transient', 'code': 'example', 'message': 'example', 'phase': 'example',
                'retryable': True}, 'forked_at_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'api_call',
                'last_activity_at': '2026-02-18T09:30:00Z', 'metadata': {'key': 'example'}, 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_snapshot': {'key': 'example'}, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'project_source': 'example', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_instance_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'sandbox_provider': 'example', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example',
                'source_refs': {'key': 'example'}, 'status': 'active', 'stop_reason': 'example', 'tenant_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z', 'user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_ids': ['example'], 'wake_at': '2026-02-18T09:30:00Z'}

        Attributes:
            computer_use (bool): Whether this session has a computer-enabled environment and a display that passed its
                readiness probe.
            config (ManagedAgentsSessionConfigType0 | None): Resolved per-session runtime settings written at start,
                including the snapshotted MCP servers and tool bindings, multi-agent roster, and delegation depth limits. Read-
                only to callers.
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            credential_refs (list[ManagedAgentsVaultCredentialRef] | None): Explicit allowlist of individual credentials the
                session may use. Read credential_refs_configured to tell an intentionally empty allowlist from a legacy session
                granted whole vaults.
            credential_refs_configured (bool): True when credential_refs is an explicit allowlist. False on legacy sessions
                granted every credential in their vaults, which would otherwise be indistinguishable from an empty allowlist.
            kind (ManagedAgentsSessionKind): What produced the session: api_call, chat, rollout (an imported RL rollout),
                subagent (delegated by another session), benchmark, evaluation (a platform-started evaluation run over other
                session snapshots), reflection (a platform-started memory consolidation), or session_analyst (a platform-started
                read-only assistant that answers questions about another session tree).
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            root_session_id (str): Root session of the multi-agent tree this session belongs to (UUID). Equal to session_id
                for a root session.
            session_id (str): Identifier for this session (UUID). Server-assigned.
            session_path (str): Position of this session within its tree, as a slash-delimited path of session ids. "/" for
                a root session.
            status (ManagedAgentsSessionStatus): Coarse session state shared by Managed Agents and imported RL rollouts.
                Example: active.
            updated_at (datetime.datetime): RFC 3339 timestamp of the last change to this record. Server-assigned.
            access_policy (ManagedAgentsSessionAccessPolicy | Unset): Explicit access classification. Omitted/null preserves
                legacy public behavior; admin_only requires RL_DATA_READ and the current Admin organization role on public APIs;
                platform_internal is the platform's own session over this organization's data, kept out of session listings but
                readable in-organization when addressed directly.
            active_handoff (ManagedAgentsActiveHandoff | Unset): Public, credential-free state of a browser handoff that is
                awaiting a person, currently driven by one, or being resolved back to the agent. Example: {'access_expires_at':
                '2026-02-18T09:30:00Z', 'deadline_at': '2026-02-18T09:30:00Z', 'handoff_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'requested_at': '2026-02-18T09:30:00Z', 'state':
                'awaiting_user', 'wake_cause': 'example'}.
            agent_id (str | Unset): Agent this session runs (UUID). Empty for imported sessions that were not started from
                an agent.
            agent_snapshot (ManagedAgentsSessionAgentSnapshot | Unset): The agent version's definition as it stood when the
                session started, frozen so later edits to the agent cannot change this session's behavior.
            agent_version_id (str | Unset): Agent version this session runs (UUID), pinned at start so a later edit to the
                agent cannot change a running session.
            concurrency_slot_held (bool | Unset): Whether this root session currently occupies the agent's
                max_concurrent_sessions slot. True while admitted and non-terminal. False exclusively while an active queued
                root waits to start. Omitted for unlimited agents, child sessions, legacy rows, and terminal or deleted
                sessions.
            effective_model (str | Unset): Provider-qualified model string frozen for this session, including a per-session
                gateway override. Prefer this over resolving model_ref_id or the current agent version when displaying what
                actually ran.
            environment_id (str | Unset): Environment whose sandbox definition this session runs in (UUID).
            execution_state (ManagedAgentsSessionExecutionState | Unset): Where the agent loop is. Empty for sessions
                without a loop, such as imported rollouts. provisioning normally clears in under a minute and is bounded: a
                sandbox that does not become ready within the deployment's compute-ready timeout (five minutes by default) fails
                the session with sandbox_provision_timeout, so a session is never stuck here indefinitely. This field, read from
                the session itself, is the authoritative status -- a session's event stream is written on a separate path and
                can lag it, so an empty event list does not mean the session is still starting. When a session leaves
                provisioning by failing, failure carries the reason.
            external_source_id (str | Unset): Identifier of the session's counterpart in the external_source_type system, so
                a caller can find the session again from that side. Set together with external_source_type.
            external_source_type (str | Unset): Kind of external system this session is correlated to, e.g. slack_thread.
                Set together with external_source_id and filterable when listing sessions.
            failure (ManagedAgentsSessionFailure | Unset): Structured, sanitized reason a session terminated abnormally.
                Present on a session only after a terminal failure; healthy and legacy sessions omit it. Example: {'at':
                '2026-02-18T09:30:00Z', 'category': 'transient', 'code': 'example', 'message': 'example', 'phase': 'example',
                'retryable': True}.
            forked_at_event_id (str | Unset): Event in the parent session (UUID) this session was forked from, so the fork's
                starting context is identifiable. Set only on forks.
            last_activity_at (datetime.datetime | Unset): RFC 3339 timestamp of when the agent loop last made progress.
                Distinct from updated_at, which any metadata write touches. Absent for sessions that run no loop.
            metadata (ManagedAgentsSessionMetadata | Unset): Caller-defined string key/value pairs supplied when the session
                was started, e.g. ids from your own system. Immutable, present on root sessions only, and filterable with
                metadata=key:value or metadata_key=key on GET /v1/sessions. At most 32 entries; keys use letters, digits, '_',
                '.', and '-' up to 64 characters; values are 1-512 characters.
            model_ref_id (str | Unset): Model reference the session's turns run on (UUID), resolved at start from the agent
                version or the start request.
            model_snapshot (ManagedAgentsSessionModelSnapshot | Unset): The resolved model reference and inference settings
                as they stood when the session started, frozen for the same reason as agent_snapshot.
            parent_session_id (str | Unset): Session that created this one (UUID) — the delegating session for a subagent,
                or the source session for a fork. Empty on a root session.
            project_id (str | Unset): Identifier of the external project the session's work belongs to, interpreted
                according to project_source.
            project_source (str | Unset): System that project_id names. Set on imported rollouts to record their provenance.
            sandbox_instance_id (str | Unset): Provider-assigned id of the sandbox instance serving this session. Empty
                before provisioning finishes; historical self_hosted sessions may also have no instance id.
            sandbox_provider (str | Unset): Sandbox runtime that provisioned this session's compute, from the supported
                sandbox providers list.
            source_refs (ManagedAgentsSessionSourceRefs | Unset): Secondary provenance ids from the originating system
                beyond the primary external source, e.g. an imported rollout's problem, problem-version, and run ids.
            stop_reason (str | Unset): Why the loop is not running. Set whenever execution_state is idle or completed.
                sleeping means the agent chose to wait and the session resumes on the next message or at wake_at;
                awaiting_subagents means a coordinator is waiting on delegated work.
            tenant_id (str | Unset): Data-residency tenant the session's content is stored under, resolved from the request
                scope. A child session inherits its parent's value.
            user_id (str | Unset): User the session was started on behalf of, resolved from the request scope. Empty for
                sessions started by a service credential.
            vault_ids (list[str] | Unset): Vaults (UUIDs) the session may draw credentials from. Combine with
                credential_refs to narrow the grant to specific credentials.
            wake_at (datetime.datetime | Unset): RFC 3339 timestamp at which a sleeping session wakes itself if nobody
                messages it first. Absent unless the agent scheduled a timed wait.
     """

    computer_use: bool
    config: ManagedAgentsSessionConfigType0 | None
    created_at: datetime.datetime
    credential_refs: list[ManagedAgentsVaultCredentialRef] | None
    credential_refs_configured: bool
    kind: ManagedAgentsSessionKind
    organization_id: str
    root_session_id: str
    session_id: str
    session_path: str
    status: ManagedAgentsSessionStatus
    updated_at: datetime.datetime
    access_policy: ManagedAgentsSessionAccessPolicy | Unset = UNSET
    active_handoff: ManagedAgentsActiveHandoff | Unset = UNSET
    agent_id: str | Unset = UNSET
    agent_snapshot: ManagedAgentsSessionAgentSnapshot | Unset = UNSET
    agent_version_id: str | Unset = UNSET
    concurrency_slot_held: bool | Unset = UNSET
    effective_model: str | Unset = UNSET
    environment_id: str | Unset = UNSET
    execution_state: ManagedAgentsSessionExecutionState | Unset = UNSET
    external_source_id: str | Unset = UNSET
    external_source_type: str | Unset = UNSET
    failure: ManagedAgentsSessionFailure | Unset = UNSET
    forked_at_event_id: str | Unset = UNSET
    last_activity_at: datetime.datetime | Unset = UNSET
    metadata: ManagedAgentsSessionMetadata | Unset = UNSET
    model_ref_id: str | Unset = UNSET
    model_snapshot: ManagedAgentsSessionModelSnapshot | Unset = UNSET
    parent_session_id: str | Unset = UNSET
    project_id: str | Unset = UNSET
    project_source: str | Unset = UNSET
    sandbox_instance_id: str | Unset = UNSET
    sandbox_provider: str | Unset = UNSET
    source_refs: ManagedAgentsSessionSourceRefs | Unset = UNSET
    stop_reason: str | Unset = UNSET
    tenant_id: str | Unset = UNSET
    user_id: str | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    wake_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_active_handoff import ManagedAgentsActiveHandoff # noqa: PLC0415
        from ..models.managed_agents_session_agent_snapshot import ManagedAgentsSessionAgentSnapshot # noqa: PLC0415
        from ..models.managed_agents_session_config_type_0 import ManagedAgentsSessionConfigType0 # noqa: PLC0415
        from ..models.managed_agents_session_failure import ManagedAgentsSessionFailure # noqa: PLC0415
        from ..models.managed_agents_session_metadata import ManagedAgentsSessionMetadata # noqa: PLC0415
        from ..models.managed_agents_session_model_snapshot import ManagedAgentsSessionModelSnapshot # noqa: PLC0415
        from ..models.managed_agents_session_source_refs import ManagedAgentsSessionSourceRefs # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        computer_use = self.computer_use

        config: dict[str, Any] | None
        if isinstance(self.config, ManagedAgentsSessionConfigType0):
            config = self.config.to_dict()
        else:
            config = self.config

        created_at = self.created_at.isoformat()

        credential_refs: list[dict[str, Any]] | None
        if isinstance(self.credential_refs, list):
            credential_refs = []
            for credential_refs_type_0_item_data in self.credential_refs:
                credential_refs_type_0_item = credential_refs_type_0_item_data.to_dict()
                credential_refs.append(credential_refs_type_0_item)


        else:
            credential_refs = self.credential_refs

        credential_refs_configured = self.credential_refs_configured

        kind = self.kind.value

        organization_id = self.organization_id

        root_session_id = self.root_session_id

        session_id = self.session_id

        session_path = self.session_path

        status = self.status.value

        updated_at = self.updated_at.isoformat()

        access_policy: str | Unset = UNSET
        if not isinstance(self.access_policy, Unset):
            access_policy = self.access_policy.value


        active_handoff: dict[str, Any] | Unset = UNSET
        if not isinstance(self.active_handoff, Unset):
            active_handoff = self.active_handoff.to_dict()

        agent_id = self.agent_id

        agent_snapshot: dict[str, Any] | Unset = UNSET
        if not isinstance(self.agent_snapshot, Unset):
            agent_snapshot = self.agent_snapshot.to_dict()

        agent_version_id = self.agent_version_id

        concurrency_slot_held = self.concurrency_slot_held

        effective_model = self.effective_model

        environment_id = self.environment_id

        execution_state: str | Unset = UNSET
        if not isinstance(self.execution_state, Unset):
            execution_state = self.execution_state.value


        external_source_id = self.external_source_id

        external_source_type = self.external_source_type

        failure: dict[str, Any] | Unset = UNSET
        if not isinstance(self.failure, Unset):
            failure = self.failure.to_dict()

        forked_at_event_id = self.forked_at_event_id

        last_activity_at: str | Unset = UNSET
        if not isinstance(self.last_activity_at, Unset):
            last_activity_at = self.last_activity_at.isoformat()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        model_ref_id = self.model_ref_id

        model_snapshot: dict[str, Any] | Unset = UNSET
        if not isinstance(self.model_snapshot, Unset):
            model_snapshot = self.model_snapshot.to_dict()

        parent_session_id = self.parent_session_id

        project_id = self.project_id

        project_source = self.project_source

        sandbox_instance_id = self.sandbox_instance_id

        sandbox_provider = self.sandbox_provider

        source_refs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.source_refs, Unset):
            source_refs = self.source_refs.to_dict()

        stop_reason = self.stop_reason

        tenant_id = self.tenant_id

        user_id = self.user_id

        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids



        wake_at: str | Unset = UNSET
        if not isinstance(self.wake_at, Unset):
            wake_at = self.wake_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "computer_use": computer_use,
            "config": config,
            "created_at": created_at,
            "credential_refs": credential_refs,
            "credential_refs_configured": credential_refs_configured,
            "kind": kind,
            "organization_id": organization_id,
            "root_session_id": root_session_id,
            "session_id": session_id,
            "session_path": session_path,
            "status": status,
            "updated_at": updated_at,
        })
        if access_policy is not UNSET:
            field_dict["access_policy"] = access_policy
        if active_handoff is not UNSET:
            field_dict["active_handoff"] = active_handoff
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if agent_snapshot is not UNSET:
            field_dict["agent_snapshot"] = agent_snapshot
        if agent_version_id is not UNSET:
            field_dict["agent_version_id"] = agent_version_id
        if concurrency_slot_held is not UNSET:
            field_dict["concurrency_slot_held"] = concurrency_slot_held
        if effective_model is not UNSET:
            field_dict["effective_model"] = effective_model
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if execution_state is not UNSET:
            field_dict["execution_state"] = execution_state
        if external_source_id is not UNSET:
            field_dict["external_source_id"] = external_source_id
        if external_source_type is not UNSET:
            field_dict["external_source_type"] = external_source_type
        if failure is not UNSET:
            field_dict["failure"] = failure
        if forked_at_event_id is not UNSET:
            field_dict["forked_at_event_id"] = forked_at_event_id
        if last_activity_at is not UNSET:
            field_dict["last_activity_at"] = last_activity_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if model_ref_id is not UNSET:
            field_dict["model_ref_id"] = model_ref_id
        if model_snapshot is not UNSET:
            field_dict["model_snapshot"] = model_snapshot
        if parent_session_id is not UNSET:
            field_dict["parent_session_id"] = parent_session_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_source is not UNSET:
            field_dict["project_source"] = project_source
        if sandbox_instance_id is not UNSET:
            field_dict["sandbox_instance_id"] = sandbox_instance_id
        if sandbox_provider is not UNSET:
            field_dict["sandbox_provider"] = sandbox_provider
        if source_refs is not UNSET:
            field_dict["source_refs"] = source_refs
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids
        if wake_at is not UNSET:
            field_dict["wake_at"] = wake_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_active_handoff import ManagedAgentsActiveHandoff # noqa: PLC0415
        from ..models.managed_agents_session_agent_snapshot import ManagedAgentsSessionAgentSnapshot # noqa: PLC0415
        from ..models.managed_agents_session_config_type_0 import ManagedAgentsSessionConfigType0 # noqa: PLC0415
        from ..models.managed_agents_session_failure import ManagedAgentsSessionFailure # noqa: PLC0415
        from ..models.managed_agents_session_metadata import ManagedAgentsSessionMetadata # noqa: PLC0415
        from ..models.managed_agents_session_model_snapshot import ManagedAgentsSessionModelSnapshot # noqa: PLC0415
        from ..models.managed_agents_session_source_refs import ManagedAgentsSessionSourceRefs # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        d = dict(src_dict)
        computer_use = d.pop("computer_use")

        def _parse_config(data: object) -> ManagedAgentsSessionConfigType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_type_0 = ManagedAgentsSessionConfigType0.from_dict(data)



                return config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsSessionConfigType0 | None, data)

        config = _parse_config(d.pop("config"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        def _parse_credential_refs(data: object) -> list[ManagedAgentsVaultCredentialRef] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                credential_refs_type_0 = []
                _credential_refs_type_0 = data
                for credential_refs_type_0_item_data in (_credential_refs_type_0):
                    credential_refs_type_0_item = ManagedAgentsVaultCredentialRef.from_dict(credential_refs_type_0_item_data)



                    credential_refs_type_0.append(credential_refs_type_0_item)

                return credential_refs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsVaultCredentialRef] | None, data)

        credential_refs = _parse_credential_refs(d.pop("credential_refs"))


        credential_refs_configured = d.pop("credential_refs_configured")

        kind = ManagedAgentsSessionKind(d.pop("kind"))




        organization_id = d.pop("organization_id")

        root_session_id = d.pop("root_session_id")

        session_id = d.pop("session_id")

        session_path = d.pop("session_path")

        status = ManagedAgentsSessionStatus(d.pop("status"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _access_policy = d.pop("access_policy", UNSET)
        access_policy: ManagedAgentsSessionAccessPolicy | Unset
        if isinstance(_access_policy,  Unset):
            access_policy = UNSET
        else:
            access_policy = ManagedAgentsSessionAccessPolicy(_access_policy)




        _active_handoff = d.pop("active_handoff", UNSET)
        active_handoff: ManagedAgentsActiveHandoff | Unset
        if isinstance(_active_handoff,  Unset):
            active_handoff = UNSET
        else:
            active_handoff = ManagedAgentsActiveHandoff.from_dict(_active_handoff)




        agent_id = d.pop("agent_id", UNSET)

        _agent_snapshot = d.pop("agent_snapshot", UNSET)
        agent_snapshot: ManagedAgentsSessionAgentSnapshot | Unset
        if isinstance(_agent_snapshot,  Unset):
            agent_snapshot = UNSET
        else:
            agent_snapshot = ManagedAgentsSessionAgentSnapshot.from_dict(_agent_snapshot)




        agent_version_id = d.pop("agent_version_id", UNSET)

        concurrency_slot_held = d.pop("concurrency_slot_held", UNSET)

        effective_model = d.pop("effective_model", UNSET)

        environment_id = d.pop("environment_id", UNSET)

        _execution_state = d.pop("execution_state", UNSET)
        execution_state: ManagedAgentsSessionExecutionState | Unset
        if isinstance(_execution_state,  Unset):
            execution_state = UNSET
        else:
            execution_state = ManagedAgentsSessionExecutionState(_execution_state)




        external_source_id = d.pop("external_source_id", UNSET)

        external_source_type = d.pop("external_source_type", UNSET)

        _failure = d.pop("failure", UNSET)
        failure: ManagedAgentsSessionFailure | Unset
        if isinstance(_failure,  Unset):
            failure = UNSET
        else:
            failure = ManagedAgentsSessionFailure.from_dict(_failure)




        forked_at_event_id = d.pop("forked_at_event_id", UNSET)

        _last_activity_at = d.pop("last_activity_at", UNSET)
        last_activity_at: datetime.datetime | Unset
        if isinstance(_last_activity_at,  Unset):
            last_activity_at = UNSET
        else:
            last_activity_at = datetime.datetime.fromisoformat(_last_activity_at)




        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsSessionMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsSessionMetadata.from_dict(_metadata)




        model_ref_id = d.pop("model_ref_id", UNSET)

        _model_snapshot = d.pop("model_snapshot", UNSET)
        model_snapshot: ManagedAgentsSessionModelSnapshot | Unset
        if isinstance(_model_snapshot,  Unset):
            model_snapshot = UNSET
        else:
            model_snapshot = ManagedAgentsSessionModelSnapshot.from_dict(_model_snapshot)




        parent_session_id = d.pop("parent_session_id", UNSET)

        project_id = d.pop("project_id", UNSET)

        project_source = d.pop("project_source", UNSET)

        sandbox_instance_id = d.pop("sandbox_instance_id", UNSET)

        sandbox_provider = d.pop("sandbox_provider", UNSET)

        _source_refs = d.pop("source_refs", UNSET)
        source_refs: ManagedAgentsSessionSourceRefs | Unset
        if isinstance(_source_refs,  Unset):
            source_refs = UNSET
        else:
            source_refs = ManagedAgentsSessionSourceRefs.from_dict(_source_refs)




        stop_reason = d.pop("stop_reason", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        user_id = d.pop("user_id", UNSET)

        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        _wake_at = d.pop("wake_at", UNSET)
        wake_at: datetime.datetime | Unset
        if isinstance(_wake_at,  Unset):
            wake_at = UNSET
        else:
            wake_at = datetime.datetime.fromisoformat(_wake_at)




        managed_agents_session = cls(
            computer_use=computer_use,
            config=config,
            created_at=created_at,
            credential_refs=credential_refs,
            credential_refs_configured=credential_refs_configured,
            kind=kind,
            organization_id=organization_id,
            root_session_id=root_session_id,
            session_id=session_id,
            session_path=session_path,
            status=status,
            updated_at=updated_at,
            access_policy=access_policy,
            active_handoff=active_handoff,
            agent_id=agent_id,
            agent_snapshot=agent_snapshot,
            agent_version_id=agent_version_id,
            concurrency_slot_held=concurrency_slot_held,
            effective_model=effective_model,
            environment_id=environment_id,
            execution_state=execution_state,
            external_source_id=external_source_id,
            external_source_type=external_source_type,
            failure=failure,
            forked_at_event_id=forked_at_event_id,
            last_activity_at=last_activity_at,
            metadata=metadata,
            model_ref_id=model_ref_id,
            model_snapshot=model_snapshot,
            parent_session_id=parent_session_id,
            project_id=project_id,
            project_source=project_source,
            sandbox_instance_id=sandbox_instance_id,
            sandbox_provider=sandbox_provider,
            source_refs=source_refs,
            stop_reason=stop_reason,
            tenant_id=tenant_id,
            user_id=user_id,
            vault_ids=vault_ids,
            wake_at=wake_at,
        )


        managed_agents_session.additional_properties = d
        return managed_agents_session

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
