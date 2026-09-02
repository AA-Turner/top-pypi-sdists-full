"""Tests for client-native agent-definition discovery."""

from __future__ import annotations

import hashlib
import os
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from runlayer_cli.scan import agent_definition_scanner as scanner_module
from runlayer_cli.scan import orchestrator as scan_orchestrator
from runlayer_cli.scan.agent_definition_scanner import (
    AGENT_DEFINITION_PATTERNS,
    DiscoveredAgentDefinition,
    dedupe_agent_definitions,
    get_agent_definition_search_patterns,
    parse_agent_definition,
    process_agent_definition_paths,
    scan_user_agent_definitions,
)
from runlayer_cli.scan.clients import MCPClientDefinition, ProjectConfigPattern
from runlayer_cli.scan.project_scanner import find_files_and_node_modules_under_home


def test_agent_definition_pattern_registry_is_immutable():
    assert isinstance(AGENT_DEFINITION_PATTERNS, tuple)
    with pytest.raises(FrozenInstanceError):
        AGENT_DEFINITION_PATTERNS[0].client = "changed"


def test_parse_claude_agent_definition_from_bytes():
    content = b"---\nname: reviewer\ndescription: Reviews code\n---\n# Instructions\n"

    definition = parse_agent_definition(
        client="claude_code",
        path=Path("/workspace/api/.claude/agents/reviewer.md"),
        content=content,
        scope="project",
        project_path="/workspace/api",
    )

    assert definition is not None
    assert definition.client == "claude_code"
    assert definition.name == "reviewer"
    assert definition.description == "Reviews code"
    assert definition.scope == "project"
    assert definition.path == "/workspace/api/.claude/agents/reviewer.md"
    assert definition.project_path == "/workspace/api"
    assert definition.content_hash == hashlib.sha256(content).hexdigest()


@pytest.mark.parametrize(
    ("client", "path", "content", "expected_name", "expected_description"),
    [
        (
            "cursor",
            "/workspace/.cursor/agents/fix.md",
            b"---\nname: fixer\ndescription: Fixes bugs\n---\n",
            "fixer",
            "Fixes bugs",
        ),
        (
            "codex",
            "/workspace/.codex/agents/review.toml",
            b'name = "reviewer"\ndescription = "Reviews code"\n',
            "reviewer",
            "Reviews code",
        ),
        (
            "gemini_cli",
            "/workspace/.gemini/agents/test.md",
            b"---\nname: tester\ndescription: Tests code\n---\n",
            "tester",
            "Tests code",
        ),
        (
            "github_copilot_cli",
            "/workspace/.github/agents/triage.agent.md",
            b"---\nname: triager\ndescription: Triages issues\n---\n",
            "triager",
            "Triages issues",
        ),
        (
            "opencode",
            "/workspace/.opencode/agents/team/docs.md",
            b"---\nname: documenter\ndescription: Writes docs\n---\n",
            "documenter",
            "Writes docs",
        ),
        (
            "goose",
            "/workspace/.goose/recipes/deploy.yaml",
            b"title: deployer\nname: ignored\ndescription: Deploys safely\n",
            "deployer",
            "Deploys safely",
        ),
    ],
)
def test_parse_registered_agent_definition_formats(
    client, path, content, expected_name, expected_description
):
    definition = parse_agent_definition(
        client=client,
        path=path,
        content=content,
        scope="project",
        project_path="/workspace",
    )

    assert definition is not None
    assert definition.name == expected_name
    assert definition.description == expected_description


@pytest.mark.parametrize(
    ("client", "path", "content"),
    [
        (
            "claude_code",
            "/workspace/.claude/agents/broken.md",
            b"---\nname: [unterminated\n---\n",
        ),
        (
            "codex",
            "/workspace/.codex/agents/broken.toml",
            b'name = "unterminated\n',
        ),
        (
            "goose",
            "/workspace/.goose/recipes/broken.yaml",
            b"title: [unterminated\n",
        ),
        (
            "cursor",
            "/workspace/.cursor/agents/binary.md",
            b"\xff\xfe",
        ),
    ],
)
def test_invalid_agent_definition_bytes_are_skipped(client, path, content):
    assert (
        parse_agent_definition(
            client=client,
            path=path,
            content=content,
            scope="project",
            project_path="/workspace",
        )
        is None
    )


@pytest.mark.parametrize(
    ("client", "path", "content", "expected_name"),
    [
        ("claude_code", "/home/u/.claude/agents/review.md", b"# Review\n", "review"),
        ("cursor", "/home/u/.cursor/agents/fix.md", b"# Fix\n", "fix"),
        ("codex", "/home/u/.codex/agents/test.toml", b"# Test\n", "test"),
        ("gemini_cli", "/home/u/.gemini/agents/docs.md", b"# Docs\n", "docs"),
        (
            "github_copilot_cli",
            "/home/u/.copilot/agents/triage.agent.md",
            b"# Triage\n",
            "triage",
        ),
        (
            "opencode",
            "/home/u/.config/opencode/agents/team/build.md",
            b"# Build\n",
            "build",
        ),
        (
            "goose",
            "/home/u/.config/goose/recipes/deploy.yaml",
            b"",
            "deploy",
        ),
    ],
)
def test_agent_definition_name_falls_back_to_filename(
    client, path, content, expected_name
):
    definition = parse_agent_definition(
        client=client,
        path=path,
        content=content,
        scope="user",
    )

    assert definition is not None
    assert definition.name == expected_name


