"""tools/vendor.py makes every copy plugins/VENDORED.json lists, with cp / cp -p / cp -R semantics."""

from __future__ import annotations

import importlib.util
import json
import os
import re
from pathlib import Path

import pytest

from probe.foundation.skills import skills as skill_versions

AGENT = Path(__file__).resolve().parents[1]


def _vendor():
    spec = importlib.util.spec_from_file_location("_vendor_under_test", AGENT / "tools" / "vendor.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vendor = _vendor()


def _write(path: Path, text: str, mode: int | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if mode is not None:
        path.chmod(mode)
    return path


def _sync(root: Path, steps: list, lists: dict | None = None) -> None:
    manifest = {"lists": lists or {}, "groups": {"g": steps}}
    vendor.run(vendor.plan("g", root, manifest), root)


def _umask() -> int:
    mask = os.umask(0)
    os.umask(mask)
    return mask


def test_copy_keeps_cp_modes_and_preserve_keeps_mode_and_times(tmp_path):
    new_src = _write(tmp_path / "src/tool.sh", "#!/bin/sh\n", 0o755)
    old_src = _write(tmp_path / "src/policy.py", "NEW = 1\n", 0o644)
    old_dest = _write(tmp_path / "hooks/policy.py", "OLD = 1\n", 0o600)
    kept_src = _write(tmp_path / "src/registry.py", "R = 1\n", 0o640)
    os.utime(kept_src, ns=(1_600_000_000_000_000_000, 1_600_000_000_000_000_000))
    _sync(tmp_path, [
        {"kind": "copy", "files": [["src/tool.sh", "hooks/new/tool.sh"], ["src/policy.py", "hooks/policy.py"]]},
        {"kind": "copy", "preserve": True, "files": [["src/registry.py", "tap/registry.py"]]},
        {"kind": "copy", "optional": True, "files": [["src/missing.md", "inline/missing.md"]]},
    ])
    new_dest = tmp_path / "hooks/new/tool.sh"
    assert new_dest.read_bytes() == new_src.read_bytes()
    assert new_dest.stat().st_mode & 0o777 == 0o755 & ~_umask()  # cp: a new file takes the source's mode
    assert old_dest.read_bytes() == old_src.read_bytes()
    assert old_dest.stat().st_mode & 0o777 == 0o600  # cp: an existing file keeps its own
    kept = (tmp_path / "tap/registry.py").stat()
    assert (kept.st_mode & 0o777, kept.st_mtime_ns) == (0o640, 1_600_000_000_000_000_000)
    assert not (tmp_path / "inline").exists()


def test_tree_replaces_the_copy_and_renders_a_versioned_skill_for_its_reader(tmp_path):
    _write(tmp_path / "skills/plain/SKILL.md", "---\nname: plain\n---\nPlain.\n")
    _write(tmp_path / "skills/plain/deep/ref.md", "ref\n")
    _write(tmp_path / "skills/plain/.hidden", "h\n")
    _write(tmp_path / "skills/versioned/SKILL.md", "---\nname: versioned\n---\nBase.\n")
    _write(tmp_path / "skills/versioned/versions/header.main-agent.md", "Main header.\n")
    _write(tmp_path / "skills/kept/SKILL.md", "kept\n")
    _write(tmp_path / "skills/profiles.json", json.dumps({"full": ["plain", "versioned", "kept"]}))
    stray = _write(tmp_path / "out/plain/STRAY.md", "stale\n")
    (tmp_path / "out/plain/deep").mkdir()
    _sync(tmp_path, [
        {"kind": "tree", "each": {"profile": "full", "except": "hand_kept"}, "reader": "main-agent",
         "files": [["skills/{name}", "out/{name}"]]},
        {"kind": "tree", "each": ["versioned"], "files": [["skills/{name}", "raw/{name}"]]},
    ], lists={"hand_kept": ["kept"]})
    assert not stray.exists()
    assert sorted(p.relative_to(tmp_path / "out").as_posix() for p in (tmp_path / "out").rglob("*") if p.is_file()) == [
        "plain/.hidden", "plain/SKILL.md", "plain/deep/ref.md", "versioned/SKILL.md"]
    rendered = (tmp_path / "out/versioned/SKILL.md").read_text()
    assert rendered == skill_versions.render(tmp_path / "skills/versioned", "main-agent")
    assert "Main header." in rendered and not (tmp_path / "out/versioned/versions").exists()
    assert (tmp_path / "raw/versioned/versions/header.main-agent.md").is_file()  # no reader: a plain copy
    assert (tmp_path / "raw/versioned/SKILL.md").read_text() == "---\nname: versioned\n---\nBase.\n"


def test_render_inline_and_remove(tmp_path):
    for name in ("one", "two"):
        _write(tmp_path / f"skills/{name}/SKILL.md", f"---\nname: {name}\n---\nBody {name}.\n")
        _write(tmp_path / f"skills/{name}/versions/header.writer.md", f"Writer {name}.\n")
    gone = _write(tmp_path / "plugin/inline/old/SKILL.md", "old\n")
    _sync(tmp_path, [
        {"kind": "render", "reader": "writer", "files": [["skills/one", "tap/rules.md"]]},
        {"kind": "inline", "reader": "main-agent", "skills": ["skills/one", "skills/two"], "dest": "fixtures/inline.md"},
        {"kind": "remove", "paths": ["plugin/inline", "plugin/never-there"]},
    ])
    assert (tmp_path / "tap/rules.md").read_text() == skill_versions.render(tmp_path / "skills/one", "writer")
    assert (tmp_path / "fixtures/inline.md").read_text() == "# Skill: one\n\nBody one.\n\n# Skill: two\n\nBody two."
    assert not gone.parent.parent.exists()


def test_unknown_kinds_and_groups_are_refused(tmp_path, capsys):
    with pytest.raises(ValueError, match="unknown kind"):
        vendor.plan("g", tmp_path, {"lists": {}, "groups": {"g": [{"kind": "symlink", "files": []}]}})
    assert vendor.main(["sync-nothing"]) == 2
    assert vendor.main([]) == 2
    assert "sync-tap-core" in capsys.readouterr().err


def test_vendored_json_names_only_files_that_exist():
    manifest = vendor.load()
    for group in manifest["groups"]:
        for op in vendor.plan(group, manifest=manifest):
            sources = [AGENT / source for source in op.sources]
            dest = AGENT / op.dest
            where = f"{group}: {op.kind} {op.sources} -> {op.dest}"
            if op.kind == "copy":
                assert op.optional or sources[0].is_file(), where
                assert dest.is_file() or (op.optional and not sources[0].exists()), where
            elif op.kind == "tree":
                assert sources[0].is_dir() and dest.is_dir(), where
            elif op.kind in ("render", "inline"):
                assert all((s / "SKILL.md").is_file() for s in sources) and dest.is_file(), where
            assert dest.resolve().is_relative_to(AGENT.parent), where  # never outside the repo


def test_every_group_is_one_makefile_target_that_calls_the_tool():
    makefile = (AGENT / "Makefile").read_text(encoding="utf-8")
    assert re.search(r"^VENDOR := python3 tools/vendor\.py$", makefile, re.MULTILINE)
    calls = dict(re.findall(r"^(sync-[a-z-]+):\n\t@\$\(VENDOR\) (\S+)$", makefile, re.MULTILINE))
    assert calls == {group: group for group in vendor.load()["groups"]}
    assert set(re.findall(r"\$\(VENDOR\) (\S+)", makefile)) == set(calls)
