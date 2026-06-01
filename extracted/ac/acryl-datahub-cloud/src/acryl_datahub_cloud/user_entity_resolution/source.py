import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from datahub.configuration import ConfigModel
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.decorators import (
    SupportStatus,
    config_class,
    platform_name,
    support_status,
)
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.api.workunit import MetadataWorkUnit
from datahub.ingestion.graph.client import DataHubGraph
from datahub.metadata.schema_classes import (
    CorpUserInfoClass,
    CorpUserStatusClass,
    MetadataAttributionClass,
    SiblingsClass,
)

_ASPECTS = ["corpUserInfo", "corpUserStatus", "siblings"]
_ASPECT_TYPES = [CorpUserInfoClass, CorpUserStatusClass, SiblingsClass]
_CORPUSER_ENTITY_NAME = "corpuser"

logger = logging.getLogger(__name__)

_CORPUSER_PREFIX = "urn:li:corpuser:"
_SOURCE_URN = "urn:li:dataHubIngestionSource:user-entity-resolution"
_SYSTEM_ACTOR = "urn:li:corpuser:__datahub_system"


def _is_manually_locked(siblings: Optional[SiblingsClass]) -> bool:
    """Return True when the Siblings aspect was set by a human admin via the UI.

    The convention: attribution is present but attribution.source is absent.
    The automated identity-resolution script must not override such assignments.
    """
    if siblings is None or siblings.attribution is None:
        return False
    return siblings.attribution.source is None


class UserEntityResolutionSourceConfig(ConfigModel):
    batch_size: int = 500
    dry_run: bool = False


@dataclass
class _UserRecord:
    urn: str
    email_key: str
    # corpUserStatus.lastModified.time in ms; None when no status aspect exists
    status_time: Optional[int] = None
    has_corp_user_info: bool = False
    existing_siblings: Optional[SiblingsClass] = None
    # True when the existing Siblings aspect carries a MANUAL attribution
    # (attribution present, attribution.source absent). The script skips the
    # entire group when any member is human-locked.
    siblings_manually_locked: bool = False


@dataclass
class UserEntityResolutionSourceReport(SourceReport):
    users_scanned: int = 0
    users_without_email: int = 0
    sibling_groups_found: int = 0
    sibling_groups_resolved: int = 0
    sibling_groups_deferred: int = 0
    sibling_groups_locked: int = 0
    siblings_aspects_emitted: int = 0
    siblings_aspects_skipped: int = 0
    # Human-readable descriptions of deferred groups for operator review
    deferred_groups: List[str] = field(default_factory=list)
    # Groups skipped because a human admin manually set the Siblings aspect
    locked_groups: List[str] = field(default_factory=list)