@pytest.mark.parametrize(
    ("client", "path", "content", "expected_name"),
    [
        (
            "claude_code",
            "/home/u/.claude/agents/review.md",
            b"---\nname: reviewer\ndescription: no closing fence\n# Instructions\n",
            "review",
        ),
        (
            "cursor",
            "/home/u/.cursor/agents/fix.md",
            b"--- a thematic break, not frontmatter\n\n# Fix\n",
            "fix",
        ),
    ],
)
def test_markdown_without_closing_frontmatter_delimiter_falls_back_to_filename(
    client, path, content, expected_name
):
    # A leading `---` with no closing `---` is not a frontmatter block, so it must
    # be treated like a file with no frontmatter (kept, name falls back to the
    # filename) rather than dropped. Delimited-but-broken frontmatter is a
    # separate, genuinely-invalid case covered by the skip test above.
    definition = parse_agent_definition(
        client=client,
        path=path,
        content=content,
        scope="user",
    )

    assert definition is not None
    assert definition.name == expected_name


def test_agent_definition_metadata_is_bounded():
    definition = parse_agent_definition(
        client="cursor",
        path="/workspace/.cursor/agents/long.md",
        content=(
            b"---\nname: " + b"n" * 101 + b"\ndescription: " + b"d" * 1025 + b"\n---\n"
        ),
        scope="project",
        project_path="/workspace",
    )

    assert definition is not None
    assert len(definition.name) == 100
    assert definition.description is not None
    assert len(definition.description) == 1024


def test_agent_definition_payload_redacts_host_paths_but_preserves_container_paths(
    monkeypatch,
):
    content = b"# Agent\n"
    monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/host")
    host_definition = parse_agent_definition(
        client="cursor",
        path="/host/Users/dev/project/.cursor/agents/fix.md",
        content=content,
        scope="project",
        project_path="/host/Users/dev/project",
    )
    container_definition = parse_agent_definition(
        client="cursor",
        path="/host/workspace/.cursor/agents/fix.md",
        content=content,
        scope="project",
        project_path="/host/workspace",
        container_id="cid",
        container_name="devbox",
        container_image_ref="devbox:latest",
        container_image_digest="sha256:abc",
        container_runtime="docker",
        container_is_devcontainer=True,
        container_labels={"safe": "value"},
    )

    assert host_definition is not None
    assert host_definition.to_api_payload()["path"] == (
        "/Users/dev/project/.cursor/agents/fix.md"
    )
    assert host_definition.to_api_payload()["project_path"] == "/Users/dev/project"
    assert container_definition is not None
    payload = container_definition.to_api_payload()
    assert payload["path"] == "/host/workspace/.cursor/agents/fix.md"
    assert payload["project_path"] == "/host/workspace"
    assert payload["container"] == {
        "container_id": "cid",
        "name": "devbox",
        "image_ref": "devbox:latest",
        "image_digest": "sha256:abc",
        "runtime": "docker",
        "is_devcontainer": True,
        "is_running": True,
        "labels": {"safe": "value"},
        "mounts_host_home": False,
    }


def test_agent_definition_payload_includes_wsl_identity():
    definition = DiscoveredAgentDefinition(
        client="cursor",
        name="reviewer",
        description=None,
        scope="project",
        path="/home/alice/repo/.cursor/agents/review.md",
        project_path="/home/alice/repo",
        content_hash="a" * 64,
        wsl_distro="Ubuntu",
        wsl_user="alice",
    )

    assert definition.to_api_payload()["wsl"] == {
        "distro": "Ubuntu",
        "user": "alice",
    }


def test_dedupe_preserves_same_linux_path_in_distinct_wsl_distros():
    ubuntu = DiscoveredAgentDefinition(
        client="cursor",
        name="reviewer",
        description=None,
        scope="project",
        path="/home/alice/repo/.cursor/agents/review.md",
        project_path="/home/alice/repo",
        content_hash="a" * 64,
        wsl_distro="Ubuntu",
        wsl_user="alice",
    )
    definitions = [ubuntu, replace(ubuntu, wsl_distro="Debian")]

    assert dedupe_agent_definitions(definitions) == definitions


