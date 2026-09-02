"""Behavior tests for bounded, technique-generic hidden-space discovery."""

import os
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from runlayer_cli.scan import hidden_space_sweep as sweep_module
from runlayer_cli.scan.hidden_space_sweep import (
    is_hidden_container_path,
    scan_hidden_spaces,
)


def test_scan_hidden_spaces_finds_files_below_arbitrarily_named_hidden_directory(
    tmp_path: Path,
):
    hidden_root = tmp_path / ".cache" / ".gtk-icon-state"
    hidden_root.mkdir(parents=True)
    hidden_file = hidden_root / "state" / "payload.dat"
    hidden_file.parent.mkdir()
    hidden_file.write_text("payload")
    ordinary_file = tmp_path / "Downloads" / "payload.dat"
    ordinary_file.parent.mkdir()
    ordinary_file.write_text("payload")

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [hidden_file]


def test_scan_hidden_spaces_includes_files_directly_in_namespace_root(
    tmp_path: Path,
):
    direct_file = tmp_path / ".cache" / "disguised-skill.dat"
    direct_file.parent.mkdir()
    direct_file.write_text("candidate")

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [direct_file]


def test_scan_hidden_spaces_truncates_when_time_budget_expires(
    monkeypatch,
    tmp_path: Path,
):
    hidden_root = tmp_path / ".cache" / ".updater-state"
    hidden_root.mkdir(parents=True)
    (hidden_root / "payload.dat").write_text("payload")
    monotonic_calls = 0

    def monotonic() -> float:
        nonlocal monotonic_calls
        monotonic_calls += 1
        return 0.0 if monotonic_calls == 1 else 2.0

    monkeypatch.setattr(
        sweep_module,
        "time",
        SimpleNamespace(monotonic=monotonic),
        raising=False,
    )

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=True,
        temp_roots=(),
        time_budget_s=1.0,
    )

    assert result.truncated is True


def test_scan_hidden_spaces_reports_package_roots_without_collecting_every_file(
    tmp_path: Path,
):
    hidden_root = tmp_path / ".local" / "share" / ".updater-state"
    node_modules = hidden_root / "lib" / "node_modules"
    node_modules.mkdir(parents=True)
    python_env = hidden_root / "runtime"
    python_env.mkdir()
    (python_env / "pyvenv.cfg").write_text("home = /usr/bin")
    (hidden_root / "noise.bin").write_bytes(b"noise")

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=False,
        temp_roots=(),
    )

    assert result.files == []
    assert result.node_modules_paths == [node_modules]
    assert result.python_env_roots == [python_env]


def test_scan_hidden_spaces_includes_main_crawl_skip_roots(tmp_path: Path):
    skipped_file = tmp_path / "vendor" / "renamed-state" / "payload.dat"
    skipped_file.parent.mkdir(parents=True)
    skipped_file.write_text("payload")

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [skipped_file]


def test_container_path_classification_uses_hidden_technique_not_directory_name():
    assert is_hidden_container_path(
        "/var/tmp/.updater-state/lib/node_modules/tool/package.json",
        root_path="/var/tmp",
    )
    assert is_hidden_container_path(
        "/var/tmp/.gtk-icon-cache-bak/state/profile.dat",
        root_path="/var/tmp",
    )
    assert not is_hidden_container_path(
        "/var/tmp/build/output.dat",
        root_path="/var/tmp",
    )
    assert not is_hidden_container_path(
        "/var/tmp/.git/objects/payload.dat",
        root_path="/var/tmp",
    )


def test_representative_home_bounds_venvs_without_truncating_shared_sweep(
    tmp_path: Path,
):
    for namespace in (tmp_path / ".cache", tmp_path / ".local" / "share"):
        for index in range(10):
            app_root = namespace / f"app-{index}" / "state"
            app_root.mkdir(parents=True)
            for item in range(10):
                (app_root / f"entry-{item}.dat").write_text("noise")
    for index in range(20):
        env_root = tmp_path / ".cache" / f"runtime-{index}"
        env_root.mkdir()
        (env_root / "pyvenv.cfg").write_text("home = /usr/bin")

    started_at = time.monotonic()
    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=False,
        temp_roots=(),
    )
    elapsed = time.monotonic() - started_at

    assert elapsed < 60
    assert len(result.python_env_roots) == 16
    assert result.python_env_roots_truncated is True
    assert result.truncated is False


