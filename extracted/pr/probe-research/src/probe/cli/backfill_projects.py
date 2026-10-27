"""Which projects a folder import files into: new ones, unless code or a person says otherwise.

On 2026-10-26 two throwaway smoke folders imported with `--yes` into team
`probe` were filed into unrelated existing projects (`import-model-benchmark`,
then `digits-perceptron-training`). The classifier was shown every existing
project, told to "prefer these", and its pick was reused at creation with no
check and nothing on the review screen saying so. A customer's folder could
mix into a stranger's project the same way.

So a NEW project is the default, and a plan's project has one of three origins
(`backfill_plan.Origin`):

    RULE   code reuses it, silently: a previous import of this folder filed
           into it (the local coverage store says so), it holds this folder's
           repository as a code source, or the import was pointed at it.
    MODEL  the classifier selected it with `probe-backfill-plan project
           --reuse <slug>`, a call checked against the real projects when it
           is made. The review screen and `plan.json` mark it EXISTING with
           what it already holds; an import nobody reviews (`--yes`, the
           desktop's automatic imports) files those files into a new project
           instead, and says so.
    NEW    everything else. A new slug an edit or two from an existing one is
           flagged on review as possibly the same project; one that IS an
           existing slug is renamed, never merged.

The model never retypes an existing slug into an answer nobody checks
(`llm-never-regurgitates-data`): reuse is a checked selection, and code owns
every other decision here.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field, replace
from pathlib import Path

from .backfill_plan import Origin, Plan, ProjectSpec

#: Pages of the workspace's projects read, at most (200 a page).
MAX_PAGES = 10
PAGE_SIZE = 200
#: Projects with a code source whose sources are read to match the folder's
#: repository, at most. One request each.
MAX_SOURCE_CHECKS = 25
#: A new slug this many single-character edits from an existing one (or fewer)
#: is flagged on review. One for slugs shorter than `SHORT_SLUG`.
NEAR_EDITS = 2
SHORT_SLUG = 6
#: Rows read to say what an existing project holds; at the cap it reads "N+".
COUNT_LIMIT = 200
#: Code-source states that mean the repository is this project's code.
LIVE_SOURCE = ("active", "missing")
MAX_SLUG = 63

IMPORTED_BEFORE = "this folder was imported into it before"
POINTED_AT = "this import was pointed at it"


def code_source_reason(repo: str) -> str:
    return f"its code source is {repo}, this folder's repository"


@dataclass
class Known:
    """The workspace's projects as one import sees them."""

    #: slug -> project row, for every project read (listing, plus own ones
    #: found by id outside it).
    rows: dict[str, dict] = field(default_factory=dict)
    #: This folder's own projects, slug -> spec (origin RULE).
    own: dict[str, ProjectSpec] = field(default_factory=dict)
    client: object = None

    @property
    def others(self) -> list[str]:
        """Existing slugs that are not this folder's: never filed into silently."""
        return [slug for slug in self.rows if slug not in self.own]

    @property
    def existing(self) -> list[str]:
        return list(dict.fromkeys([*self.rows, *self.own]))

    def own_pairs(self) -> list[tuple[str, str]]:
        """`(slug, about)` for the prompts: name and why code chose it."""
        return [(slug, f"{spec.name or slug} ({spec.reason})") for slug, spec in self.own.items()]


def folder_slug(folder: Path) -> str:
    """A project slug named for the folder, the server's slug rules applied."""
    slug = re.sub(r"[^a-z0-9]+", "-", Path(folder).name.lower()).strip("-")[:56].strip("-")
    slug = slug or "imported-research"
    try:
        uuid.UUID(slug)
    except ValueError:
        return slug
    # The server refuses a UUID-shaped slug (one string, two meanings), and
    # random-hex folder names are common in the drives this imports.
    return f"folder-{slug}"


def free_slug(base: str, taken) -> str:
    """`base`, or the first `base-N` nobody holds."""
    taken = set(taken)
    if base not in taken:
        return base
    n = 2
    while True:
        suffix = f"-{n}"
        candidate = base[:MAX_SLUG - len(suffix)].rstrip("-") + suffix
        if candidate not in taken:
            return candidate
        n += 1


def _edits(a: str, b: str, limit: int) -> int:
    """Levenshtein distance, or `limit + 1` as soon as it must exceed `limit`."""
    if abs(len(a) - len(b)) > limit:
        return limit + 1
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (ca != cb)))
        if min(current) > limit:
            return limit + 1
        previous = current
    return previous[-1]