def test_project_search_patterns_and_exact_project_path_inference(
    tmp_path, monkeypatch
):
    home = tmp_path / "home"
    monkeypatch.setattr(Path, "home", lambda: home)
    project = home / "src" / "orders"
    claude_path = project / ".claude" / "agents" / "review.md"
    opencode_path = project / ".opencode" / "agents" / "team" / "docs.md"
    goose_path = project / ".agents" / "recipes" / "deploy.yaml"
    user_path = home / ".claude" / "agents" / "personal.md"
    for path, content in (
        (claude_path, b"# Review\n"),
        (opencode_path, b"# Docs\n"),
        (goose_path, b"title: deploy\n"),
        (user_path, b"# Personal\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    assert set(get_agent_definition_search_patterns()) == {
        ".claude/agents/*.md",
        ".cursor/agents/*.md",
        ".codex/agents/*.toml",
        ".gemini/agents/*.md",
        ".github/agents/*.agent.md",
        ".opencode/agents/*.md",
        ".opencode/agents/**/*.md",
        ".goose/recipes/*.yaml",
        ".agents/recipes/*.yaml",
    }

    definitions = process_agent_definition_paths(
        [claude_path, opencode_path, goose_path, user_path, claude_path]
    )

    assert [(item.client, item.path, item.project_path) for item in definitions] == [
        ("claude_code", str(claude_path), str(project)),
        ("opencode", str(opencode_path), str(project)),
        ("goose", str(goose_path), str(project)),
    ]


@pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
def test_project_file_symlink_preserves_logical_definition_path(
    tmp_path,
    monkeypatch,
):
    home = tmp_path / "home"
    project = home / "project"
    agent_root = project / ".claude" / "agents"
    agent_root.mkdir(parents=True)
    target = home / "notes" / "payload.md"
    target.parent.mkdir()
    target.write_text("# Review\n", encoding="utf-8")
    logical_path = agent_root / "review.md"
    try:
        logical_path.symlink_to(target)
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    crawl = find_files_and_node_modules_under_home(
        [".claude/agents/*.md"],
        timeout=10,
        max_depth=7,
    )
    assert crawl.found_paths == [target.resolve()]
    assert crawl.logical_paths == {target.resolve(): (logical_path,)}

    definitions = process_agent_definition_paths(
        crawl.found_paths,
        logical_paths=crawl.logical_paths,
    )

    assert [(item.path, item.project_path) for item in definitions] == [
        (str(logical_path), str(project))
    ]


@pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
def test_project_file_symlink_keeps_direct_target_definition(
    tmp_path,
    monkeypatch,
):
    home = tmp_path / "home"
    direct_project = home / "direct-project"
    target = direct_project / ".claude" / "agents" / "review.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Review\n", encoding="utf-8")
    alias_project = home / "alias-project"
    logical_path = alias_project / ".claude" / "agents" / "review.md"
    logical_path.parent.mkdir(parents=True)
    try:
        logical_path.symlink_to(target)
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    crawl = find_files_and_node_modules_under_home(
        [".claude/agents/*.md"],
        timeout=10,
        max_depth=7,
    )
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILES", 1)
    monkeypatch.setattr(
        scanner_module,
        "MAX_AGENT_DEFINITION_TOTAL_BYTES",
        len(target.read_bytes()),
    )
    definitions = process_agent_definition_paths(
        crawl.found_paths,
        logical_paths=crawl.logical_paths,
    )

    assert [(item.path, item.project_path) for item in definitions] == [
        (str(target), str(direct_project)),
        (str(logical_path), str(alias_project)),
    ]


@pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
def test_project_file_symlinks_keep_every_logical_definition(
    tmp_path,
    monkeypatch,
):
    home = tmp_path / "home"
    target = home / "notes" / "payload.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Review\n", encoding="utf-8")
    logical_paths = [
        home / project / ".claude" / "agents" / "review.md"
        for project in ("project-a", "project-b")
    ]
    for logical_path in logical_paths:
        logical_path.parent.mkdir(parents=True)
        try:
            logical_path.symlink_to(target)
        except OSError:
            pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    crawl = find_files_and_node_modules_under_home(
        [".claude/agents/*.md"],
        timeout=10,
        max_depth=7,
    )
    definitions = process_agent_definition_paths(
        crawl.found_paths,
        logical_paths=crawl.logical_paths,
    )

    assert [(item.path, item.project_path) for item in definitions] == [
        (str(path), str(path.parents[2])) for path in logical_paths
    ]


@pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
def test_dir_follow_discovered_target_keeps_physical_definition(
    tmp_path,
    monkeypatch,
):
    # Physical project beyond max_depth, so only the directory-symlink follow
    # discovers it; a file-symlink alias to the same target must not suppress
    # the physical identity.
    home = tmp_path / "home"
    deep_project = home.joinpath(
        "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "real-project"
    )
    target = deep_project / ".claude" / "agents" / "review.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Review\n", encoding="utf-8")
    directory_link = home / "link-project"
    alias_project = home / "alias-project"
    logical_path = alias_project / ".claude" / "agents" / "review.md"
    logical_path.parent.mkdir(parents=True)
    try:
        directory_link.symlink_to(deep_project, target_is_directory=True)
        logical_path.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    crawl = find_files_and_node_modules_under_home(
        [".claude/agents/*.md"],
        timeout=10,
        max_depth=7,
    )
    physical = target.resolve()
    assert crawl.found_paths == [physical]
    assert crawl.logical_paths == {physical: (physical, logical_path)}

    definitions = process_agent_definition_paths(
        crawl.found_paths,
        logical_paths=crawl.logical_paths,
    )

    assert [(item.path, item.project_path) for item in definitions] == [
        (str(physical), str(physical.parents[2])),
        (str(logical_path), str(alias_project)),
    ]


def test_bare_project_recipes_dir_is_not_attributed_to_goose(tmp_path):
    # A bare project-root recipes/ dir is not a goose location (goose reads
    # .goose/recipes/ and .agents/recipes/). Unrelated recipes/*.yaml files that
    # parse as YAML mappings must not be misattributed as goose agent defs.
    unrelated = tmp_path / "project" / "recipes" / "build.yaml"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("steps:\n  - run: make\n", encoding="utf-8")

    assert process_agent_definition_paths([unrelated]) == []


