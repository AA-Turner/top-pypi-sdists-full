"""the entity card: a per-kind glance projection, literal field paths, the notes excerpt."""

from __future__ import annotations
import json
from typing import Any
from ....sdk import errors
from ....shared.reads.search_contract import EntityType


# (entity kind, view) -> builder method. Explicit and greppable: this table IS the
# answer to "what can I read about a run?", and _checked_view derives its error
# message from it, so a view can never be advertised without a builder behind it.
#: How much of the notes rides along on a card before it defers to
#: `view="notes"`. Bounded because a card is the cheap glance.
_NOTES_CARD_EXCERPT = 1200

# These are projections of already-fetched fields, never another set of source
# reads. Long documents/configs are available through RECORD instead of riding
# every purpose-shaped view. A complete card is complete for this projection;
# its optional detail doors do not imply failed or incomplete delivery.
_ENTITY_IDENTITY_FIELDS = (
    "id",
    "slug",
    "name",
    "title",
    "kind",
    "status",
    "project_id",
    "experiment_id",
    "run_id",
    "parent_project_id",
    "parent_run_id",
    "parent_relation",
    "group_id",
    "created_at",
    "updated_at",
    "started_at",
    "ended_at",
)
_ENTITY_REF_FIELDS = ("id", "slug", "name", "kind", "project_id", "experiment_id", "run_id")
#: Card fields that are COUNTS a server may not know yet (a sub-note's token
#: count before its backfill): null is left off the card, never shown as a value
#: an agent could read as zero.
_UNKNOWN_COUNT_FIELDS = frozenset({"tokens", "remaining_tokens"})
_CARD_FIELDS: dict[str, tuple[str, ...]] = {
    EntityType.PROJECT: (
        "workspace_id",
        "workspace_name",
        "repo",
        "code_source_count",
        "subproject_count",
        "experiment_count",
        "run_count",
        "direct_run_count",
        "active_run_count",
        "contributor_count",
    ),
    EntityType.EXPERIMENT: ("question", "run_count", "active_run_count"),
    EntityType.RUN: ("source", "env_ref", "counts"),
    EntityType.TRIAL: (
        "rollout_span_id",
        "provider",
        "step_index",
        "name_customized",
        "description_customized",
    ),
    EntityType.ARTIFACT: (
        "shared",
        "version",
        "version_id",
        "content_hash",
        "sha256",
        "size_bytes",
        "mime_type",
        "is_reference",
        "workspace_id",
        "shared_folder_id",
    ),
    EntityType.GROUP: (),
    EntityType.SESSION: ("session_id", "agent", "name", "work_observed"),
    EntityType.TEAM_NOTE: ("version",),
    # Fullness rides the card because a sub-note is capped at its carrier's
    # limit, and an agent about to append needs the room left, not a guess.
    # TOKENS, the unit the cap refuses in; the `*_chars` pair beside them on the
    # row measures the character backstop and is left off. A count the server
    # could not give (null) is left off too (`_UNKNOWN_COUNT_FIELDS`).
    EntityType.SUB_NOTE: ("tokens", "limit_tokens", "remaining_tokens", "notes_version"),
    # The data catalog (C4). `ref` is the server's canonical address, the one
    # a run's use names; a dataset's version, a checkpoint's facts and a
    # source's counts are what a reader decides with.
    EntityType.DATASET: ("ref", "registered"),
    EntityType.SOURCE: (
        "ref",
        "canonical_key",
        "provider",
        "revision",
        "uri",
        "license",
        "homepage",
        "citation",
        "retrieved_at",
        "counts",
    ),
    EntityType.CHECKPOINT: (
        "ref",
        "step",
        "best",
        "score",
        "monitor_key",
        "rewound",
        "stored",
        "location",
        "size_bytes",
        "run",
        "project",
        "telemetry",
        "started_from",
        "locked",
    ),
}
_CARD_DESCRIPTION_CHARS = 480
_CARD_TEXT_CHARS = 240
_CARD_LIST_ITEMS = 8


def _card_text(out: dict, entity: dict, key: str, limit: int) -> None:
    value = entity.get(key)
    if value is None:
        return
    if not isinstance(value, str):
        return
    out[key] = value[:limit]
    if len(value) > limit:
        out[f"{key}_truncated"] = True


#: Where a fork's inherited runs and files are read, on its card. A hint
#: rather than a line in the tool description: that description is at the
#: client's 2,048-char cap, and this costs nothing on an experiment that is
#: no fork.
_READ_INHERITED_HINT = 'view="inherited"; view_options={"runs": true} for its runs'


