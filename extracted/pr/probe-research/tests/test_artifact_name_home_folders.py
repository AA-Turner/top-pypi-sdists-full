"""An artifact name is a repo-relative path, and a `Users/` or `home/` folder in
it is part of the path, not a home directory.

CLI 0.260.0 scrubbed names with `scrub_text`, whose home-path rule cut
`apps/web/pages/Admin/Users/Edit.tsx` to `apps/web/pages/Admin<path>`. Every file
in such a folder collapsed onto one name: the first delivered under it, the
next 409'd as superseded, and the folder import refused (2026-10-16, a
customer's 11,084-file import). These pin the name and the repair of an import
whose requests were frozen under the cut name.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

from probe.cli.backfill_coverage import Coverage, Scope
from probe.cli.backfill_delivery import enqueue
from probe.sdk import errors
from probe.sdk import journal as jm
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import Journal, drain
from probe.sdk.redaction import scrub_text

ADMIN_USERS = ("apps/web/pages/Admin/Users/Edit.tsx", "apps/web/pages/Admin/Users/New.tsx")
SRC = Path(__file__).resolve().parents[1] / "src" / "probe"


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_ATTRIBUTION", raising=False)
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)


class Server:
    """The artifact store's one rule that matters here: a name holds one live
    file, and a second file confirmed under it is a superseded upload (409,
    `StaleUpload` in `app/artifacts/uploads_router.py`)."""

    def __init__(self):
        self.live = {}

    def upload_fingerprinted(self, anchor, anchor_id, name, path, *, digest, size, **kwargs):
        data = Path(path).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
        held = self.live.get((anchor_id, name))
        if held is not None and held["content_hash"] != digest:
            raise errors.ConflictError(
                "a newer version of this file is already live; this upload is superseded"
            )
        return self.live.setdefault((anchor_id, name), {
            "id": f"artifact-{len(self.live)}", "name": name, "status": "complete",
            "uri": f"r2://artifacts/{digest}", "content_hash": digest,
            "size_bytes": size, "is_reference": False,
        })


@pytest.mark.parametrize("name", [
    "apps/web/pages/Admin/Users/Edit.tsx",
    "services/home/index.ts",
    "data/home/alice/train.csv",
])
def test_a_queued_upload_keeps_a_users_or_home_folder_in_its_name(tmp_path, name):
    source = tmp_path / "file"
    source.write_bytes(b"x")
    queue = Journal(tmp_path / "outbox")
    queue.append_upload(anchor="project", anchor_id="p1", name=name, src_path=str(source))
    [(_, op)] = queue.pending()
    assert op["upload"]["name"] == name


def test_a_credential_in_a_name_is_still_redacted(tmp_path):
    source = tmp_path / "file"
    source.write_bytes(b"x")
    queue = Journal(tmp_path / "outbox")
    token = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
    queue.append_upload(anchor="project", anchor_id="p1", name=f"notes token={token}.txt",
                        src_path=str(source))
    [(_, op)] = queue.pending()
    assert token not in op["upload"]["name"]


def test_no_artifact_name_goes_through_the_prose_scrubber():
    """`scrub_text` is for prose (notes, errors). Every site that scrubs a name
    -- `Client.upload`, `Run.log_artifact`, the journal, `probe artifact add`'s
    multipart door -- must use `scrub_string`; this finds a fifth."""
    offenders = [
        f"{path.relative_to(SRC)}:{number}"
        for path in SRC.rglob("*.py")
        for number, line in enumerate(path.read_text().splitlines(), 1)
        if re.search(r"\bname\w*\s*=\s*scrub_text\(|scrub_text\(\s*name", line)
    ]
    assert offenders == []


def _import(tmp_path, paths=ADMIN_USERS):
    folder = tmp_path / "repo"
    for index, path in enumerate(paths):
        (folder / path).parent.mkdir(parents=True, exist_ok=True)
        (folder / path).write_text(f"export default function Page{index}() {{}}\n")
    scope = Scope("http://test", "tenant", "workspace", "project")
    project = {"id": "project", "slug": "project", "customer_id": "tenant", "workspace_id": "workspace"}
    store = Coverage.for_folder(folder, scope, directory=tmp_path / "coverage")
    client = Client(settings=Settings(base_url="http://test", token="test-token"),
                    spool_dir=tmp_path / "outbox", auto_drain=False,
                    async_writes=False, attribution="backfill")
    with store.writer() as state:
        state.observe(folder, list(paths))
        state.approve({path: project for path in paths})
        for path in paths:
            state.remember_manifest(path, {"path": path})
    return folder, store, client


def _versions(state):
    return state.conn.execute("SELECT COUNT(*) FROM versions").fetchone()[0]


def test_an_import_frozen_under_cut_names_is_reissued_once_and_lands(tmp_path, monkeypatch):
    folder, store, client = _import(tmp_path)
    server = Server()
    outbox = client._delivery_journal()
    with client, store.writer() as state:
        # What 0.260.0 froze: both names cut to the same `<path>` form.
        with monkeypatch.context() as legacy:
            legacy.setattr(jm, "scrub_string", scrub_text)
            assert enqueue(state, client, folder) == (2, [])
        result = drain(outbox, client_factory=lambda _: server)
        assert (result.delivered, result.dead_lettered) == (1, 1)
        assert {name for _, name in server.live} == {"apps/web/pages/Admin<path>"}
        stale = {row["path"]: row["correlation"] for row in state.rows()}
        state.reconcile(client)
        assert state.report()["delivered"] == []  # the refused import

        # The fixed CLI resumes: both files are reissued under their own names.
        assert enqueue(state, client, folder) == (2, [])
        assert {client.delivery_state(c)["state"] for c in stale.values()} == {
            "delivered", "discarded"}  # the 409'd request no longer retries
        assert drain(outbox, client_factory=lambda _: server).delivered == 2
        state.reconcile(client)
        assert sorted(state.report()["delivered"]) == sorted(ADMIN_USERS)
        assert {name for _, name in server.live} >= set(ADMIN_USERS)

        # And it converges: another pass mints nothing and uploads nothing.
        assert enqueue(state, client, folder) == (0, [])
        assert _versions(state) == 4


@pytest.mark.parametrize("left", ["queued", "pending"])
def test_a_cut_off_import_retires_its_waiting_requests_before_reissuing(tmp_path, monkeypatch, left):
    """The old CLI was interrupted before its drain: both requests still wait,
    queued or half-appended (intent committed, op file not). A reissue that
    left them waiting would send the cut name beside the right one."""
    folder, store, client = _import(tmp_path)
    server = Server()
    outbox = client._delivery_journal()
    with client, store.writer() as state:
        with monkeypatch.context() as legacy:
            legacy.setattr(jm, "scrub_string", scrub_text)
            assert enqueue(state, client, folder) == (2, [])
        stale = [row["correlation"] for row in state.rows()]
        if left == "pending":
            for path in outbox.ops_dir.iterdir():
                path.unlink()
        assert {client.delivery_state(c)["state"] for c in stale} == {left}

        assert enqueue(state, client, folder) == (2, [])
        assert {client.delivery_state(c)["state"] for c in stale} == {"discarded"}
        result = drain(outbox, client_factory=lambda _: server)
        assert (result.delivered, result.dead_lettered) == (2, 0)
        assert {name for _, name in server.live} == set(ADMIN_USERS)  # no `<path>` name
        assert outbox.failed() == []
        state.reconcile(client)
        assert sorted(state.report()["delivered"]) == sorted(ADMIN_USERS)


def test_a_request_under_its_own_name_is_never_reissued(tmp_path):
    """Delivered, its receipt not yet accepted (the import stopped between the
    drain and `reconcile`): the resume accepts it as it is."""
    folder, store, client = _import(tmp_path)
    server = Server()
    with client, store.writer() as state:
        assert enqueue(state, client, folder) == (2, [])
        assert drain(client._delivery_journal(), client_factory=lambda _: server).delivered == 2
        assert enqueue(state, client, folder) == (0, [])
        assert sorted(state.report()["delivered"]) == sorted(ADMIN_USERS)
        assert _versions(state) == 2


def test_a_legacy_adoption_under_the_raw_path_still_verifies(tmp_path):
    """`backfill_legacy` adopts an artifact already stored under the file's
    path and writes its receipt under that name. When `scrub_string` changes
    the path, the uploader would send another name; both name this file."""
    path = "models/sk-learn-baseline-v1/model.pkl"
    from probe.sdk.redaction import scrub_string

    assert scrub_string(path) != path  # what makes the two names differ
    folder, store, client = _import(tmp_path, paths=(path,))
    with client, store.writer() as state:
        [row] = state.rows()
        intent = state.intend(row, reference=False, uri=None)
        state.accept_receipt(intent["correlation"], {
            "correlation": intent["correlation"], "state": "delivered", "status": "complete",
            "artifact_id": "artifact-1", "anchor": "project", "anchor_id": "project",
            "name": path, "content_hash": row["observed_hash"], "size_bytes": row["size"],
            "is_reference": False, "uri": None, "readable": True,
            "provenance": "legacy_download_verified",
        })
        assert state.report()["delivered"] == [path]


def test_nothing_wakes_the_uploader_while_a_cut_name_still_waits(tmp_path, monkeypatch):
    """A resumed request wakes the background uploader (`_wake_delivery`), and
    that uploader sends whatever is queued. A healthy file sorting before the
    cut ones is resumed first, so the cut requests are retired before it."""
    paths = ("apps/web/index.tsx", *ADMIN_USERS)
    folder, store, client = _import(tmp_path, paths=paths)
    with client, store.writer() as state:
        with monkeypatch.context() as legacy:
            legacy.setattr(jm, "scrub_string", scrub_text)
            assert enqueue(state, client, folder) == (3, [])
        stale = [row["correlation"] for row in state.rows() if row["path"] in ADMIN_USERS]
        woken = []
        monkeypatch.setattr(client, "_wake_delivery", lambda: woken.append(
            {client.delivery_state(c)["state"] for c in stale}))
        assert enqueue(state, client, folder) == (3, [])
        assert woken and all(states == {"discarded"} for states in woken)