def test_project_path_processing_enforces_file_and_total_byte_caps(
    tmp_path, monkeypatch
):
    project = tmp_path / "project"
    root = project / ".cursor" / "agents"
    root.mkdir(parents=True)
    large = root / "a-large.md"
    first = root / "b-first.md"
    over_total = root / "c-over-total.md"
    large.write_bytes(b"12345")
    first.write_bytes(b"123")
    over_total.write_bytes(b"123")
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILE_BYTES", 4)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_TOTAL_BYTES", 4)

    bounded = process_agent_definition_paths([large, first, over_total])

    assert [Path(item.path).name for item in bounded] == ["b-first.md"]

    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILE_BYTES", 100)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_TOTAL_BYTES", 100)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILES", 1)

    file_bounded = process_agent_definition_paths([first, over_total])

    assert [Path(item.path).name for item in file_bounded] == ["b-first.md"]


def test_user_scan_covers_all_registered_roots_recursively(tmp_path, monkeypatch):
    home = tmp_path / "home"
    monkeypatch.setattr(Path, "home", lambda: home)
    files = {
        ".claude/agents/claude.md": b"# Claude\n",
        ".cursor/agents/cursor.md": b"# Cursor\n",
        ".codex/agents/codex.toml": b"# Codex\n",
        ".gemini/agents/gemini.md": b"# Gemini\n",
        ".copilot/agents/copilot.agent.md": b"# Copilot\n",
        ".github/agents/github.agent.md": b"# GitHub\n",
        ".config/opencode/agents/team/opencode.md": b"# OpenCode\n",
        ".config/goose/recipes/goose.yaml": b"description: Goose\n",
    }
    for relative_path, content in files.items():
        path = home / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    definitions = scan_user_agent_definitions()

    assert [(item.client, Path(item.path).name) for item in definitions] == [
        ("claude_code", "claude.md"),
        ("cursor", "cursor.md"),
        ("codex", "codex.toml"),
        ("gemini_cli", "gemini.md"),
        ("github_copilot_cli", "copilot.agent.md"),
        ("github_copilot_cli", "github.agent.md"),
        ("opencode", "opencode.md"),
        ("goose", "goose.yaml"),
    ]
    assert all(item.scope == "user" for item in definitions)
    assert all(item.project_path is None for item in definitions)


def test_user_scan_covers_extra_home_roots(tmp_path, monkeypatch):
    native_home = tmp_path / "native-home"
    wsl_home = tmp_path / "wsl-home"
    definition_path = wsl_home / ".claude" / "agents" / "review.md"
    definition_path.parent.mkdir(parents=True)
    definition_path.write_text("# Review\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: native_home)

    definitions = scan_user_agent_definitions(extra_home_roots=[wsl_home])

    assert [(item.client, item.path, item.scope) for item in definitions] == [
        ("claude_code", str(definition_path), "user")
    ]


def test_user_scan_file_cap_is_per_home(tmp_path, monkeypatch):
    # A native home that saturates the file cap must not starve later homes.
    native_home = tmp_path / "native-home"
    wsl_home = tmp_path / "wsl-home"
    native_agents = native_home / ".claude" / "agents"
    native_agents.mkdir(parents=True)
    (native_agents / "a.md").write_text("# A\n", encoding="utf-8")
    (native_agents / "b.md").write_text("# B\n", encoding="utf-8")
    wsl_definition = wsl_home / ".claude" / "agents" / "review.md"
    wsl_definition.parent.mkdir(parents=True)
    wsl_definition.write_text("# Review\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: native_home)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILES", 1)

    definitions = scan_user_agent_definitions(extra_home_roots=[wsl_home])

    paths = {item.path for item in definitions}
    # WSL home is still scanned despite the native home hitting the file cap.
    assert str(wsl_definition) in paths
    # The cap still bounds the native home to a single file.
    native_paths = [path for path in paths if path.startswith(str(native_agents))]
    assert len(native_paths) == 1


def test_user_scan_total_byte_cap_is_per_home(tmp_path, monkeypatch):
    # A native home that saturates the byte cap must not starve later homes.
    native_home = tmp_path / "native-home"
    wsl_home = tmp_path / "wsl-home"
    native_agents = native_home / ".claude" / "agents"
    native_agents.mkdir(parents=True)
    (native_agents / "a.md").write_bytes(b"123")
    (native_agents / "b.md").write_bytes(b"123")
    wsl_definition = wsl_home / ".claude" / "agents" / "review.md"
    wsl_definition.parent.mkdir(parents=True)
    wsl_definition.write_bytes(b"123")
    monkeypatch.setattr(Path, "home", lambda: native_home)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILE_BYTES", 3)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_TOTAL_BYTES", 3)

    definitions = scan_user_agent_definitions(extra_home_roots=[wsl_home])

    paths = {item.path for item in definitions}
    # WSL home is still scanned despite the native home hitting the byte cap.
    assert str(wsl_definition) in paths
    # The cap still bounds the native home to the single 3-byte file.
    native_paths = [path for path in paths if path.startswith(str(native_agents))]
    assert len(native_paths) == 1


