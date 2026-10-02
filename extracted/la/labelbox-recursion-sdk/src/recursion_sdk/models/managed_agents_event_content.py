from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_content_block import ManagedAgentsContentBlock
  from ..models.managed_agents_evaluation_budget_reached import ManagedAgentsEvaluationBudgetReached
  from ..models.managed_agents_evaluation_plan_frozen import ManagedAgentsEvaluationPlanFrozen
  from ..models.managed_agents_evaluation_run_finished import ManagedAgentsEvaluationRunFinished
  from ..models.managed_agents_evaluation_target_skipped import ManagedAgentsEvaluationTargetSkipped
  from ..models.managed_agents_evaluation_target_started import ManagedAgentsEvaluationTargetStarted
  from ..models.managed_agents_evaluation_verdict_recorded import ManagedAgentsEvaluationVerdictRecorded
  from ..models.managed_agents_event_content_metadata import ManagedAgentsEventContentMetadata
  from ..models.managed_agents_plan_item import ManagedAgentsPlanItem
  from ..models.managed_agents_tool_definition import ManagedAgentsToolDefinition
  from ..models.managed_agents_usage import ManagedAgentsUsage





T = TypeVar("T", bound="ManagedAgentsEventContent")



@_attrs_define
class ManagedAgentsEventContent:
    """ The body of a session event, shaped like a provider message: content blocks plus the stop reason and token usage the
    provider returned. Every event in a session transcript carries one.

        Example:
            {'blocks': [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example', 'encrypted_content':
                'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error':
                True, 'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example', 'provider':
                'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256': 'example',
                'signature': 'example', 'source': {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'},
                'summary': [], 'text': 'example', 'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'type': 'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at': '2026-02-18T09:30:00Z',
                'width': 1}], 'evaluation_budget_reached': {'affected_target_session_ids':
                ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'max_tree_cost_usd': 'example'}, 'evaluation_plan_frozen':
                {'criteria': [{'criterion_key': 'example', 'criterion_text': 'example'}], 'max_concurrent_threads': 1,
                'max_tree_cost_usd': 'example', 'targets': [{'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}, 'evaluation_run_finished': {'failure_code':
                'plan_failed', 'failure_message': 'example', 'targets_budget_reached': 1, 'targets_skipped': 1, 'targets_total':
                1, 'terminal_status': 'completed', 'verdicts_recorded': 1}, 'evaluation_target_skipped': {'child_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'reason_code': 'child_create_failed',
                'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'evaluation_target_started': {'child_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'clone_state': 'ready', 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_provider': 'example', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'evaluation_verdict_recorded': {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cost_completeness':
                'complete', 'cost_usd': 'example', 'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'failed_criterion_keys': ['example'], 'result': 'pass', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'metadata': {'key': 'example'}, 'plan': [{'content': 'example', 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'status': 'example'}], 'stop_reason': 'example', 'tools': [{'description': 'example', 'input_schema': {'key':
                'example'}, 'name': 'example-name'}], 'usage': {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_usd':
                1.5, 'input_tokens': 1, 'output_tokens': 1}}

        Attributes:
            blocks (list[ManagedAgentsContentBlock] | None): Ordered content blocks of this message, in the provider's
                content-block form. Empty for events that carry no message body.
            evaluation_budget_reached (ManagedAgentsEvaluationBudgetReached | Unset): Audit event payload listing targets
                stopped or left unadmitted when the evaluation tree reached its exact USD cap. Example:
                {'affected_target_session_ids': ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'max_tree_cost_usd': 'example'}.
            evaluation_plan_frozen (ManagedAgentsEvaluationPlanFrozen | Unset): Audit event payload that freezes the
                complete target set, rubric, concurrency, and cost cap before child work starts. Example: {'criteria':
                [{'criterion_key': 'example', 'criterion_text': 'example'}], 'max_concurrent_threads': 1, 'max_tree_cost_usd':
                'example', 'targets': [{'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}.
            evaluation_run_finished (ManagedAgentsEvaluationRunFinished | Unset): Terminal audit payload summarizing planned
                targets, completed verdict audits, skips, budget stops, and any systemic failure. Example: {'failure_code':
                'plan_failed', 'failure_message': 'example', 'targets_budget_reached': 1, 'targets_skipped': 1, 'targets_total':
                1, 'terminal_status': 'completed', 'verdicts_recorded': 1}.
            evaluation_target_skipped (ManagedAgentsEvaluationTargetSkipped | Unset): Audit event payload for a target whose
                processing ended without a completed verdict audit. Example: {'child_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'reason_code': 'child_create_failed',
                'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            evaluation_target_started (ManagedAgentsEvaluationTargetStarted | Unset): Audit event payload linking one frozen
                target to its isolated evaluation child and reserved verdict identity. Example: {'child_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'clone_state': 'ready', 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_provider': 'example', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            evaluation_verdict_recorded (ManagedAgentsEvaluationVerdictRecorded | Unset): Audit event payload emitted after
                the authoritative immutable verdict and clone cost are recorded. Example: {'child_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cost_completeness': 'complete', 'cost_usd': 'example', 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'failed_criterion_keys': ['example'], 'result': 'pass',
                'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            metadata (ManagedAgentsEventContentMetadata | Unset): Extra key/value detail about this event that is not part
                of the message body, such as the ingest subtype or the sandbox working directory.
            plan (list[ManagedAgentsPlanItem] | Unset): Plan items reported by the agent, present on a plan_update event.
            stop_reason (str | Unset): The provider's own stop_reason for the assistant turn, recorded verbatim, e.g.
                end_turn, tool_use, or max_tokens. Absent on events that are not a model response.
            tools (list[ManagedAgentsToolDefinition] | Unset): Tool definitions that were in scope for the turn, as sent to
                the provider. Recorded on the session's system message so a transcript shows what the model could call.
            usage (ManagedAgentsUsage | Unset): Token counts and cost for a single unit of work, in the provider's usage
                vocabulary. Attached to an event's content for the model turn that produced it; see session usage for whole-
                session totals. Example: {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_usd': 1.5, 'input_tokens': 1,
                'output_tokens': 1}.
     """

    blocks: list[ManagedAgentsContentBlock] | None
    evaluation_budget_reached: ManagedAgentsEvaluationBudgetReached | Unset = UNSET
    evaluation_plan_frozen: ManagedAgentsEvaluationPlanFrozen | Unset = UNSET
    evaluation_run_finished: ManagedAgentsEvaluationRunFinished | Unset = UNSET
    evaluation_target_skipped: ManagedAgentsEvaluationTargetSkipped | Unset = UNSET
    evaluation_target_started: ManagedAgentsEvaluationTargetStarted | Unset = UNSET
    evaluation_verdict_recorded: ManagedAgentsEvaluationVerdictRecorded | Unset = UNSET
    metadata: ManagedAgentsEventContentMetadata | Unset = UNSET
    plan: list[ManagedAgentsPlanItem] | Unset = UNSET
    stop_reason: str | Unset = UNSET
    tools: list[ManagedAgentsToolDefinition] | Unset = UNSET
    usage: ManagedAgentsUsage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_content_block import ManagedAgentsContentBlock # noqa: PLC0415
        from ..models.managed_agents_evaluation_budget_reached import ManagedAgentsEvaluationBudgetReached # noqa: PLC0415
        from ..models.managed_agents_evaluation_plan_frozen import ManagedAgentsEvaluationPlanFrozen # noqa: PLC0415
        from ..models.managed_agents_evaluation_run_finished import ManagedAgentsEvaluationRunFinished # noqa: PLC0415
        from ..models.managed_agents_evaluation_target_skipped import ManagedAgentsEvaluationTargetSkipped # noqa: PLC0415
        from ..models.managed_agents_evaluation_target_started import ManagedAgentsEvaluationTargetStarted # noqa: PLC0415
        from ..models.managed_agents_evaluation_verdict_recorded import ManagedAgentsEvaluationVerdictRecorded # noqa: PLC0415
        from ..models.managed_agents_event_content_metadata import ManagedAgentsEventContentMetadata # noqa: PLC0415
        from ..models.managed_agents_plan_item import ManagedAgentsPlanItem # noqa: PLC0415
        from ..models.managed_agents_tool_definition import ManagedAgentsToolDefinition # noqa: PLC0415
        from ..models.managed_agents_usage import ManagedAgentsUsage # noqa: PLC0415
        blocks: list[dict[str, Any]] | None
        if isinstance(self.blocks, list):
            blocks = []
            for blocks_type_0_item_data in self.blocks:
                blocks_type_0_item = blocks_type_0_item_data.to_dict()
                blocks.append(blocks_type_0_item)


        else:
            blocks = self.blocks

        evaluation_budget_reached: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation_budget_reached, Unset):
            evaluation_budget_reached = self.evaluation_budget_reached.to_dict()

        evaluation_plan_frozen: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation_plan_frozen, Unset):
            evaluation_plan_frozen = self.evaluation_plan_frozen.to_dict()

        evaluation_run_finished: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation_run_finished, Unset):
            evaluation_run_finished = self.evaluation_run_finished.to_dict()

        evaluation_target_skipped: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation_target_skipped, Unset):
            evaluation_target_skipped = self.evaluation_target_skipped.to_dict()

        evaluation_target_started: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation_target_started, Unset):
            evaluation_target_started = self.evaluation_target_started.to_dict()

        evaluation_verdict_recorded: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation_verdict_recorded, Unset):
            evaluation_verdict_recorded = self.evaluation_verdict_recorded.to_dict()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        plan: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.plan, Unset):
            plan = []
            for plan_item_data in self.plan:
                plan_item = plan_item_data.to_dict()
                plan.append(plan_item)



        stop_reason = self.stop_reason

        tools: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.to_dict()
                tools.append(tools_item)



        usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "blocks": blocks,
        })
        if evaluation_budget_reached is not UNSET:
            field_dict["evaluation_budget_reached"] = evaluation_budget_reached
        if evaluation_plan_frozen is not UNSET:
            field_dict["evaluation_plan_frozen"] = evaluation_plan_frozen
        if evaluation_run_finished is not UNSET:
            field_dict["evaluation_run_finished"] = evaluation_run_finished
        if evaluation_target_skipped is not UNSET:
            field_dict["evaluation_target_skipped"] = evaluation_target_skipped
        if evaluation_target_started is not UNSET:
            field_dict["evaluation_target_started"] = evaluation_target_started
        if evaluation_verdict_recorded is not UNSET:
            field_dict["evaluation_verdict_recorded"] = evaluation_verdict_recorded
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if plan is not UNSET:
            field_dict["plan"] = plan
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if tools is not UNSET:
            field_dict["tools"] = tools
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_content_block import ManagedAgentsContentBlock # noqa: PLC0415
        from ..models.managed_agents_evaluation_budget_reached import ManagedAgentsEvaluationBudgetReached # noqa: PLC0415
        from ..models.managed_agents_evaluation_plan_frozen import ManagedAgentsEvaluationPlanFrozen # noqa: PLC0415
        from ..models.managed_agents_evaluation_run_finished import ManagedAgentsEvaluationRunFinished # noqa: PLC0415
        from ..models.managed_agents_evaluation_target_skipped import ManagedAgentsEvaluationTargetSkipped # noqa: PLC0415
        from ..models.managed_agents_evaluation_target_started import ManagedAgentsEvaluationTargetStarted # noqa: PLC0415
        from ..models.managed_agents_evaluation_verdict_recorded import ManagedAgentsEvaluationVerdictRecorded # noqa: PLC0415
        from ..models.managed_agents_event_content_metadata import ManagedAgentsEventContentMetadata # noqa: PLC0415
        from ..models.managed_agents_plan_item import ManagedAgentsPlanItem # noqa: PLC0415
        from ..models.managed_agents_tool_definition import ManagedAgentsToolDefinition # noqa: PLC0415
        from ..models.managed_agents_usage import ManagedAgentsUsage # noqa: PLC0415
        d = dict(src_dict)
        def _parse_blocks(data: object) -> list[ManagedAgentsContentBlock] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                blocks_type_0 = []
                _blocks_type_0 = data
                for blocks_type_0_item_data in (_blocks_type_0):
                    blocks_type_0_item = ManagedAgentsContentBlock.from_dict(blocks_type_0_item_data)



                    blocks_type_0.append(blocks_type_0_item)

                return blocks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsContentBlock] | None, data)

        blocks = _parse_blocks(d.pop("blocks"))


        _evaluation_budget_reached = d.pop("evaluation_budget_reached", UNSET)
        evaluation_budget_reached: ManagedAgentsEvaluationBudgetReached | Unset
        if isinstance(_evaluation_budget_reached,  Unset):
            evaluation_budget_reached = UNSET
        else:
            evaluation_budget_reached = ManagedAgentsEvaluationBudgetReached.from_dict(_evaluation_budget_reached)




        _evaluation_plan_frozen = d.pop("evaluation_plan_frozen", UNSET)
        evaluation_plan_frozen: ManagedAgentsEvaluationPlanFrozen | Unset
        if isinstance(_evaluation_plan_frozen,  Unset):
            evaluation_plan_frozen = UNSET
        else:
            evaluation_plan_frozen = ManagedAgentsEvaluationPlanFrozen.from_dict(_evaluation_plan_frozen)




        _evaluation_run_finished = d.pop("evaluation_run_finished", UNSET)
        evaluation_run_finished: ManagedAgentsEvaluationRunFinished | Unset
        if isinstance(_evaluation_run_finished,  Unset):
            evaluation_run_finished = UNSET
        else:
            evaluation_run_finished = ManagedAgentsEvaluationRunFinished.from_dict(_evaluation_run_finished)




        _evaluation_target_skipped = d.pop("evaluation_target_skipped", UNSET)
        evaluation_target_skipped: ManagedAgentsEvaluationTargetSkipped | Unset
        if isinstance(_evaluation_target_skipped,  Unset):
            evaluation_target_skipped = UNSET
        else:
            evaluation_target_skipped = ManagedAgentsEvaluationTargetSkipped.from_dict(_evaluation_target_skipped)




        _evaluation_target_started = d.pop("evaluation_target_started", UNSET)
        evaluation_target_started: ManagedAgentsEvaluationTargetStarted | Unset
        if isinstance(_evaluation_target_started,  Unset):
            evaluation_target_started = UNSET
        else:
            evaluation_target_started = ManagedAgentsEvaluationTargetStarted.from_dict(_evaluation_target_started)




        _evaluation_verdict_recorded = d.pop("evaluation_verdict_recorded", UNSET)
        evaluation_verdict_recorded: ManagedAgentsEvaluationVerdictRecorded | Unset
        if isinstance(_evaluation_verdict_recorded,  Unset):
            evaluation_verdict_recorded = UNSET
        else:
            evaluation_verdict_recorded = ManagedAgentsEvaluationVerdictRecorded.from_dict(_evaluation_verdict_recorded)




        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsEventContentMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsEventContentMetadata.from_dict(_metadata)




        _plan = d.pop("plan", UNSET)
        plan: list[ManagedAgentsPlanItem] | Unset = UNSET
        if _plan is not UNSET:
            plan = []
            for plan_item_data in _plan:
                plan_item = ManagedAgentsPlanItem.from_dict(plan_item_data)



                plan.append(plan_item)


        stop_reason = d.pop("stop_reason", UNSET)

        _tools = d.pop("tools", UNSET)
        tools: list[ManagedAgentsToolDefinition] | Unset = UNSET
        if _tools is not UNSET:
            tools = []
            for tools_item_data in _tools:
                tools_item = ManagedAgentsToolDefinition.from_dict(tools_item_data)



                tools.append(tools_item)


        _usage = d.pop("usage", UNSET)
        usage: ManagedAgentsUsage | Unset
        if isinstance(_usage,  Unset):
            usage = UNSET
        else:
            usage = ManagedAgentsUsage.from_dict(_usage)




        managed_agents_event_content = cls(
            blocks=blocks,
            evaluation_budget_reached=evaluation_budget_reached,
            evaluation_plan_frozen=evaluation_plan_frozen,
            evaluation_run_finished=evaluation_run_finished,
            evaluation_target_skipped=evaluation_target_skipped,
            evaluation_target_started=evaluation_target_started,
            evaluation_verdict_recorded=evaluation_verdict_recorded,
            metadata=metadata,
            plan=plan,
            stop_reason=stop_reason,
            tools=tools,
            usage=usage,
        )


        managed_agents_event_content.additional_properties = d
        return managed_agents_event_content

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
