from __future__ import annotations

from .memory_runtime_support import *  # noqa: F401,F403

class MemoryRuntime:
    def __init__(
        self,
        *,
        ledger: MemoryLedger | None = None,
        store: MemoryStore | None = None,
        extractor: MemoryExtractor | None = None,
        consolidator: MemoryConsolidator | None = None,
        retriever: MemoryRetriever | None = None,
        governance: MemoryGovernance | None = None,
    ) -> None:
        self.ledger = ledger or InMemoryMemoryLedger()
        self.store = store or InMemoryMemoryStore()
        self.extractor = extractor or DefaultMemoryExtractor()
        self.consolidator = consolidator or DefaultMemoryConsolidator()
        self.retriever = retriever or DefaultMemoryRetriever(self.store)
        self.governance = governance or DefaultMemoryGovernance()

    def _governance_event_entry(
        self,
        session_id: str,
        decision: MemoryGovernanceDecision,
        *,
        target_memory_id: str | None,
        related_memory_ids: tuple[str, ...] = (),
    ) -> MemoryLedgerEntry:
        created_at = _now()
        digest_source = "|".join(
            (
                session_id,
                decision.action,
                target_memory_id or "",
                decision.actor,
                decision.reason,
                decision.replacement_memory_id or "",
                ",".join(related_memory_ids),
                created_at.isoformat(),
            )
        )
        entry_id = "memory.governance." + hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:16]
        state_tag = "allowed" if decision.allowed else "denied"
        content = f"{decision.action}:{state_tag}:{target_memory_id or 'session'}:{decision.reason}"
        metadata = {
            "action": decision.action,
            "target_memory_id": target_memory_id or "",
            "allowed": "true" if decision.allowed else "false",
            "actor": decision.actor,
            "reason": decision.reason,
            "replacement_memory_id": decision.replacement_memory_id or "",
            "related_memory_ids": ",".join(related_memory_ids),
        }
        return MemoryLedgerEntry(
            entry_id=entry_id,
            session_id=session_id,
            event_id=entry_id,
            event_type="memory_governance",
            content=content,
            kind="governance",
            source_event_id=target_memory_id,
            goal_refs=(),
            tags=("governance", decision.action, state_tag),
            created_at=created_at,
            metadata=metadata,
        )

    def _record_governance_event(
        self,
        session_id: str,
        decision: MemoryGovernanceDecision,
        *,
        target_memory_id: str | None,
        related_memory_ids: tuple[str, ...] = (),
    ) -> None:
        self.ledger.append(
            self._governance_event_entry(
                session_id,
                decision,
                target_memory_id=target_memory_id,
                related_memory_ids=related_memory_ids,
            )
        )

    @classmethod
    def from_repository(
        cls,
        repository: RuntimeStorageRepository,
        *,
        extractor: MemoryExtractor | None = None,
        consolidator: MemoryConsolidator | None = None,
        retriever: MemoryRetriever | None = None,
        governance: MemoryGovernance | None = None,
    ) -> "MemoryRuntime":
        store = SQLiteMemoryStore(repository)
        ledger = SQLiteMemoryLedger(repository)
        return cls(
            ledger=ledger,
            store=store,
            extractor=extractor,
            consolidator=consolidator,
            retriever=retriever or DefaultMemoryRetriever(store, repository=repository),
            governance=governance,
        )

    def append_event(self, event: EventEnvelope) -> MemoryAppendResult:
        result = self.extractor.extract(event)
        self.ledger.append(result.ledger_entry)
        for record in result.extracted_records:
            decision = self.governance.can_record(record)
            if decision.allowed:
                self.store.upsert(record)
        return result

    def record_memory(self, record: MemoryRecord) -> MemoryGovernanceDecision:
        decision = self.governance.can_record(record)
        if not decision.allowed:
            self._record_governance_event(
                record.session_id,
                decision,
                target_memory_id=record.memory_id,
            )
            return decision
        self.store.upsert(record)
        return decision

    def consolidate_session(self, session_id: str, memory_ids: tuple[str, ...] = ()) -> MemoryConsolidationResult:
        if memory_ids:
            records = tuple(
                record
                for memory_id in memory_ids
                if (record := self.store.get(memory_id)) is not None
            )
        else:
            records = self.store.list(session_id=session_id)
        decision = self.governance.can_consolidate(records)
        if not decision.allowed:
            self._record_governance_event(
                session_id,
                decision,
                target_memory_id=None,
                related_memory_ids=tuple(record.memory_id for record in records),
            )
            return MemoryConsolidationResult(
                session_id=session_id,
                input_memory_ids=tuple(record.memory_id for record in records),
                summary_record=None,
                rationale=decision.reason,
            )
        result = self.consolidator.consolidate(session_id, records)
        if result.summary_record is not None:
            self.store.upsert(result.summary_record)
            self.store.mark_consolidated(tuple(result.input_memory_ids), result.summary_record.memory_id)
            self._record_governance_event(
                session_id,
                MemoryGovernanceDecision(
                    "consolidate",
                    result.summary_record.memory_id,
                    True,
                    result.rationale or decision.reason,
                    actor=decision.actor,
                    replacement_memory_id=result.summary_record.memory_id,
                ),
                target_memory_id=result.summary_record.memory_id,
                related_memory_ids=tuple(result.input_memory_ids),
            )
        return result

    def retrieve(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        limit: int = 5,
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
    ) -> MemoryRetrievalResult:
        return self.retriever.retrieve(
            session_id,
            query,
            goal_ids=goal_ids,
            limit=limit,
            scope_session_ids=scope_session_ids,
            scope_reason=scope_reason,
        )

    def retrieve_evidence(self, request: EvidenceRetrievalRequest) -> EvidenceRetrievalResult:
        detailed = getattr(self.retriever, "retrieve_evidence", None)
        if callable(detailed):
            return detailed(request)
        focus_work_item_ids = request.work_item_ids
        if not focus_work_item_ids and request.intent_decision is not None and request.intent_decision.focus_activity_ids:
            focus_work_item_ids = request.intent_decision.focus_activity_ids
        opened_scopes = request.scopes
        if (
            request.intent_decision is not None
            and request.intent_decision.scope_suggestion not in {"", "session"}
            and request.intent_decision.scope_suggestion not in opened_scopes
        ):
            opened_scopes = (*opened_scopes, request.intent_decision.scope_suggestion)
        fallback = self.retrieve(
            request.session_id,
            request.query,
            goal_ids=focus_work_item_ids,
            limit=request.limit,
            scope_session_ids=request.lineage_session_ids,
            scope_reason=request.scope_reason,
        )
        candidates = tuple(
            EvidenceCandidate(
                evidence_id=candidate.record.memory_id,
                memory=candidate.record,
                score=candidate.score,
                matched_scopes=("session",),
                reasons=tuple(
                    RecallReason("memory.fallback", detail, 0.0)
                    for detail in candidate.reasons
                ),
            )
            for candidate in fallback.candidates
        )
        return EvidenceRetrievalResult(
            request=request,
            scope_session_ids=fallback.scope_session_ids,
            scope_reason=fallback.scope_reason,
            candidates=candidates,
            recall_reasons=RecallReasons(
                opened_scopes=opened_scopes,
                evidence_ids=tuple(candidate.evidence_id for candidate in candidates),
                scope_reason=fallback.scope_reason,
                rerank_summary="fallback memory retrieval adapter reused existing ranking output",
                reasons=tuple(
                    RecallReason("memory.fallback", fallback.scope_reason, 0.0),
                ),
            ),
            index_policy=self.index_policy(),
        )

    def index_policy(self) -> EmbeddingIndexPolicy:
        return build_embedding_index_policy(self.store)

    def build_resume_packet(
        self,
        request: EvidenceRetrievalRequest,
        retrieval: EvidenceRetrievalResult,
        *,
        next_move: str = "",
        artifact_ids: tuple[str, ...] = (),
        constraint_ids: tuple[str, ...] = (),
    ) -> ResumePacket:
        return build_resume_packet(
            request,
            retrieval,
            next_move=next_move,
            artifact_ids=artifact_ids,
            constraint_ids=constraint_ids,
        )

    def maintain_session(
        self,
        session_id: str,
        *,
        now: datetime | None = None,
        maximum_ephemeral_age: timedelta = timedelta(hours=6),
    ) -> MemoryMaintenanceResult:
        current = now or _now()
        eligible = tuple(
            record
            for record in self.store.list(session_id=session_id)
            if self._eligible_for_maintenance(record, now=current, maximum_ephemeral_age=maximum_ephemeral_age)
        )
        if len(eligible) < 2:
            return MemoryMaintenanceResult(
                session_id=session_id,
                maintained_memory_ids=tuple(record.memory_id for record in eligible),
                summary_record=None,
                rationale="no aged episodic memories required maintenance",
            )

        result = self.consolidator.consolidate(session_id, eligible)
        if result.summary_record is None:
            return MemoryMaintenanceResult(
                session_id=session_id,
                maintained_memory_ids=tuple(record.memory_id for record in eligible),
                summary_record=None,
                rationale=result.rationale or "maintenance consolidation produced no summary",
            )

        summary = replace(
            result.summary_record,
            tags=_unique(result.summary_record.tags + ("maintenance", "aged")),
        )
        self.store.upsert(summary)
        self.store.mark_consolidated(tuple(result.input_memory_ids), summary.memory_id)
        self._record_governance_event(
            session_id,
            MemoryGovernanceDecision(
                "consolidate",
                summary.memory_id,
                True,
                "aged episodic memories consolidated into a maintained summary",
                actor="system",
                replacement_memory_id=summary.memory_id,
            ),
            target_memory_id=summary.memory_id,
            related_memory_ids=tuple(result.input_memory_ids),
        )
        return MemoryMaintenanceResult(
            session_id=session_id,
            maintained_memory_ids=tuple(result.input_memory_ids),
            summary_record=summary,
            rationale="aged episodic memories were consolidated into a maintained summary",
        )

    def list_governance_events(
        self,
        session_id: str,
        *,
        target_memory_id: str | None = None,
    ) -> tuple[MemoryGovernanceEvent, ...]:
        events: list[MemoryGovernanceEvent] = []
        for entry in self.ledger.list(session_id=session_id):
            if entry.event_type != "memory_governance":
                continue
            action = str(entry.metadata.get("action", ""))
            if not action:
                continue
            event_target = str(entry.metadata.get("target_memory_id", "")) or entry.source_event_id
            if target_memory_id is not None and event_target != target_memory_id:
                related_ids = _split_csv(str(entry.metadata.get("related_memory_ids", "")))
                if target_memory_id not in related_ids:
                    continue
            events.append(
                MemoryGovernanceEvent(
                    entry_id=entry.entry_id,
                    session_id=entry.session_id,
                    action=action,
                    target_memory_id=event_target,
                    allowed=str(entry.metadata.get("allowed", "false")).lower() == "true",
                    actor=str(entry.metadata.get("actor", "user")),
                    reason=str(entry.metadata.get("reason", entry.content)),
                    replacement_memory_id=str(entry.metadata.get("replacement_memory_id", "")) or None,
                    related_memory_ids=_split_csv(str(entry.metadata.get("related_memory_ids", ""))),
                    created_at=entry.created_at,
                )
            )
        return tuple(events)

    def correct_memory(
        self,
        target_memory_id: str,
        corrected_content: str,
        *,
        actor: str = "user",
        reason: str = "",
    ) -> MemoryMutationResult:
        original = self.store.get(target_memory_id)
        if original is None:
            decision = MemoryGovernanceDecision("correct", target_memory_id, False, "target memory not found", actor=actor)
            return MemoryMutationResult(decision=decision)
        decision = self.governance.can_correct(original, corrected_content, actor=actor)
        if not decision.allowed:
            self._record_governance_event(
                original.session_id,
                decision,
                target_memory_id=target_memory_id,
            )
            return MemoryMutationResult(decision=decision)
        protected_tags: tuple[str, ...] = ()
        policy = getattr(self.governance, "policy", None)
        if policy is not None:
            protected_tags = tuple(getattr(policy, "protected_tags", ()))
        preserved_tags = tuple(tag for tag in original.tags if tag not in protected_tags)
        reason_tag = (f"reason:{reason}",) if reason else ()
        corrected = MemoryRecord(
            memory_id=f"{target_memory_id}:corrected",
            session_id=original.session_id,
            kind=original.kind,
            content=corrected_content,
            source_event_id=original.source_event_id,
            goal_refs=original.goal_refs,
            tags=_unique(preserved_tags + ("corrected",) + reason_tag),
            created_at=_now(),
            metadata=dict(original.metadata),
        )
        self.store.upsert(corrected)
        self.store.mark_superseded(target_memory_id, corrected.memory_id)
        applied_decision = MemoryGovernanceDecision(
            "correct",
            target_memory_id,
            True,
            "memory corrected",
            actor=actor,
            replacement_memory_id=corrected.memory_id,
        )
        self._record_governance_event(
            original.session_id,
            applied_decision,
            target_memory_id=target_memory_id,
            related_memory_ids=(corrected.memory_id,),
        )
        return MemoryMutationResult(
            decision=applied_decision,
            record=corrected,
        )

    def delete_memory(
        self,
        target_memory_id: str,
        *,
        actor: str = "user",
        reason: str,
    ) -> MemoryMutationResult:
        original = self.store.get(target_memory_id)
        if original is None:
            decision = MemoryGovernanceDecision("delete", target_memory_id, False, "target memory not found", actor=actor)
            return MemoryMutationResult(decision=decision)
        decision = self.governance.can_delete(original, actor=actor, reason=reason)
        if not decision.allowed:
            self._record_governance_event(
                original.session_id,
                decision,
                target_memory_id=target_memory_id,
            )
            return MemoryMutationResult(decision=decision)
        self.store.mark_deleted(target_memory_id)
        self._record_governance_event(
            original.session_id,
            decision,
            target_memory_id=target_memory_id,
        )
        return MemoryMutationResult(decision=decision)

    def pin_memory(
        self,
        target_memory_id: str,
        *,
        actor: str = "user",
        reason: str = "",
    ) -> MemoryMutationResult:
        original = self.store.get(target_memory_id)
        if original is None:
            decision = MemoryGovernanceDecision("pin", target_memory_id, False, "target memory not found", actor=actor)
            return MemoryMutationResult(decision=decision)
        if "pinned" in original.tags:
            decision = MemoryGovernanceDecision("pin", target_memory_id, True, "memory already pinned", actor=actor)
            return MemoryMutationResult(decision=decision, record=original)
        updated = replace(original, tags=_unique(original.tags + ("pinned",)))
        self.store.upsert(updated)
        decision = MemoryGovernanceDecision(
            "pin",
            target_memory_id,
            True,
            reason or "memory pinned",
            actor=actor,
        )
        self._record_governance_event(
            original.session_id,
            decision,
            target_memory_id=target_memory_id,
            related_memory_ids=(updated.memory_id,),
        )
        return MemoryMutationResult(decision=decision, record=updated)

    def unpin_memory(
        self,
        target_memory_id: str,
        *,
        actor: str = "user",
        reason: str = "",
    ) -> MemoryMutationResult:
        original = self.store.get(target_memory_id)
        if original is None:
            decision = MemoryGovernanceDecision("unpin", target_memory_id, False, "target memory not found", actor=actor)
            return MemoryMutationResult(decision=decision)
        if "pinned" not in original.tags:
            decision = MemoryGovernanceDecision("unpin", target_memory_id, True, "memory was not pinned", actor=actor)
            return MemoryMutationResult(decision=decision, record=original)
        updated = replace(original, tags=tuple(tag for tag in original.tags if tag != "pinned"))
        self.store.upsert(updated)
        decision = MemoryGovernanceDecision(
            "unpin",
            target_memory_id,
            True,
            reason or "memory unpinned",
            actor=actor,
        )
        self._record_governance_event(
            original.session_id,
            decision,
            target_memory_id=target_memory_id,
            related_memory_ids=(updated.memory_id,),
        )
        return MemoryMutationResult(decision=decision, record=updated)

    def _eligible_for_maintenance(
        self,
        record: MemoryRecord,
        *,
        now: datetime,
        maximum_ephemeral_age: timedelta,
    ) -> bool:
        if record.kind != "episodic":
            return False
        if record.created_at is None:
            return False
        age = now - record.created_at
        if age < maximum_ephemeral_age:
            return False
        if not record.goal_refs:
            return False
        if any(tag in {"pinned", "locked", "system"} for tag in record.tags):
            return False
        return True