def test_extra_home_roots_skip_appdata_templates(tmp_path, monkeypatch):
    native_home = tmp_path / "native-home"
    native_appdata = tmp_path / "native-appdata"
    wsl_home = tmp_path / "wsl-home"
    invalid_wsl_appdata_path = wsl_home / "Block" / "goose" / "recipes" / "windows.yaml"
    invalid_wsl_appdata_path.parent.mkdir(parents=True)
    invalid_wsl_appdata_path.write_text("title: windows\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: native_home)
    monkeypatch.setattr(scanner_module.platform, "system", lambda: "Windows")
    monkeypatch.setenv("APPDATA", str(native_appdata))

    definitions = scan_user_agent_definitions(extra_home_roots=[wsl_home])

    assert definitions == []


def test_project_processing_excludes_extra_home_user_roots(tmp_path, monkeypatch):
    native_home = tmp_path / "native-home"
    wsl_home = tmp_path / "wsl-home"
    definition_path = wsl_home / ".claude" / "agents" / "review.md"
    definition_path.parent.mkdir(parents=True)
    definition_path.write_text("# Review\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: native_home)

    definitions = process_agent_definition_paths(
        [definition_path],
        extra_home_roots=[wsl_home],
    )

    assert definitions == []


def test_project_phase_collects_agent_definitions_in_shared_crawl(
    tmp_path, monkeypatch
):
    project = tmp_path / "project"
    logical_path = project / ".cursor" / "agents" / "fix.md"
    definition_target = tmp_path / "definition-target.md"
    definition_target.write_text("# Fix\n", encoding="utf-8")

    def fake_find(patterns, *args, **kwargs):
        assert ".cursor/agents/*.md" in patterns
        return SimpleNamespace(
            found_paths=[definition_target],
            node_modules_paths=[],
            logical_paths={definition_target: (logical_path,)},
        )

    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_and_node_modules_under_home",
        fake_find,
    )
    monkeypatch.setattr(
        scan_orchestrator, "get_clients_with_project_configs", lambda: []
    )
    monkeypatch.setattr(scan_orchestrator, "scan_for_project_configs", lambda **_: [])
    monkeypatch.setattr(
        scan_orchestrator,
        "process_skill_paths",
        lambda *args, **kwargs: [],
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "process_project_gemini_extensions",
        lambda _: ([], []),
    )

    result = scan_orchestrator._scan_project_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        project_scan_timeout=60,
        project_scan_depth=7,
        run_static_agents=False,
    )

    assert [(item.client, item.project_path) for item in result.agent_definitions] == [
        ("cursor", str(project))
    ]


def test_project_phase_searches_below_external_config_roots(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    project = tmp_path / "a" / "b" / "c" / "d" / "project"
    config_path = project / ".mcp.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        '{"mcpServers":{"example":{"command":"example"}}}',
        encoding="utf-8",
    )
    skill_path = project / ".claude" / "skills" / "deep" / "SKILL.md"
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text("---\nname: deep\n---\n# Deep\n", encoding="utf-8")
    definition_path = project / ".cursor" / "agents" / "fix.md"
    definition_path.parent.mkdir(parents=True)
    definition_path.write_text("# Fix\n", encoding="utf-8")
    client = MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[],
        project_config=ProjectConfigPattern(".mcp.json"),
    )

    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_and_node_modules_under_home",
        lambda *args, **kwargs: SimpleNamespace(
            found_paths=[config_path],
            node_modules_paths=[],
            logical_paths={},
        ),
    )

    def fake_secondary_search(patterns, roots, **kwargs):
        assert "SKILL.md" in patterns
        assert ".cursor/agents/*.md" in patterns
        assert roots == [project]
        assert kwargs["timeout"] <= 15
        assert kwargs["max_depth"] == 8
        return [skill_path, definition_path]

    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_under_project_roots",
        fake_secondary_search,
        raising=False,
    )
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setattr(
        scan_orchestrator, "get_clients_with_project_configs", lambda: [client]
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "get_client_by_name",
        lambda name: client if name == "cursor" else None,
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "process_project_gemini_extensions",
        lambda _: ([], []),
    )

    result = scan_orchestrator._scan_project_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        project_scan_timeout=60,
        project_scan_depth=7,
        run_static_agents=False,
    )

    assert [skill.name for skill in result.skills] == ["deep"]
    assert [definition.name for definition in result.agent_definitions] == ["fix"]
    assert set(result.found_paths) == {config_path, skill_path, definition_path}


