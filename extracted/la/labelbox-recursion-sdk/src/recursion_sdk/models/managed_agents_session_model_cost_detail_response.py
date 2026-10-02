from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_model_cost_detail_response_scope import ManagedAgentsSessionModelCostDetailResponseScope
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_model_cost_attempt_response import ManagedAgentsModelCostAttemptResponse
  from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse
  from ..models.managed_agents_session_model_cost_summary_response import ManagedAgentsSessionModelCostSummaryResponse





T = TypeVar("T", bound="ManagedAgentsSessionModelCostDetailResponse")



@_attrs_define
class ManagedAgentsSessionModelCostDetailResponse:
    """ One page of model-cost attempts for a session scope, together with the rollups for the same pinned snapshot, so a
    page and its totals cannot disagree. Continuation pages and companion hierarchy reads stay on that snapshot rather
    than re-reading a moving ledger.

        Example:
            {'attempts': [{'attempt_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'catalog_version': 'example', 'charge':
                {'adjustments': [{'adjustment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z',
                'created_by': 'example', 'kind': 'provider_authority', 'model_cost_usd': 'example', 'reason': 'example'}],
                'charge_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'completeness': 'complete', 'components': [{'cache_state':
                'none', 'category': 'input', 'component_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'dimension': 'example',
                'modality': 'text', 'model_cost_usd': 'example', 'price': {'catalog_version': 'example', 'currency': 'USD',
                'denominator_units': 'example', 'model': 'example', 'numerator_nano_usd': 'example', 'provider': 'example',
                'region': 'example', 'rule_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example'},
                'price_redacted': True, 'quantity': 'example', 'unit': 'token'}], 'locally_priced_model_cost_usd': 'example',
                'model_cost_usd': 'example', 'original_model_cost_usd': 'example', 'provider_reported_model_cost_usd':
                'example', 'receipt': {'gateway': {'call_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'discount_amount_usd':
                'example', 'margin_amount_usd': 'example', 'margin_percent': 'example', 'original_total_usd': 'example',
                'reported_total_usd': 'example', 'selected_deployment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'selected_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'total_state': 'example'}, 'provider_request_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'quantities': [{'cache_state': 'none', 'category': 'input', 'dimension':
                'example', 'modality': 'text', 'quantity': 'example', 'unit': 'token'}], 'recovery': {'method': 'example',
                'recovered_at': '2026-02-18T09:30:00Z', 'reference': 'example'}, 'redacted_fields': ['example'], 'region':
                'example', 'requested_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'resolved_model_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example', 'source': 'example'}, 'receipt_sha256':
                'example', 'recorded_at': '2026-02-18T09:30:00Z'}, 'completeness': 'complete', 'created_at':
                '2026-02-18T09:30:00Z', 'kind': 'model', 'model': 'example', 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider':
                'example', 'root_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example', 'state': 'prepared', 'thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z'}], 'model_cost_snapshot_token':
                'example', 'next_page_token': 'example', 'read_timestamp': '2026-02-18T09:30:00Z', 'scope': 'self',
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'summaries': {'self': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'subtree': {'adjustment_count': 'example', 'attempt_count': 'example',
                'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self',
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'tree': {'adjustment_count': 'example', 'attempt_count':
                'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self',
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}, 'summary': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}

        Attributes:
            attempts (list[ManagedAgentsModelCostAttemptResponse] | None): Attempts in scope, oldest first by reservation
                time, up to the requested limit.
            model_cost_snapshot_token (str): Signed organization/session/scope-bound token that pins companion model-cost
                reads to this exact snapshot.
            read_timestamp (datetime.datetime): RFC 3339 timestamp of the database snapshot every figure on this page was
                read from.
            scope (ManagedAgentsSessionModelCostDetailResponseScope): How far the read reached from that session: this
                session alone (self), this session and its descendants (subtree), or every session under the same root (tree).
            session_id (str): Session the read was scoped to (UUID).
            summaries (ManagedAgentsSessionModelCostSummariesResponse): One session's three scope rollups, read from a
                single database snapshot so self, subtree, and tree cannot disagree with one another. Example: {'self':
                {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'subtree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'tree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}.
            summary (ManagedAgentsSessionModelCostSummaryResponse): Model-cost rollup for one session scope: the exact
                ledger amount, how complete the accounting behind it is, and the counts it was derived from. attempt_count is
                every provider call the ledger is accountable for, charge_count only those that produced a receipt, and
                adjustment_count the signed corrections applied since. Model spend only: sandbox, tool, and storage cost are not
                included. Example: {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example',
                'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            next_page_token (str | Unset): Continuation for the next page, passed back as page_token. Absent on the last
                page. It is bound to this organization, session, scope, limit, and snapshot, so it cannot be replayed against a
                different read.
     """

    attempts: list[ManagedAgentsModelCostAttemptResponse] | None
    model_cost_snapshot_token: str
    read_timestamp: datetime.datetime
    scope: ManagedAgentsSessionModelCostDetailResponseScope
    session_id: str
    summaries: ManagedAgentsSessionModelCostSummariesResponse
    summary: ManagedAgentsSessionModelCostSummaryResponse
    next_page_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_model_cost_attempt_response import ManagedAgentsModelCostAttemptResponse # noqa: PLC0415
        from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse # noqa: PLC0415
        from ..models.managed_agents_session_model_cost_summary_response import ManagedAgentsSessionModelCostSummaryResponse # noqa: PLC0415
        attempts: list[dict[str, Any]] | None
        if isinstance(self.attempts, list):
            attempts = []
            for attempts_type_0_item_data in self.attempts:
                attempts_type_0_item = attempts_type_0_item_data.to_dict()
                attempts.append(attempts_type_0_item)


        else:
            attempts = self.attempts

        model_cost_snapshot_token = self.model_cost_snapshot_token

        read_timestamp = self.read_timestamp.isoformat()

        scope = self.scope.value

        session_id = self.session_id

        summaries = self.summaries.to_dict()

        summary = self.summary.to_dict()

        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "attempts": attempts,
            "model_cost_snapshot_token": model_cost_snapshot_token,
            "read_timestamp": read_timestamp,
            "scope": scope,
            "session_id": session_id,
            "summaries": summaries,
            "summary": summary,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_model_cost_attempt_response import ManagedAgentsModelCostAttemptResponse # noqa: PLC0415
        from ..models.managed_agents_session_model_cost_summaries_response import ManagedAgentsSessionModelCostSummariesResponse # noqa: PLC0415
        from ..models.managed_agents_session_model_cost_summary_response import ManagedAgentsSessionModelCostSummaryResponse # noqa: PLC0415
        d = dict(src_dict)
        def _parse_attempts(data: object) -> list[ManagedAgentsModelCostAttemptResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                attempts_type_0 = []
                _attempts_type_0 = data
                for attempts_type_0_item_data in (_attempts_type_0):
                    attempts_type_0_item = ManagedAgentsModelCostAttemptResponse.from_dict(attempts_type_0_item_data)



                    attempts_type_0.append(attempts_type_0_item)

                return attempts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsModelCostAttemptResponse] | None, data)

        attempts = _parse_attempts(d.pop("attempts"))


        model_cost_snapshot_token = d.pop("model_cost_snapshot_token")

        read_timestamp = datetime.datetime.fromisoformat(d.pop("read_timestamp"))




        scope = ManagedAgentsSessionModelCostDetailResponseScope(d.pop("scope"))




        session_id = d.pop("session_id")

        summaries = ManagedAgentsSessionModelCostSummariesResponse.from_dict(d.pop("summaries"))




        summary = ManagedAgentsSessionModelCostSummaryResponse.from_dict(d.pop("summary"))




        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_session_model_cost_detail_response = cls(
            attempts=attempts,
            model_cost_snapshot_token=model_cost_snapshot_token,
            read_timestamp=read_timestamp,
            scope=scope,
            session_id=session_id,
            summaries=summaries,
            summary=summary,
            next_page_token=next_page_token,
        )


        managed_agents_session_model_cost_detail_response.additional_properties = d
        return managed_agents_session_model_cost_detail_response

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