def near_miss(slug: str, existing) -> str:
    """The existing slug a small edit away from `slug` (not equal), or ""."""
    limit = 1 if len(slug) < SHORT_SLUG else NEAR_EDITS
    best, best_edits = "", limit + 1
    for other in existing:
        if other == slug:
            continue
        edits = _edits(slug, other, limit)
        if edits < best_edits or (edits == best_edits and best and other < best):
            best, best_edits = other, edits
    return best if best_edits <= limit else ""


# -- what exists, and which of it is this folder's ------------------------------


def _list(client, workspace_id) -> list[dict]:
    rows: list[dict] = []
    cursor = None
    seen: set[str] = set()
    for _ in range(MAX_PAGES):
        page = client.list_projects(
            workspace_id=workspace_id, limit=PAGE_SIZE, **({"cursor": cursor} if cursor else {})
        )
        items = page if isinstance(page, list) else page.items
        rows.extend(row for row in items if isinstance(row, dict) and row.get("slug"))
        cursor = getattr(page, "next_cursor", None)
        if not cursor or cursor in seen:
            break
        seen.add(cursor)
    return rows


def _is_gone(exc: BaseException) -> bool:
    """An answer that means a project is not this import's to reuse.

    Deleted (404), out of this credential's reach (403) or in the trash: a
    deleted project answers 410 `in_trash` until it is purged, a plain
    `RosError` the SDK marks `in_trash`. Anything else (a dropped connection,
    a 5xx, an expired credential) is raised: treating this folder's own
    project as absent would give a re-import a second, duplicate project,
    splitting one folder's record over a blip.
    """
    from probe.sdk import errors

    return isinstance(exc, (errors.NotFoundError, errors.ScopeError)) or bool(
        isinstance(exc, errors.RosError) and getattr(exc, "in_trash", False))


def _row(client, project_id: str, by_id: dict, workspace_id) -> dict | None:
    """A project by id, if it still exists in this workspace."""
    row = by_id.get(str(project_id))
    if row is None:
        try:
            row = client.get_project(str(project_id))
        except Exception as exc:  # noqa: BLE001 - only a gone project is skipped
            if _is_gone(exc):
                return None
            raise
    if not isinstance(row, dict) or not row.get("slug"):
        return None
    if row.get("workspace_id") is not None and workspace_id and str(row["workspace_id"]) != str(workspace_id):
        return None
    return row


def _own(row: dict, reason: str) -> ProjectSpec:
    return ProjectSpec(slug=row["slug"], name=str(row.get("name") or row["slug"]),
                       description=str(row.get("description") or ""), origin=Origin.RULE.value,
                       project_id=str(row["id"]), reason=reason)


def _folder_repo(folder: Path):
    from .backfill import git_context

    try:
        context = git_context(Path(folder))
    except Exception:  # noqa: BLE001 - a broken .git never stops an import
        return None
    if context is None or not context.repo:
        return None
    return context


def _inside(source_prefix: str, folder_prefix: str) -> bool:
    """The source's code is this folder, or sits inside it.

    Never the other way round: a source attached to the whole repository (the
    default, prefix "") is every folder's ancestor, and treating it as this
    folder's would make every project on a shared repo -- a monorepo -- this
    folder's own, which is the misfile this module exists to stop.
    """
    source, folder = source_prefix.strip("/"), folder_prefix.strip("/")
    return source == folder or not folder or source.startswith(folder + "/")


def load(client, coverage, folder: Path) -> Known:
    """The workspace's projects, and which of them are this folder's own.

    A project that is gone or out of reach is not reused. A read that FAILED
    (the network, the server) stops the import like the listing's own failure
    does, before anything is classified: guessing "not this folder's" there
    would split a re-imported folder into a duplicate project.
    """
    workspace_id = coverage.scope.workspace_id
    known = Known(client=client)
    rows = _list(client, workspace_id)
    known.rows = {row["slug"]: row for row in rows}
    by_id = {str(row.get("id")): row for row in rows}

    def adopt(row: dict | None, reason: str) -> None:
        if row is None or row["slug"] in known.own:
            return
        known.rows.setdefault(row["slug"], row)
        known.own[row["slug"]] = _own(row, reason)

    if coverage.scope.project_id:
        adopt(_row(client, coverage.scope.project_id, by_id, workspace_id), POINTED_AT)
    for project_id in _filed_before(coverage):
        adopt(_row(client, project_id, by_id, workspace_id), IMPORTED_BEFORE)

    context = _folder_repo(folder)
    if context is not None:
        repo = context.repo.lower()
        # Projects that name the repository first, then any with a code source.
        candidates = sorted(
            (row for row in rows if row.get("code_source_count") or row.get("repo")),
            key=lambda row: str(row.get("repo") or "").lower() != repo,
        )[:MAX_SOURCE_CHECKS]
        matched: list[dict] = []
        for row in candidates:
            try:
                sources = client.list_project_code_sources(str(row["id"]))
            except Exception as exc:  # noqa: BLE001 - only a gone project is skipped
                if _is_gone(exc):
                    continue
                raise
            if any(isinstance(source, dict)
                   and str(source.get("repo") or "").lower() == repo
                   and source.get("status") in LIVE_SOURCE
                   and _inside(str(source.get("path_prefix") or ""), context.path_prefix)
                   for source in sources or ()):
                matched.append(row)
        # ONE project, or none: two projects holding this folder's code leave
        # the choice to the classifier and a person, never to code.
        if len(matched) == 1:
            adopt(matched[0], code_source_reason(context.repo))
    return known


