from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_define_outcome_request import ManagedAgentsDefineOutcomeRequest
  from ..models.managed_agents_evaluation_selector_request import ManagedAgentsEvaluationSelectorRequest
  from ..models.managed_agents_session_resource_request import ManagedAgentsSessionResourceRequest
  from ..models.managed_agents_start_session_request_metadata import ManagedAgentsStartSessionRequestMetadata
  from ..models.managed_agents_team_request import ManagedAgentsTeamRequest
  from ..models.managed_agents_vault_credential_ref_request import ManagedAgentsVaultCredentialRefRequest





T = TypeVar("T", bound="ManagedAgentsStartSessionRequest")



@_attrs_define
class ManagedAgentsStartSessionRequest:
    """ Request body for starting a session: which agent to run, the environment to run it in, the vault grants it receives,
    and the opening message and/or outcome that gives it work.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluation': {'limit': 1, 'session_ids': ['example'], 'statuses':
                ['active']}, 'external_source_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example',
                'message': 'example', 'metadata': {'key': 'example'}, 'outcome': {'description': 'Export the product catalog to
                /out/catalog.csv', 'rubric': '- /out/catalog.csv exists\\n- The CSV has a header row with sku, name, and price
                columns\\n- Every price value is a number'}, 'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'referenced_session_ids': ['example'], 'resources': [{'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'mount_path': 'example', 'relative_path': 'example', 'type': 'file'}], 'skip_default_outcome': True, 'team':
                {'mode': 'auto'}, 'vault_ids': ['example']}

        Attributes:
            agent_id (str): The agent to run, from POST /v1/agents or GET /v1/agents. Its current version is snapshotted
                into the session, so later edits to the agent do not affect this run.
            credential_refs (list[ManagedAgentsVaultCredentialRefRequest] | Unset): Optional per-item allowlist inside
                vault_ids. The list is a whitelist across every granted vault, not a filter within one, so it must name every
                item the session should receive. Omit with explicit vault_ids to enable all items; [] alongside a non-empty
                vault_ids is rejected because it would enable none. Omit both fields to use the agent version's defaults.
            environment_id (str | Unset): The environment whose sandbox the session runs in, from POST /v1/environments or
                GET /v1/environments. Required for ordinary agents; evaluation agents omit it because the run has no parent
                sandbox and each child clones its target workspace.
            evaluation (ManagedAgentsEvaluationSelectorRequest | Unset): A bounded evaluation target selector: explicit
                session ids, or statuses plus a newest-first limit. Example: {'limit': 1, 'session_ids': ['example'],
                'statuses': ['active']}.
            external_source_id (str | Unset): Stable identity inside the external system, e.g. a Slack thread key or a pull-
                request key. Set together with external_source_type.
            external_source_type (str | Unset): Kind of external system this session correlates to, e.g. slack or github.
                Set together with external_source_id; sessions can then be filtered by both on GET /v1/sessions.
            message (str | Unset): Opening user message for the session, and the context the agent works from. Send it
                alongside an outcome to supply facts the agent needs without making them part of what the grader measures; the
                grader never sees it. Kept in the session's system prompt for the whole run, so context compaction cannot
                summarize it away.
            metadata (ManagedAgentsStartSessionRequestMetadata | Unset): Caller-defined string key/value pairs stored on the
                session, e.g. ids that map it back to your own system. Write-once: they cannot be changed after start. At most
                32 entries; keys use letters, digits, '_', '.', and '-' up to 64 characters; values are 1-512 characters without
                control characters. Returned as metadata on GET /v1/sessions and filterable with metadata=key:value (repeatable,
                AND) or metadata_key=key.
            outcome (ManagedAgentsDefineOutcomeRequest | Unset): A definition of done for a session -- the task plus the
                rubric it is graded against. Accepted both when starting a session and when adding an outcome to a running one.
                Exactly one of rubric and rubric_ref is required. Example: {'description': 'Export the product catalog to
                /out/catalog.csv', 'rubric': '- /out/catalog.csv exists\\n- The CSV has a header row with sku, name, and price
                columns\\n- Every price value is a number'}.
            project_id (str | Unset): Labelbox project this session's work is attributed to, which the model gateway bills
                against. A non-empty value overrides the agent version's default_project_id. Required after defaulting when the
                chosen model runs on an account restricted to customer projects, such as the Anthropic HDO models.
            referenced_session_ids (list[str] | Unset): Prior sessions this one may read, by session id. Each grants read
                access to the whole tree containing it -- transcript, agents, tools, cost, outcome, and output files -- through
                a set of read-only tools offered to the agent only when at least one reference exists. Each id is authorized
                under your own scope, so a session you cannot read refuses the whole request with 404 and starts nothing.
                Sessions from another organization, RL data (admin_only) sessions, and session analysts are never referenceable.
                More may be added later with referenced_session_ids on POST /v1/sessions/{session_id}/events.
            resources (list[ManagedAgentsSessionResourceRequest] | Unset): Files to mount read-only into the session's
                sandbox, under its files directory, before the first turn. Each is frozen at the digest it has now. All-or-
                nothing: one unknown or out-of-scope file_id refuses the whole request with 404 and creates nothing. Requires an
                environment with a sandbox.
            skip_default_outcome (bool | Unset): Start ungraded even when the agent version defines a default_rubric. Only
                needed for an agent that has one, since omitting outcome otherwise inherits it.
            team (ManagedAgentsTeamRequest | Unset): Per-session override of the agent's team setting: whether the tree may
                become a team. Omit the mode to keep the agent's setting. The seats a team may fill are the roster's
                limits.max_concurrent_threads; recruits are sized to the claimable work under that cap, and teammates may always
                message each other directly. Example: {'mode': 'auto'}.
            vault_ids (list[str] | Unset): Vault grants for this session. Omit to use the agent version's default_vault_ids;
                send [] to disable all defaults.
     """

    agent_id: str
    credential_refs: list[ManagedAgentsVaultCredentialRefRequest] | Unset = UNSET
    environment_id: str | Unset = UNSET
    evaluation: ManagedAgentsEvaluationSelectorRequest | Unset = UNSET
    external_source_id: str | Unset = UNSET
    external_source_type: str | Unset = UNSET
    message: str | Unset = UNSET
    metadata: ManagedAgentsStartSessionRequestMetadata | Unset = UNSET
    outcome: ManagedAgentsDefineOutcomeRequest | Unset = UNSET
    project_id: str | Unset = UNSET
    referenced_session_ids: list[str] | Unset = UNSET
    resources: list[ManagedAgentsSessionResourceRequest] | Unset = UNSET
    skip_default_outcome: bool | Unset = UNSET
    team: ManagedAgentsTeamRequest | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_define_outcome_request import ManagedAgentsDefineOutcomeRequest # noqa: PLC0415
        from ..models.managed_agents_evaluation_selector_request import ManagedAgentsEvaluationSelectorRequest # noqa: PLC0415
        from ..models.managed_agents_session_resource_request import ManagedAgentsSessionResourceRequest # noqa: PLC0415
        from ..models.managed_agents_start_session_request_metadata import ManagedAgentsStartSessionRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_team_request import ManagedAgentsTeamRequest # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref_request import ManagedAgentsVaultCredentialRefRequest # noqa: PLC0415
        agent_id = self.agent_id

        credential_refs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.credential_refs, Unset):
            credential_refs = []
            for credential_refs_item_data in self.credential_refs:
                credential_refs_item = credential_refs_item_data.to_dict()
                credential_refs.append(credential_refs_item)



        environment_id = self.environment_id

        evaluation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation, Unset):
            evaluation = self.evaluation.to_dict()

        external_source_id = self.external_source_id

        external_source_type = self.external_source_type

        message = self.message

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        outcome: dict[str, Any] | Unset = UNSET
        if not isinstance(self.outcome, Unset):
            outcome = self.outcome.to_dict()

        project_id = self.project_id

        referenced_session_ids: list[str] | Unset = UNSET
        if not isinstance(self.referenced_session_ids, Unset):
            referenced_session_ids = self.referenced_session_ids



        resources: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = []
            for resources_item_data in self.resources:
                resources_item = resources_item_data.to_dict()
                resources.append(resources_item)



        skip_default_outcome = self.skip_default_outcome

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
        })
        if credential_refs is not UNSET:
            field_dict["credential_refs"] = credential_refs
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if evaluation is not UNSET:
            field_dict["evaluation"] = evaluation
        if external_source_id is not UNSET:
            field_dict["external_source_id"] = external_source_id
        if external_source_type is not UNSET:
            field_dict["external_source_type"] = external_source_type
        if message is not UNSET:
            field_dict["message"] = message
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if outcome is not UNSET:
            field_dict["outcome"] = outcome
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if referenced_session_ids is not UNSET:
            field_dict["referenced_session_ids"] = referenced_session_ids
        if resources is not UNSET:
            field_dict["resources"] = resources
        if skip_default_outcome is not UNSET:
            field_dict["skip_default_outcome"] = skip_default_outcome
        if team is not UNSET:
            field_dict["team"] = team
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_define_outcome_request import ManagedAgentsDefineOutcomeRequest # noqa: PLC0415
        from ..models.managed_agents_evaluation_selector_request import ManagedAgentsEvaluationSelectorRequest # noqa: PLC0415
        from ..models.managed_agents_session_resource_request import ManagedAgentsSessionResourceRequest # noqa: PLC0415
        from ..models.managed_agents_start_session_request_metadata import ManagedAgentsStartSessionRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_team_request import ManagedAgentsTeamRequest # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref_request import ManagedAgentsVaultCredentialRefRequest # noqa: PLC0415
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        _credential_refs = d.pop("credential_refs", UNSET)
        credential_refs: list[ManagedAgentsVaultCredentialRefRequest] | Unset = UNSET
        if _credential_refs is not UNSET:
            credential_refs = []
            for credential_refs_item_data in _credential_refs:
                credential_refs_item = ManagedAgentsVaultCredentialRefRequest.from_dict(credential_refs_item_data)



                credential_refs.append(credential_refs_item)


        environment_id = d.pop("environment_id", UNSET)

        _evaluation = d.pop("evaluation", UNSET)
        evaluation: ManagedAgentsEvaluationSelectorRequest | Unset
        if isinstance(_evaluation,  Unset):
            evaluation = UNSET
        else:
            evaluation = ManagedAgentsEvaluationSelectorRequest.from_dict(_evaluation)




        external_source_id = d.pop("external_source_id", UNSET)

        external_source_type = d.pop("external_source_type", UNSET)

        message = d.pop("message", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsStartSessionRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsStartSessionRequestMetadata.from_dict(_metadata)




        _outcome = d.pop("outcome", UNSET)
        outcome: ManagedAgentsDefineOutcomeRequest | Unset
        if isinstance(_outcome,  Unset):
            outcome = UNSET
        else:
            outcome = ManagedAgentsDefineOutcomeRequest.from_dict(_outcome)




        project_id = d.pop("project_id", UNSET)

        referenced_session_ids = cast(list[str], d.pop("referenced_session_ids", UNSET))


        _resources = d.pop("resources", UNSET)
        resources: list[ManagedAgentsSessionResourceRequest] | Unset = UNSET
        if _resources is not UNSET:
            resources = []
            for resources_item_data in _resources:
                resources_item = ManagedAgentsSessionResourceRequest.from_dict(resources_item_data)



                resources.append(resources_item)


        skip_default_outcome = d.pop("skip_default_outcome", UNSET)

        _team = d.pop("team", UNSET)
        team: ManagedAgentsTeamRequest | Unset
        if isinstance(_team,  Unset):
            team = UNSET
        else:
            team = ManagedAgentsTeamRequest.from_dict(_team)




        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        managed_agents_start_session_request = cls(
            agent_id=agent_id,
            credential_refs=credential_refs,
            environment_id=environment_id,
            evaluation=evaluation,
            external_source_id=external_source_id,
            external_source_type=external_source_type,
            message=message,
            metadata=metadata,
            outcome=outcome,
            project_id=project_id,
            referenced_session_ids=referenced_session_ids,
            resources=resources,
            skip_default_outcome=skip_default_outcome,
            team=team,
            vault_ids=vault_ids,
        )


        managed_agents_start_session_request.additional_properties = d
        return managed_agents_start_session_request

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