def test_windows_user_scan_includes_goose_appdata_root(tmp_path, monkeypatch):
    home = tmp_path / "home"
    appdata = tmp_path / "AppData" / "Roaming"
    recipe = appdata / "Block" / "goose" / "recipes" / "windows.yaml"
    recipe.parent.mkdir(parents=True)
    recipe.write_text("title: windows\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setattr(scanner_module.platform, "system", lambda: "Windows")
    monkeypatch.setenv("APPDATA", str(appdata))

    definitions = scan_user_agent_definitions()

    assert [(item.client, item.path) for item in definitions] == [
        ("goose", str(recipe))
    ]


def test_user_scan_follows_external_file_and_directory_symlinks(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    external_file = tmp_path / "external-file.md"
    external_file.write_text("---\nname: external-file\n---\n", encoding="utf-8")
    external_directory = tmp_path / "external-directory"
    external_directory.mkdir()
    (external_directory / "nested.md").write_text(
        "---\nname: external-directory\n---\n",
        encoding="utf-8",
    )
    file_link = root / "linked-file.md"
    directory_link = root / "linked-directory"
    try:
        file_link.symlink_to(external_file)
        directory_link.symlink_to(external_directory, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert [(item.name, item.path) for item in definitions] == [
        ("external-file", str(file_link)),
        ("external-directory", str(directory_link / "nested.md")),
    ]


def test_user_scan_follows_linked_definition_root_and_preserves_logical_path(
    tmp_path, monkeypatch
):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    external = tmp_path / "external"
    external.mkdir()
    (external / "nested.md").write_text("# Linked root\n", encoding="utf-8")
    root.parent.mkdir(parents=True)
    try:
        root.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert [item.path for item in definitions] == [str(root / "nested.md")]


def test_user_scan_rejects_linked_definition_root_for_system(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    external = tmp_path / "external"
    external.mkdir()
    (external / "nested.md").write_text("# Linked root\n", encoding="utf-8")
    root.parent.mkdir(parents=True)
    try:
        root.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setattr(scanner_module, "is_windows_system_context", lambda: True)

    assert scan_user_agent_definitions() == []


def test_user_scan_system_rejects_linked_root_component_before_target_access(
    tmp_path, monkeypatch
):
    home = tmp_path / "home"
    outside_client = tmp_path / "outside-client"
    target_root = outside_client / "agents"
    target_root.mkdir(parents=True)
    (target_root / "escaped.md").write_text("# Escaped\n", encoding="utf-8")
    home.mkdir()
    try:
        (home / ".cursor").symlink_to(outside_client, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setattr(scanner_module, "is_windows_system_context", lambda: True)
    real_stat = Path.stat

    def reject_target_stat(path, *args, **kwargs):
        if path == home / ".cursor" / "agents" or path == target_root:
            raise AssertionError("linked target stat attempted")
        return real_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", reject_target_stat)
    monkeypatch.setattr(
        scanner_module.os,
        "walk",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("linked target walk attempted")
        ),
    )

    assert scan_user_agent_definitions() == []


def test_user_scan_coverage_is_client_aware_for_linked_root(tmp_path, monkeypatch):
    home = tmp_path / "home"
    claude_root = home / ".claude" / "agents"
    claude_root.mkdir(parents=True)
    shared = claude_root / "shared.md"
    shared.write_text("# Shared\n", encoding="utf-8")
    cursor_root = home / ".cursor" / "agents"
    cursor_root.parent.mkdir(parents=True)
    try:
        cursor_root.symlink_to(claude_root, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert {(item.client, item.path) for item in definitions} == {
        ("claude_code", str(shared)),
        ("cursor", str(cursor_root / "shared.md")),
    }


def test_user_scan_client_policies_share_one_unique_target_ledger(
    tmp_path, monkeypatch
):
    home = tmp_path / "home"
    shared_target = tmp_path / "shared-target"
    shared_target.mkdir()
    (shared_target / "shared.md").write_text("# Shared\n", encoding="utf-8")
    overflow_target = tmp_path / "overflow-target"
    overflow_target.mkdir()
    (overflow_target / "overflow.md").write_text("# Overflow\n", encoding="utf-8")
    claude_root = home / ".claude" / "agents"
    cursor_root = home / ".cursor" / "agents"
    gemini_root = home / ".gemini" / "agents"
    for root in (claude_root, cursor_root, gemini_root):
        root.parent.mkdir(parents=True)
    try:
        claude_root.symlink_to(shared_target, target_is_directory=True)
        cursor_root.symlink_to(shared_target, target_is_directory=True)
        gemini_root.symlink_to(overflow_target, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setattr(scanner_module, "MAX_FOLLOWED_AGENT_DEFINITION_TARGETS", 1)

    definitions = scan_user_agent_definitions()

    assert {(item.client, item.path) for item in definitions} == {
        ("claude_code", str(claude_root / "shared.md")),
        ("cursor", str(cursor_root / "shared.md")),
    }


def test_ledger_rejection_does_not_consume_client_policy_slot(tmp_path, monkeypatch):
    home = tmp_path / "home"
    shared_target = tmp_path / "shared-target"
    shared_target.mkdir()
    (shared_target / "shared.agent.md").write_text("# Shared\n", encoding="utf-8")
    rejected_target = tmp_path / "rejected-target"
    rejected_target.mkdir()
    (rejected_target / "rejected.agent.md").write_text(
        "# Rejected\n",
        encoding="utf-8",
    )
    claude_root = home / ".claude" / "agents"
    rejected_copilot_root = home / ".copilot" / "agents"
    accepted_copilot_root = home / ".github" / "agents"
    for root in (claude_root, rejected_copilot_root, accepted_copilot_root):
        root.parent.mkdir(parents=True)
    try:
        claude_root.symlink_to(shared_target, target_is_directory=True)
        rejected_copilot_root.symlink_to(rejected_target, target_is_directory=True)
        accepted_copilot_root.symlink_to(shared_target, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setattr(scanner_module, "MAX_FOLLOWED_AGENT_DEFINITION_TARGETS", 1)

    definitions = scan_user_agent_definitions()

    assert {(item.client, item.path) for item in definitions} == {
        ("claude_code", str(claude_root / "shared.agent.md")),
        ("github_copilot_cli", str(accepted_copilot_root / "shared.agent.md")),
    }


def test_user_scan_reads_followed_file_via_resolved_target(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    link = root / "linked.md"
    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)
    read_paths = []
    real_read_bounded = scanner_module.read_bounded

    def track_read(path, *, max_bytes):
        read_paths.append(path)
        return real_read_bounded(path, max_bytes=max_bytes)

    monkeypatch.setattr(scanner_module, "read_bounded", track_read)

    definitions = scan_user_agent_definitions()

    assert [item.path for item in definitions] == [str(link)]
    assert read_paths == [target.resolve()]


def test_user_scan_skips_entry_when_link_probe_fails(tmp_path, monkeypatch):
    home = tmp_path / "home"
    blocked = home / ".cursor" / "agents" / "blocked.md"
    blocked.parent.mkdir(parents=True)
    blocked.write_text("# Blocked\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: home)
    real_lstat = Path.lstat

    def deny_blocked_lstat(path, *args, **kwargs):
        if path == blocked:
            raise PermissionError("denied")
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", deny_blocked_lstat)

    assert scan_user_agent_definitions() == []


def test_user_scan_skips_in_area_aliases_and_follows_beyond_depth_targets(
    tmp_path, monkeypatch
):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    within_file = root / "within" / "real.md"
    within_file.parent.mkdir()
    within_file.write_text("# Within\n", encoding="utf-8")
    within_link = root / "within-alias.md"

    deep_file_parent = root / "file-target"
    deep_directory = root / "directory-target"
    for index in range(scanner_module.MAX_AGENT_DEFINITION_USER_DEPTH + 1):
        deep_file_parent /= f"f{index}"
        deep_directory /= f"d{index}"
    deep_file_parent.mkdir(parents=True)
    deep_file = deep_file_parent / "deep.md"
    deep_file.write_text("# Deep file\n", encoding="utf-8")
    deep_directory.mkdir(parents=True)
    (deep_directory / "nested.md").write_text("# Deep directory\n", encoding="utf-8")
    deep_file_link = root / "linked-file.md"
    deep_directory_link = root / "linked-directory"
    try:
        within_link.symlink_to(within_file)
        deep_file_link.symlink_to(deep_file)
        deep_directory_link.symlink_to(deep_directory, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert {item.path for item in definitions} == {
        str(within_file),
        str(deep_file_link),
        str(deep_directory_link / "nested.md"),
    }


def test_user_scan_depth_boundary_covers_file_but_not_deeper_directory(
    tmp_path, monkeypatch
):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    max_depth_parent = root
    beyond_depth_directory = root
    for index in range(scanner_module.MAX_AGENT_DEFINITION_USER_DEPTH):
        max_depth_parent /= f"file-{index}"
        beyond_depth_directory /= f"directory-{index}"
    beyond_depth_directory /= "beyond"
    max_depth_parent.mkdir(parents=True)
    max_depth_file = max_depth_parent / "real.md"
    max_depth_file.write_text("# Boundary file\n", encoding="utf-8")
    beyond_depth_directory.mkdir(parents=True)
    (beyond_depth_directory / "nested.md").write_text(
        "# Beyond directory\n",
        encoding="utf-8",
    )
    file_alias = root / "file-alias.md"
    directory_alias = root / "directory-alias"
    try:
        file_alias.symlink_to(max_depth_file)
        directory_alias.symlink_to(beyond_depth_directory, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert {item.path for item in definitions} == {
        str(max_depth_file),
        str(directory_alias / "nested.md"),
    }


def test_user_scan_skips_broken_ancestor_and_looping_links(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    first_target = tmp_path / "first-target"
    second_target = tmp_path / "second-target"
    first_target.mkdir()
    second_target.mkdir()
    (first_target / "first.md").write_text("# First\n", encoding="utf-8")
    (second_target / "second.md").write_text("# Second\n", encoding="utf-8")
    try:
        (root / "a-broken.md").symlink_to(tmp_path / "missing.md")
        (root / "b-ancestor").symlink_to(home, target_is_directory=True)
        (root / "c-entry").symlink_to(first_target, target_is_directory=True)
        (first_target / "to-second").symlink_to(
            second_target,
            target_is_directory=True,
        )
        (second_target / "to-first").symlink_to(
            first_target,
            target_is_directory=True,
        )
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert [(item.name, item.path) for item in definitions] == [
        ("first", str(root / "c-entry" / "first.md")),
        ("second", str(root / "c-entry" / "to-second" / "second.md")),
    ]


def test_user_scan_caps_followed_targets_at_64(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    external = tmp_path / "external"
    root.mkdir(parents=True)
    external.mkdir()
    links = []
    try:
        for index in range(65):
            target = external / f"target-{index:03}.md"
            target.write_text(f"# {index}\n", encoding="utf-8")
            link = root / f"link-{index:03}.md"
            link.symlink_to(target)
            links.append(link)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert [item.path for item in definitions] == [str(link) for link in links[:64]]


def test_nonmatching_file_links_do_not_consume_follow_cap(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    external = tmp_path / "external"
    root.mkdir(parents=True)
    external.mkdir()
    valid_target = external / "valid.md"
    valid_target.write_text("# Valid\n", encoding="utf-8")
    valid_link = root / "z-valid.md"
    try:
        for index in range(64):
            target = external / f"ignored-{index:03}.txt"
            target.write_text("ignored\n", encoding="utf-8")
            (root / f"a-ignored-{index:03}.txt").symlink_to(target)
        valid_link.symlink_to(valid_target)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert [item.path for item in definitions] == [str(valid_link)]


def test_unreadable_file_links_do_not_consume_follow_cap(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    external = tmp_path / "external"
    root.mkdir(parents=True)
    external.mkdir()
    unreadable_target = external / "unreadable.md"
    unreadable_target.write_text("# Unreadable\n", encoding="utf-8")
    valid_target = external / "valid.md"
    valid_target.write_text("# Valid\n", encoding="utf-8")
    unreadable_link = root / "a-unreadable.md"
    valid_link = root / "z-valid.md"
    try:
        unreadable_link.symlink_to(unreadable_target)
        valid_link.symlink_to(valid_target)
    except OSError:
        pytest.skip("symlinks unavailable")
    real_read = scanner_module._read_bounded_file

    def reject_first(path):
        return None if path == unreadable_target.resolve() else real_read(path)

    monkeypatch.setattr(scanner_module, "_read_bounded_file", reject_first)
    monkeypatch.setattr(scanner_module, "MAX_FOLLOWED_AGENT_DEFINITION_TARGETS", 1)
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert [item.path for item in definitions] == [str(valid_link)]


def test_repeated_unreadable_file_links_do_not_exhaust_file_cap(
    tmp_path,
    monkeypatch,
):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    unreadable_target = tmp_path / "unreadable.md"
    unreadable_target.write_text("# Unreadable\n", encoding="utf-8")
    valid = root / "z-valid.md"
    valid.write_text("# Valid\n", encoding="utf-8")
    try:
        (root / "a-first.md").symlink_to(unreadable_target)
        (root / "b-second.md").symlink_to(unreadable_target)
    except OSError:
        pytest.skip("symlinks unavailable")
    real_read = scanner_module._read_bounded_file

    def reject_unreadable(path):
        return None if path == unreadable_target.resolve() else real_read(path)

    monkeypatch.setattr(scanner_module, "_read_bounded_file", reject_unreadable)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILES", 2)
    monkeypatch.setattr(Path, "home", lambda: home)

    definitions = scan_user_agent_definitions()

    assert [item.path for item in definitions] == [str(valid)]


def test_user_scan_uses_one_follow_policy_across_homes(tmp_path, monkeypatch):
    native_home = tmp_path / "native-home"
    extra_home = tmp_path / "extra-home"
    native_link = native_home / ".cursor" / "agents" / "native.md"
    extra_link = extra_home / ".cursor" / "agents" / "extra.md"
    target = tmp_path / "external.md"
    target.write_text("# External\n", encoding="utf-8")
    native_link.parent.mkdir(parents=True)
    extra_link.parent.mkdir(parents=True)
    try:
        native_link.symlink_to(target)
        extra_link.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: native_home)

    definitions = scan_user_agent_definitions(extra_home_roots=[extra_home])

    assert [item.path for item in definitions] == [str(native_link)]


@pytest.mark.parametrize("budget", ["file-count", "total-bytes"])
def test_user_scan_shares_budgets_with_followed_roots(tmp_path, monkeypatch, budget):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    external = tmp_path / "external"
    root.mkdir(parents=True)
    external.mkdir()
    regular = root / "a.md"
    regular.write_bytes(b"A")
    (external / "nested.md").write_bytes(b"B")
    try:
        (root / "z-linked").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)
    if budget == "file-count":
        monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILES", 1)
    else:
        monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILE_BYTES", 1)
        monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_TOTAL_BYTES", 1)

    definitions = scan_user_agent_definitions()

    assert [item.path for item in definitions] == [str(regular)]


def test_user_scan_follows_external_file_for_user_but_system_skips_links(
    tmp_path, monkeypatch
):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    regular = root / "real.md"
    regular.write_text("# Real\n", encoding="utf-8")
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    link = root / "linked.md"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(Path, "home", lambda: home)

    assert [item.path for item in scan_user_agent_definitions()] == [
        str(link),
        str(regular),
    ]

    monkeypatch.setattr(scanner_module, "is_windows_system_context", lambda: True)

    assert [item.path for item in scan_user_agent_definitions()] == [str(regular)]


def test_user_scan_enforces_byte_caps(tmp_path, monkeypatch):
    home = tmp_path / "home"
    root = home / ".cursor" / "agents"
    root.mkdir(parents=True)
    (root / "a-large.md").write_bytes(b"12345")
    (root / "b-first.md").write_bytes(b"123")
    (root / "c-over-total.md").write_bytes(b"123")
    monkeypatch.setattr(Path, "home", lambda: home)

    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_FILE_BYTES", 4)
    monkeypatch.setattr(scanner_module, "MAX_AGENT_DEFINITION_TOTAL_BYTES", 4)

    bounded = scan_user_agent_definitions()

    assert [Path(item.path).name for item in bounded] == ["b-first.md"]