def _card_fork(out: dict, entity: dict) -> None:
    """An experiment's fork facts, each only when it says something, so a card
    with no fork either way is the card it always was.

    `forked_from` is the source the caller can see. `read_inherited` keys on
    `inherits`, NOT on `forked_from`: a fork whose source is in the trash has
    no `forked_from` and still reads through it (CONTRACT.md, Forks). A source
    read without `inherits` (an API older than it) still gets the hint.
    `fork_count` stands alone: a source with forks is no fork itself."""
    source = entity.get("forked_from")
    if isinstance(source, dict):
        link = {
            key: source[key]
            for key in ("id", "slug", "name", "forked_at")
            if source.get(key) is not None
        }
        name = link.get("name")
        if isinstance(name, str) and len(name) > _CARD_TEXT_CHARS:
            link["name"] = name[:_CARD_TEXT_CHARS]
            link["name_truncated"] = True
        out["forked_from"] = link
    count = entity.get("fork_count")
    if isinstance(count, int) and not isinstance(count, bool) and count > 0:
        out["fork_count"] = count
    if entity.get("inherits") is True or isinstance(source, dict):
        out["read_inherited"] = _READ_INHERITED_HINT


def _card_summary(value: Any) -> tuple[Any, bool]:
    """Keep supplied headline values; never synthesize results or recurse into metadata."""
    if isinstance(value, str):
        return value[:_CARD_DESCRIPTION_CHARS], len(value) > _CARD_DESCRIPTION_CHARS
    if not isinstance(value, dict):
        return None, value is not None
    result: dict = {}
    is_truncated = False
    for key, item in value.items():
        if len(result) == _CARD_LIST_ITEMS or not isinstance(key, str):
            is_truncated = True
            continue
        if item is None or isinstance(item, (bool, int, float)):
            result[key] = item
        elif isinstance(item, str):
            result[key] = item[:_CARD_TEXT_CHARS]
            is_truncated |= len(item) > _CARD_TEXT_CHARS
        else:
            is_truncated = True
    return result, is_truncated