def test_node_modules_output_cap_does_not_truncate_shared_sweep(
    tmp_path: Path,
    monkeypatch,
):
    first = tmp_path / ".cache" / "a-package" / "node_modules"
    second = tmp_path / ".cache" / "b-package" / "node_modules"
    first.mkdir(parents=True)
    second.mkdir(parents=True)
    skill = tmp_path / ".cache" / "z-skill" / "skill.dat"
    skill.parent.mkdir(parents=True)
    skill.write_text("candidate")
    python_env = tmp_path / ".cache" / "z-runtime"
    python_env.mkdir()
    (python_env / "pyvenv.cfg").write_text("home = /usr/bin")
    monkeypatch.setattr(sweep_module, "MAX_NODE_MODULES_PATHS", 1)

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert len(result.node_modules_paths) == 1
    assert result.node_modules_paths_truncated is True
    assert skill in result.files
    assert result.python_env_roots == [python_env]
    assert result.truncated is False


def test_known_benign_dot_roots_are_pruned_after_direct_structure_checks(
    tmp_path: Path,
):
    hidden_skill = tmp_path / ".git" / "objects" / "skill.md"
    hidden_skill.parent.mkdir(parents=True)
    hidden_skill.write_text(
        "---\nname: ignored\ndescription: Ignored content\n---\n# Ignored"
    )
    node_modules = tmp_path / ".npm" / "node_modules"
    node_modules.mkdir(parents=True)
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "pyvenv.cfg").write_text("home = /usr/bin")

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert hidden_skill not in result.files
    assert result.node_modules_paths == [node_modules]
    assert result.python_env_roots == [venv]
    assert result.truncated is False


@pytest.mark.parametrize("package_directory", ["site-packages", "dist-packages"])
def test_package_directory_shape_discovers_relocated_env_without_pyvenv(
    tmp_path: Path,
    package_directory: str,
):
    env_root = tmp_path / ".updater-state" / "runtime"
    (env_root / "lib" / "python3.13" / package_directory).mkdir(parents=True)

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        temp_roots=(),
    )

    assert result.python_env_roots == [env_root]


def test_owned_ordinary_temp_prefix_reports_package_roots(tmp_path: Path):
    home = tmp_path / "home"
    home.mkdir()
    temp_root = tmp_path / "temp"
    node_modules = temp_root / "ordinary-prefix" / "lib" / "node_modules"
    node_modules.mkdir(parents=True)
    env_root = temp_root / "ordinary-runtime"
    (env_root / "pyvenv.cfg").parent.mkdir(parents=True)
    (env_root / "pyvenv.cfg").write_text("home = /usr/bin")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        temp_roots=(temp_root,),
    )

    assert result.node_modules_paths == [node_modules]
    assert result.python_env_roots == [env_root]


def test_symlinked_namespace_follows_external_directory_for_user(tmp_path: Path):
    home = tmp_path / "home"
    home.mkdir()
    external = tmp_path / "external"
    escaped_file = external / "app" / "payload.dat"
    escaped_file.parent.mkdir(parents=True)
    escaped_file.write_text("payload")
    cache = home / ".cache"
    try:
        cache.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [escaped_file]


def test_nested_symlinked_namespace_ancestor_follows_external_directory(
    tmp_path: Path,
):
    home = tmp_path / "home"
    home.mkdir()
    outside = tmp_path / "outside"
    hidden_root = outside / "share" / ".updater-state"
    hidden_root.mkdir(parents=True)
    (hidden_root / "payload.dat").write_text("payload")
    try:
        (home / ".local").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [hidden_root / "payload.dat"]


def test_non_hidden_namespace_symlink_follows_external_root(tmp_path: Path):
    home = tmp_path / "home"
    home.mkdir()
    external = tmp_path / "external"
    escaped_file = external / "Local" / "app" / "payload.dat"
    escaped_file.parent.mkdir(parents=True)
    escaped_file.write_text("payload")
    try:
        (home / "AppData").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Windows",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [escaped_file]


