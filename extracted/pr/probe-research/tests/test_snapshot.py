"""Snapshot plumbing against a real throwaway git repo. No network."""

from __future__ import annotations

import os
import subprocess
import time

import pytest

from probe import snapshot


def _git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "repo"
    d.mkdir()
    _git(d, "init", "-q")
    _git(d, "config", "user.email", "t@example.com")
    _git(d, "config", "user.name", "t")
    (d / "a.txt").write_text("hello\n")
    _git(d, "add", "-A")
    _git(d, "commit", "-q", "-m", "init")
    return d


def _repo_state(repo):
    """Everything a capture could write into `.git`, read without writing:
    loose + packed object counts, every ref, and the index's mtime."""
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    counts = subprocess.run(
        ["git", "count-objects", "-v"], cwd=repo, env=env, capture_output=True, text=True
    ).stdout
    refs = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname) %(objectname)"],
        cwd=repo, env=env, capture_output=True, text=True,
    ).stdout
    return counts, refs, os.stat(repo / ".git" / "index").st_mtime_ns


def _make_index_stale(repo):
    """Rewrite a tracked file with the SAME bytes and a new mtime: the index's
    stat cache is now stale, so a plain `git status` WOULD rewrite `.git/index`
    to refresh it. That is what makes an unchanged index mtime mean something."""
    path = repo / "a.txt"
    data = path.read_bytes()
    time.sleep(0.02)
    path.write_bytes(data)
    later = time.time() + 5
    os.utime(path, (later, later))


def test_git_provenance_is_read_only(repo):
    """Plan 2.6. The capture used to commit the working tree into
    `refs/probe/snapshots/<run>` -- needing a git identity, growing `.git`
    (20 MB -> 306 MB on one repo) and publishing an untracked `.env` on
    `git push --mirror`. Now it reads HEAD, branch and dirty and writes nothing."""
    (repo / "a.txt").write_text("hello world\n")
    (repo / "untracked.txt").write_text("new\n")
    _git(repo, "add", "a.txt")  # the index now differs from HEAD too
    _make_index_stale(repo)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    before = _repo_state(repo)

    snap = snapshot.capture_git_snapshot("run-xyz", cwd=str(repo))

    assert _repo_state(repo) == before, "no object, ref or index write"
    assert snap == {
        "commit": None,
        "ref": None,
        "branch": subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"], cwd=repo, capture_output=True, text=True
        ).stdout.strip(),
        "head": head,
        "dirty": True,
    }
    # Control: the same tree DOES get its index rewritten by an ordinary
    # `git status`, so the unchanged mtime above is evidence, not luck.
    subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True)
    assert _repo_state(repo)[2] != before[2]


def test_the_whole_manifest_is_read_only_too(repo):
    """`capture_manifest` runs `ls-files`/`status`-class reads on the same repo;
    none may refresh the index or add an object."""
    (repo / "untracked.txt").write_text("new\n")
    _make_index_stale(repo)
    before = _repo_state(repo)
    snapshot.capture_manifest(str(repo))
    assert _repo_state(repo) == before


def test_snapshot_errors_outside_git(tmp_path):
    with pytest.raises(snapshot.SnapshotError):
        snapshot.capture_git_snapshot("r", cwd=str(tmp_path))


# --- 0.5: secret-safe code capture ---------------------------------------------
#
# Live-verified on prod before this: an untracked, non-ignored `.env` and a
# scratch file holding a `probe_pat_` token went up byte-identical from a git
# repo, and a `config.yaml` with HF/AWS/GitHub/Probe tokens from a plain folder.
# The same bytes through `log_artifact` were redacted. A snapshot cannot redact
# (restore needs the exact bytes), so a file with a finding is LEFT OUT and
# listed as skipped, reason `secret`.
#
# Every credential below is assembled at import time: no literal in this file
# has a credential's shape, so a secret scanner reading the repo stays quiet.

import hashlib  # noqa: E402

from probe.sdk import snapshot as _snap_mod  # noqa: E402

PROBE_PAT = "probe_pat_" + "0123456789abcdef" * 2
HF_TOKEN = "hf_" + "AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh"
AWS_KEY_ID = "AKIA" + "Q3ZP7XK2M5N8R4T6"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/" + "bPxRfiCYQ3ZP7XK2M5nq"
GITHUB_TOKEN = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
GENERIC_KEY = "a8f5f167f44f4964" + "e6c998dee827110c"


def _manifest_paths(m):
    """Paths whose bytes a capture keeps (a withheld file stays in `entries`, as
    `source: "withheld"`, and is never uploaded)."""
    return {e["path"] for e in m["entries"] if e.get("source") != "withheld"}


def _withheld(m):
    return {e["path"] for e in m["entries"] if e.get("source") == "withheld"}


def _skipped(m):
    return {s["path"]: s["reason"] for s in m.get("skipped") or []}


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_scratch(path):
    path.write_text(
        "# scratch: paste-and-go keys\n"
        f'PROBE = "{PROBE_PAT}"\n'
        f'HF = "{HF_TOKEN}"\n'
        f'AWS_ACCESS_KEY_ID = "{AWS_KEY_ID}"\n'
        f'AWS_SECRET_ACCESS_KEY = "{AWS_SECRET}"\n'
        f'GH = "{GITHUB_TOKEN}"\n'
    )


def test_git_capture_skips_an_untracked_env_and_a_scratch_file_with_keys(repo):
    (repo / ".env").write_text(f"PROBE_TOKEN={PROBE_PAT}\n")
    _write_scratch(repo / "scratch.py")
    (repo / "train.py").write_text("import torch\nlr = 3e-4\n")

    m = snapshot.capture_manifest(str(repo))

    assert ".env" not in _manifest_paths(m)
    assert "scratch.py" not in _manifest_paths(m)
    skipped = _skipped(m)
    assert skipped[".env"] == "secret"
    assert skipped["scratch.py"] == "secret"
    # The clean files are still captured, and their record is the exact bytes.
    by_path = {e["path"]: e for e in m["entries"] if e["source"] != "withheld"}
    assert set(by_path) == {"a.txt", "train.py"}
    assert _withheld(m) == {"scratch.py"}, "withheld, not dropped: it stays in the record"
    for name in ("a.txt", "train.py"):
        assert by_path[name]["source"] == "blob"
        assert by_path[name]["sha256"] == _sha(repo / name)
        assert by_path[name]["size"] == (repo / name).stat().st_size


def test_git_capture_content_skip_names_the_rules_never_the_values(repo):
    _write_scratch(repo / "scratch.py")
    m = snapshot.capture_manifest(str(repo))
    entry = next(s for s in m["skipped"] if s["path"] == "scratch.py")
    assert entry["found_in"] == "content"
    assert {"probe-token", "huggingface-token", "aws-access-key-id", "github-token"} <= set(
        entry["rules"]
    )
    text = repr(m)
    for value in (PROBE_PAT, HF_TOKEN, AWS_KEY_ID, AWS_SECRET, GITHUB_TOKEN):
        assert value not in text


def test_git_capture_applies_the_name_filter_to_tracked_files_too(repo):
    (repo / "service-account.json").write_text('{"type": "service_account"}\n')
    _git(repo, "add", "service-account.json")
    _git(repo, "commit", "-q", "-m", "oops")
    m = snapshot.capture_manifest(str(repo))
    assert "service-account.json" not in _manifest_paths(m)
    assert _skipped(m)["service-account.json"] == "secret"


