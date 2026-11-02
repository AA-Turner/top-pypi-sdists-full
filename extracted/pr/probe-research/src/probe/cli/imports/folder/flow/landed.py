"""count what landed (artifacts across the projects the agent filed into) and read those projects from its summary."""

from __future__ import annotations


#: One page of the anchor listing, matching the server's per-request artifact
#: ceiling. Hitting it exactly means "at least this many", never "this many".
RECONCILE_PAGE = 1_000


def _rows(payload) -> list | None:
    """The item list out of a bare list, a page dict, or a Page object.

    dict is tested BEFORE the attribute lookup: `dict.items` is a bound method,
    so a getattr-first version reads every page dict as "no rows" and quietly
    counts zero.
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        items = payload.get("items", payload)
    else:
        items = getattr(payload, "items", None)
    return items if isinstance(items, list) else None


def _project_id(client, project: str) -> str | None:
    """`project` as a UUID. A bare ref is a SLUG; ids arrive as `id:<uuid>`.

    ``/v1/projects/{project_id}/artifacts`` types its path param as a UUID, so a
    slug arrives as a 422 about UUID parsing rather than a lookup -- the same
    trap :func:`resolve_anchor` documents. It matters here because the slugs come
    from :func:`summary_projects`, i.e. the read-back is fed the one form the
    route cannot take, and the 422 is swallowed as "could not read back".
    """
    from ....commands import ref_syntax as refs

    try:
        # verify=False: this is a READ-BACK, so an `id:` ref needs no round trip
        # to confirm what it already states, and one fewer request per project.
        return refs.resolve(client, "project", project, verify=False).id
    except Exception:  # noqa: BLE001 - a read-back miss degrades, never raises here
        return None


def count_landed(client, project: str) -> tuple[int, bool]:
    """Artifacts under a project, INCLUDING its experiments. (count, at_least).

    Counting only the project anchor would undercount every import that did what
    it was told: step 3 of the prompt asks the agent to attach artifacts to an
    experiment where the evidence supports one, and an experiment-anchored
    artifact is not returned by the project listing. A faithful 204-file import
    that grouped 83 of them read back as 121, printing a 40% shortfall that was
    entirely an artifact of where the reconcile looked.

    One page per anchor, deliberately. Walking every page of a 12,000-artifact
    project to print one number would make the cheap half of this feature the
    slow half; hitting the page exactly reports "at least", which is honest,
    instead of a total that is quietly a page size.

    The experiment reads run CONCURRENTLY. Serially this was an N+1 -- one
    round trip per experiment, after the one for the project -- and a project
    with fifty experiments spent fifty sequential round trips producing a
    single number at the very end of an import someone is already waiting on.
    They are independent reads of independent anchors, so nothing is ordered
    between them and the only reason it was a loop is that it was written as
    one.
    """
    from concurrent.futures import ThreadPoolExecutor

    from probe.sdk.artifact.anchors import Anchor

    try:
        project_id = _project_id(client, project)
        if project_id is None:
            return -1, False
        counted = _rows(client.list_anchored(Anchor.PROJECT, project_id, limit=RECONCILE_PAGE))
        if counted is None:
            return -1, False
        total = len(counted)
        at_least = total >= RECONCILE_PAGE

        # EVERY experiment of the project, not the first page: the list pages
        # by offset (100 a page unless asked), and a short list here would
        # report a short count as if it were the whole one.
        experiments: list = []
        cursor = None
        while True:
            listed = client.list_experiments(project_id=project_id, limit=500, cursor=cursor)
            page_rows = _rows(listed)
            if page_rows is None:
                return -1, False
            experiments.extend(page_rows)
            cursor = getattr(listed, "next_cursor", None)
            if not cursor:
                break
        exp_ids = []
        for exp in experiments or []:
            exp_id = exp.get("id") if isinstance(exp, dict) else getattr(exp, "id", None)
            if exp_id:
                exp_ids.append(str(exp_id))
        if not exp_ids:
            return total, at_least

        def page(exp_id: str):
            return _rows(
                client.list_anchored(
                    Anchor.EXPERIMENT, exp_id, project_id=project_id, limit=RECONCILE_PAGE
                )
            )

        # Bounded: a project with hundreds of experiments must not open
        # hundreds of sockets to print one number.
        with ThreadPoolExecutor(max_workers=min(8, len(exp_ids))) as pool:
            for rows in pool.map(page, exp_ids):
                if rows is None:
                    # One unreadable anchor makes the WHOLE count unknown rather
                    # than silently short: reporting a shortfall that is really a
                    # failed lookup trains people to ignore the one number this
                    # feature exists for.
                    return -1, False
                total += len(rows)
                at_least = at_least or len(rows) >= RECONCILE_PAGE
        return total, at_least
    except Exception:  # noqa: BLE001 - reconcile must never fail the import
        return -1, False


def _embedded_summaries(text: str, key: str = "projects"):
    """Every ``{...}`` in `text` that parses and carries a list under `key`.

    `key` exists because the chunked classification asks for three different
    shapes -- a survey, a project list, a slice of assignments -- and each has
    to be told apart from the others in the same stream. Defaulting to
    ``projects`` keeps every existing caller reading the same thing.

    The summary does not arrive on a line of its own. Both agents are run with
    an EVENT STREAM (`agent_argv`), so the closing JSON is a STRING INSIDE an
    envelope -- `{"type":"result","result":"...done.\\n{...}"}` -- and the
    braces of the two are nested in one line of stdout. Scanning for balanced
    brace runs finds the inner object wherever it sits; matching only the whole
    line finds it exactly when the agent is NOT streaming, which is never.
    """
    import json

    def scan(blob: str):
        depth = 0
        start = -1
        for i, ch in enumerate(blob):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}" and depth:
                depth -= 1
                if depth == 0 and start >= 0:
                    try:
                        data = json.loads(blob[start : i + 1])
                    except ValueError:
                        continue
                    if isinstance(data, dict) and isinstance(data.get(key), list):
                        yield data

    def strings(node):
        """Every string anywhere in a decoded envelope."""
        if isinstance(node, str):
            yield node
        elif isinstance(node, dict):
            for value in node.values():
                yield from strings(value)
        elif isinstance(node, list):
            for value in node:
                yield from strings(value)

    yield from scan(text)
    # The inner object is a STRING FIELD of the envelope, so in the raw line its
    # quotes are backslash-escaped and no substring of it parses. It only becomes
    # JSON again once the envelope itself is decoded — hence the second pass over
    # the decoded strings rather than more clever matching on the raw text.
    try:
        envelope = json.loads(text)
    except ValueError:
        return
    for blob in strings(envelope):
        if key in blob:
            yield from scan(blob)


def summary_projects(tail: str) -> list[str]:
    """The project slugs the agent says it filed into.

    Parsed from its closing JSON summary. This is the ONLY thing taken from the
    agent's own account of the run, and deliberately the least load-bearing one:
    it says WHERE to look, never how much landed. The count still comes from the
    server and the denominator still comes from the walk, so an agent that
    overstates its work cannot make the numbers agree — the gap just shows up.

    It says where to look, but nothing looks anywhere if this returns empty:
    with no pinned `--project` there is no fallback, so a parse miss here
    silently downgrades the whole run to "could not read back". That is what a
    top-level-only match did -- see :func:`_embedded_summaries`.
    """
    found: list[str] = []
    for line in reversed(tail.splitlines()):
        text = line.strip()
        if "projects" not in text:
            continue
        for data in _embedded_summaries(text):
            for slug in data["projects"]:
                if isinstance(slug, str) and slug and slug not in found:
                    found.append(slug)
        if found:
            return found
    return found


def count_landed_across(client, projects: list[str]) -> tuple[int, bool]:
    """Artifacts across every project the agent used. Returns (count, at_least).

    A project that cannot be read counts as unknown for the whole reconcile
    rather than silently zero: reporting a shortfall that is really a failed
    lookup would train people to ignore the one number this feature exists for.
    """
    if not projects:
        return -1, False
    total = 0
    at_least = False
    for slug in projects:
        count, capped = count_landed(client, slug)
        if count < 0:
            return -1, False
        total += count
        at_least = at_least or capped
    return total, at_least
