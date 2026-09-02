"""Behavior tests for the shared filesystem-scanner primitives."""

import os
import threading
from collections import deque
from collections.abc import Generator
from pathlib import Path

import pytest

from runlayer_cli.scan import scanner_primitives as scanner_primitives_module
from runlayer_cli.scan.scanner_primitives import (
    MAX_PLUGIN_NAME_LENGTH,
    MAX_PLUGIN_SOURCE_IDENTIFIER_LENGTH,
    SymlinkFollowBudget,
    SymlinkFollowPolicy,
    SymlinkLayoutResolver,
    bound_plugin_metadata,
    drain_round_robin,
    has_link_or_reparse_component,
    is_contained_real_directory,
    is_real_directory,
    iter_directory_entries,
    plugin_artifact_identifier,
    read_bounded,
    read_safe_relative_file,
)


def _tracking_generator(
    items: list[str],
    closed: list[str],
    label: str,
) -> Generator[str, None, None]:
    try:
        yield from items
    finally:
        closed.append(label)


def _inspect_and_claim(
    policy: SymlinkFollowPolicy,
    link_path: Path,
) -> Path | None:
    target = policy.inspect(link_path)
    return target if target is not None and policy.claim(target) else None


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFO unavailable")
def test_layout_resolver_non_directory_link_does_not_consume_follow_cap(
    tmp_path: Path,
):
    root = tmp_path / "root"
    root.mkdir()
    special_target = tmp_path / "special"
    os.mkfifo(special_target)
    special_link = root / "a-special"
    special_link.symlink_to(special_target)
    valid_target = tmp_path / "valid"
    valid_target.mkdir()
    valid_link = root / "b-valid"
    valid_link.symlink_to(valid_target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=(), max_followed=1)
    resolver = SymlinkLayoutResolver(
        policy=policy,
        windows_system_context=False,
    )

    assert resolver.resolve_policy_link(special_link, current=root) is None
    assert resolver.resolve_policy_link(valid_link, current=root) == valid_target


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_follows_only_targets_missing_from_scan_area(tmp_path: Path):
    scan_root = tmp_path / "home"
    scan_root.mkdir()
    in_area = scan_root / "project"
    in_area.mkdir()
    outside = tmp_path / "external"
    outside.mkdir()
    in_area_link = scan_root / "in-area"
    in_area_link.symlink_to(in_area, target_is_directory=True)
    outside_link = scan_root / "outside"
    outside_link.symlink_to(outside, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[(scan_root, None)])

    assert _inspect_and_claim(policy, in_area_link) is None
    assert _inspect_and_claim(policy, outside_link) == outside.resolve()


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_follows_in_area_targets_beyond_depth(tmp_path: Path):
    scan_root = tmp_path / "home"
    within_depth = scan_root / "project"
    beyond_depth = within_depth / "nested"
    beyond_depth.mkdir(parents=True)
    within_link = tmp_path / "within"
    within_link.symlink_to(within_depth, target_is_directory=True)
    beyond_link = tmp_path / "beyond"
    beyond_link.symlink_to(beyond_depth, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[(scan_root, 1)])

    assert _inspect_and_claim(policy, within_link) is None
    assert _inspect_and_claim(policy, beyond_link) == beyond_depth.resolve()


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_registers_followed_scan_areas(tmp_path: Path):
    followed_root = tmp_path / "followed"
    within_depth = followed_root / "nested"
    beyond_depth = within_depth / "deep"
    beyond_depth.mkdir(parents=True)
    within_link = tmp_path / "within-link"
    within_link.symlink_to(within_depth, target_is_directory=True)
    beyond_link = tmp_path / "beyond-link"
    beyond_link.symlink_to(beyond_depth, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[])

    policy.add_scan_area(followed_root, 1)

    assert _inspect_and_claim(policy, within_link) is None
    assert _inspect_and_claim(policy, beyond_link) == beyond_depth.resolve()


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_skips_ancestor_of_scan_area(tmp_path: Path):
    ancestor = tmp_path / "home"
    scan_root = ancestor / "project"
    scan_root.mkdir(parents=True)
    ancestor_link = tmp_path / "ancestor"
    ancestor_link.symlink_to(ancestor, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[(scan_root, 1)])

    assert _inspect_and_claim(policy, ancestor_link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
@pytest.mark.parametrize("relationship", ["equal", "ancestor"])
def test_layout_resolver_checks_scan_area_root_or_ancestor_as_single_directory(
    tmp_path: Path,
    relationship: str,
):
    target = tmp_path / "target"
    scan_root = target if relationship == "equal" else target / "nested"
    scan_root.mkdir(parents=True)
    source = tmp_path / "source"
    source.mkdir()
    link = source / "link"
    link.symlink_to(target, target_is_directory=True)
    walk_link = source / "walk-link"
    walk_link.symlink_to(target, target_is_directory=True)
    overflow_target = tmp_path / "overflow"
    overflow_target.mkdir()
    overflow_link = source / "overflow-link"
    overflow_link.symlink_to(overflow_target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[(scan_root, 1)], max_followed=1)
    resolver = SymlinkLayoutResolver(
        policy=policy,
        windows_system_context=False,
    )

    assert resolver.resolve_policy_link(link, current=source) is None
    assert (
        resolver.resolve_policy_link(
            link,
            current=source,
            target_is_walk_root=False,
        )
        == target.resolve()
    )
    assert resolver.resolve_policy_link(walk_link, current=source) is None
    assert (
        resolver.resolve_policy_link(
            overflow_link,
            current=source,
            target_is_walk_root=False,
        )
        is None
    )


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_layout_resolver_checks_walk_visited_target_as_single_directory(
    tmp_path: Path,
):
    target = tmp_path / "target"
    target.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    link = source / "link"
    link.symlink_to(target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[], max_followed=1)
    assert policy.claim(target)
    policy.add_scan_area(target, 0)
    resolver = SymlinkLayoutResolver(
        policy=policy,
        windows_system_context=False,
    )

    assert (
        resolver.resolve_policy_link(
            link,
            current=source,
            target_is_walk_root=False,
        )
        == target.resolve()
    )


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_covered_link_excludes_scan_area_ancestors(tmp_path: Path):
    ancestor = tmp_path / "home"
    scan_root = ancestor / "project"
    covered = scan_root / "covered"
    covered.mkdir(parents=True)
    ancestor_link = tmp_path / "ancestor-link"
    ancestor_link.symlink_to(ancestor, target_is_directory=True)
    covered_link = tmp_path / "covered-link"
    covered_link.symlink_to(covered, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[(scan_root, 1)], max_followed=0)

    assert policy.inspect_covered_link(covered_link) == covered.resolve()
    assert policy.inspect_covered_link(ancestor_link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_mark_visited_normalizes_realpath(tmp_path: Path):
    target = tmp_path / "target"
    target.mkdir()
    seed_alias = tmp_path / "seed"
    seed_alias.symlink_to(target, target_is_directory=True)
    candidate_link = tmp_path / "candidate"
    candidate_link.symlink_to(target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[])

    policy.mark_visited(seed_alias)

    assert policy.evaluate(candidate_link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_caps_followed_targets_not_seeded_visits(tmp_path: Path):
    seeded = tmp_path / "seeded"
    seeded.mkdir()
    first_target = tmp_path / "first-target"
    first_target.mkdir()
    second_target = tmp_path / "second-target"
    second_target.mkdir()
    first_link = tmp_path / "first-link"
    first_link.symlink_to(first_target, target_is_directory=True)
    second_link = tmp_path / "second-link"
    second_link.symlink_to(second_target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[], max_followed=1)
    policy.mark_visited(seeded)

    assert policy.evaluate(first_link) == first_target.resolve()
    assert policy.evaluate(second_link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_inspection_does_not_consume_follow_cap(tmp_path: Path):
    first_target = tmp_path / "first-target"
    first_target.mkdir()
    second_target = tmp_path / "second-target"
    second_target.mkdir()
    first_link = tmp_path / "first-link"
    first_link.symlink_to(first_target, target_is_directory=True)
    second_link = tmp_path / "second-link"
    second_link.symlink_to(second_target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[], max_followed=1)

    assert policy.inspect(first_link) == first_target.resolve()
    assert policy.inspect(second_link) == second_target.resolve()
    assert policy.claim(second_target) is True
    assert policy.claim(first_target) is False


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policies_share_unique_target_budget(tmp_path: Path):
    shared_target = tmp_path / "shared-target"
    shared_target.mkdir()
    distinct_target = tmp_path / "distinct-target"
    distinct_target.mkdir()
    first_link = tmp_path / "first-link"
    first_link.symlink_to(shared_target, target_is_directory=True)
    alias_link = tmp_path / "alias-link"
    alias_link.symlink_to(shared_target, target_is_directory=True)
    distinct_link = tmp_path / "distinct-link"
    distinct_link.symlink_to(distinct_target, target_is_directory=True)
    budget = SymlinkFollowBudget(1)
    first_policy = SymlinkFollowPolicy(scan_areas=[], follow_budget=budget)
    second_policy = SymlinkFollowPolicy(scan_areas=[], follow_budget=budget)

    assert first_policy.evaluate(first_link) == shared_target.resolve()
    assert second_policy.evaluate(alias_link) == shared_target.resolve()
    assert second_policy.evaluate(distinct_link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_allows_files_one_level_beyond_directory_depth(
    tmp_path: Path,
):
    scan_root = tmp_path / "scan-root"
    deepest_directory = scan_root / "within"
    deeper_directory = deepest_directory / "beyond"
    deeper_directory.mkdir(parents=True)
    covered_file = deepest_directory / "covered.md"
    covered_file.write_text("covered")
    file_link = tmp_path / "file-link"
    file_link.symlink_to(covered_file)
    directory_link = tmp_path / "directory-link"
    directory_link.symlink_to(deeper_directory, target_is_directory=True)
    policy = SymlinkFollowPolicy(
        scan_areas=[(scan_root, 1)],
        scan_area_file_depth_delta=1,
    )

    assert policy.evaluate(file_link) is None
    assert policy.evaluate(directory_link) == deeper_directory.resolve()


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_read_safe_relative_file_admits_visited_intermediate_without_capacity(
    tmp_path: Path,
):
    install_root = tmp_path / "install"
    install_root.mkdir()
    marker_target = tmp_path / "marker-target"
    marker_target.mkdir()
    manifest = marker_target / "plugin.xml"
    manifest.write_text("<plugin />")
    (install_root / "META-INF").symlink_to(
        marker_target,
        target_is_directory=True,
    )
    later_target = tmp_path / "later-target"
    later_target.mkdir()
    later_link = tmp_path / "later-link"
    later_link.symlink_to(later_target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[], max_followed=1)
    policy.mark_visited(marker_target)
    resolver = SymlinkLayoutResolver(
        policy=policy,
        windows_system_context=False,
    )

    result = read_safe_relative_file(
        install_root,
        Path("META-INF") / "plugin.xml",
        resolver=resolver,
        max_bytes=1024,
    )

    assert result == {
        "path": manifest,
        "content": manifest.read_bytes(),
    }
    assert policy.evaluate(later_link) == later_target.resolve()


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_layout_resolver_accepts_covered_final_after_intermediate_link(
    tmp_path: Path,
):
    install_root = tmp_path / "install"
    install_root.mkdir()
    relocated_layout = tmp_path / "relocated"
    covered_final = relocated_layout / "final"
    covered_final.mkdir(parents=True)
    (install_root / "layout").symlink_to(
        relocated_layout,
        target_is_directory=True,
    )
    later_target = tmp_path / "later-target"
    later_target.mkdir()
    later_link = tmp_path / "later-link"
    later_link.symlink_to(later_target, target_is_directory=True)
    policy = SymlinkFollowPolicy(
        scan_areas=[(covered_final, 0)],
        max_followed=1,
    )
    resolver = SymlinkLayoutResolver(
        policy=policy,
        windows_system_context=False,
    )

    resolved = resolver.resolve_directory(
        install_root,
        Path("layout") / "final",
        claim_final=True,
    )

    assert resolved == covered_final.resolve()
    assert policy.evaluate(later_link) == later_target.resolve()


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_skips_unreadable_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target, target_is_directory=True)
    target_realpath = os.path.realpath(target)
    real_access = os.access

    def deny_target(path: os.PathLike[str], mode: int) -> bool:
        if os.path.realpath(path) == target_realpath:
            return False
        return real_access(path, mode)

    monkeypatch.setattr(os, "access", deny_target)
    policy = SymlinkFollowPolicy(scan_areas=[])

    assert _inspect_and_claim(policy, link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_skips_broken_target(tmp_path: Path):
    link = tmp_path / "link"
    link.symlink_to(tmp_path / "missing", target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[])

    assert _inspect_and_claim(policy, link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_skips_all_links_in_windows_system_context(tmp_path: Path):
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target, target_is_directory=True)
    policy = SymlinkFollowPolicy(
        scan_areas=[],
        windows_system_context=True,
    )

    assert _inspect_and_claim(policy, link) is None


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlink_policy_atomically_claims_approved_target(tmp_path: Path):
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[])
    thread_count = 16
    barrier = threading.Barrier(thread_count)
    results: list[Path | None] = []
    results_lock = threading.Lock()

    def inspect_then_claim() -> None:
        barrier.wait()
        inspected = policy.inspect(link)
        result = (
            inspected if inspected is not None and policy.claim(inspected) else None
        )
        with results_lock:
            results.append(result)

    threads = [threading.Thread(target=inspect_then_claim) for _ in range(thread_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert results.count(target.resolve()) == 1
    assert results.count(None) == thread_count - 1


def test_link_component_check_stops_at_linked_parent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    linked_parent = tmp_path / "linked"
    leaf = linked_parent / "target"
    inspected: list[Path] = []

    def is_link(path: Path) -> bool:
        inspected.append(path)
        if path == leaf:
            raise AssertionError("descendant inspected before linked parent")
        return path == linked_parent

    monkeypatch.setattr(
        scanner_primitives_module,
        "is_link_or_reparse",
        is_link,
    )

    assert has_link_or_reparse_component(leaf) is True
    assert inspected[-1] == linked_parent


def test_drain_round_robin_interleaves_fairly():
    visited: list[tuple[str, str]] = []
    closed: list[str] = []
    iterators = deque(
        [
            ("a", _tracking_generator(["a1", "a2"], closed, "a")),
            ("b", _tracking_generator(["b1"], closed, "b")),
        ]
    )

    consumed = drain_round_robin(
        iterators,
        visit=lambda context, item: visited.append((context, item)),
    )

    assert consumed == 3
    assert visited == [("a", "a1"), ("b", "b1"), ("a", "a2")]
    assert sorted(closed) == ["a", "b"]


def test_drain_round_robin_closes_suspended_generators_at_max_entries():
    closed: list[str] = []
    iterators = deque(
        [
            ("a", _tracking_generator(["a1", "a2"], closed, "a")),
            ("b", _tracking_generator(["b1", "b2"], closed, "b")),
        ]
    )

    consumed = drain_round_robin(
        iterators,
        visit=lambda _context, _item: None,
        max_entries=2,
    )

    assert consumed == 2
    assert sorted(closed) == ["a", "b"]


def test_drain_round_robin_closes_suspended_generators_on_should_stop():
    closed: list[str] = []
    visits = 0

    def visit(_context: str, _item: str) -> None:
        nonlocal visits
        visits += 1

    iterators = deque(
        [
            ("a", _tracking_generator(["a1", "a2"], closed, "a")),
            ("b", _tracking_generator(["b1", "b2"], closed, "b")),
        ]
    )

    consumed = drain_round_robin(
        iterators,
        visit=visit,
        should_stop=lambda: visits >= 2,
    )

    assert consumed == 2
    assert sorted(closed) == ["a", "b"]


def test_drain_round_robin_closes_generators_when_visit_raises():
    closed: list[str] = []

    def visit(_context: str, _item: str) -> None:
        raise RuntimeError("boom")

    iterators = deque(
        [("a", _tracking_generator(["a1", "a2"], closed, "a"))],
    )

    try:
        drain_round_robin(iterators, visit=visit)
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected RuntimeError")

    assert closed == ["a"]


def test_drain_round_robin_checkpoint_runs_per_item():
    checkpoints: list[int] = []
    iterators = deque(
        [("a", _tracking_generator(["a1", "a2"], [], "a"))],
    )

    drain_round_robin(
        iterators,
        visit=lambda _context, _item: None,
        checkpoint=lambda: checkpoints.append(1),
    )

    assert len(checkpoints) == 2


def test_is_real_directory_accepts_directories_only(tmp_path: Path):
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    regular_file = tmp_path / "file.txt"
    regular_file.write_text("content")

    assert is_real_directory(real_dir) is True
    assert is_real_directory(regular_file) is False
    assert is_real_directory(tmp_path / "missing") is False


def test_is_real_directory_rejects_symlinked_directories(tmp_path: Path):
    if os.name == "nt":
        return
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real_dir)

    assert is_real_directory(link) is False


def test_is_contained_real_directory_accepts_real_descendants(tmp_path: Path):
    home = tmp_path / "home"
    candidate = home / "nested" / "plugins"
    candidate.mkdir(parents=True)

    assert is_contained_real_directory(home, candidate) is True
    assert is_contained_real_directory(home, home) is True


def test_is_contained_real_directory_rejects_escape_and_symlink_components(
    tmp_path: Path,
):
    home = tmp_path / "home"
    home.mkdir()
    outside = tmp_path / "outside"
    (outside / "plugins").mkdir(parents=True)

    assert is_contained_real_directory(home, outside / "plugins") is False
    assert (
        is_contained_real_directory(home, home / "nested" / ".." / "plugins") is False
    )

    if os.name != "nt":
        (home / "linked").symlink_to(outside, target_is_directory=True)
        assert is_contained_real_directory(home, home / "linked" / "plugins") is False


def test_iter_directory_entries_treats_unreadable_directory_as_empty(tmp_path: Path):
    assert list(iter_directory_entries(tmp_path / "missing")) == []

    (tmp_path / "child").mkdir()
    assert [entry.name for entry in iter_directory_entries(tmp_path)] == ["child"]


@pytest.mark.skipif(os.name == "nt", reason="POSIX FIFO regression")
def test_read_bounded_rejects_fifo_without_waiting_for_writer(tmp_path: Path):
    fifo = tmp_path / "package.json"
    os.mkfifo(fifo)
    values: list[bytes | None] = []
    completed = threading.Event()

    def read_fifo() -> None:
        values.append(read_bounded(fifo, max_bytes=1024))
        completed.set()

    reader = threading.Thread(target=read_fifo, daemon=True)
    reader.start()
    returned_without_writer = completed.wait(timeout=0.5)

    if not returned_without_writer:
        writer = threading.Thread(
            target=lambda: os.close(os.open(fifo, os.O_WRONLY)),
            daemon=True,
        )
        writer.start()
        assert completed.wait(timeout=1), "failed to release blocked FIFO reader"
        writer.join(timeout=1)
    reader.join(timeout=1)

    assert returned_without_writer
    assert values == [None]


def test_plugin_artifact_identifier_preserves_scanner_identity_contract():
    assert (
        plugin_artifact_identifier(
            "jetbrains_plugin",
            "com.github.copilot",
            "1.5.0",
        )
        == "a128fe45ea788ef3468047ad0175a0fc62806817360a3124b7b93f3d7990905f"
    )
    assert (
        plugin_artifact_identifier(
            "vscode_extension",
            "github.copilot",
            "1.250.0",
        )
        == "095ed7584a5aeca3f59cdc2a728cdd5f6677065296a3e3f23c496e35415d2a35"
    )
    assert (
        plugin_artifact_identifier(
            "jetbrains_plugin",
            "com.example.none",
            None,
        )
        == "39ab4d045568a1722751edf1d7564097792e55641cb80eec0842a20d5686494f"
    )
    assert (
        plugin_artifact_identifier(
            "vscode_extension",
            "example.none",
            None,
        )
        == "3c95b48e2cc99bcd1f9c048758cc56c4b2770bf6a2758b8e1bfe7f54ea0f291f"
    )


def test_bound_plugin_metadata_truncates_display_fields():
    bounded = bound_plugin_metadata(
        source_identifier="publisher.extension",
        name="n" * (MAX_PLUGIN_NAME_LENGTH + 10),
        version=None,
        author=None,
    )

    assert bounded is not None
    assert bounded["name"] == "n" * MAX_PLUGIN_NAME_LENGTH
    assert bounded["version"] is None
    assert bounded["author"] is None


def test_bound_plugin_metadata_rejects_overlong_source_identifier():
    assert (
        bound_plugin_metadata(
            source_identifier="s" * (MAX_PLUGIN_SOURCE_IDENTIFIER_LENGTH + 1),
            name="name",
            version="1.0",
            author="author",
        )
        is None
    )
