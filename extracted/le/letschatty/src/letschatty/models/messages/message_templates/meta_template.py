from __future__ import annotations
from typing import Any, ClassVar, Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import ConfigDict, Field, field_validator
from ...base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from ...utils.types.serializer_type import SerializerType

if TYPE_CHECKING:
    from .raw_meta_template import WhatsappTemplate


# Tolerant reference constants — the UNION of Meta's node + GET-filter + webhook value spaces.
# These are NEVER used as a field annotation (that would make the field strict and re-introduce the
# "unknown enum value silently drops the whole template" bug, border 24). The persisted fields stay
# bare `str`. These exist only for UI labels / lint code that wants a known-value reference.
class MetaTemplateStatus:
    APPROVED = "APPROVED"; PENDING = "PENDING"; REJECTED = "REJECTED"; IN_APPEAL = "IN_APPEAL"
    PAUSED = "PAUSED"; DISABLED = "DISABLED"; PENDING_DELETION = "PENDING_DELETION"; DELETED = "DELETED"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"; ARCHIVED = "ARCHIVED"; UNARCHIVED = "UNARCHIVED"
    FLAGGED = "FLAGGED"; LOCKED = "LOCKED"; REINSTATED = "REINSTATED"


class MetaTemplatePreview(ChattyAssetPreview):
    waba_id: Optional[str] = None
    meta_template_id: Optional[str] = None
    language: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    quality_score: Optional[str] = None                # a display STRING ("GREEN") — see the validator
    is_sendable_by_chatty: bool = True
    last_synced_at: Optional[datetime] = None

    # B-7 (CRITICAL): previews are built from a PROJECTED doc via from_dict() = cls(**doc), and the
    # projected `quality_score` is the stored DICT {score, date}. A dict into Optional[str] would raise a
    # ValidationError and the WHOLE preview would be silently skipped by the collection loader — every
    # quality-scored template would vanish from the list (the exact G2 bug this project exists to kill,
    # reintroduced through the fix). Coerce here so BOTH the from_dict (dict) and from_asset (str already
    # coerced) paths yield a clean display string.
    @field_validator("quality_score", mode="before")
    @classmethod
    def _coerce_quality_score(cls, v: Any) -> Optional[str]:
        if isinstance(v, dict):
            return v.get("score")
        return v

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        projection = super().get_projection()          # base: _id, name, company_id, created_at, updated_at, deleted_at
        for f in ("waba_id", "meta_template_id", "language", "status", "category",
                  "quality_score", "is_sendable_by_chatty", "last_synced_at"):
            projection[f] = 1
        return projection

    @classmethod
    def from_asset(cls, asset: "MetaTemplate") -> "MetaTemplatePreview":
        return cls(_id=asset.id, name=asset.name, company_id=asset.company_id,
                   created_at=asset.created_at, deleted_at=asset.deleted_at,
                   waba_id=asset.waba_id, meta_template_id=asset.meta_template_id,
                   language=asset.language, status=asset.status, category=asset.category,
                   quality_score=asset.quality_score,     # dict -> coerced to score str by the validator (B-7)
                   is_sendable_by_chatty=asset.is_sendable_by_chatty, last_synced_at=asset.last_synced_at)


class MetaTemplate(CompanyAssetModel):
    """A Meta WhatsApp message template, persisted as a per-company asset.

    Natural key: (company_id, meta_template_id). Scoped by company_id (fanned out across a shared WABA);
    waba_id is a first-class indexed field. `id` (Mongo ObjectId, aliased _id) and `company_id` (frozen)
    come from the base — C15: meta_template_id is a SEPARATE field, never the Mongo id.
    """
    waba_id: str = Field(frozen=True)
    meta_template_id: str = Field(frozen=True, description="Meta's numeric template id. NEVER reuse ChattyAssetModel.id (C15).")
    name: str                                            # required; projected by the preview
    language: Optional[str] = None
    status: str = "PENDING"                              # tolerant str, NEVER a strict enum (border 24)
    category: Optional[str] = None                       # tolerant str
    sub_category: Optional[str] = None                   # tolerant str — real data has "CUSTOM"
    parameter_format: Optional[str] = None
    components: list[dict[str, Any]] = Field(default_factory=list)  # RAW Meta components — tolerant, never a typed parse that could drop (G2)
    quality_score: Optional[dict[str, Any]] = None       # {score, date} or {score, reasons, date}
    rejected_reason: Optional[str] = None
    previous_category: Optional[str] = None
    correct_category: Optional[str] = None               # border 13: correct_category != category => pending recategorization
    message_send_ttl_seconds: Optional[int] = None
    # ---- ours ----
    is_sendable_by_chatty: bool = True                   # G2: False => displayed with a reason, not hidden
    unsupported_reason: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    last_sync_error: Optional[str] = None
    edit_history: list[datetime] = Field(default_factory=list)   # S-7/RF-15: Chatty-side edit timestamps.
    # Meta exposes NO edit-count API — this is our own record, blind to edits made directly in WhatsApp
    # Manager. Appended on every successful edit; the UI computes "n/10 en 30 días / próxima a HH:MM" from
    # it and must say "según ediciones hechas en Chatty".

    preview_class: ClassVar[type[MetaTemplatePreview]] = MetaTemplatePreview
    # extra="allow": stop dropping undeclared Meta fields (quality_score/rejected_reason/... used to vanish).
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    # S-11 (documented, accepted): model_dump_json(serializer=DATABASE) BSON-converts only
    # created_at/updated_at/deleted_at/start_time/end_time. last_synced_at and edit_history[] persist as ISO
    # STRINGS in Mongo -> Mongo-side sorts on them are lexicographic (fine for ISO-8601 UTC). Pydantic
    # re-parses them on read. Extend the DATABASE serializer branch if a Mongo range query is ever needed.

    def to_whatsapp_template(self) -> Optional["WhatsappTemplate"]:
        """Build the send-path WhatsappTemplate from the raw components. Returns None if the components
        can't be parsed into a supported shape (the caller keeps is_sendable_by_chatty=False). This is the
        tolerant, on-demand parse — the persisted `components` stay raw so nothing is ever dropped (G2)."""
        from .raw_meta_template import WhatsappTemplate
        try:
            wa = WhatsappTemplate(id=self.meta_template_id, name=self.name, language=self.language or "",
                                  status=self.status, category=self.category or "MARKETING",
                                  parameter_format=self.parameter_format, components=self.components)
        except Exception:
            return None
        # The send path renders the BODY (build_template_payload derefs body_component.text). A template
        # with no BODY component cannot go through Chatty's send path even if it otherwise parses (e.g. a
        # media/carousel-only shape after the A3 enum widening) — treat it as not-sendable so it is
        # displayed read-only rather than offered in the picker and crashing the sender.
        if wa.body_component is None:
            return None
        return wa
