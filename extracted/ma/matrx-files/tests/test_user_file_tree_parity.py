"""The browser's door and the daemon's filters admit the same rows — D16's guard.

D16: only user-visible files sync, **by ONE database predicate shared with the
browser**. Two independent spellings of that predicate are in service:

* ``files.get_user_file_tree`` (scope ``'tree'``) — the SQL door the browser reads its tree
  through, which inlines ``files.is_user_visible_path`` plus the row half;
* ``matrx_files.user_visible.user_visible_filters()`` — the matrx-orm kwargs the
  change feed applies, which is what actually reaches a device's disk.

If those two ever part company, the browser shows a user a file their laptop
does not have, or hides one it does — the disagreement D16 exists to forbid.
This test runs both over the same owner's corpus and asserts the id sets are
equal. It passes; it is not xfail.

🚨 WHAT THIS TEST USED TO BE, and why it had to change (folder-sync L5-5).
Until 2026-09-21 it transcribed matrx-frontend's own TypeScript copy of the
rule (``isHiddenFromUserTree = isSystemPath() || isFastFirePath()``) and
xfailed on the difference, with the note "this goes green when FS-L5 deletes
isHiddenFromUserTree and its ten call sites." FS-L5 deleted it (commit
``fd074e96c5``). The transcription outlived the thing it transcribed, so the
test went on asserting a disagreement that no longer existed and could never
go red again — blind in both directions. The browser's remaining TypeScript
mirror is guarded where it lives, by matrx-frontend's
``pnpm check:user-visible-parity``; what this test owns is the two SERVER
spellings, which is the half aidream can actually see.

``files.is_crawl_artifact`` is NOT part of the rule (SPEC-SERVER §1.2 S2): it
is a provenance test each consumer adds as its own conjunct. The tree adds it
and the feed does not, so it is subtracted explicitly below rather than being
allowed to look like drift.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

#: The heaviest live owner (18,722 alive rows, 15 of them top-level ``FastFire/``
#: — the corpus where a visibility rule's edges actually bite). Read 2026-09-21.
_OWNER = "87a6e699-3622-4869-8843-d0867456c0dd"

#: The names of the deleted second rule. Their return would re-create the exact
#: browser/disk disagreement D16 forbids, so their ABSENCE is asserted rather
#: than their behavior transcribed.
_DELETED_TS_RULE = ("isHiddenFromUserTree", "isFastFirePath")


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


@pytest.mark.asyncio
async def test_the_browsers_rendered_set_equals_the_feeds():
    """The tree RPC's set == the feed's set, over the same live corpus."""
    _skip_without_db()
    asyncpg = pytest.importorskip("asyncpg")

    from matrx_files.db import bootstrap_db, connection_url, models_files
    from matrx_files.user_visible import explain_rule, user_visible_filters

    bootstrap_db()
    feed_rows = await (
        models_files.Files.filter(created_by=_OWNER, deleted_at__isnull=True)
        .filter(**user_visible_filters())
        .values("id", "file_path")
    )
    feed = {str(r["id"]): r["file_path"] for r in feed_rows}
    assert feed, "the corpus owner has no visible rows — the test proves nothing"

    conn = await asyncpg.connect(connection_url())
    try:
        # The browser's own door, paged to exhaustion at its own ceiling.
        tree: dict[str, str] = {}
        offset = 0
        page_size = 5000
        while True:
            payload = await conn.fetchval(
                "select files.get_user_file_tree($1::uuid, $2::int, $3::int,"
                " false, false, 'name', 'tree')",
                _OWNER,
                page_size,
                offset,
            )
            page = json.loads(payload) if isinstance(payload, str) else payload
            rows = [r for r in (page or []) if r.get("kind") == "file"]
            for row in rows:
                # Shared-in files reach the tree through iam.permissions, not
                # through the owner path the feed reads; scope both sides to
                # rows this user owns.
                if str(row.get("created_by")) == _OWNER:
                    tree[str(row["id"])] = row.get("path")
            if len(page or []) < page_size:
                break
            offset += page_size

        # The tree's EXTRA conjunct, subtracted by name instead of by guess.
        crawl = {
            str(r["id"])
            for r in await conn.fetch(
                "select id from files.files"
                " where created_by = $1::uuid and deleted_at is null"
                "   and files.is_crawl_artifact(id)",
                _OWNER,
            )
        }
    finally:
        await conn.close()

    expected = {file_id: path for file_id, path in feed.items() if file_id not in crawl}

    only_in_feed = sorted(expected[i] for i in set(expected) - set(tree))
    only_in_tree = sorted(tree[i] for i in set(tree) - set(expected))
    assert not only_in_feed and not only_in_tree, (
        "D16 BROKEN: the browser's tree and the sync feed no longer admit the same "
        f"rows for {_OWNER}.\n"
        f"  synced to disk but NOT shown in the browser ({len(only_in_feed)}): "
        f"{only_in_feed[:5]}\n"
        f"  shown in the browser but NOT synced ({len(only_in_tree)}): "
        f"{only_in_tree[:5]}\n"
        "Neither list may be non-empty: there is supposed to be ONE predicate.\n"
        f"{explain_rule()}"
    )
    assert len(expected) == len(tree)


def test_the_browser_keeps_no_second_visibility_rule():
    """The deleted TypeScript rule has not come back.

    Cross-repo and therefore conditional: it runs when the matrx-frontend
    checkout sits beside this one, and SKIPS with the reason when it does not —
    never a quiet pass. matrx-frontend guards its own remaining mirror (the one
    deliberate realtime-payload copy) with ``pnpm check:user-visible-parity``.
    """
    # The independence gate copies this package into a shallow temporary
    # directory, so a fixed parents[4] lookup raises before this optional
    # cross-repository witness can honestly skip.
    checkout_parent = next(
        (
            parent
            for parent in Path(__file__).resolve().parents
            if (parent / "matrx-frontend" / "features" / "files").is_dir()
        ),
        None,
    )
    frontend = (
        checkout_parent / "matrx-frontend" / "features" / "files"
        if checkout_parent is not None
        else None
    )
    if frontend is None:
        pytest.skip(
            "matrx-frontend checkout not found beside this package — this half of D16 is "
            "UNMEASURED on this machine, not proven"
        )
    offenders: list[str] = []
    for path in frontend.rglob("*.ts*"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for name in _DELETED_TS_RULE:
            # A tombstone comment naming the deleted function is fine; a
            # declaration of it is the second rule coming back.
            if f"function {name}" in text or f"const {name} =" in text:
                offenders.append(f"{path}: {name}")
    assert not offenders, (
        "the browser has declared a second visibility rule again "
        f"({offenders}). D16 allows ONE predicate, in the database, shared with "
        "the feed; a TypeScript rule applied after the RPC hides rows the daemon "
        "syncs to disk."
    )