@platform_name(id="datahub", platform_name="DataHub")
@config_class(UserEntityResolutionSourceConfig)
@support_status(SupportStatus.INCUBATING)
class UserEntityResolutionSource(Source):
    """Links duplicate CorpUser URNs caused by email case mismatches.

    Scans all corpuser entities, groups those that share the same email
    address (case-insensitively), and emits a Siblings aspect for each
    group so that ownership display, user profile owned assets, people
    search, and ownership-based policy evaluation all resolve to the
    authoritative (most recently active) URN.

    Run this source on a nightly schedule so that new duplicates created
    by ingestion pipelines are automatically resolved.
    """

    def __init__(
        self,
        config: UserEntityResolutionSourceConfig,
        ctx: PipelineContext,
    ) -> None:
        super().__init__(ctx)
        self.config = config
        self.report = UserEntityResolutionSourceReport()
        self.graph: DataHubGraph = ctx.require_graph("UserEntityResolutionSource")

    @classmethod
    def create(
        cls, config_dict: dict, ctx: PipelineContext
    ) -> "UserEntityResolutionSource":
        config = UserEntityResolutionSourceConfig.parse_obj(config_dict)
        return cls(config, ctx)

    def get_workunits(self) -> Iterable[MetadataWorkUnit]:
        logger.info("Starting user entity resolution run")

        records = self._fetch_all_users()
        sibling_groups = self._group_by_email(records)

        self.report.sibling_groups_found = len(sibling_groups)
        logger.info(
            f"Scanned {self.report.users_scanned} users, "
            f"found {self.report.sibling_groups_found} sibling groups"
        )

        for email_key, group in sibling_groups.items():
            yield from self._resolve_group(email_key, group)

        logger.info(
            f"Resolved {self.report.sibling_groups_resolved} groups, "
            f"deferred {self.report.sibling_groups_deferred} groups, "
            f"locked (manual) {self.report.sibling_groups_locked} groups, "
            f"emitted {self.report.siblings_aspects_emitted} Siblings aspects"
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fetch_all_users(self) -> List[_UserRecord]:
        seen_urns: set = set()
        # URNs referenced as siblings but not visible in the scroll —
        # NonPrimarySiblingFilter hides non-primary users from search.
        extra_urns: List[str] = []

        primary_urns = list(
            self.graph.get_urns_by_filter(
                entity_types=[_CORPUSER_ENTITY_NAME],
                batch_size=self.config.batch_size,
            )
        )

        records: List[_UserRecord] = []
        for record in self._batch_fetch_records(primary_urns):
            if record.urn in seen_urns:
                continue
            seen_urns.add(record.urn)
            records.append(record)
            if record.existing_siblings and record.existing_siblings.siblings:
                for sibling_urn in record.existing_siblings.siblings:
                    if sibling_urn not in seen_urns:
                        extra_urns.append(sibling_urn)

        # Fetch any ghost URNs that were hidden from the scroll by NonPrimarySiblingFilter.
        unseen_extras = [u for u in extra_urns if u not in seen_urns]
        for record in self._batch_fetch_records(unseen_extras):
            if record.urn in seen_urns:
                continue
            seen_urns.add(record.urn)
            records.append(record)

        return records

    def _batch_fetch_records(self, urns: List[str]) -> Iterator[_UserRecord]:
        """Fetch aspects for a list of URNs in batches, yielding one _UserRecord per URN."""
        for i in range(0, len(urns), self.config.batch_size):
            batch = urns[i : i + self.config.batch_size]
            try:
                # get_entities() issues a single POST to /openapi/v3/entity/corpuser/batchGet,
                # returning all three aspects for the entire batch in one round-trip.
                batch_result = self.graph.get_entities(
                    entity_name=_CORPUSER_ENTITY_NAME,
                    urns=batch,
                    aspects=_ASPECTS,
                )
            except Exception as e:
                self.report.report_warning(
                    message="Failed to batch-fetch user aspects; falling back to per-user fetch",
                    context=f"batch_start={i}, batch_size={len(batch)}",
                )
                logger.warning("Batch fetch failed for URNs %s...: %s", batch[:3], e)
                # Fall back to individual fetches so a single bad batch doesn't drop all users.
                for urn in batch:
                    record = self._fetch_user_record_single(urn)
                    self.report.users_scanned += 1
                    if record is not None:
                        yield record
                continue

            for urn in batch:
                self.report.users_scanned += 1
                aspect_map = batch_result.get(urn, {})
                # get_entities returns (aspect, system_metadata) tuples; unwrap.
                user_info_raw = aspect_map.get("corpUserInfo")
                user_status_raw = aspect_map.get("corpUserStatus")
                siblings_raw = aspect_map.get("siblings")

                user_info = user_info_raw[0] if user_info_raw else None
                user_status = user_status_raw[0] if user_status_raw else None
                siblings = siblings_raw[0] if siblings_raw else None

                record = self._build_user_record(urn, user_info, user_status, siblings)
                if record is not None:
                    yield record
                else:
                    self.report.users_without_email += 1

    def _fetch_user_record_single(self, urn: str) -> Optional[_UserRecord]:
        """Single-entity fallback used only when batch fetch fails."""
        try:
            aspects = self.graph.get_aspects_for_entity(
                entity_urn=urn,
                aspects=_ASPECTS,
                aspect_types=_ASPECT_TYPES,
            )
        except Exception as e:
            self.report.report_warning(
                message="Failed to fetch aspects for user; skipping",
                context=f"urn={urn}",
            )
            logger.debug("Error fetching aspects for %s: %s", urn, e)
            return None

        record = self._build_user_record(
            urn,
            aspects.get("corpUserInfo"),
            aspects.get("corpUserStatus"),
            aspects.get("siblings"),
        )
        if record is None:
            self.report.users_without_email += 1
        return record

    @staticmethod
    def _build_user_record(
        urn: str,
        user_info: Optional[object],
        user_status: Optional[object],
        siblings: Optional[object],
    ) -> Optional[_UserRecord]:
        email_key = UserEntityResolutionSource._derive_email_key(urn, user_info)
        if email_key is None:
            return None  # caller should increment report.users_without_email

        status_time: Optional[int] = None
        if isinstance(user_status, CorpUserStatusClass):
            last_modified = user_status.lastModified
            if last_modified is not None:
                status_time = last_modified.time

        siblings_aspect = siblings if isinstance(siblings, SiblingsClass) else None
        return _UserRecord(
            urn=urn,
            email_key=email_key,
            status_time=status_time,
            has_corp_user_info=isinstance(user_info, CorpUserInfoClass),
            existing_siblings=siblings_aspect,
            siblings_manually_locked=_is_manually_locked(siblings_aspect),
        )

    @staticmethod
    def _derive_email_key(urn: str, user_info: Optional[object]) -> Optional[str]:
        """Return a lowercased grouping key for this user.

        Prefers the explicit email from corpUserInfo; falls back to the URN's
        identity component when it looks like an email address.
        """
        if isinstance(user_info, CorpUserInfoClass) and user_info.email:
            return user_info.email.lower()

        prefix = "urn:li:corpuser:"
        if urn.startswith(prefix):
            identity = urn[len(prefix) :]
            if "@" in identity:
                return identity.lower()

        return None

    @staticmethod
    def _group_by_email(
        records: List[_UserRecord],
    ) -> Dict[str, List[_UserRecord]]:
        groups: Dict[str, List[_UserRecord]] = defaultdict(list)
        for record in records:
            groups[record.email_key].append(record)
        # Only keep groups that have more than one URN.
        return {k: v for k, v in groups.items() if len(v) > 1}

    def _skip_if_locked(self, email_key: str, group: List[_UserRecord]) -> bool:
        """Return True (and update report) if any member has a human-set Siblings aspect."""
        locked = [r for r in group if r.siblings_manually_locked]
        if not locked:
            return False
        self.report.sibling_groups_locked += 1
        detail = (
            f"{email_key!r}: manually linked by admin "
            f"(locked urns={[r.urn for r in locked]}). "
            "Use 'Reset to auto' in the admin UI to re-enable auto-resolution."
        )
        self.report.locked_groups.append(detail)
        logger.info(
            "Skipping group %r — manually locked by admin on urns=%s",
            email_key,
            [r.urn for r in locked],
        )
        return True

    def _resolve_group(
        self, email_key: str, group: List[_UserRecord]
    ) -> Iterable[MetadataWorkUnit]:
        if self._skip_if_locked(email_key, group):
            return

        authoritative, deferred_reason = self._pick_authoritative(group)

        if deferred_reason is not None:
            self.report.sibling_groups_deferred += 1
            detail = f"{email_key!r}: {deferred_reason} (urns={[r.urn for r in group]})"
            self.report.deferred_groups.append(detail)
            self.report.report_warning(
                message="Deferred: cannot determine authoritative user — manual review needed",
                context=f"email_key={email_key!r}, reason={deferred_reason!r}",
            )
            return

        assert authoritative is not None
        self.report.sibling_groups_resolved += 1

        if self.config.dry_run:
            ghost_urns = [r.urn for r in group if r is not authoritative]
            logger.info(
                "[dry_run] Would link siblings: email_key=%r primary=%s ghosts=%s",
                email_key,
                authoritative.urn,
                ghost_urns,
            )
            return

        all_urns = [r.urn for r in group]
        for record in group:
            sibling_urns = [u for u in all_urns if u != record.urn]
            is_primary = record is authoritative
            existing = record.existing_siblings
            if (
                isinstance(existing, SiblingsClass)
                and set(existing.siblings or []) == set(sibling_urns)
                and existing.primary == is_primary
            ):
                self.report.siblings_aspects_skipped += 1
                continue
            attribution = MetadataAttributionClass(
                time=int(time.time() * 1000),
                actor=_SYSTEM_ACTOR,
                source=_SOURCE_URN,
            )
            aspect = SiblingsClass(
                siblings=sibling_urns,
                primary=is_primary,
                attribution=attribution,
            )
            self.report.siblings_aspects_emitted += 1
            yield MetadataChangeProposalWrapper(
                entityUrn=record.urn,
                aspect=aspect,
            ).as_workunit()

    @staticmethod
    def _pick_authoritative(
        group: List[_UserRecord],
    ) -> Tuple[Optional[_UserRecord], Optional[str]]:
        """Choose the authoritative URN within a sibling group.

        Returns (record, None) on success or (None, reason) when the group
        should be deferred for manual review.
        """
        with_status = [r for r in group if r.status_time is not None]

        if with_status:
            # Tier 1: most recently active login wins.
            with_status.sort(key=lambda r: r.status_time or 0, reverse=True)
            return with_status[0], None

        # Tier 2: no login events recorded for any URN. corpUserInfo presence
        # signals SSO provisioning — bare stubs created by asset ingestion never
        # have corpUserInfo written to them.
        with_info = [r for r in group if r.has_corp_user_info]
        if len(with_info) == 1:
            return with_info[0], None

        return None, "no corpUserStatus recorded for any URN in this group"

    def get_report(self) -> SourceReport:
        return self.report
