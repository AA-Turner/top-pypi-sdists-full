"""Discovery tests: unit grouping, ignore-list, orphan source, bounded reads."""

from __future__ import annotations

import tracemalloc

from runlayer_cli.scan.agents.discover import MAX_FILE_BYTES, _read_text, discover


def _unit_by_name(units, name):
    return next(u for u in units if u.name == name)


def test_groups_manifest_with_nested_source(tmp_path):
    proj = tmp_path / "proj"
    (proj / "src").mkdir(parents=True)
    (proj / "package.json").write_text('{"dependencies": {"ai": "^5"}}')
    (proj / "src" / "agent.ts").write_text('import { generateText } from "ai";')

    units = discover(tmp_path)

    assert len(units) == 1
    unit = units[0]
    assert unit.root == proj
    # Nested source attaches to the nearest manifest ancestor.
    assert [sf.path.name for sf in unit.sources] == ["agent.ts"]
    assert "ai" in unit.deps
    assert {"TypeScript", "JavaScript"} & unit.languages


def test_ignore_list_skips_dependency_dirs(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "pyproject.toml").write_text("[project]\nname='x'\n")
    # These must be skipped entirely.
    for ignored in ("node_modules", ".venv", "dist", "__pycache__"):
        d = proj / ignored
        d.mkdir()
        (d / "package.json").write_text('{"dependencies": {"langchain": "1"}}')
        (d / "junk.py").write_text("import langchain")

    units = discover(tmp_path)

    assert len(units) == 1
    assert units[0].root == proj
    # No manifest from node_modules leaked in.
    assert all("langchain" not in u.deps for u in units)


def test_ignore_list_skips_tool_caches_and_detection_fixtures(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "pyproject.toml").write_text("[project]\nname='project'\n")

    ignored_paths = (
        project / ".cursor" / "extensions" / "cached-extension",
        project / ".vscode" / "extensions" / "cached-extension",
        project / ".mintlify" / "cached-project",
        project / "tests" / "fixtures" / "agent_detection" / "sample",
    )
    for ignored in ignored_paths:
        ignored.mkdir(parents=True)
        (ignored / "package.json").write_text('{"dependencies":{"ai":"^5"}}')
        (ignored / "agent.ts").write_text('import { generateText } from "ai";')

    units = discover(tmp_path)

    assert [unit.root for unit in units] == [project]
    assert units[0].sources == []


def test_orphan_source_dir_becomes_manifestless_unit(tmp_path):
    loose = tmp_path / "loose"
    loose.mkdir()
    (loose / "thing.py").write_text("print('hello')")

    units = discover(tmp_path)

    assert len(units) == 1
    unit = units[0]
    assert unit.manifests == []
    assert [sf.path.name for sf in unit.sources] == ["thing.py"]
    assert unit.languages == {"Python"}


def test_bounded_read_truncates_large_files(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "go.mod").write_text("module x\n")
    big = "x" * (MAX_FILE_BYTES + 50_000)
    (proj / "main.go").write_text(big)

    units = discover(tmp_path)

    source = _unit_by_name(units, "proj").sources[0]
    assert len(source.text) <= MAX_FILE_BYTES


def test_read_text_does_not_load_entire_file_into_memory(tmp_path):
    """A huge source file must not be slurped whole into memory before truncation.

    Regression: ``_read_text`` did ``path.read_bytes()[:MAX_FILE_BYTES]``, which
    pulls the entire file into memory before slicing, so peak memory equals the
    real file size and the MAX_FILE_BYTES cap is defeated. A bounded read should
    allocate on the order of MAX_FILE_BYTES regardless of how big the file is.
    """
    big = tmp_path / "huge.py"
    big_size = 32 * 1024 * 1024  # 32 MB, far above the 512 KB cap
    big.write_bytes(b"x" * big_size)

    tracemalloc.start()
    try:
        text = _read_text(big)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert len(text) <= MAX_FILE_BYTES
    assert peak < big_size // 4, (
        f"peak allocation {peak} bytes ~ full file size; "
        f"bounded read should stay near {MAX_FILE_BYTES} bytes"
    )


def test_separate_manifest_dirs_are_separate_units(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "pyproject.toml").write_text("[project]\nname='a'\n")
    (tmp_path / "b" / "go.mod").write_text("module b\n")

    units = discover(tmp_path)

    names = {u.name for u in units}
    assert names == {"a", "b"}
