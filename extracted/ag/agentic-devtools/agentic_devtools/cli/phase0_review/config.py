"""Constants for deterministic Phase 0 factual review."""

SCHEMA_VERSION = "phase0_factual_review_input/v1"
FACTUAL_REVIEW_INPUT_STATE_KEY = "phase0.factualReviewInputPath"
INTEGRITY_STATE_KEY = "phase0.integrityPath"
PROCESSING_TIMEOUT_SECONDS = 120.0
TRUNCATION_THRESHOLD_BYTES = 102_400
MAX_PAYLOAD_BYTES = 4_194_304
MAX_ISSUE_MD_BYTES = 500_000
MAX_TEMPLATE_BYTES = 200_000
MAX_SNAPSHOT_BYTES = 200_000
MAX_BODY_BYTES = 102_400
MAX_TITLE_CHARACTERS = 1_024
MAX_STRING_CHARACTERS = 2_048
MAX_PROPERTY_KEY_CHARACTERS = 128
MAX_COLLECTION_MEMBER_CHARACTERS = 500
MAX_COLLECTION_ITEMS = 50
MAX_PROPERTIES = 50
MAX_PROPERTY_RENDERED_CHARACTERS = 1_024
MAX_JSON_DEPTH = 10

FRONTMATTER_FIELDS = ("id", "title", "type", "status", "provider", "labels", "rendered_at")
UNORDERED_FIELDS = frozenset({"labels", "assignees", "dependencies"})
RENDERER_METADATA_FIELDS = frozenset(
    {
        "content_hash",
        "provenance_content_hash",
        "rendered_at",
        "source_content_hash",
    }
)
RESERVED_PROPERTY_NAMES = frozenset(
    {
        "provider",
        "issue_id",
        "id",
        "title",
        "status",
        "body",
        "description",
        "url",
        "created_at",
        "updated_at",
        "labels",
        "dependencies",
        "constraints",
        "type",
        "truncated",
        "original_size",
        "priority",
        "assignees",
        "milestone",
    }
)

PHASE0_PR_CHECKLIST = """## Phase 0 Review Checklist

This review is limited to factual accuracy and template conformance. Writing quality, prose style,
requirement quality, and requirement testability are out of scope and belong to the later
specification review.

- [ ] Title matches the authoritative source
- [ ] Description matches the authoritative source
- [ ] Labels match the authoritative source
- [ ] Type matches the resolved source type
- [ ] Properties match the authoritative source
- [ ] Template compliance has been verified"""