def _filed_before(coverage) -> list[str]:
    """Project ids a previous import of this folder filed into or created.

    The files' own rows first; then the approved units' bindings and the
    projects a superseded request created, which outlive a row whose project
    was cleared (`--retry-dead` clears it before this import reads it).
    """
    ids: dict[str, None] = {}
    for item in coverage.rows():
        if item.get("project_id"):
            ids.setdefault(str(item["project_id"]), None)
    for binding in (coverage.meta("approved_units", {}) or {}).values():
        if isinstance(binding, dict) and binding.get("project_id"):
            ids.setdefault(str(binding["project_id"]), None)
    for request in (coverage.meta("superseded_request"), coverage.meta("approved_request")):
        for made in ((request or {}).get("created") or {}).values() if isinstance(request, dict) else ():
            if isinstance(made, str):
                ids.setdefault(made, None)
    return list(ids)


# -- the plan's projects --------------------------------------------------------


@dataclass
class Settled:
    #: Review lines saying what code changed.
    notes: list[str] = field(default_factory=list)
    #: Projects the classifier selected that became new ones (nobody reviews).
    declined: int = 0


def retarget(plan: Plan, mapping: dict[str, str]) -> None:
    """Move every decision naming a slug in `mapping` to its new slug."""
    if not mapping:
        return
    for row in plan.assignments:
        row.project = mapping.get(row.project, row.project)
    for spec in (plan.experiments or {}).values():
        if spec.get("project") in mapping:
            spec["project"] = mapping[spec["project"]]
    for spec in (plan.runs or {}).values():
        if spec.get("project") in mapping:
            spec["project"] = mapping[spec["project"]]


def _used(plan: Plan) -> dict[str, int]:
    """Slugs the plan files anything into, with their assigned-row counts."""
    used: dict[str, int] = {}
    for row in plan.assignments:
        used[row.project] = used.get(row.project, 0) + 1
    for spec in [*(plan.experiments or {}).values(), *(plan.runs or {}).values()]:
        if spec.get("project"):
            used.setdefault(spec["project"], 0)
    for slug in (plan.fixed or {}).values():
        used.setdefault(slug, 0)
    return used


