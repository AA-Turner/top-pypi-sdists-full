"""`probe._shared.pins`: the copies an owner keeps of a package someone else
rewrites (the service's tap pins, the update's pi pins)."""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from probe._shared import pins


def _tree(root: Path, files: dict[str, str]) -> Path:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return root


def _clone(tmp_path: Path) -> Path:
    """A pi clone's layout: the package, a sibling plugin, node_modules with a
    `.bin` link inside it, and the root package.json."""
    clone = _tree(tmp_path / "clone", {
        "plugins/probe-research-pi/index.ts": "export default 1",
        "plugins/probe-research-tap/tap/main.py": "x = 1",
        "node_modules/@modelcontextprotocol/sdk/index.js": "module.exports = {}",
        "node_modules/@modelcontextprotocol/sdk/bin/cli.js": "#!/usr/bin/env node",
        "package.json": "{}",
    })
    (clone / "node_modules" / ".bin").mkdir()
    os.symlink("../@modelcontextprotocol/sdk/bin/cli.js", clone / "node_modules" / ".bin" / "mcp")
    return clone


def _sources(clone: Path) -> dict[str, Path]:
    return {rel: clone / rel for rel in
            ("plugins/probe-research-pi", "plugins/probe-research-tap", "node_modules", "package.json")}


def test_several_sources_land_at_their_paths_and_the_same_files_reuse_the_pin(tmp_path):
    clone = _clone(tmp_path)
    store = tmp_path / "pins"
    first = pins.make(store, "0.7.0", _sources(clone), default="pi", meta={"from": str(clone)}, symlinks=True)
    assert first.name.startswith("0.7.0-") and (first / pins.PIN_DONE).is_file()
    assert (first / "plugins/probe-research-pi/index.ts").read_text() == "export default 1"
    assert (first / "package.json").is_file()
    link = first / "node_modules" / ".bin" / "mcp"
    assert link.is_symlink() and link.resolve() == (first / "node_modules/@modelcontextprotocol/sdk/bin/cli.js")
    assert pins.make(store, "0.7.0", _sources(clone), default="pi", symlinks=True) == first, "same files: same pin"
    deref = pins.make(tmp_path / "deref", "0.7.0", _sources(clone), default="pi")
    assert not (deref / "node_modules" / ".bin" / "mcp").is_symlink(), "by default a link's target is copied (taps)"
    assert pins.complete(store, first.name) and not pins.complete(store, "../x") and not pins.complete(store, "")


def test_a_source_changed_while_copied_is_never_marked_done(tmp_path, monkeypatch):
    clone = _clone(tmp_path)
    store = tmp_path / "pins"
    real = pins.fingerprint
    calls = {"n": 0}

    def moving(sources, *, times=True):
        calls["n"] += 1
        if calls["n"] == 2:  # the second look, after the copy: the clone moved
            (clone / "package.json").write_text('{"changed": true}')
        return real(sources, times=times)

    monkeypatch.setattr(pins, "fingerprint", moving)
    with pytest.raises(OSError):
        pins.make(store, "0.7.0", _sources(clone), default="pi")
    assert not [p for p in store.iterdir() if (p / pins.PIN_DONE).exists()]
    assert not [p for p in store.iterdir() if p.name.startswith(".")], "no staging left behind"


def test_a_pin_cut_short_is_made_again(tmp_path):
    clone = _clone(tmp_path)
    store = tmp_path / "pins"
    pin = pins.make(store, "0.7.0", _sources(clone), default="pi")
    (pin / pins.PIN_DONE).unlink()
    (pin / "package.json").unlink()
    assert pins.make(store, "0.7.0", _sources(clone), default="pi") == pin
    assert (pin / pins.PIN_DONE).is_file() and (pin / "package.json").is_file()


def test_prune_keeps_what_live_processes_still_load_from(tmp_path):
    store = tmp_path / "pins"
    now = time.time()
    made = []
    for n in range(pins.PIN_KEEP + 3):
        folder = store / f"0.7.{n}-abc"
        (folder).mkdir(parents=True)
        (folder / pins.PIN_DONE).write_text("{}")
        os.utime(folder, (now - 1000 + n,) * 2)
        made.append(folder)
    staging = store / ".0.7.9-abc.123.4"
    staging.mkdir()
    os.utime(staging, (now - pins.STALE_STAGING_S - 1,) * 2)
    oldest, live = made[0], made[1]
    removed = pins.prune(store, keep={made[-1]}, referenced={live.name})
    left = sorted(p.name for p in store.iterdir())
    assert live.name in left, "a pin a live process loads from is never removed"
    assert oldest not in [p for p in store.iterdir()] and oldest in removed
    assert staging in removed and not staging.exists()
    assert made[-1].name in left


def test_a_pin_another_writer_published_meanwhile_is_kept(tmp_path, monkeypatch):
    """Codex review of the pi pins: two pi sessions starting at once each pin
    the package; the second never removes the first's pin (a shim may be
    importing it)."""
    clone = _clone(tmp_path)
    store = tmp_path / "pins"
    real = pins.fingerprint
    calls = {"n": 0}

    def other_writer_finishes(sources, *, times=True):
        calls["n"] += 1
        found = real(sources, times=times)
        if calls["n"] == 2:  # after our copy: the other writer published the same pin
            theirs = store / pins.pin_name("0.7.0", real(_sources(clone)), "pi")
            (theirs / "package.json").parent.mkdir(parents=True, exist_ok=True)
            (theirs / "package.json").write_text("{}")
            (theirs / "theirs").write_text("loading")
            (theirs / pins.PIN_DONE).write_text("{}")
        return found

    monkeypatch.setattr(pins, "fingerprint", other_writer_finishes)
    made = pins.make(store, "0.7.0", _sources(clone), default="pi")
    assert (made / "theirs").read_text() == "loading", "their published pin was not replaced"
    assert not [p for p in store.iterdir() if p.name.startswith(".") and p.is_dir()], "our copy was dropped"
    assert pins.prune(tmp_path / "missing") == [] and not (tmp_path / "missing").exists()