def test_non_git_capture_skips_config_files_holding_keys(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    (root / "config.yaml").write_text(
        "model: llama\n"
        f"hf_token: {HF_TOKEN}\n"
        f"aws_access_key_id: {AWS_KEY_ID}\n"
        f"aws_secret_access_key: {AWS_SECRET}\n"
        f"github: {GITHUB_TOKEN}\n"
        f"probe: {PROBE_PAT}\n"
    )
    (root / "cfg.json").write_text('{"lr": 0.001, "probe_token": "%s"}\n' % PROBE_PAT)
    (root / "train.py").write_text("print('train')\n")

    m = snapshot.capture_manifest(str(root))

    assert _manifest_paths(m) == {"train.py"}
    assert _skipped(m)["config.yaml"] == "secret"
    assert _skipped(m)["cfg.json"] == "secret"


def test_prose_and_code_that_only_mention_tokens_are_captured(tmp_path):
    """The false-positive control: the scanner's key-name tier reads code like
    `token = tokens[0]` as an assignment of a credential. A snapshot drops the
    WHOLE file on a finding, so in source code only a quoted literal counts."""
    root = tmp_path / "plain"
    root.mkdir()
    (root / "NOTES.md").write_text(
        "Each token costs money. The access token is refreshed hourly;\n"
        "ask an admin for a token if yours expired. Tokens per second: 1.2k.\n"
    )
    (root / "train.py").write_text(
        "import getpass\n"
        "tokens = tokenizer(text)\n"
        "token = tokens[0]\n"
        "self_token: contextvars.Token | None = None\n"
        "password = getpass.getpass()\n"
        "api_key = os.environ['OPENAI_API_KEY']\n"
        "pad_token_id = tokenizer.pad_token_id\n"
    )
    (root / "sweep.yaml").write_text("max_tokens: 2048\neos_token: </s>\n")

    m = snapshot.capture_manifest(str(root))

    assert _manifest_paths(m) == {"NOTES.md", "train.py", "sweep.yaml"}
    assert "secret" not in _skipped(m).values()


def test_a_hardcoded_generic_key_is_still_caught_in_code_and_config(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    (root / "client.py").write_text(f'API_KEY = "{GENERIC_KEY}"\n')
    (root / "db.py").write_text('DB_PASSWORD = "correct horse battery"\n')
    (root / "settings.ini").write_text(f"[svc]\napi_key = {GENERIC_KEY}\n")
    (root / "ok.py").write_text("print(1)\n")

    m = snapshot.capture_manifest(str(root))

    assert _manifest_paths(m) == {"ok.py"}
    assert {p for p, r in _skipped(m).items() if r == "secret"} == {
        "client.py", "db.py", "settings.ini",
    }


def test_an_included_file_is_content_scanned(repo):
    (repo / ".gitignore").write_text("data/\n")
    (repo / "data").mkdir()
    (repo / "data" / "keys.txt").write_text(f"token: {GITHUB_TOKEN}\n")
    (repo / "data" / "rows.csv").write_text("a,b\n1,2\n")

    m = snapshot.capture_manifest(str(repo), include=["data/*"])

    assert "data/rows.csv" in _manifest_paths(m)
    assert "data/keys.txt" not in _manifest_paths(m)
    assert _skipped(m)["data/keys.txt"] == "secret"


def test_a_forced_lockfile_with_an_index_password_is_skipped(repo):
    (repo / ".gitignore").write_text("requirements.txt\n")
    (repo / "requirements.txt").write_text(
        "--extra-index-url https://deploy:" + "Zq8vT3mNpL" + "@pypi.example.com/simple\ntorch\n"
    )
    m = snapshot.capture_manifest(str(repo))
    assert "requirements.txt" not in _manifest_paths(m)
    assert _skipped(m)["requirements.txt"] == "secret"


def test_a_file_too_large_to_scan_is_referenced_never_copied(repo, monkeypatch):
    monkeypatch.setattr(_snap_mod, "CONTENT_SCAN_MAX_BYTES", 1024)
    (repo / "big.txt").write_text("x" * 4096)
    m = snapshot.capture_manifest(str(repo))
    entry = next(e for e in m["entries"] if e["path"] == "big.txt")
    assert entry["source"] == "reference", "unscanned bytes must never be classified for upload"
    assert entry["sha256"] == _sha(repo / "big.txt")


def test_a_plain_token_inside_binary_bytes_is_caught(repo):
    """Bytes that are not UTF-8 (a pickled config, a stored zip member) are read
    through a one-char-per-byte view, so a plainly written token still shows."""
    import pickle

    (repo / "state.pkl").write_bytes(
        b"\xff\xfe" + pickle.dumps({"lr": 3e-4, "hub_token": HF_TOKEN, "blob": bytes(range(256))})
    )
    (repo / "weights.bin").write_bytes(bytes(range(256)) * 64)

    m = snapshot.capture_manifest(str(repo))

    assert "state.pkl" not in _manifest_paths(m)
    assert _skipped(m)["state.pkl"] == "secret"
    assert "weights.bin" in _manifest_paths(m), "binary bytes with no token are captured"


def test_upload_disabled_scans_nothing_and_a_budget_bounds_the_scan(repo, monkeypatch):
    """The scan is paid only for bytes that could leave, and never past the
    upload cap: a tree over it is refused before anything is scanned past it."""
    _write_scratch(repo / "scratch.py")
    calls = []
    real = _snap_mod.credential_rules
    monkeypatch.setattr(
        _snap_mod, "credential_rules", lambda raw, name, **kw: calls.append(name) or real(raw, name, **kw)
    )

    m = snapshot.capture_manifest(str(repo), scan=False)
    assert "scratch.py" in _manifest_paths(m) and calls == [], "scan=False scans nothing"

    (repo / "big.txt").write_text("y" * 5000)
    with pytest.raises(snapshot.SnapshotError, match="over the cap"):
        _snap_mod.capture_manifest(str(repo), scan_budget_bytes=1000)


@pytest.mark.parametrize("git", [True, False], ids=["git", "no-git"])
def test_an_include_cannot_bring_back_a_skipped_file(tmp_path, git):
    """Before 0.5 a non-git include re-added a name-filtered `.env` to the
    manifest; now anything already skipped stays skipped, reported once."""
    root = tmp_path / "t"
    root.mkdir()
    (root / "train.py").write_text("print(1)\n")
    if git:
        _git(root, "init", "-q")
    (root / ".env").write_text("A=1\n")
    (root / "config.yaml").write_text(f"hf: {HF_TOKEN}\n")

    m = snapshot.capture_manifest(str(root), include=["*", ".env"])

    assert _manifest_paths(m) == {"train.py"}
    reported = [s["path"] for s in m["skipped"]]
    assert sorted(reported) == [".env", "config.yaml"], "one report per path"


# --- #2006 review: every finding, reproduced through the real Run.snapshot ----------
#
# Each test drives `Run.snapshot` against the fake server and reads EVERY byte
# the client sent (archives unpacked), so "not uploaded" means "not on the wire".

import base64  # noqa: E402
import gzip  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import tarfile  # noqa: E402
import urllib.parse  # noqa: E402

from tests.conftest import open_run  # noqa: E402

OPENAI_KEY = "sk-proj-" + "Zq7Xv2Lm9Pn4Rt6Wy8Ab1Cd3Ef5Gh7Jk9Lm2Np4Qr6St8Uv0"
WANDB_KEY = "3f9c2a7b1e8d4c6a" + "9b0e2f5d7a1c3e8b" + "4d6f0a2c"
COHERE_KEY = "Qx7Lm2Np9Rt4Wv6Yz8Ab1Cd3Ef5Gh7Jk9Ln2Mp4"
PASSWORD = "Hunter2" + "Qz9!vX4m"


def _sent(app) -> bytes:
    """Every body the client sent, with gzip archives expanded, as one blob."""
    out = []
    for request in app.requests:
        body = request.content or b""
        out.append(body)
        if body[:2] == b"\x1f\x8b":
            with gzip.open(io.BytesIO(body)) as gz, tarfile.open(fileobj=gz) as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        out.append(tar.extractfile(member).read())
    return b"\n".join(out)


def _snap_run(client, cwd, **kw):
    run = open_run(client, experiment="e", name="r")
    import warnings

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        snap = run.snapshot(cwd=str(cwd), include_env=False, include_gpu=False, **kw)
    return run, snap, [str(w.message) for w in caught if issubclass(w.category, UserWarning)]


def _plain(tmp_path, files: dict) -> "object":
    root = tmp_path / "plain"
    root.mkdir()
    for rel, data in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode())
    return root


# 1 CRITICAL -- a vendor token merged into an unquoted key-name hit was dropped.
@pytest.mark.parametrize(
    ("line", "secret"),
    [
        (f'URL = "https://huggingface.co/api/models/x?token={HF_TOKEN}&download=1"\n', HF_TOKEN),
        (f"# CI login: password: {GITHUB_TOKEN} (rotate monthly)\n", GITHUB_TOKEN),
        (f"# api_key: {OPENAI_KEY}+rw/prod (rotate)\n", OPENAI_KEY),
        (f"# token={GITHUB_TOKEN})\n", GITHUB_TOKEN),
        (f'CMD = "login --token={HF_TOKEN}/x"\n', HF_TOKEN),
    ],
    ids=["url-query", "comment-password", "comment-api-key", "comment-token-paren", "cli-flag"],
)
def test_review_1_a_vendor_token_inside_a_code_shaped_hit_is_never_uploaded(
    client, app, tmp_path, line, secret
):
    root = _plain(tmp_path, {"ok.py": "print(1)\n", "leak.py": "import os\n" + line})
    run, snap, _ = _snap_run(client, root)
    assert secret.encode() not in _sent(app)
    assert b"print(1)" in _sent(app), "the clean file still goes up"


# 2 HIGH -- credential folders inside a git repo.
def test_review_2_credential_folders_in_a_git_repo_are_never_uploaded(client, app, repo):
    files = {
        ".secrets/wandb": WANDB_KEY + "\n",
        "secrets/db.txt": "prod database, ask ops\n",
        ".aws/config": "[default]\nregion = us-west-2\n",
        ".ssh/config": "Host box\n  User me\n",
        ".docker/config.json": '{"auths": {}}\n',
    }
    for rel, text in files.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    run, snap, _ = _snap_run(client, repo, include=["secrets/*"])
    sent = _sent(app)
    for text in files.values():
        assert text.encode() not in sent
    reasons = {s["path"]: s["reason"] for s in snap["manifest"]["skipped"]}
    for rel in files:
        assert reasons.get(rel) == "secret", (rel, reasons)


# 3 HIGH -- unquoted keys in comments, docstrings and notebooks.
@pytest.mark.parametrize(
    ("name", "text", "secret"),
    [
        ("a.py", f"# api_key={GENERIC_KEY}\n", GENERIC_KEY),
        ("b.py", f'"""Staging login.\n\npassword: {PASSWORD}\n"""\n', PASSWORD),
        ("c.py", f"# aws_secret_access_key={AWS_SECRET}\n", AWS_SECRET),
        ("d.ipynb", json.dumps({"cells": [{"cell_type": "code", "source": [f"%env COHERE_API_KEY={COHERE_KEY}\n"]}]}), COHERE_KEY),
        ("e.ipynb", json.dumps({"cells": [{"cell_type": "code", "outputs": [{"text": [f"password: {PASSWORD}\n"]}]}]}), PASSWORD),
    ],
    ids=["comment-hex", "docstring-password", "comment-aws", "notebook-env", "notebook-output"],
)
def test_review_3_unquoted_keys_in_source_are_caught(client, app, tmp_path, name, text, secret):
    root = _plain(tmp_path, {"ok.py": "print(1)\n", name: text})
    _snap_run(client, root)
    assert secret.encode() not in _sent(app)


def test_review_3_code_that_only_names_tokens_is_still_uploaded(client, app, tmp_path):
    code = (
        "import contextvars, getpass\n"
        "token = tokens[0]\n"
        "password = getpass.getpass()\n"
        "_token: contextvars.Token | None = None\n"
        "def f(user, pw):\n    return connect(user, password=pw, token=token)\n"
    )
    root = _plain(tmp_path, {"train.py": code})
    run, snap, _ = _snap_run(client, root)
    assert code.encode() in _sent(app)
    assert not snap["manifest"]["skipped"]


# 4 MED-HIGH -- encoded and UTF-16 credentials.
@pytest.mark.parametrize(
    ("name", "data", "secret"),
    [
        ("b64.yaml", f"blob: {base64.b64encode(GITHUB_TOKEN.encode()).decode()}\n", base64.b64encode(GITHUB_TOKEN.encode())),
        ("esc.json", '{"x": "' + "".join(f"\\u{ord(c):04x}" for c in GITHUB_TOKEN) + '"}', "".join(f"\\u{ord(c):04x}" for c in GITHUB_TOKEN).encode()),
        ("url.txt", "u=" + urllib.parse.quote(f"https://h/?t={GITHUB_TOKEN}", safe="") + "\n", urllib.parse.quote(GITHUB_TOKEN, safe="").encode()),
        ("u16.txt", ("﻿key " + GITHUB_TOKEN + "\n").encode("utf-16-le"), GITHUB_TOKEN.encode("utf-16-le")),
    ],
    ids=["base64", "unicode-escape", "url-encoded", "utf16-bom"],
)
def test_review_4_encoded_credentials_in_small_files_are_caught(client, app, tmp_path, name, data, secret):
    root = _plain(tmp_path, {"ok.py": "print(1)\n", name: data})
    _snap_run(client, root)
    assert secret not in _sent(app)


def test_review_4_pgpass_and_docker_config_are_withheld_by_name(client, app, tmp_path):
    root = _plain(tmp_path, {"ok.py": "print(1)\n", ".pgpass": f"db:5432:*:me:{PASSWORD}\n"})
    run, snap, _ = _snap_run(client, root)
    assert PASSWORD.encode() not in _sent(app)


# 5 MED -- tracked files lose only exact/suffix/prefix names, and it is said.
def test_review_5_tracked_code_named_like_secrets_is_captured(client, app, repo):
    tracked = {
        "tap_core/secrets.py": "RULES = []\n",
        "scripts/deploy/sync-secrets.sh": "echo sync\n",
        ".env.example": "API_URL=https://example.invalid\n",
        "lib/_native.so": "\x7fELF-not-really\n",
    }
    for rel, text in tracked.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    (repo / ".env").write_text("A=1\n")
    _git(repo, "add", "-f", *tracked, ".env")
    _git(repo, "commit", "-q", "-m", "tracked")
    run, snap, warned = _snap_run(client, repo)
    sent = _sent(app)
    for text in tracked.values():
        assert text.encode() in sent, text
    assert b"A=1" not in sent, "an exact credential NAME still stops a tracked file"
    assert any(".env" in w and "tracked" in w for w in warned), warned


# 6 MED -- a withheld file stays in the record, so identity never depends on it being left out.
def test_review_6_a_withheld_file_stays_in_the_record(client, app, tmp_path):
    root = _plain(tmp_path, {"train.py": "print(1)\n", "cfg.yaml": f"hf: {HF_TOKEN}\n"})
    run, snap, _ = _snap_run(client, root)
    entry = next(e for e in snap["manifest"]["entries"] if e["path"] == "cfg.yaml")
    assert entry["source"] == "withheld" and entry["reason"] == "secret"
    assert entry["size"] == (root / "cfg.yaml").stat().st_size
    assert "sha256" not in entry, "a small secret's hash could be guessed offline"
    assert HF_TOKEN.encode() not in _sent(app)
    # Same tree, upload off: same identity.
    _, again, _ = _snap_run(client, root, upload=False)
    assert again["manifest"]["tree_sha256"] == snap["manifest"]["tree_sha256"]
    assert again["content_hash"] == snap["content_hash"]
    # A different secret of a different size is a different tree.
    (root / "cfg.yaml").write_text(f"hf: {HF_TOKEN}\nextra: 1\n")
    _, changed, _ = _snap_run(client, root)
    assert changed["manifest"]["tree_sha256"] != snap["manifest"]["tree_sha256"]


# 7 MED -- a big file is scanned in bounded memory, and a huge non-source one is
# recorded where it lives instead of scanned at start-up.
def test_review_7_a_big_file_is_scanned_without_copying_it_whole(tmp_path):
    import tracemalloc

    root = tmp_path / "big"
    root.mkdir()
    line = b"step 1 loss=0.25 lr=0.0003 grad_norm=1.5\n"
    (root / "train.log").write_bytes(line * (12 * 1024 * 1024 // len(line)))
    tracemalloc.start()
    try:
        m = snapshot.capture_manifest(str(root))
        peak = tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()
    assert m["entries"][0]["source"] == "blob"
    assert peak < 16 * 1024 * 1024, f"peak {peak / 1e6:.0f} MB scanning a 12 MB file"


# The time budget that replaced a size cap (capture stays broad: every file up to
# 64 MiB is scanned; only a scan that cannot finish in time withholds a file).
def _csv(path, mb: int) -> bytes:
    row = b"3,0.2500,0.5000,17,train\n"
    data = b"step,loss,acc,epoch,split\n" + row * (mb * 1024 * 1024 // len(row))
    path.write_bytes(data)
    return data


def _tokens_log(path, mb: int) -> bytes:
    line = b"step 1200 | loss 2.3125 | tokens/s 45210 | token_budget ok | lr 3e-4\n"
    data = line * (mb * 1024 * 1024 // len(line))
    path.write_bytes(data)
    return data


def test_budget_a_20mb_csv_is_scanned_and_uploaded(client, app, tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    data = _csv(root / "metrics.csv", 20)
    run, snap, _ = _snap_run(client, root)
    entry = snap["manifest"]["entries"][0]
    assert entry["source"] == "blob", entry
    assert data in _sent(app), "the whole CSV went up, byte for byte"
    assert snap["code_bytes"]["pending_upload"] == 0


def test_budget_a_pathological_tokens_log_is_withheld_not_uploaded(client, app, tmp_path, monkeypatch):
    # 60 MB of keyword-dense text scans at ~4 MB/s here (~15 s); a 1 s budget
    # keeps the test fast and holds on any machine under 60 MB/s.
    monkeypatch.setenv("PROBE_SNAPSHOT_FILE_SCAN_BUDGET_SEC", "1")
    root = tmp_path / "plain"
    root.mkdir()
    (root / "train.py").write_text("print('train')\n")
    _tokens_log(root / "train.log", 60)
    run, snap, warned = _snap_run(client, root)
    entry = next(e for e in snap["manifest"]["entries"] if e["path"] == "train.log")
    assert entry["source"] == "withheld" and entry["reason"] == "scan_budget"
    assert entry["sha256"] == _sha(root / "train.log"), "a big withheld file keeps its identity"
    sent = _sent(app)
    assert b"tokens/s 45210" not in sent, "no byte of an unscanned file is uploaded"
    assert b"print('train')" in sent
    skip = next(s for s in snap["manifest"]["skipped"] if s["path"] == "train.log")
    assert skip["reason"] == "scan_budget" and skip["found_in"] == "scan_time"
    assert any("1 file(s) whose credential scan" in w and "PROBE_SNAPSHOT_SCAN_BUDGET_SEC" in w for w in warned), warned


def test_budget_the_snapshot_total_holds(tmp_path, monkeypatch):
    """Once the snapshot's budget is spent, large non-source files are withheld
    without being read by the scanner; small and source files still are."""
    import time as _time

    monkeypatch.setenv("PROBE_SNAPSHOT_SCAN_BUDGET_SEC", "0.3")
    root = tmp_path / "plain"
    root.mkdir()
    for i in range(4):
        _tokens_log(root / f"run{i}.log", 6)
    (root / "small.txt").write_text("tokens/s 1\n" * 100)
    (root / "train.py").write_text("print('train')\n")
    started = _time.monotonic()
    m = snapshot.capture_manifest(str(root))
    elapsed = _time.monotonic() - started
    by_path = {e["path"]: e for e in m["entries"]}
    assert {p for p, e in by_path.items() if e.get("reason") == "scan_budget"} == {
        f"run{i}.log" for i in range(4)
    }
    assert by_path["small.txt"]["source"] == "blob" and by_path["train.py"]["source"] == "blob"
    # 0.3 s of scanning plus at most one chunk past it, and hashing 24 MB.
    assert elapsed < 3.0, f"{elapsed:.1f}s"


@pytest.mark.parametrize("budget", ["0.05", None], ids=["tiny-budget", "default-budget"])
def test_budget_holds_for_a_small_file_too(client, app, tmp_path, monkeypatch, budget):
    """A file up to FULL_SCAN_MAX_BYTES used to be scanned with no clock at all
    (#2034 re-review). Past its budget it is withheld, never uploaded unscanned;
    with the default budget the same clean file goes up (the control)."""
    if budget is not None:
        monkeypatch.setenv("PROBE_SNAPSHOT_FILE_SCAN_BUDGET_SEC", budget)
    root = tmp_path / "plain"
    root.mkdir()
    (root / "train.py").write_text("print('train')\n")
    _tokens_log(root / "train.log", 1)  # keyword-dense, clean, under 2 MiB
    run, snap, warned = _snap_run(client, root)
    entry = next(e for e in snap["manifest"]["entries"] if e["path"] == "train.log")
    sent = _sent(app)
    if budget is None:
        assert entry["source"] == "blob" and b"tokens/s 45210" in sent, entry
        return
    assert entry["source"] == "withheld" and entry["reason"] == "scan_budget", entry
    assert b"tokens/s 45210" not in sent, "no byte of an unscanned file is uploaded"
    skip = next(s for s in snap["manifest"]["skipped"] if s["path"] == "train.log")
    assert skip["reason"] == "scan_budget" and skip["found_in"] == "scan_time"
    assert any("1 file(s) whose credential scan" in w for w in warned), warned


#: One long line, read whole (#2034 re-review): each key-name hit's verdict
#: read the whole line around it. Before: 24 s, over 150 s, 27 s and over
#: 150 s here (the reviewer measured 37 s and 550 s); now 0.2-1.4 s. The
#: ceiling leaves room for a slow CI machine; the verdict is checked too.
LONG_LINES = {
    "camel-comma-2mb": ("x.json", "dbPassword=a8Kd93jLm2Qx,", 2_000_000, ()),
    "vendor-key-1mb": ("x.yaml", "azure_openai_key=abcdef0123456789ABCDEFgh ", 1_000_000, ("anchored-secret",)),
    "minified-json-200kb": ("hosts.min.json", '{"host":"db1","password":"Kx81mQp0Lz7R"},', 200_000, ("anchored-secret",)),
    "code-in-one-line-1mb": ("gen.py", "token = tokens[0]; ", 1_000_000, ()),
}


@pytest.mark.parametrize("case", list(LONG_LINES))
def test_one_long_line_is_scanned_in_linear_time(case):
    name, unit, size, expected = LONG_LINES[case]
    raw = (unit * (size // len(unit) + 1))[:size].encode()
    started = time.perf_counter()
    rules = _snap_mod.credential_rules(raw, name)
    elapsed = time.perf_counter() - started
    assert rules == expected
    assert elapsed < 10.0, f"{case}: {elapsed:.1f}s"


def test_budget_env_zero_means_no_limit(monkeypatch):
    monkeypatch.setenv("PROBE_SNAPSHOT_FILE_SCAN_BUDGET_SEC", "0")
    monkeypatch.setenv("PROBE_SNAPSHOT_SCAN_BUDGET_SEC", "nonsense")
    gate = _snap_mod._ContentGate()
    assert gate.file_budget == float("inf")
    assert gate.total_budget == _snap_mod.SNAPSHOT_SCAN_BUDGET_SEC


# 8 LOW -- `scan` is its own switch.
def test_review_8_scan_is_an_explicit_switch(repo, monkeypatch):
    _write_scratch(repo / "scratch.py")
    calls = []
    real = _snap_mod.credential_rules
    monkeypatch.setattr(_snap_mod, "credential_rules", lambda *a, **k: calls.append(1) or real(*a, **k))
    m = snapshot.capture_manifest(str(repo), scan=False)
    assert calls == [] and "scratch.py" in _manifest_paths(m)


# --- #2006 security re-review: every shape, every mode, both storages -------------
#
# The reviewer's leak matrix, kept: each shape is written into a project in four
# ways (plain folder, untracked in git, tracked in git, gitignored and named by
# `include=`), snapshotted under both code storages, and every byte sent is
# searched for the secret. A clean control file must still go up.

import tarfile as _tarfile  # noqa: E402
import zipfile as _zipfile  # noqa: E402

TRUB = "Tr0ub4" + "dor&3xQ"
ALNUM_PW = "a8Kd93" + "jLm2Qx"
ALNUM_PW2 = "S3cr3t" + "Passw0rd"
HEX_PW = "e3b0c442" + "98fc1c14"
HEX32 = "5e8a1c9f3b7d2e4a" + "6c0f9b1d3e5a7c2f"
HEX40 = HEX32 + "8d4b6e1a"
FERNETISH = "Qh8zK3mN7pR2tV5wY9bC4dF6gJ1kL0" + "sX8uA3eB7A="
# Repeated so the compressed bytes cannot carry the token verbatim by chance.
ENV_BYTES = f"GITHUB_TOKEN={GITHUB_TOKEN}\nHF_TOKEN={HF_TOKEN}\n".encode() * 50


def _tgz(member: str, data: bytes) -> bytes:
    buf = io.BytesIO()
    with _tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = _tarfile.TarInfo(member)
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def _zip(member: str, data: bytes, method=_zipfile.ZIP_DEFLATED) -> bytes:
    buf = io.BytesIO()
    with _zipfile.ZipFile(buf, "w", method) as zf:
        zf.writestr(member, data)
    return buf.getvalue()


_BIG_CODE = b"x = compute(alpha, beta)  # ordinary code line\n" * 46000  # > 2 MiB


def _notebook(*code: str, output: str = "") -> str:
    """An nbformat-4 notebook with one code cell, as Jupyter writes it (its JSON
    escapes every `"` of the cell), and an image output of ``output`` if given."""
    outputs = [{"output_type": "display_data", "metadata": {}, "data": {"image/png": output}}] if output else []
    cell = {"cell_type": "code", "execution_count": 1, "metadata": {}, "outputs": outputs,
            "source": [line + "\n" for line in code]}
    return json.dumps({"cells": [cell], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}, indent=1)


#: A plot's worth of base64: makes a notebook bigger than the 2 MiB full scan.
_BIG_PNG = base64.b64encode(bytes(range(256)) * 10_000).decode()

SHAPES = {
    # H1: only the value's first word decides; the rest of the line is not code.
    "pw-comment-paren": ("app/settings.py", f"import os\n# password: {TRUB} (rotate monthly)\n", TRUB),
    "pw-comment-sentence": ("app/settings.py", f"# staging db password: {TRUB}. Ask ops for prod.\n", TRUB),
    "yaml-in-docstring": ("deploy.py", f'"""Notes.\n\ndb:\n  password: {TRUB}  # prod db (see wiki)\n"""\n', TRUB),
    "api-key-period": ("client.py", f"# api_key: {HEX32}.\nimport requests\n", HEX32),
    "url-query": ("client.py", f'URL = "https://api.example.com/v1/export?api_key={HEX32}&format=csv.gz"\n', HEX32),
    "hash-prefixed-pw": ("a.py", f"# password: #{TRUB}\n", TRUB),
    "pw-then-call": ("a.py", f"# password: {TRUB}.strip()\n", TRUB),
    # M1: base64 padding is not an operator; a lone word used once is not a name.
    "b64-padding": ("settings.py", f"# secret_key={FERNETISH}\n", FERNETISH),
    "letters-only-pw": ("a.py", "# password: correcthorse" + "batterystaple\n", "correcthorse" + "batterystaple"),
    # H2: typed settings fields.
    "annotated-attr": ("config.py", f'class Settings:\n    password: str = "{TRUB}"\n', TRUB),
    "final": ("config.py", f'from typing import Final\nDB_PASSWORD: Final[str] = "{TRUB}"\n', TRUB),
    "dataclass-field": ("config.py", f'@dataclass\nclass C:\n    password: str = field(default="{TRUB}")\n', TRUB),
    # M2: credential file names.
    "netrc-underscore": ("_netrc", f"machine api.wandb.ai\n  login u\n  password {HEX40}\n", HEX40),
    "pgpass-conf": ("pgpass.conf", f"db:5432:*:app:{TRUB}\n", TRUB),
    "envrc": (".envrc", f"export AZURE_OPENAI_KEY={HEX32}\n", HEX32),
    "dot-env-dash": (".env-prod", f"AZURE_OPENAI_KEY={HEX32}\n", HEX32),
    "star-env": ("prod.env", f"AZURE_OPENAI_KEY={HEX32}\n", HEX32),
    # M4: compressed archives are opened.
    "tar-gz-env": ("backup.tar.gz", _tgz(".env", ENV_BYTES), GITHUB_TOKEN),
    "zip-deflated-env": ("configs.zip", _zip(".env", ENV_BYTES), GITHUB_TOKEN),
    "plain-gz": ("env.gz", gzip.compress(ENV_BYTES), GITHUB_TOKEN),
    # M7 / L1: UTF-16 without a byte-order mark, and above 2 MiB.
    "utf16-no-bom": ("setup.ps1", f'$env:GITHUB_TOKEN = "{GITHUB_TOKEN}"\n'.encode("utf-16-le"), GITHUB_TOKEN.encode("utf-16-le")),
    "utf16-bom-3mib": ("logs/ps.txt", ("\ufeff" + "hello world line\n" * 120000 + f"key {GITHUB_TOKEN}\n").encode("utf-16"), GITHUB_TOKEN.encode("utf-16-le")),
    # H1 in a file above 2 MiB (the chunked scan applies the same rules).
    "pw-comment-big-file": ("gen/big.py", _BIG_CODE + f"# password: {TRUB} (rotate monthly)\n".encode(), TRUB),
    # The scanner-rule follow-up (#2000): shapes the shared scanner's rules did
    # not see until `tap_core/secrets.py` learned them.
    "camelcase-key (H3)": ("web/client.ts", f'const openaiApiKey = "{HEX32}";\n', HEX32),
    "camelcase-helm (H3)": ("deploy/values.yaml", f"postgresql:\n  auth:\n    postgresPassword: {TRUB}\n", TRUB),
    "fstring-prefix (M3)": ("client.py", f'API_KEY = f"{HEX32}"\n', HEX32),
    "environ-setdefault (M3)": ("train.py", f'os.environ.setdefault("WANDB_API_KEY", "{HEX40}")\n', HEX40),
    "star-key-env-example (M2)": (".env.example", f"AZURE_OPENAI_KEY={HEX32}\n", HEX32),
    "star-key-env-production (M2)": ("env.production", f"AZURE_OPENAI_KEY={HEX32}\n", HEX32),
    "yaml-wandb-key (M2)": ("conf/config.yaml", f"wandb:\n  project: foo\n  key: {HEX40}\n", HEX40),
    "netrc-line (M5)": ("deploy/netrc.txt", f"machine api.wandb.ai\n  login user\n  password {HEX40}\n", HEX40),
    "maven-password (M5)": ("settings.xml", f"<server><id>r</id><password>{TRUB}</password></server>\n", TRUB),
    "docker-auth (M5)": ("ci/config.json", '{"auths": {"r.io": {"auth": "' + base64.b64encode(f"me:{TRUB}".encode()).decode() + '"}}}\n', base64.b64encode(f"me:{TRUB}".encode())),
    "long-uri-password (M6)": ("db.py", 'URL = "postgresql://app:' + "Zq7" * 24 + '@db:5432/app"\n', "Zq7" * 24),
    # The #2000 security review: letters-and-digits passwords under camelCase
    # keys (HIGH-1; `TRUB`'s `&` had hidden it), and the MED-1 shapes.
    "camel-helm-alnum (review H1)": ("deploy/values.yaml", f"postgresql:\n  auth:\n    postgresPassword: {ALNUM_PW}\n", ALNUM_PW),
    "camel-ts-quoted-alnum (review H1)": ("web/db.ts", f'const dbPassword = "{ALNUM_PW2}";\n', ALNUM_PW2),
    "camel-gradle-alnum (review H1)": ("gradle.properties", f"mavenPassword={ALNUM_PW}\n", ALNUM_PW),
    "camel-helm-hex (review H1)": ("deploy/values.yaml", f"redis:\n  auth:\n    redisPassword: {HEX_PW}\n", HEX_PW),
    "getenv-default-keyword (review M1)": ("train.py", f'import os\nkey = os.getenv("WANDB_API_KEY", default="{HEX40}")\n', HEX40),
    "lower-vendor-key (review M1)": ("conf/config.yaml", f"model:\n  azure_openai_key: {HEX32}\n", HEX32),
    "wandb-key-yaml (review M1)": ("conf/config.yaml", f"logging:\n  wandb_key: {HEX40}\n", HEX40),
    "argparse-default (review M1)": ("train.py", f'import argparse\np = argparse.ArgumentParser()\np.add_argument("--wandb-api-key", default="{HEX40}")\n', HEX40),
    "k8s-env-pair (review M1)": ("deploy/job.yaml", f"env:\n- name: AZURE_OPENAI_KEY\n  value: {HEX32}\n", HEX32),
    "camel-short-secret (review M1)": ("web/config.ts", f'export const jwtSecret = "{TRUB}";\n', TRUB),
    "camel-vendor-key (review M1)": ("web/client.ts", f'const openaiKey = "{HEX32}";\n', HEX32),
    "js-env-fallback (review M1)": ("web/client.js", f'const key = process.env.AZURE_OPENAI_KEY || "{HEX32}";\n', HEX32),
    "acronym-password (review M1)": ("appsettings.json", f'{{"ConnectionStrings": {{}}, "DBPassword": "{TRUB}"}}\n', TRUB),
    "typed-field-default (review M1)": ("settings.py", f'class S:\n    api_key: str = Field(default="{HEX32}")\n', HEX32),
    # The #2034 re-review. A notebook's JSON escapes each `"` in a cell, which
    # hid every quoted literal (on main too); its code cells are now read as
    # Python, a big notebook's included. And a `*_KEY` name ending in `API_KEY`
    # lost its anchor to the new `*_KEY` rule (caught on main).
    "notebook-api-key (re-review)": ("notebooks/explore.ipynb", _notebook(f'OPENAI_API_KEY = "{HEX32}"'), HEX32),
    "notebook-wandb-login (re-review)": ("notebooks/train.ipynb", _notebook("import wandb", f'wandb.login(key="{HEX40}")'), HEX40),
    "notebook-big-api-key (re-review)": ("notebooks/plots.ipynb", _notebook(f'OPENAI_API_KEY = "{HEX32}"', "plot(x)", output=_BIG_PNG), HEX32),
    "star-key-letters (re-review)": ("client.py", 'OPENAI_API_KEY = "abcdefghijklmnopqrstuvwxyzabcdef"\n', "abcdefghijklmnopqrstuvwxyzabcdef"),
}

# Named residual, documented: decoding (base64, escapes) runs only up to the
# 2 MiB full-scan size, so a base64-wrapped token in a bigger file still goes
# up. strict: if a change ever catches it, this flips and the docs must too.
RESIDUAL_SHAPES = {
    "base64-above-2mib (decoding)": ("gen/big2.py", _BIG_CODE + f"BLOB = '{base64.b64encode(GITHUB_TOKEN.encode()).decode()}'\n".encode(), base64.b64encode(GITHUB_TOKEN.encode())),
}

MODES = ["nongit", "git-untracked", "git-tracked", "git-ignored+include"]


def _shape_run(client, app, tmp_path, monkeypatch, rel, content, mode, storage):
    from probe.sdk import run as run_mod

    monkeypatch.setenv(run_mod.CODE_STORAGE_ENV, storage)
    root = tmp_path / "proj"
    root.mkdir()
    (root / "main.py").write_text("print('clean marker 2006')\n")
    include = None
    if mode != "nongit":
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "t@example.com")
        _git(root, "config", "user.name", "t")
    if mode == "git-ignored+include":
        (root / ".gitignore").write_text(rel + "\n")
        include = [rel]
    if mode.startswith("git"):
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "init")
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content if isinstance(content, bytes) else content.encode())
    if mode == "git-tracked":
        _git(root, "add", "-f", rel)
        _git(root, "commit", "-q", "-m", "add")
    run, snap, _ = _snap_run(client, root, include=include)
    return snap, _sent(app)


@pytest.mark.parametrize("storage", ["artifacts", "archive"])
@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("shape", list(SHAPES))
def test_rereview_no_shape_reaches_the_wire(client, app, tmp_path, monkeypatch, shape, mode, storage):
    rel, content, secret = SHAPES[shape]
    snap, sent = _shape_run(client, app, tmp_path, monkeypatch, rel, content, mode, storage)
    assert b"clean marker 2006" in sent, "control: the clean file must go up"
    secret = secret if isinstance(secret, bytes) else secret.encode()
    raw = content if isinstance(content, bytes) else content.encode()
    assert secret not in sent, f"{shape} leaked ({mode}/{storage})"
    # A compressed file's secret is not visible in its bytes: the FILE itself
    # must not have gone up (the byte check alone is vacuous for archives).
    assert raw not in sent, f"{shape}: the file itself was uploaded ({mode}/{storage})"
    entry = next((e for e in snap["manifest"]["entries"] if e["path"] == rel), None)
    assert entry is None or entry["source"] != "blob", entry


@pytest.mark.parametrize("shape", list(RESIDUAL_SHAPES))
@pytest.mark.xfail(strict=True, reason="documented residual: no decoding above the 2 MiB full-scan size")
def test_rereview_named_residuals_still_leak(client, app, tmp_path, monkeypatch, shape):
    rel, content, secret = RESIDUAL_SHAPES[shape]
    snap, sent = _shape_run(client, app, tmp_path, monkeypatch, rel, content, "nongit", "artifacts")
    secret = secret if isinstance(secret, bytes) else secret.encode()
    assert secret not in sent


# False positives the rules must not have: each would withhold real code whole.
BENIGN = [
    ("db.py", 'DSN = f"postgresql://{user}:{password}@{host}:5432/{db}"\n'),
    ("clone.py", 'url = f"https://x-access-token:{token}@github.com/{repo}.git"\n'),
    ("train.py", 'p.add_argument("--token", help="Hugging Face token")\n'),
    ("train.py", 'p.add_argument("--hf_token", type=str, default=None, help="HF access token")\n'),
    ("q.py", 'SQL = "UPDATE t SET used = true WHERE lease_token = $2::uuid"\n'),
    ("Page.tsx", "<Foo refreshToken={workReloadCounter} />\n"),
    ("a.py", "from x import token_fingerprint  # noqa: PLC0415\n"),
    ("conf.yaml", "auth:\n  token:\n    header: X-Api\n"),
    ("a.py", '"""Connect with postgresql://user:password@localhost/db."""\n'),
    ("a.py", '"""Clone https://x-access-token:<TOKEN>@github.com/org/repo."""\n'),
    ("a.py", "# the refresh_token and `expires_at <= now+1h` decide it\n"),
    ("a.py", "def login(user: str, password: str | None = None) -> Token: ...\n"),
    ("a.py", "password: SecretStr = Field(default=None, description='db password')\n"),
    ("a.py", "token = tokens[0]\npassword = getpass.getpass()\n"),
    ("a.py", "def f(user, pw):\n    return connect(user, password=pw)\n"),
    ("a.py", "tokenizer.pad_token = tokenizer.eos_token\n"),
    ("compose.yml", "environment:\n  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}\n"),
    # The #2000 security review's false positives (MED-2, HIGH-2).
    ("rows.jsonl", ('{"source":"https://huggingface.co","id":"a1b2c3","n_tokens":123456,"label":"positive",'
                    '"split":"train","annotator":"worker-17","score":0.9321,"created":"2026-09-01T12:00:00Z",'
                    '"reviewer":"alice@lab.org"}\n') * 3),
    ("settings-template.xml", "<settings><servers><server><id>central</id><username>{user}</username>"
                              "<password>{password}</password></server></servers></settings>\n"),
    ("README.md", "Set it in `~/.m2/settings.xml` as `<password>...</password>`.\n"),
    ("client_messages.py", "class Db:\n    adminPassword = _messages.StringField(1)\n    sslKeyPassword = _messages.StringField(7)\n"),
    ("notes.txt", 'cfg.get("secret_name", "prod-db-2")\n'),
    ("ci-netrc.sh", 'printf "machine github.com login ci password $GH_TOKEN\\n" > ~/.netrc\n'),
    ("claims.py", 'self.setdefault("id_token_encrypted_response_enc", "A128CBC-HS256")\n'),
    ("examples-1.json", '{"ClientRequestToken": "a8f5f167-f44f-4964-a6c9-8f1b2d3e4a5b", "NextToken": "CpHNsscimcV5oH7bSbub03CI2Qms5+ypNpNm"}\n'),
    ("helpers.py", 'WS_KEY: Final[bytes] = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"\n'),
    # The #2034 re-review's: UI labels under camelCase keys, names of secret
    # OBJECTS, netrc words in prose, lower-case variables, and notebook code.
    ("en.json", '{\n  "forgotPassword": "Forgot password?",\n  "confirmPassword": "Confirm password",\n  "email": "Email"\n}\n'),
    ("labels.ts", 'export const labels = {\n  newPassword: "New password",\n  email: "Email",\n};\n'),
    ("de.json", '{"forgotPassword": "Passwort vergessen?"}\n'),
    ("Form.tsx", 'const errors = { confirmPassword: "Must match!" };\n'),
    ("Main.java", 'String newPassword = "n/a";\n'),
    ("values.yaml", "auth:\n  existingSecret: pg-auth-v2\nglobal:\n  imagePullSecret: regcred-v1\n"),
    ("notes.md", "Use the machine gpu01 password reset flow.\n"),
    ("build.gradle", 'credentials {\n  username "$mavenUser"\n  password "$mavenPassword"\n}\n'),
    ("ci.sh", 'echo "machine github.com login x password $github_token" > ~/.netrc\n'),
    ("explore.ipynb", _notebook('token = tokenizer(text)["input_ids"]', 'api_key = os.environ["OPENAI_API_KEY"]',
                                "secret = cfg.secret", 'print("set api_key first")')),
    ("plots.ipynb", _notebook("plot(x)", output=_BIG_PNG)),
    # The two archives stay LAST: `test_rereview_benign_archives_are_captured` reads BENIGN[-2:].
    ("metrics.zip", _zip("metrics.csv", b"step,loss\n" + b"1,0.5\n" * 1000)),
    ("model.pt", _zip("archive/data.pkl", b"\x80\x04weights" * 100, _zipfile.ZIP_STORED)),
]


@pytest.mark.parametrize(("name", "content"), BENIGN, ids=[f"{n}-{i}" for i, (n, _) in enumerate(BENIGN)])
def test_rereview_benign_code_is_not_withheld(name, content):
    raw = content if isinstance(content, bytes) else content.encode()
    assert _snap_mod.credential_rules(raw, name) == ()


def test_rereview_benign_archives_are_captured(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    for name, content in BENIGN[-2:]:
        (root / name).write_bytes(content)
    m = snapshot.capture_manifest(str(root))
    assert {e["path"]: e["source"] for e in m["entries"]} == {"metrics.zip": "blob", "model.pt": "blob"}


def test_rereview_an_unreadable_archive_is_withheld_not_uploaded(client, app, tmp_path):
    root = _plain(tmp_path, {"ok.py": "print(1)\n", "broken.tar.gz": b"\x1f\x8b\x08\x00" + b"not deflate data" * 8})
    run, snap, _ = _snap_run(client, root)
    entry = next(e for e in snap["manifest"]["entries"] if e["path"] == "broken.tar.gz")
    assert entry["source"] == "withheld" and entry["reason"] == "uninspectable"


# L2: include= never reads through a link or out of the project.
def test_rereview_include_never_follows_a_link_out_of_the_project(client, app, tmp_path):
    outside = tmp_path / "shared-home"
    (outside / ".config" / "rclone").mkdir(parents=True)
    (outside / ".config" / "rclone" / "rclone.conf").write_text(f"[mirror]\nnote = key {HEX40}\n")
    (tmp_path / "wandb_key").write_text(HEX40 + "\n")
    root = tmp_path / "proj"
    root.mkdir()
    (root / "main.py").write_text("print('clean marker 2006')\n")
    os.symlink(outside, root / "ext")
    os.symlink(tmp_path / "wandb_key", root / "key.txt")
    run, snap, _ = _snap_run(client, root, include=["ext", "key.txt"])
    sent = _sent(app)
    assert HEX40.encode() not in sent
    reasons = {s["path"]: s["reason"] for s in snap["manifest"]["skipped"]}
    assert reasons.get("ext/.config/rclone/rclone.conf") == "outside_tree"
    link = next(e for e in snap["manifest"]["entries"] if e["path"] == "key.txt")
    assert link["mode"] == "120000" and link["symlink_target"] == str(tmp_path / "wandb_key")


# --- .probeignore (plan (n)) -------------------------------------------------------

_PAT = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"


def _ignore_tree(repo):
    (repo / "data").mkdir()
    for i in range(3):
        (repo / "data" / f"shard-{i}.csv").write_text("x,y\n")
    (repo / "run.ckpt").write_text("weights")
    (repo / "keep.ckpt").write_text("weights")
    (repo / "src").mkdir()
    (repo / "src" / "train.py").write_text("print('train')\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "tree")


def test_probeignore_excludes_tracked_and_untracked_paths(repo):
    from probe.sdk import ignore

    _ignore_tree(repo)
    (repo / ".probeignore").write_text("data/\n*.ckpt\n!keep.ckpt\n")
    (repo / "notes.scratch").write_text("untracked scratch")  # untracked, ignored below
    rules = ignore.load(str(repo), extra=["*.scratch"])
    m = snapshot.capture_manifest(str(repo), ignore=rules)
    paths = _manifest_paths(m)
    assert {"a.txt", "src/train.py", "keep.ckpt", ".probeignore"} <= paths
    assert not [p for p in paths if p.startswith("data/")] and "run.ckpt" not in paths
    skipped = _skipped(m)
    # One line for the directory, not one per file under it.
    assert skipped["data"] == "probeignore" and not [p for p in skipped if p.startswith("data/")]
    assert skipped["run.ckpt"] == "probeignore" and skipped["notes.scratch"] == "probeignore"
    # The identity changes with what is excluded, since the bytes are not there.
    assert m["tree_sha256"] != snapshot.capture_manifest(str(repo))["tree_sha256"]


def test_probeignore_applies_from_a_subdirectory(repo):
    from probe.sdk import ignore

    _ignore_tree(repo)
    (repo / ".probeignore").write_text("/src/train.py\n")
    sub = repo / "src"
    m = snapshot.capture_manifest(str(sub), ignore=ignore.load(str(sub)))
    assert "train.py" not in _manifest_paths(m) and _skipped(m)["train.py"] == "probeignore"


def test_probeignore_applies_through_a_symlinked_checkout(repo, tmp_path):
    """git reports its toplevel resolved; a run started through a link to the
    checkout (a symlinked workspace, macOS's /var -> /private/var) still
    matches the file's patterns."""
    from probe.sdk import ignore

    _ignore_tree(repo)
    (repo / ".probeignore").write_text("data/\n")
    link = tmp_path / "link"
    link.symlink_to(repo, target_is_directory=True)
    m = snapshot.capture_manifest(str(link), ignore=ignore.load(str(link)))
    paths = _manifest_paths(m)
    assert "src/train.py" in paths and not [p for p in paths if p.startswith("data/")]
    assert _skipped(m)["data"] == "probeignore"


def test_probeignore_records_are_capped_with_an_exact_count(repo):
    """#2045 review LOW-3: `*.jsonl` over a results tree put one record per
    file into the code-snapshot's meta (6,667 records, 450 KB)."""
    from probe.sdk import ignore
    from probe.sdk.snapshot import PROBEIGNORE_REPORT_LIMIT

    for i in range(PROBEIGNORE_REPORT_LIMIT + 10):
        (repo / f"r{i:03d}.jsonl").write_text("{}\n")
    (repo / ".probeignore").write_text("*.jsonl\n")
    m = snapshot.capture_manifest(str(repo), ignore=ignore.load(str(repo)))
    listed = [s for s in m["skipped"] if s["reason"] == "probeignore"]
    assert len(listed) == PROBEIGNORE_REPORT_LIMIT
    assert m["n_probeignore"] == PROBEIGNORE_REPORT_LIMIT + 10
    assert "n_probeignore" not in snapshot.capture_manifest(str(repo)), "no rules, no key"


def test_probeignore_never_re_includes_a_safety_stop(repo):
    from probe.sdk import ignore

    (repo / ".env").write_text("OPENAI_API_KEY=sk-proj-" + "a" * 48 + "\n")
    (repo / "notes.txt").write_text(f"token {_PAT}\n")
    (repo / ".probeignore").write_text("!.env\n!notes.txt\n")
    m = snapshot.capture_manifest(str(repo), ignore=ignore.load(str(repo)))
    assert ".env" not in _manifest_paths(m) and _skipped(m)[".env"] != "probeignore"
    assert "notes.txt" in _withheld(m), "content gate still withholds it"


def test_an_explicit_include_wins_over_probeignore(repo):
    from probe.sdk import ignore

    _ignore_tree(repo)
    (repo / ".probeignore").write_text("data/\n")
    m = snapshot.capture_manifest(
        str(repo), include=["data/shard-1.csv"], ignore=ignore.load(str(repo))
    )
    paths = _manifest_paths(m)
    assert "data/shard-1.csv" in paths and "data/shard-0.csv" not in paths
    assert _skipped(m)["data"] == "probeignore"


def test_probeignore_keeps_a_forced_lockfile_out(repo):
    from probe.sdk import ignore

    (repo / ".gitignore").write_text("uv.lock\n")
    (repo / "uv.lock").write_text("version = 1\n")
    assert "uv.lock" in _manifest_paths(snapshot.capture_manifest(str(repo))), "forced in by default"
    (repo / ".probeignore").write_text("uv.lock\n")
    m = snapshot.capture_manifest(str(repo), ignore=ignore.load(str(repo)))
    assert "uv.lock" not in _manifest_paths(m) and _skipped(m)["uv.lock"] == "probeignore"


def test_run_snapshot_reads_the_probeignore_file(client, repo):
    _ignore_tree(repo)
    (repo / ".probeignore").write_text("data/\n")
    _run, snap, _warnings = _snap_run(client, repo)
    paths = {e["path"] for e in snap["manifest"]["entries"]}
    assert "src/train.py" in paths and not [p for p in paths if p.startswith("data/")]
    assert {"path": "data", "reason": "probeignore"} in snap["manifest"]["skipped"]


def test_client_run_ignore_reaches_the_auto_snapshot(client, repo, monkeypatch):
    _ignore_tree(repo)
    monkeypatch.chdir(repo)
    run = open_run(client, experiment="e-ign", snapshot=True, ignore=["data/", "*.ckpt"])
    row = next(a for a in client.run_bundle(run.id)["artifacts"] if a.get("kind") == "code_snapshot")
    listed = row["meta"]["paths_text"].split("\n")
    assert "src/train.py" in listed and "run.ckpt" not in listed
    assert not [p for p in listed if p.startswith("data/")]


def test_a_bad_ignore_argument_opens_no_run(client, app):
    from probe.sdk import errors

    before = len(app.runs)
    with pytest.raises(errors.ValidationError, match="ignore="):
        open_run(client, experiment="e-bad", ignore=[3])
    assert len(app.runs) == before