def settle(plan: Plan, known: Known, *, attended: bool, folder: Path) -> Settled:
    """Give every project in `plan` its origin, in place. Idempotent.

    `attended` is False when nobody reviews the plan before it is imported
    (`--yes`, the desktop's automatic imports): a project the classifier chose
    to reuse then becomes a new one, named for the folder.
    """
    out = Settled()
    used = _used(plan)
    specs: dict[str, ProjectSpec] = {}
    for spec in plan.projects:
        specs.setdefault(spec.slug, spec)
    for slug in used:
        specs.setdefault(slug, ProjectSpec(slug=slug, name=slug))
    existing = set(known.existing)
    renamed: dict[str, str] = {}
    final: dict[str, ProjectSpec] = {}
    taken = set(existing) | set(specs)
    # Where files imported before already are. Never renamed: their coverage
    # rows carry this slug, and the plan only organizes them.
    kept = set((plan.fixed or {}).values())

    for slug, spec in specs.items():
        if slug in kept and slug not in known.own:
            final[slug] = spec
        elif slug in known.own:
            final[slug] = replace(known.own[slug], tags=spec.tags or known.own[slug].tags)
        elif spec.origin == Origin.MODEL.value and slug in known.rows:
            row = known.rows[slug]
            final[slug] = replace(spec, name=str(row.get("name") or slug),
                                  description=str(row.get("description") or ""),
                                  project_id=str(row["id"]), near="")
        elif slug in existing:
            # A NEW name that IS an existing slug (the chunked naming answer, a
            # selection whose project went away): never merged, renamed.
            new = free_slug(slug, taken)
            taken.add(new)
            renamed[slug] = new
            final[new] = replace(spec, slug=new, origin=Origin.NEW.value, project_id=None,
                                 near=slug, reason="")
        else:
            final[slug] = replace(spec, origin=Origin.NEW.value, project_id=None,
                                  near=spec.near or near_miss(slug, existing))

    if not attended:
        home = folder_slug(folder)
        for slug, spec in list(final.items()):
            if spec.origin != Origin.MODEL.value or slug not in used:
                continue
            del final[slug]
            count = out.declined = out.declined + 1
            if home in known.own:
                # An earlier unattended import already gave this folder a
                # project named for it: the files go there, not to `-2`.
                new = renamed[slug] = home
                final.setdefault(home, known.own[home])
                out.notes.append(
                    f"Your agent matched {used[slug]:,} file{'s' if used[slug] != 1 else ''} to the "
                    f"existing project {slug}; they go into this folder's own project, {home}, "
                    "instead: an import nobody reviews never adds files to another existing project.")
                continue
            new = free_slug(home, taken)
            taken.add(new)
            renamed[slug] = new
            final[new] = ProjectSpec(
                slug=new, name=Path(folder).name + (f" {count}" if count > 1 else ""),
                description=(f"Files from {Path(folder).name} that the import's agent matched to the "
                             f"existing project {spec.name or slug}. An import nobody reviews never "
                             "adds files to an existing project; move them there if they belong."),
                origin=Origin.NEW.value, near=slug,
                reason=f"the agent matched these files to existing project {slug}",
            )
            n = used[slug]
            out.notes.append(
                f"Your agent matched {n:,} file{'s' if n != 1 else ''} to the existing project "
                f"{slug}; they go into a new project, {new}, instead: an import nobody reviews "
                f"never adds files to an existing project. Move them into {slug} if they belong there.")

    retarget(plan, renamed)
    plan.projects = list(final.values())
    return out


def fill_counts(plan: Plan, known: Known) -> None:
    """What each project the classifier chose to reuse already holds, best-effort."""
    client = known.client
    if client is None:
        return
    for spec in plan.projects:
        if spec.origin != Origin.MODEL.value or not spec.project_id or spec.existing_runs is not None:
            continue
        try:
            page = client.list_runs(project_id=spec.project_id, limit=COUNT_LIMIT)
            items = page if isinstance(page, list) else page.items
            spec.existing_runs = len(items)
        except Exception:  # noqa: BLE001 - a hint, never a reason to stop
            pass
        try:
            rows = client.transport.get(f"/v1/projects/{spec.project_id}/artifacts",
                                        params={"limit": COUNT_LIMIT})
            spec.existing_files = len(rows) if isinstance(rows, list) else None
        except Exception:  # noqa: BLE001
            pass


def _count(n: int | None, what: str) -> str:
    if n is None:
        return ""
    more = "+" if n >= COUNT_LIMIT else ""
    return f"{n:,}{more} {what}{'' if n == 1 and not more else 's'}"


def holds(spec: ProjectSpec) -> str:
    """"14 runs and 52 files", or "" when nothing could be read."""
    parts = [p for p in (_count(spec.existing_runs, "run"), _count(spec.existing_files, "file")) if p]
    return " and ".join(parts)


def tag(spec: ProjectSpec | None) -> str:
    """The review screen's one-word mark."""
    if spec is None or spec.origin in (Origin.NEW.value, ""):
        return "new"
    return "EXISTING"


def detail(spec: ProjectSpec | None) -> str:
    """The review screen's line under a project, or ""."""
    if spec is None:
        return ""
    if spec.origin == Origin.RULE.value:
        return f"\"{spec.name or spec.slug}\": {spec.reason}"
    if spec.origin == Origin.MODEL.value:
        has = holds(spec)
        return (f"\"{spec.name or spec.slug}\"" + (f", which already has {has}" if has else "")
                + ". Your agent chose it: change the plan if these files are new work.")
    if spec.near:
        return f"possibly the same project as existing {spec.near}"
    return ""


def counts(plan: Plan, assigned: dict[str, str]) -> dict[str, int]:
    """`backfill.plan_ready`'s project counts, over the projects files go into."""
    specs = {spec.slug: spec for spec in plan.projects}
    out = {"projects_new": 0, "projects_reused_rule": 0, "projects_reused_model": 0,
           "projects_near_miss": 0}
    for slug in set(assigned.values()):
        spec = specs.get(slug)
        origin = spec.origin if spec is not None else Origin.NEW.value
        if origin == Origin.RULE.value:
            out["projects_reused_rule"] += 1
        elif origin == Origin.MODEL.value:
            out["projects_reused_model"] += 1
        else:
            out["projects_new"] += 1
            if spec is not None and spec.near:
                out["projects_near_miss"] += 1
    return out