def _entity_projection(kind: str, entity: dict, *, card: bool, document: bool = False) -> dict:
    """Per-kind useful glance, or minimal identity beside an explicit detail read."""
    keys = _ENTITY_IDENTITY_FIELDS if card else _ENTITY_REF_FIELDS
    out = {key: entity[key] for key in keys if key in entity}
    if document and "status" in entity:
        out["status"] = entity["status"]
    # `summary_metrics` since the rename; `summary` is the deprecated alias an
    # older server still emits. Reading both keeps this client working across a
    # server that has already dropped the alias AND one that has not.
    summary_key = "summary_metrics" if "summary_metrics" in entity else "summary"
    if (card or document) and summary_key in entity:
        summary, is_truncated = _card_summary(entity[summary_key])
        # An empty summary (`{}`, "") is omitted like an absent one: it rode every
        # document read as `"summary": {}`, a key with nothing in it. Kept when
        # truncation emptied it, so `summary_truncated` has what it describes.
        if summary is not None and (summary or is_truncated):
            out["summary"] = summary
        if is_truncated:
            out["summary_truncated"] = True
    if not card:
        return out
    out.update(
        {
            key: entity[key]
            for key in _CARD_FIELDS[kind]
            if key in entity and not (entity[key] is None and key in _UNKNOWN_COUNT_FIELDS)
        }
    )
    if kind == EntityType.PROJECT:
        # Projects are flat (retire subprojects): what a project is part of
        # rides the card as `part_of` and its parts as `parts` (names and ids,
        # `_card_part_of`), so the server's compatibility fields are not shown
        # under the old tree's names -- no `parent_project_id` (one projected
        # link of many), and the count of its parts as `part_count`.
        out.pop("parent_project_id", None)
        if "subproject_count" in out:
            out["part_count"] = out.pop("subproject_count")
    if kind == EntityType.EXPERIMENT:
        _card_fork(out, entity)
    _card_text(out, entity, "description", _CARD_DESCRIPTION_CHARS)
    _card_text(out, entity, "question", _CARD_DESCRIPTION_CHARS)
    _card_text(out, entity, "conclusion", _CARD_DESCRIPTION_CHARS)
    if out.get("conclusion") and entity.get("conclusion_source"):
        # Whose answer it is: `human`, `agent`, or `lane` (the page's AI summary).
        out["conclusion_source"] = entity["conclusion_source"]
    if kind == EntityType.EXPERIMENT and entity.get("outcome") == "dead_end":
        # Marked a dead end (0408): why, bounded like the conclusion (the
        # branches view's `dead_end` row key; `True` when no reason came).
        _card_text(out, {"dead_end": entity.get("outcome_reason")}, "dead_end", _CARD_DESCRIPTION_CHARS)
        out.setdefault("dead_end", True)
    if kind == EntityType.ARTIFACT:
        _card_text(out, entity, "resolution_note", _CARD_DESCRIPTION_CHARS)
        if entity.get("shared") is False:
            out["read_versions"] = 'view="versions"'
        if not entity.get("is_reference"):
            out["read_content"] = 'view="content"'
    if isinstance(entity.get("tags"), list):
        tags = entity["tags"]
        out["tags"] = [str(tag)[:_CARD_TEXT_CHARS] for tag in tags[:_CARD_LIST_ITEMS]]
        if len(tags) > _CARD_LIST_ITEMS or any(len(str(t)) > _CARD_TEXT_CHARS for t in tags):
            out["tags_truncated"] = True
    if kind == EntityType.GROUP and "spec" in entity:
        # A small sweep definition is the group's meaning. For a large one,
        # show its dimension names and an explicit excerpt, not an apparently
        # complete subset that changes the sweep's scientific interpretation.
        spec = entity["spec"]
        encoded = json.dumps(spec, ensure_ascii=False, default=str, separators=(",", ":"))
        if len(encoded) <= 800:
            out["spec"] = spec
        else:
            out["spec_excerpt"] = encoded[:800]
            out["spec_truncated"] = True
    if kind == EntityType.SESSION:
        # The work inventory is the useful first answer for a session. Keep
        # names and exact observed counts, with RECORD for larger inventories.
        for key in ("projects", "experiments", "runs", "artifacts"):
            if key not in entity:
                continue
            rows = entity[key]
            if rows is None:
                out[key] = None
                continue
            out[key] = [
                {field: row[field] for field in ("id", "name", "slug", "status") if field in row}
                for row in rows[:_CARD_LIST_ITEMS]
            ]
            out[f"{key}_count"] = len(rows)
            if len(rows) > _CARD_LIST_ITEMS:
                out[f"{key}_truncated"] = True
    if kind in (EntityType.TEAM_NOTE, EntityType.SUB_NOTE):
        # These name the document itself: asking for one must deliver its text
        # immediately. The common delivery boundary pages it.
        out["body"] = entity.get("body") or ""
    return out


def _record_field(entity: dict, field: Any) -> tuple[list[str | int], Any]:
    """Select a literal JSON path, without expressions, wildcards, eval or getattr."""
    if isinstance(field, str):
        path = field.removeprefix("$.").split(".")
    elif isinstance(field, list):
        path = field
    else:
        raise errors.ValidationError(
            "record field must be a dotted string or a path list", status=422
        )
    if (
        not path
        or len(path) > 32
        or any(
            isinstance(part, bool)
            or not isinstance(part, (str, int))
            or (isinstance(part, str) and (not part or len(part) > 512))
            or (isinstance(part, int) and part < 0)
            for part in path
        )
    ):
        raise errors.ValidationError("invalid record field path", status=422)
    value: Any = entity
    for part in path:
        if isinstance(value, dict) and isinstance(part, str) and part in value:
            value = value[part]
        elif isinstance(value, list) and isinstance(part, int) and part < len(value):
            value = value[part]
        else:
            raise errors.NotFoundError("record field not found")
    return path, value


def _notes_excerpt(text: str | None, *, read_all: str = 'view="notes"') -> dict | None:
    """The `{text, truncated, read_all?}` block a card carries, or None.

    ONE renderer for every carrier (0124): a note reads the same whether it hangs
    off a project, experiment or run, and the shape matches the
    browse orientation's excerpt so the product feels like one thing rather than
    four independently invented excerpt formats.

    None rather than an empty block when there is nothing: a `notes` key with no
    text reads as "this entity has notes" and is worse than silence.
    """
    if not text:
        return None
    is_truncated = len(text) > _NOTES_CARD_EXCERPT
    excerpt: dict = {"text": text[:_NOTES_CARD_EXCERPT], "truncated": is_truncated}
    if is_truncated:
        excerpt["read_all"] = read_all
    return excerpt