def test_hidden_space_bfs_follows_external_directory_and_file_targets(
    tmp_path: Path,
):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    external_directory = tmp_path / "external-directory"
    nested_skill = external_directory / "nested" / "skill.dat"
    nested_skill.parent.mkdir(parents=True)
    nested_skill.write_text("nested")
    external_file = tmp_path / "external-file.dat"
    external_file.write_text("direct")
    try:
        (hidden_root / "directory-link").symlink_to(
            external_directory,
            target_is_directory=True,
        )
        (hidden_root / "file-link.dat").symlink_to(external_file)
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert sorted(result.files) == sorted([external_file, nested_skill])


def test_hidden_space_symlink_following_stays_disabled_for_system(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    home.mkdir()
    external = tmp_path / "external"
    escaped_file = external / "payload.dat"
    escaped_file.parent.mkdir()
    escaped_file.write_text("payload")
    try:
        (home / ".cache").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(sweep_module, "is_windows_system_context", lambda: True)

    result = scan_hidden_spaces(
        home=home,
        system="Windows",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == []


def test_hidden_space_follows_linked_home_for_user(tmp_path: Path):
    home = tmp_path / "home"
    external = tmp_path / "external-home"
    payload = external / ".cache" / "app" / "payload.dat"
    payload.parent.mkdir(parents=True)
    payload.write_text("payload")
    try:
        home.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [home / ".cache" / "app" / "payload.dat"]


def test_hidden_space_system_context_rejects_linked_home(tmp_path: Path, monkeypatch):
    home = tmp_path / "home"
    external = tmp_path / "external-home"
    payload = external / "AppData" / "Local" / "app" / "payload.dat"
    payload.parent.mkdir(parents=True)
    payload.write_text("payload")
    try:
        home.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(sweep_module, "is_windows_system_context", lambda: True)

    result = scan_hidden_spaces(
        home=home,
        system="Windows",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == []


@pytest.mark.parametrize("root_kind", ["home", "temp"])
def test_hidden_space_system_rejects_linked_root_component_before_access(
    tmp_path: Path,
    monkeypatch,
    root_kind: str,
):
    outside_parent = tmp_path / "outside-parent"
    target_root = outside_parent / "admitted-root"
    target_root.mkdir(parents=True)
    linked_parent = tmp_path / "linked-parent"
    try:
        linked_parent.symlink_to(outside_parent, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    admitted_root = linked_parent / "admitted-root"
    safe_home = tmp_path / "safe-home"
    safe_home.mkdir()
    monkeypatch.setattr(sweep_module, "is_windows_system_context", lambda: True)
    target_stats = []
    target_scandirs = []
    real_stat = Path.stat
    real_scandir = sweep_module.os.scandir

    def track_target_stat(path, *args, **kwargs):
        if path in {admitted_root, target_root}:
            target_stats.append(path)
        return real_stat(path, *args, **kwargs)

    def track_target_scandir(path):
        if Path(path) in {admitted_root, target_root}:
            target_scandirs.append(Path(path))
        return real_scandir(path)

    monkeypatch.setattr(Path, "stat", track_target_stat)
    monkeypatch.setattr(sweep_module.os, "scandir", track_target_scandir)

    result = scan_hidden_spaces(
        home=admitted_root if root_kind == "home" else safe_home,
        system="Windows",
        extra_home_roots=(),
        temp_roots=(admitted_root,) if root_kind == "temp" else (),
    )

    assert result.files == []
    assert target_stats == []
    assert target_scandirs == []


def test_hidden_space_linked_home_walks_claimed_target_after_retarget(
    tmp_path: Path,
    monkeypatch,
):
    first_target = tmp_path / "first-target"
    (first_target / ".cache").mkdir(parents=True)
    second_target = tmp_path / "second-target"
    escaped = second_target / ".cache" / "app" / "escaped.dat"
    escaped.parent.mkdir(parents=True)
    escaped.write_text("escaped")
    home = tmp_path / "home"
    try:
        home.symlink_to(first_target, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    real_claim = sweep_module.SymlinkFollowPolicy.claim

    def retarget_after_claim(policy, target):
        claimed = real_claim(policy, target)
        if target == first_target and claimed:
            home.unlink()
            home.symlink_to(second_target, target_is_directory=True)
        return claimed

    monkeypatch.setattr(
        sweep_module.SymlinkFollowPolicy,
        "claim",
        retarget_after_claim,
    )

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == []


def test_hidden_space_linked_homes_count_toward_follow_cap(tmp_path: Path, monkeypatch):
    native_home = tmp_path / "native-home"
    native_home.mkdir()
    linked_homes = []
    expected = []
    try:
        for index in range(2):
            target = tmp_path / f"target-{index}"
            payload = target / ".cache" / "app" / "payload.dat"
            payload.parent.mkdir(parents=True)
            payload.write_text(str(index))
            linked_home = tmp_path / f"linked-home-{index}"
            linked_home.symlink_to(target, target_is_directory=True)
            linked_homes.append(linked_home)
            expected.append(linked_home / ".cache" / "app" / "payload.dat")
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(sweep_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

    result = scan_hidden_spaces(
        home=native_home,
        system="Linux",
        extra_home_roots=linked_homes,
        include_files=True,
        temp_roots=(),
    )

    assert result.files == expected[:1]


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFO unavailable")
def test_non_directory_home_link_does_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch,
):
    native_home = tmp_path / "native-home"
    native_home.mkdir()
    special_target = tmp_path / "special"
    os.mkfifo(special_target)
    special_home = tmp_path / "a-special-home"
    special_home.symlink_to(special_target)
    valid_target = tmp_path / "valid-target"
    payload = valid_target / ".cache" / "app" / "payload.dat"
    payload.parent.mkdir(parents=True)
    payload.write_text("payload")
    valid_home = tmp_path / "b-valid-home"
    valid_home.symlink_to(valid_target, target_is_directory=True)
    monkeypatch.setattr(sweep_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

    result = scan_hidden_spaces(
        home=native_home,
        system="Linux",
        extra_home_roots=(special_home, valid_home),
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [valid_home / ".cache" / "app" / "payload.dat"]


def test_hidden_space_follows_relocated_and_beyond_depth_targets(
    tmp_path: Path,
):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    relocated = home / "ordinary" / "relocated.dat"
    relocated.parent.mkdir()
    relocated.write_text("relocated")
    beyond_depth = home / "deep"
    for index in range(sweep_module.MAX_DEPTH):
        beyond_depth /= str(index)
    beyond_depth.mkdir(parents=True)
    beyond_file = beyond_depth / "beyond.dat"
    beyond_file.write_text("follow")
    beyond_root = hidden_root / "deep"
    for index in range(sweep_module.MAX_DEPTH + 1):
        beyond_root /= str(index)
    beyond_root.mkdir(parents=True)
    beyond_root_file = beyond_root / "beyond-root.dat"
    beyond_root_file.write_text("follow directory")
    try:
        (hidden_root / "relocated-link.dat").symlink_to(relocated)
        (hidden_root / "beyond-link.dat").symlink_to(beyond_file)
        (hidden_root / "beyond-directory").symlink_to(
            beyond_root,
            target_is_directory=True,
        )
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert sorted(result.files) == sorted([relocated, beyond_file, beyond_root_file])


def test_hidden_space_follows_in_home_target_outside_walked_paths(tmp_path: Path):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    relocated = home / "ordinary" / "payload.dat"
    relocated.parent.mkdir()
    relocated.write_text("payload")
    try:
        (hidden_root / "relocated.dat").symlink_to(relocated)
    except OSError:
        pytest.skip("file symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [relocated]


def test_hidden_space_linked_pyvenv_records_target_env_root(tmp_path: Path):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    external_env = tmp_path / "external-env"
    external_env.mkdir()
    target = external_env / "pyvenv.cfg"
    target.write_text("home = /usr/bin")
    try:
        (hidden_root / "pyvenv.cfg").symlink_to(target)
    except OSError:
        pytest.skip("file symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=False,
        temp_roots=(),
    )

    assert result.python_env_roots == [external_env]


def test_hidden_space_skips_broken_ancestor_and_loop_links(tmp_path: Path):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    ordinary_file = home / "ordinary" / "not-hidden.dat"
    ordinary_file.parent.mkdir()
    ordinary_file.write_text("not hidden")
    try:
        (hidden_root / "ancestor").symlink_to(home, target_is_directory=True)
        (hidden_root / "broken").symlink_to(tmp_path / "missing")
        loop = hidden_root / "loop"
        loop.symlink_to(loop)
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == []


def test_hidden_space_follow_cap_counts_unique_realpaths(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    targets = []
    for index in range(3):
        target = tmp_path / f"external-{index}.dat"
        target.write_text(str(index))
        targets.append(target)
    try:
        (hidden_root / "00-first.dat").symlink_to(targets[0])
        (hidden_root / "01-duplicate.dat").symlink_to(targets[0])
        (hidden_root / "02-second.dat").symlink_to(targets[1])
        (hidden_root / "03-third.dat").symlink_to(targets[2])
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(sweep_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 2)

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert len(result.files) == 2
    assert len({path.resolve() for path in result.files}) == 2
    assert set(result.files) <= set(targets)


def test_hidden_space_followed_frontier_shares_entry_budget(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    external = tmp_path / "external"
    external.mkdir()
    external_files = [external / f"{index}.dat" for index in range(2)]
    for path in external_files:
        path.write_text(path.name)
    try:
        (hidden_root / "external").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(sweep_module, "MAX_ENTRIES", 2)

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert len(result.files) == 1
    assert result.files[0] in external_files
    assert result.truncated is True


def test_structural_only_walk_round_robins_roots_before_global_entry_cap(
    tmp_path: Path,
    monkeypatch,
):
    heavy_root = tmp_path / ".cache" / "a-heavy"
    heavy_root.mkdir(parents=True)
    for index in range(3):
        (heavy_root / f"noise-{index}.dat").write_text("noise")
    signal_root = tmp_path / ".cache" / "z-signal"
    signal_root.mkdir(parents=True)
    (signal_root / "pyvenv.cfg").write_text("home = /usr/bin")
    monkeypatch.setattr(sweep_module, "MAX_ENTRIES", 2)

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        temp_roots=(),
    )

    assert result.python_env_roots == [signal_root]
    assert result.truncated is True


def test_root_discovery_round_robins_namespaces_before_global_cap(
    tmp_path: Path,
    monkeypatch,
):
    cache_signal = tmp_path / ".cache" / "signal"
    cache_signal.mkdir(parents=True)
    (cache_signal / "pyvenv.cfg").write_text("home = /usr/bin")
    for index in range(4):
        (tmp_path / f".noise-{index}").mkdir()
    monkeypatch.setattr(sweep_module, "MAX_ROOT_DISCOVERY_ENTRIES", 4)

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        temp_roots=(),
    )

    assert cache_signal in result.python_env_roots
    assert result.truncated is True


def test_non_directory_root_entries_do_not_starve_namespaces(
    tmp_path: Path,
    monkeypatch,
):
    (tmp_path / "noise.dat").write_text("noise")
    cache_signal = tmp_path / ".cache" / "signal"
    cache_signal.mkdir(parents=True)
    (cache_signal / "pyvenv.cfg").write_text("home = /usr/bin")
    monkeypatch.setattr(sweep_module, "MAX_ROOT_DISCOVERY_ENTRIES", 2)

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        temp_roots=(),
    )

    assert cache_signal in result.python_env_roots
    assert result.truncated is True


def test_hidden_space_walk_checkpoints_each_entry(tmp_path: Path):
    hidden_root = tmp_path / ".cache" / ".updater-state"
    hidden_root.mkdir(parents=True)
    files = []
    for index in range(16):
        path = hidden_root / f"entry-{index}.dat"
        path.write_text("noise")
        files.append(path)
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        include_files=True,
        temp_roots=(),
        checkpoint=checkpoint,
    )

    assert sorted(result.files) == sorted(files)
    assert checkpoints >= len(files)


def test_root_cap_still_walks_selected_roots(tmp_path: Path, monkeypatch):
    selected_root = tmp_path / ".cache" / "a-signal"
    selected_root.mkdir(parents=True)
    (selected_root / "pyvenv.cfg").write_text("home = /usr/bin")
    (tmp_path / ".cache" / "z-overflow").mkdir()
    monkeypatch.setattr(sweep_module, "MAX_HIDDEN_ROOTS", 1)

    result = scan_hidden_spaces(
        home=tmp_path,
        system="Linux",
        temp_roots=(),
    )

    assert result.python_env_roots == [selected_root]
    assert result.truncated is True


@pytest.mark.parametrize(
    ("source_name", "max_hidden_roots"),
    [(".cargo", sweep_module.MAX_HIDDEN_ROOTS), (".overflow", 0)],
)
def test_pruned_linked_roots_do_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    source_name: str,
    max_hidden_roots: int,
):
    home = tmp_path / "home"
    home.mkdir()
    target = tmp_path / "target"
    target.mkdir()
    try:
        (home / source_name).symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    claimed_targets: list[Path] = []
    real_claim = sweep_module.SymlinkFollowPolicy.claim

    def track_claim(policy, candidate):
        claimed_targets.append(candidate)
        return real_claim(policy, candidate)

    monkeypatch.setattr(sweep_module.SymlinkFollowPolicy, "claim", track_claim)
    monkeypatch.setattr(sweep_module, "MAX_HIDDEN_ROOTS", max_hidden_roots)

    scan_hidden_spaces(home=home, system="Linux", temp_roots=())

    assert target.resolve() not in claimed_targets


@pytest.mark.parametrize("source_name", ["node_modules", "site-packages", ".git"])
def test_pruned_linked_walk_directories_do_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    source_name: str,
):
    home = tmp_path / "home"
    hidden_root = home / ".cache" / "app"
    hidden_root.mkdir(parents=True)
    target = tmp_path / "terminal-target"
    target.mkdir()
    try:
        (hidden_root / source_name).symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    claimed_targets: list[Path] = []
    real_claim = sweep_module.SymlinkFollowPolicy.claim

    def track_claim(policy, candidate):
        claimed_targets.append(candidate)
        return real_claim(policy, candidate)

    monkeypatch.setattr(sweep_module.SymlinkFollowPolicy, "claim", track_claim)

    scan_hidden_spaces(home=home, system="Linux", temp_roots=())

    assert target.resolve() not in claimed_targets


def test_benign_link_alias_does_not_hide_later_full_root(tmp_path: Path):
    home = tmp_path / "home"
    home.mkdir()
    target = tmp_path / "target"
    payload = target / "deep" / "payload.dat"
    payload.parent.mkdir(parents=True)
    payload.write_text("payload")
    try:
        (home / ".cargo").symlink_to(target, target_is_directory=True)
        (home / ".wanted").symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=True,
        temp_roots=(),
    )

    assert result.files == [payload]


def test_trusted_temp_root_alias_is_canonicalized(tmp_path: Path):
    real_temp = tmp_path / "real-tmp"
    env_root = real_temp / ".relocated-runtime"
    env_root.mkdir(parents=True)
    (env_root / "pyvenv.cfg").write_text("home = /usr/bin")
    temp_alias = tmp_path / "tmp-alias"
    try:
        temp_alias.symlink_to(real_temp, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_hidden_spaces(
        home=tmp_path / "home",
        system="Darwin",
        temp_roots=(temp_alias,),
    )

    assert result.python_env_roots == [env_root]


def test_default_temp_aliases_do_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    home = tmp_path / "home"
    home.mkdir()
    relocated_cache = tmp_path / "relocated-cache"
    relocated_cache.mkdir()
    payload = relocated_cache / "payload.dat"
    payload.write_text("payload")
    (home / ".cache").symlink_to(relocated_cache, target_is_directory=True)

    real_temp = tmp_path / "real-temp"
    real_temp.mkdir()
    temp_alias = tmp_path / "temp-alias"
    temp_alias.symlink_to(real_temp, target_is_directory=True)
    monkeypatch.setattr(
        sweep_module,
        "_default_temp_roots",
        lambda _system: (real_temp, temp_alias),
    )
    monkeypatch.setattr(sweep_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

    result = scan_hidden_spaces(
        home=home,
        system="Darwin",
        include_files=True,
    )

    assert result.files == [payload]


def test_windows_temp_owner_requirement_fails_closed_without_identity(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    home.mkdir()
    shared_temp = tmp_path / "shared-temp"
    other_principal = shared_temp / "other-principal"
    other_principal.mkdir(parents=True)
    (other_principal / "payload.dat").write_text("payload")
    monkeypatch.delattr(sweep_module.os, "getuid", raising=False)

    result = scan_hidden_spaces(
        home=home,
        system="Windows",
        include_files=True,
        temp_roots=(shared_temp,),
    )

    assert result.files == []