def plan_entry(spec: ProjectSpec | None) -> dict:
    """A project's origin fields in `plan.json`."""
    if spec is None:
        return {"existing": False, "origin": Origin.NEW.value}
    out: dict = {"existing": spec.origin in (Origin.RULE.value, Origin.MODEL.value),
                 "origin": spec.origin or Origin.NEW.value, "name": spec.name or spec.slug}
    if spec.project_id:
        out["project_id"] = spec.project_id
    if spec.reason:
        out["reason"] = spec.reason
    if spec.existing_runs is not None:
        out["existing_runs"] = spec.existing_runs
    if spec.existing_files is not None:
        out["existing_files"] = spec.existing_files
    if spec.near:
        out["possibly_same_as"] = spec.near
    return out


# -- after approval -------------------------------------------------------------


class ExistingGone(Exception):
    """An existing project the review showed was deleted before the import used it."""

    def __init__(self, slug: str):
        super().__init__(f"the existing project {slug} no longer exists")
        self.slug = slug


#: The `metadata` key a new project carries the create's own nonce under, so a
#: create whose answer was lost is recognised as ours, never someone else's.
CREATE_NONCE_KEY = "backfill_create"


def destination(client, slug: str, spec: dict, *, workspace_id, created: dict, remember,
                authored_by: str) -> dict:
    """The project an approved plan's `slug` files into, creating a new one.

    EXISTING (RULE, MODEL): read by the id the review showed, never by slug.
    NEW: created, and never an existing project: a slug someone holds by now
    (a project outside the listing, a race) moves to the next free `slug-N`.
    `created` records what this import made so a resumed one finds it rather
    than making another; `remember()` saves it before anything else happens.
    A spec saved by an older CLI (no origin) resolves by slug as it did then.
    """
    from probe.sdk import errors

    origin = spec.get("origin") or ""
    if origin in (Origin.RULE.value, Origin.MODEL.value) and spec.get("project_id"):
        try:
            return client.get_project(str(spec["project_id"]))
        except Exception as exc:  # noqa: BLE001 - only a gone project is named
            if _is_gone(exc):
                raise ExistingGone(slug) from None
            raise
    name = spec.get("name") or slug
    description = spec.get("description") or None
    if origin != Origin.NEW.value:
        project = client.resolve_project(slug, strict=True)
        if project is not None:
            return project
        try:
            return client.create_project(slug, name, kind="general", authored_by=authored_by,
                                         description=description, workspace_id=workspace_id)
        except errors.ConflictError:
            project = client.resolve_project(slug, strict=True)
            if project is None:
                raise
            return project
    made = created.get(slug)
    if isinstance(made, str):
        try:
            return client.get_project(made)
        except Exception as exc:  # noqa: BLE001 - a gone one is made again
            if not _is_gone(exc):
                raise
    elif isinstance(made, dict) and made.get("pending"):
        # A create whose answer was lost (a timeout after the server made it):
        # ours only if it carries this create's nonce, never a project someone
        # else made under that slug in the meantime.
        project = client.resolve_project(str(made["pending"]), strict=True)
        if project is not None and made.get("nonce") and \
                (project.get("metadata") or {}).get(CREATE_NONCE_KEY) == made["nonce"]:
            created[slug] = str(project["id"])
            remember()
            return project
    tried: set[str] = set()
    for _ in range(20):
        candidate = free_slug(slug, tried)
        tried.add(candidate)
        if client.resolve_project(candidate, strict=True) is not None:
            continue
        nonce = uuid.uuid4().hex
        created[slug] = {"pending": candidate, "nonce": nonce}
        remember()
        try:
            project = client.create_project(candidate, name, kind="general", authored_by=authored_by,
                                            description=description, workspace_id=workspace_id,
                                            metadata={CREATE_NONCE_KEY: nonce})
        except errors.ConflictError:
            continue
        created[slug] = str(project["id"])
        remember()
        return project
    raise errors.ConflictError(f"no free project slug near {slug!r}")


def retarget_structure(structure: dict | None, mapping: dict[str, str]) -> None:
    """Point a saved plan's experiments and runs at the slugs projects got."""
    if not structure or not mapping:
        return
    for group in ("experiments", "runs"):
        for spec in (structure.get(group) or {}).values():
            if isinstance(spec, dict) and spec.get("project") in mapping:
                spec["project"] = mapping[spec["project"]]
