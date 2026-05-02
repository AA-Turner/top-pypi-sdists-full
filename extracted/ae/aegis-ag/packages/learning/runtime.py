"""Learning loop from captured experiences to verified procedures and optional skills."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import re

from packages.contracts import (
    ExperienceRecord,
    PatternCluster,
    ProcedureCandidate,
    ProcedureLibrary,
    ProcedureRecord,
    ProcedureStep,
    VerificationBundle,
)
from packages.skills import SkillManifestLoadRecord, SkillPackageLoader, SkillRuntime, write_skill_package
from packages.storage import RuntimeStorageRepository

_STOPWORDS = {
    "a",
    "an",
    "and",
    "after",
    "around",
    "the",
    "to",
    "for",
    "with",
    "from",
    "into",
    "that",
    "this",
    "then",
    "was",
    "were",
    "will",
    "your",
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def _tokens(text: str) -> tuple[str, ...]:
    seen: list[str] = []
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        if token in _STOPWORDS or len(token) <= 2:
            continue
        if token not in seen:
            seen.append(token)
    return tuple(seen)


def _cluster_signature(experience: ExperienceRecord) -> str:
    goal = experience.goal_id or "goal:none"
    keywords = _tokens(f"{experience.title} {experience.summary}")[:4]
    skills = tuple(sorted(experience.related_skill_ids))[:2]
    return "|".join((goal, *keywords, *skills))


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}:{digest}"


def _is_useful_experience(experience: ExperienceRecord) -> bool:
    if experience.status != "captured":
        return False
    lowered_tags = {tag.lower() for tag in experience.tags}
    if any(tag.startswith("outcome:error") or tag.startswith("outcome:deferred") for tag in lowered_tags):
        return False
    if experience.summary.strip().lower().startswith("it looks like"):
        return False
    return bool(_normalize_text(experience.summary))


def _procedure_steps_from_summary(candidate_id: str, summary: str) -> tuple[ProcedureStep, ...]:
    normalized = _normalize_text(summary)
    if not normalized:
        return ()
    raw_segments = re.split(r"(?:\.\s+|;\s+|\bthen\b)", normalized)
    segments = [segment.strip(" ,") for segment in raw_segments if segment.strip(" ,")]
    if not segments:
        segments = [normalized]
    steps: list[ProcedureStep] = []
    for index, segment in enumerate(segments[:3], start=1):
        title = segment[:72].rstrip(".")
        steps.append(
            ProcedureStep(
                step_id=f"{candidate_id}:step-{index}",
                title=title[:72] or f"Step {index}",
                instruction=segment,
            )
        )
    return tuple(steps)


def _skill_id_from_candidate(candidate: ProcedureCandidate) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", candidate.title.lower()).strip("-") or candidate.candidate_id.replace(":", "-")
    return f"procedure-{base}"[:64].rstrip("-")


def _instruction_text_from_candidate(candidate: ProcedureCandidate) -> str:
    lines = [candidate.summary.strip(), "", "Checklist:"]
    for step in candidate.ordered_steps:
        lines.append(f"- {step.instruction}")
    if candidate.constraints:
        lines.extend(("", "Constraints:"))
        lines.extend(f"- {constraint}" for constraint in candidate.constraints)
    return "\n".join(line for line in lines if line is not None).strip()


def _instruction_text_from_procedure(procedure: ProcedureRecord) -> str:
    lines = [procedure.summary.strip(), "", "Checklist:"]
    for step in procedure.steps:
        lines.append(f"- {step.instruction}")
    return "\n".join(line for line in lines if line is not None).strip()


@dataclass(frozen=True, slots=True)
class ProcedurePromotionResult:
    candidate: ProcedureCandidate
    verification: VerificationBundle
    procedure: ProcedureRecord
    library: ProcedureLibrary
    skill_manifest: SkillManifestLoadRecord | None = None
    skill_package_path: str | None = None


class PatternClusterer:
    def cluster(
        self,
        experiences: tuple[ExperienceRecord, ...],
        *,
        minimum_support: int = 2,
    ) -> tuple[PatternCluster, ...]:
        grouped: dict[tuple[str, str], list[ExperienceRecord]] = {}
        for experience in experiences:
            if not _is_useful_experience(experience):
                continue
            grouped.setdefault((experience.profile_id, _cluster_signature(experience)), []).append(experience)
        clusters: list[PatternCluster] = []
        for (profile_id, signature), members in grouped.items():
            if len(members) < minimum_support:
                continue
            members.sort(key=lambda item: (item.updated_at or item.created_at or _utc_now(), item.experience_id), reverse=True)
            representative = members[0]
            ordered_members = tuple(
                sorted(
                    members,
                    key=lambda item: (item.created_at or item.updated_at or _utc_now(), item.experience_id),
                )
            )
            experience_ids = tuple(member.experience_id for member in ordered_members)
            source_work_item_ids = tuple(dict.fromkeys(member.goal_id for member in members if member.goal_id))
            related_skill_ids = tuple(
                dict.fromkeys(skill_id for member in members for skill_id in member.related_skill_ids if skill_id)
            )
            clusters.append(
                PatternCluster(
                    cluster_id=_stable_id("cluster", profile_id, signature),
                    profile_id=profile_id,
                    signature=signature,
                    status="clustered",
                    experience_ids=experience_ids,
                    source_evidence_ids=experience_ids,
                    source_work_item_ids=source_work_item_ids,
                    related_skill_ids=related_skill_ids,
                    summary=_normalize_text(representative.summary),
                    support_count=len(members),
                )
            )
        clusters.sort(key=lambda item: (-item.support_count, item.cluster_id))
        return tuple(clusters)


class DerivedProcedureCandidateStore:
    def __init__(self, clusterer: PatternClusterer | None = None) -> None:
        self.clusterer = clusterer or PatternClusterer()

    def list_candidates(
        self,
        experiences: tuple[ExperienceRecord, ...],
        *,
        minimum_support: int = 2,
    ) -> tuple[ProcedureCandidate, ...]:
        indexed = {experience.experience_id: experience for experience in experiences}
        candidates: list[ProcedureCandidate] = []
        for cluster in self.clusterer.cluster(experiences, minimum_support=minimum_support):
            representative = indexed[cluster.experience_ids[0]]
            candidate_id = _stable_id("procedure-candidate", cluster.profile_id, cluster.signature)
            steps = _procedure_steps_from_summary(candidate_id, representative.summary)
            confidence = min(0.55 + max(cluster.support_count - minimum_support, 0) * 0.15, 0.95)
            trigger_conditions = tuple(
                dict.fromkeys(
                    condition
                    for condition in (
                        *(f"goal:{goal_id}" for goal_id in cluster.source_work_item_ids),
                        *(f"skill:{skill_id}" for skill_id in cluster.related_skill_ids),
                        f"support:{cluster.support_count}",
                    )
                    if condition
                )
            )
            constraints = tuple(
                dict.fromkeys(
                    constraint
                    for constraint in (
                        f"workspace:{representative.workspace_id}" if representative.workspace_id else "",
                        "promote only after explicit verification",
                    )
                    if constraint
                )
            )
            candidates.append(
                ProcedureCandidate(
                    candidate_id=candidate_id,
                    profile_id=cluster.profile_id,
                    cluster_id=cluster.cluster_id,
                    title=representative.title,
                    summary=cluster.summary,
                    trigger_conditions=trigger_conditions,
                    ordered_steps=steps,
                    constraints=constraints,
                    source_evidence_ids=cluster.source_evidence_ids,
                    source_work_item_ids=cluster.source_work_item_ids,
                    related_skill_ids=cluster.related_skill_ids,
                    confidence=confidence,
                    verification_status="needs_review",
                    promotion_decision="pending",
                )
            )
        candidates.sort(key=lambda item: (-item.confidence, item.candidate_id))
        return tuple(candidates)

    def get_candidate(
        self,
        candidate_id: str,
        experiences: tuple[ExperienceRecord, ...],
        *,
        minimum_support: int = 2,
    ) -> ProcedureCandidate:
        for candidate in self.list_candidates(experiences, minimum_support=minimum_support):
            if candidate.candidate_id == candidate_id:
                return candidate
        raise KeyError(candidate_id)


class VerificationService:
    def verify(
        self,
        candidate: ProcedureCandidate,
        *,
        method: str = "operator-review",
        scenario_ids: tuple[str, ...] = (),
        now: datetime | None = None,
    ) -> VerificationBundle:
        timestamp = now or _utc_now()
        reasons: list[str] = []
        status = "verified"
        if len(candidate.source_evidence_ids) < 2:
            status = "rejected"
            reasons.append("candidate does not have repeated evidence support")
        if not candidate.ordered_steps:
            status = "rejected"
            reasons.append("candidate does not expose executable ordered steps")
        if candidate.confidence < 0.55:
            status = "rejected"
            reasons.append("candidate confidence stayed below the promotion floor")
        if status == "verified":
            reasons.append(
                f"{method} verified {len(candidate.source_evidence_ids)} evidence ref(s) across {max(len(scenario_ids), 1)} review path(s)"
            )
        return VerificationBundle(
            bundle_id=_stable_id("verification", candidate.profile_id, candidate.candidate_id, method),
            profile_id=candidate.profile_id,
            candidate_id=candidate.candidate_id,
            method=method,
            status=status,
            notes="; ".join(reasons),
            evidence_ids=candidate.source_evidence_ids,
            scenario_ids=scenario_ids,
            verified_at=timestamp if status == "verified" else None,
            created_at=timestamp,
            updated_at=timestamp,
        )


class ProcedurePromotionService:
    def __init__(
        self,
        repository: RuntimeStorageRepository,
        *,
        authored_skills_dir: Path | None = None,
        skill_runtime: SkillRuntime | None = None,
    ) -> None:
        self.repository = repository
        self.authored_skills_dir = authored_skills_dir
        self.skill_runtime = skill_runtime

    def promote(
        self,
        candidate: ProcedureCandidate,
        verification: VerificationBundle,
        *,
        install_skill: bool = False,
    ) -> ProcedurePromotionResult:
        if verification.status != "verified":
            raise ValueError("procedure promotion requires a verified bundle")
        skill_manifest: SkillManifestLoadRecord | None = None
        skill_package_path: str | None = None
        skill_id: str | None = None
        if install_skill:
            if self.authored_skills_dir is None:
                raise ValueError("authored_skills_dir is required to package a procedure skill")
            skill_id = _skill_id_from_candidate(candidate)
            package_dir = write_skill_package(
                self.authored_skills_dir,
                skill_id=skill_id,
                display_name=candidate.title,
                summary=candidate.summary,
                instruction_text=_instruction_text_from_candidate(candidate),
                category="procedure",
                overwrite=True,
                source_kind="aegis-procedure",
            )
            skill_package_path = str(package_dir)
            if self.skill_runtime is not None:
                self.skill_runtime.load_package(package_dir)
                skill_manifest = self.skill_runtime.list_manifest_loads()[-1]
            else:
                manifest = SkillPackageLoader().load(package_dir)
                skill_manifest = SkillManifestLoadRecord(
                    source_path=manifest.source_path,
                    skill_ids=tuple(skill.skill_id for skill in manifest.skills),
                    loaded_at=_utc_now(),
                    status="written",
                    detail="verified procedure skill package",
                )
                if manifest.skills:
                    skill_id = manifest.skills[0].skill_id
        procedure = ProcedureRecord(
            procedure_id=_stable_id("procedure", candidate.profile_id, candidate.candidate_id),
            title=candidate.title,
            summary=candidate.summary,
            status="active",
            trigger_refs=candidate.trigger_conditions,
            evidence_refs=candidate.source_evidence_ids,
            verification_bundle_id=verification.bundle_id,
            skill_id=skill_id,
            steps=candidate.ordered_steps,
        )
        current = self.repository.load_procedure_library(candidate.profile_id) or ProcedureLibrary(profile_id=candidate.profile_id)
        retained = [item for item in current.procedures if item.procedure_id != procedure.procedure_id]
        library = ProcedureLibrary(profile_id=candidate.profile_id, procedures=tuple((procedure, *retained)))
        self.repository.upsert_verification_bundle(verification)
        self.repository.upsert_procedure_library(library)
        return ProcedurePromotionResult(
            candidate=candidate,
            verification=verification,
            procedure=procedure,
            library=library,
            skill_manifest=skill_manifest,
            skill_package_path=skill_package_path,
        )

    def _load_library(self, profile_id: str) -> ProcedureLibrary:
        library = self.repository.load_procedure_library(profile_id)
        if library is None:
            raise KeyError(profile_id)
        return library

    def _load_procedure(self, profile_id: str, procedure_id: str) -> tuple[ProcedureLibrary, ProcedureRecord]:
        library = self._load_library(profile_id)
        for procedure in library.procedures:
            if procedure.procedure_id == procedure_id:
                return library, procedure
        raise KeyError(procedure_id)

    def _persist_library(self, library: ProcedureLibrary, procedure: ProcedureRecord) -> ProcedureLibrary:
        updated_procedures = tuple(
            procedure if existing.procedure_id == procedure.procedure_id else existing
            for existing in library.procedures
        )
        updated_library = ProcedureLibrary(profile_id=library.profile_id, procedures=updated_procedures)
        self.repository.upsert_procedure_library(updated_library)
        return updated_library

    def _reload_skill_package(self, procedure: ProcedureRecord) -> None:
        if procedure.skill_id is None or self.authored_skills_dir is None:
            return
        package_dir = write_skill_package(
            self.authored_skills_dir,
            skill_id=procedure.skill_id,
            display_name=procedure.title,
            summary=procedure.summary,
            instruction_text=_instruction_text_from_procedure(procedure),
            category="procedure",
            overwrite=True,
            source_kind="aegis-procedure",
        )
        if self.skill_runtime is not None:
            self.skill_runtime.load_package(package_dir)

    def retire(self, *, profile_id: str, procedure_id: str) -> ProcedureRecord:
        library, current = self._load_procedure(profile_id, procedure_id)
        retired = replace(current, status="retired")
        self._persist_library(library, retired)
        if retired.skill_id is not None and self.skill_runtime is not None and self.skill_runtime.describe(retired.skill_id) is not None:
            self.skill_runtime.set_enabled(retired.skill_id, False)
        return retired

    def patch(
        self,
        *,
        profile_id: str,
        procedure_id: str,
        title: str | None = None,
        summary: str | None = None,
        trigger_refs: tuple[str, ...] | None = None,
        steps: tuple[ProcedureStep, ...] | None = None,
        status: str | None = None,
    ) -> ProcedureRecord:
        library, current = self._load_procedure(profile_id, procedure_id)
        updated = replace(
            current,
            title=title if title is not None else current.title,
            summary=summary if summary is not None else current.summary,
            trigger_refs=trigger_refs if trigger_refs is not None else current.trigger_refs,
            steps=steps if steps is not None else current.steps,
            status=status if status is not None else current.status,
        )
        self._persist_library(library, updated)
        if updated.skill_id is not None:
            self._reload_skill_package(updated)
            if self.skill_runtime is not None and self.skill_runtime.describe(updated.skill_id) is not None:
                self.skill_runtime.set_enabled(updated.skill_id, updated.status != "retired")
        return updated


class LearningRuntime:
    def __init__(
        self,
        repository: RuntimeStorageRepository,
        *,
        authored_skills_dir: Path | None = None,
        skill_runtime: SkillRuntime | None = None,
        clusterer: PatternClusterer | None = None,
        candidate_store: DerivedProcedureCandidateStore | None = None,
        verifier: VerificationService | None = None,
        promoter: ProcedurePromotionService | None = None,
    ) -> None:
        self.repository = repository
        self.clusterer = clusterer or PatternClusterer()
        self.candidate_store = candidate_store or DerivedProcedureCandidateStore(self.clusterer)
        self.verifier = verifier or VerificationService()
        self.promoter = promoter or ProcedurePromotionService(
            repository,
            authored_skills_dir=authored_skills_dir,
            skill_runtime=skill_runtime,
        )

    def _experiences(
        self,
        *,
        profile_id: str,
        session_id: str | None = None,
        limit: int | None = None,
    ) -> tuple[ExperienceRecord, ...]:
        return self.repository.list_experiences(
            profile_id=profile_id,
            session_id=session_id,
            statuses=("captured",),
            limit=limit,
        )

    def list_pattern_clusters(
        self,
        *,
        profile_id: str,
        session_id: str | None = None,
        minimum_support: int = 2,
        limit: int | None = None,
    ) -> tuple[PatternCluster, ...]:
        experiences = self._experiences(profile_id=profile_id, session_id=session_id, limit=limit)
        return self.clusterer.cluster(experiences, minimum_support=minimum_support)

    def list_procedure_candidates(
        self,
        *,
        profile_id: str,
        session_id: str | None = None,
        minimum_support: int = 2,
        limit: int | None = None,
    ) -> tuple[ProcedureCandidate, ...]:
        experiences = self._experiences(profile_id=profile_id, session_id=session_id, limit=limit)
        return self.candidate_store.list_candidates(experiences, minimum_support=minimum_support)

    def verify_candidate(
        self,
        *,
        profile_id: str,
        candidate_id: str,
        session_id: str | None = None,
        minimum_support: int = 2,
        scenario_ids: tuple[str, ...] = (),
        method: str = "operator-review",
    ) -> VerificationBundle:
        experiences = self._experiences(profile_id=profile_id, session_id=session_id)
        candidate = self.candidate_store.get_candidate(candidate_id, experiences, minimum_support=minimum_support)
        bundle = self.verifier.verify(candidate, method=method, scenario_ids=scenario_ids)
        self.repository.upsert_verification_bundle(bundle)
        return bundle

    def promote_candidate(
        self,
        *,
        profile_id: str,
        candidate_id: str,
        session_id: str | None = None,
        minimum_support: int = 2,
        scenario_ids: tuple[str, ...] = (),
        method: str = "operator-review",
        install_skill: bool = False,
    ) -> ProcedurePromotionResult:
        experiences = self._experiences(profile_id=profile_id, session_id=session_id)
        candidate = self.candidate_store.get_candidate(candidate_id, experiences, minimum_support=minimum_support)
        verification = self.verifier.verify(candidate, method=method, scenario_ids=scenario_ids)
        return self.promoter.promote(candidate, verification, install_skill=install_skill)

    def retire_procedure(self, *, profile_id: str, procedure_id: str) -> ProcedureRecord:
        return self.promoter.retire(profile_id=profile_id, procedure_id=procedure_id)

    def patch_procedure(
        self,
        *,
        profile_id: str,
        procedure_id: str,
        title: str | None = None,
        summary: str | None = None,
        trigger_refs: tuple[str, ...] | None = None,
        steps: tuple[ProcedureStep, ...] | None = None,
        status: str | None = None,
    ) -> ProcedureRecord:
        return self.promoter.patch(
            profile_id=profile_id,
            procedure_id=procedure_id,
            title=title,
            summary=summary,
            trigger_refs=trigger_refs,
            steps=steps,
            status=status,
        )
