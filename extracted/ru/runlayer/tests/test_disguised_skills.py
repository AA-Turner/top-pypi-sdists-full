"""Behavior tests for the bounded disguised-skill probe."""

import hashlib
import os
from pathlib import Path
from types import SimpleNamespace

import pytest
import structlog

from runlayer_cli.scan import disguised_skills as disguised_skills_module
from runlayer_cli.scan.disguised_skills import scan_disguised_skills
from runlayer_cli.scan.hidden_space_sweep import scan_hidden_spaces
from runlayer_cli.scan.skill_scanner import _scan_skill_md_dir


SKILL_CONTENT = """\
---
name: deploy
description: Deploy safely
---
# Deploy

Follow the deployment runbook.
"""


@pytest.mark.parametrize(
    "hidden_directory",
    [".mozilla-profile-bak", ".gtk-icon-cache-bak"],
)
def test_probe_finds_skill_in_generically_hidden_cache_directory(
    tmp_path: Path,
    hidden_directory: str,
):
    hidden_root = tmp_path / ".cache" / hidden_directory
    hidden_root.mkdir(parents=True)
    skill = hidden_root / ".state" / "profile.dat"
    skill.parent.mkdir()
    skill.write_text(SKILL_CONTENT)

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


@pytest.mark.parametrize("suffix", [".dat", ".js", ".bin", ".tmp"])
def test_disguised_skill_reuses_normal_skill_content_identity(
    tmp_path: Path, suffix: str
):
    skill_content = SKILL_CONTENT.replace("name: deploy", f"name: deploy-{suffix[1:]}")
    normal_dir = tmp_path / ".claude" / "skills" / "deploy"
    normal_dir.mkdir(parents=True)
    (normal_dir / "SKILL.md").write_text(skill_content)
    cache_dir = (
        tmp_path
        / "Library"
        / "Caches"
        / "Google"
        / "Chrome"
        / "Default"
        / "Cache"
        / "Cache_Data"
    )
    cache_dir.mkdir(parents=True)
    disguised_path = cache_dir / f"f_000123{suffix}"
    disguised_path.write_text(skill_content)

    [disguised] = scan_disguised_skills(
        home=tmp_path,
        normal_skill_paths=[normal_dir],
    )
    normal = _scan_skill_md_dir(normal_dir, scope="global", tool="claude_code")

    assert normal is not None
    assert disguised.identifier == normal.identifier
    assert disguised.path == str(disguised_path)
    assert disguised.scope == "user"
    assert disguised.tool == "browser_cache"
    assert [file.title for file in disguised.files] == ["SKILL.md"]


def test_probe_normalizes_each_normal_skill_path_once(monkeypatch, tmp_path: Path):
    candidates = []
    for index in range(3):
        candidate = tmp_path / ".cache" / f"candidate-{index}.dat"
        candidate.parent.mkdir(exist_ok=True)
        candidate.write_text("noise")
        candidates.append(candidate)
    normal_skill_paths = [
        tmp_path / ".claude" / "skills" / f"skill-{index}" for index in range(4)
    ]
    normalized_skill_paths: list[Path] = []
    real_abspath = os.path.abspath

    def track_skill_normalization(path: os.PathLike[str] | str) -> str:
        candidate = Path(path)
        if candidate in normal_skill_paths:
            normalized_skill_paths.append(candidate)
        return real_abspath(path)

    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())
    monkeypatch.setattr(
        disguised_skills_module.os.path,
        "abspath",
        track_skill_normalization,
    )

    assert (
        scan_disguised_skills(
            home=tmp_path,
            hidden_candidates=candidates,
            normal_skill_paths=normal_skill_paths,
        )
        == []
    )
    assert normalized_skill_paths == normal_skill_paths


@pytest.mark.parametrize("use_relative_skill_path", [False, True])
def test_normal_skill_coverage_uses_path_component_boundaries(
    monkeypatch,
    tmp_path: Path,
    use_relative_skill_path: bool,
):
    normal_skill = tmp_path / "a" / "b"
    normal_skill.mkdir(parents=True)
    covered_candidate = normal_skill / "cached-copy.dat"
    covered_candidate.write_text(SKILL_CONTENT)
    sibling_candidate = tmp_path / "a" / "bc" / "cached-copy.dat"
    sibling_candidate.parent.mkdir()
    sibling_candidate.write_text(SKILL_CONTENT.replace("name: deploy", "name: sibling"))
    normal_skill_path = Path("a/b") if use_relative_skill_path else normal_skill
    if use_relative_skill_path:
        monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=[normal_skill, covered_candidate, sibling_candidate],
        normal_skill_paths=[normal_skill_path],
    )

    assert [artifact.path for artifact in artifacts] == [str(sibling_candidate)]


def test_probe_returns_partial_results_when_time_budget_expires(
    monkeypatch,
    tmp_path: Path,
):
    candidates = []
    for index in range(2):
        candidate = tmp_path / ".cache" / f"skill-{index}.dat"
        candidate.parent.mkdir(exist_ok=True)
        candidate.write_text(
            SKILL_CONTENT.replace("name: deploy", f"name: deploy-{index}")
        )
        candidates.append(candidate)
    monotonic_calls = 0

    def monotonic() -> float:
        nonlocal monotonic_calls
        monotonic_calls += 1
        return 0.0 if monotonic_calls <= 2 else 2.0

    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())
    monkeypatch.setattr(
        disguised_skills_module,
        "time",
        SimpleNamespace(monotonic=monotonic),
        raising=False,
    )

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=candidates,
        time_budget_s=1.0,
    )

    assert [artifact.path for artifact in artifacts] == [str(candidates[0])]


def test_probe_rejects_benign_files_and_stays_inside_allowlist(tmp_path: Path):
    cache_dir = (
        tmp_path
        / "AppData"
        / "Local"
        / "Microsoft"
        / "Edge"
        / "User Data"
        / "Default"
        / "Cache"
    )
    cache_dir.mkdir(parents=True)
    (cache_dir / "binary.bin").write_bytes(b"\x00\xff\x10\x80")
    (cache_dir / "random.json").write_text("ordinary browser cache text")
    extensionless = cache_dir / "cached-skill"
    extensionless.write_text(SKILL_CONTENT)
    outside = tmp_path / "Downloads" / "hidden.js"
    outside.parent.mkdir()
    outside.write_text(SKILL_CONTENT)

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(extensionless)]


def test_probe_finds_late_extensionless_skill_in_noisy_warm_cache(
    monkeypatch, tmp_path: Path
):
    cache_dir = tmp_path / ".cache" / "chromium" / "Default" / "Cache"
    cache_dir.mkdir(parents=True)
    for index in range(4):
        (cache_dir / f"{index}-cache.dat").write_bytes(b"x" * 550)
    skill = cache_dir / "late-extensionless-skill"
    skill.write_text(SKILL_CONTENT)
    sniff_budget = disguised_skills_module.MAX_CANDIDATE_SNIFF_BYTES
    monkeypatch.setattr(disguised_skills_module, "MAX_CANDIDATES", 1)
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_TOTAL_CANDIDATE_BYTES",
        (4 * sniff_budget) + len(SKILL_CONTENT.encode()),
    )

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_probe_charges_only_sniff_bytes_for_benign_candidate(
    monkeypatch, tmp_path: Path
):
    cache_dir = tmp_path / ".cache" / "chromium" / "Default" / "Cache"
    cache_dir.mkdir(parents=True)
    (cache_dir / "0-cache.bin").write_bytes(b"x" * 32)
    skill = cache_dir / "1-skill.yaml"
    skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_TOTAL_CANDIDATE_BYTES",
        len(SKILL_CONTENT.encode()) + 16,
    )

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_probe_skips_oversized_candidate_and_finds_small_skill_in_other_root(
    monkeypatch, tmp_path: Path
):
    large_cache = tmp_path / ".cache" / "google-chrome" / "Default" / "Cache"
    large_cache.mkdir(parents=True)
    (large_cache / "too-large.dat").write_text("---\n" + ("x" * 2048))
    small_cache = tmp_path / ".cache" / "microsoft-edge" / "Default" / "Cache"
    small_cache.mkdir(parents=True)
    skill = small_cache / "skill.dat"
    skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_TOTAL_CANDIDATE_BYTES",
        len(SKILL_CONTENT.encode()),
    )

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_probe_prefilters_oversized_candidate_before_secure_open(
    monkeypatch,
    tmp_path: Path,
):
    candidate = tmp_path / ".cache" / "oversized.dat"
    candidate.parent.mkdir()
    candidate.write_bytes(b"x" * (disguised_skills_module.MAX_CANDIDATE_BYTES + 1))
    secure_open_called = False

    def track_secure_open(_candidate: Path):
        nonlocal secure_open_called
        secure_open_called = True
        raise AssertionError("oversized candidate reached secure open")

    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())
    monkeypatch.setattr(disguised_skills_module, "_open_candidate", track_secure_open)

    assert (
        scan_disguised_skills(
            home=tmp_path,
            hidden_candidates=[candidate],
        )
        == []
    )
    assert secure_open_called is False


def test_probe_logs_bounded_work_stats(monkeypatch, tmp_path: Path):
    candidate = tmp_path / ".cache" / "noise.dat"
    candidate.parent.mkdir()
    candidate.write_text("noise")
    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())

    with structlog.testing.capture_logs() as logs:
        assert (
            scan_disguised_skills(
                home=tmp_path,
                hidden_candidates=[candidate],
            )
            == []
        )

    [event] = [
        item for item in logs if item["event"] == "Disguised skill probe complete"
    ]
    assert event["directories"] == 0
    assert event["entries"] == 0
    assert event["candidates"] == 0
    assert event["bytes_read"] == len("noise")
    assert event["truncated"] is False
    assert event["elapsed_ms"] >= 0


def test_probe_truncation_closes_suspended_candidate_iterators(
    monkeypatch, tmp_path: Path
):
    """Budget exhaustion mid-scan must close every candidate generator."""
    for browser in ("google-chrome", "microsoft-edge"):
        cache_dir = tmp_path / ".cache" / browser / "Default" / "Cache"
        cache_dir.mkdir(parents=True)
        (cache_dir / "0-plausible.dat").write_text("---\ninvalid")
        (cache_dir / "1-plausible.dat").write_text("---\ninvalid")

    opened: list[Path] = []
    closed: list[Path] = []
    real_candidate_paths = disguised_skills_module._candidate_paths

    def tracking_candidate_paths(
        root,
        *,
        budget,
        checkpoint,
        symlink_policy,
        seen_directories,
    ):
        opened.append(root)
        try:
            yield from real_candidate_paths(
                root,
                budget=budget,
                checkpoint=checkpoint,
                symlink_policy=symlink_policy,
                seen_directories=seen_directories,
            )
        finally:
            closed.append(root)

    monkeypatch.setattr(
        disguised_skills_module, "_candidate_paths", tracking_candidate_paths
    )
    monkeypatch.setattr(disguised_skills_module, "MAX_CANDIDATES", 1)

    assert scan_disguised_skills(home=tmp_path) == []
    assert len(opened) == 2
    assert sorted(closed) == sorted(opened)


def test_probe_shares_candidate_budget_across_roots(monkeypatch, tmp_path: Path):
    noisy_cache = tmp_path / ".cache" / "google-chrome" / "Default" / "Cache"
    noisy_cache.mkdir(parents=True)
    (noisy_cache / "0-random.dat").write_text("random")
    (noisy_cache / "1-random.dat").write_text("random")
    other_cache = tmp_path / ".cache" / "microsoft-edge" / "Default" / "Cache"
    other_cache.mkdir(parents=True)
    skill = other_cache / "0-skill.dat"
    skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(disguised_skills_module, "MAX_CANDIDATES", 2)

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_probe_reaches_late_firefox_root_despite_chrome_profile_flood(
    monkeypatch, tmp_path: Path
):
    """A profile-heavy early browser family must not starve later allowlist
    roots of the shared ``MAX_PROBE_ROOTS`` cap."""
    chrome_base = tmp_path / "Library" / "Application Support" / "Google" / "Chrome"
    for profile in range(6):
        for subtree in (
            "Cache",
            "Code Cache",
            "Service Worker/CacheStorage",
            "Local Extension Settings",
        ):
            (chrome_base / f"Profile {profile}" / subtree).mkdir(parents=True)
    firefox_storage = (
        tmp_path
        / "Library"
        / "Application Support"
        / "Firefox"
        / "Profiles"
        / "abc.default"
        / "storage"
    )
    firefox_storage.mkdir(parents=True)
    skill = firefox_storage / "hidden-skill.dat"
    skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(disguised_skills_module, "MAX_PROBE_ROOTS", 8)

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_probe_root_cap_shared_fairly_across_homes(monkeypatch, tmp_path: Path):
    """Roots from ``extra_home_roots`` (WSL) homes must not be starved by a
    root-heavy native home."""
    native_home = tmp_path / "native"
    chrome_base = native_home / ".config" / "google-chrome"
    for profile in range(6):
        base = chrome_base / f"Profile {profile}"
        (base / "Service Worker" / "CacheStorage").mkdir(parents=True)
        (base / "Local Extension Settings").mkdir(parents=True)
    wsl_home = tmp_path / "wsl"
    wsl_cache = wsl_home / ".cache" / "google-chrome" / "Default" / "Cache"
    wsl_cache.mkdir(parents=True)
    skill = wsl_cache / "hidden-skill.dat"
    skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(disguised_skills_module, "MAX_PROBE_ROOTS", 4)

    artifacts = scan_disguised_skills(home=native_home, extra_home_roots=[wsl_home])

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_noisy_early_home_does_not_exhaust_shared_expansion_budget(
    monkeypatch,
    tmp_path: Path,
):
    native_home = tmp_path / "native"
    noisy_parent = native_home / ".cache" / "browser"
    noisy_parent.mkdir(parents=True)
    for index in range(4):
        (noisy_parent / f"noise-{index}.dat").write_text("noise")
    other_home = tmp_path / "other"
    signal_root = other_home / ".cache" / "browser" / "Default" / "Cache"
    signal_root.mkdir(parents=True)
    skill = signal_root / "hidden-skill.dat"
    skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/browser/*/Cache",),
    )
    monkeypatch.setattr(disguised_skills_module, "MAX_ROOT_EXPANSION_ENTRIES", 2)

    artifacts = scan_disguised_skills(
        home=native_home,
        extra_home_roots=[other_home],
        hidden_candidates=(),
    )

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_noisy_early_pattern_does_not_exhaust_shared_expansion_budget(
    monkeypatch,
    tmp_path: Path,
):
    noisy_parent = tmp_path / ".cache" / "browser"
    noisy_parent.mkdir(parents=True)
    for index in range(4):
        (noisy_parent / f"noise-{index}.dat").write_text("noise")
    signal_root = tmp_path / ".cache" / "signal"
    signal_root.mkdir(parents=True)
    skill = signal_root / "hidden-skill.dat"
    skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/browser/*/Cache", ".cache/signal"),
    )
    monkeypatch.setattr(disguised_skills_module, "MAX_ROOT_EXPANSION_ENTRIES", 2)

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=(),
    )

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_probe_bounds_and_checkpoints_wildcard_root_expansion(
    monkeypatch, tmp_path: Path
):
    for index in range(3):
        cache_dir = tmp_path / ".cache" / "chromium" / f"Profile {index}" / "Cache"
        cache_dir.mkdir(parents=True)
        (cache_dir / "skill.dat").write_text(SKILL_CONTENT)
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/chromium/*/Cache",),
    )
    monkeypatch.setattr(disguised_skills_module, "MAX_ROOT_EXPANSION_ENTRIES", 2)
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=(),
        checkpoint=checkpoint,
    )

    assert len(artifacts) == 2
    assert checkpoints >= 2


def test_probe_checkpoints_each_allowlisted_candidate_entry(
    monkeypatch,
    tmp_path: Path,
):
    cache_root = tmp_path / ".cache" / "heavy"
    cache_root.mkdir(parents=True)
    for index in range(16):
        (cache_root / f"noise-{index}.dat").write_text("noise")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/heavy",),
    )
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    assert (
        scan_disguised_skills(
            home=tmp_path,
            hidden_candidates=(),
            checkpoint=checkpoint,
        )
        == []
    )
    assert checkpoints >= 16


def test_probe_checkpoints_each_hidden_candidate(
    monkeypatch,
    tmp_path: Path,
):
    candidates = []
    for index in range(16):
        candidate = tmp_path / ".cache" / f"noise-{index}.dat"
        candidate.parent.mkdir(exist_ok=True)
        candidate.write_text("noise")
        candidates.append(candidate)
    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    assert (
        scan_disguised_skills(
            home=tmp_path,
            hidden_candidates=candidates,
            checkpoint=checkpoint,
        )
        == []
    )
    assert checkpoints >= len(candidates)


def test_probe_scans_linux_chromium_service_worker_storage(tmp_path: Path):
    cache_dir = (
        tmp_path
        / ".config"
        / "google-chrome"
        / "Default"
        / "Service Worker"
        / "CacheStorage"
    )
    cache_dir.mkdir(parents=True)
    skill = cache_dir / "cached-skill.dat"
    skill.write_text(SKILL_CONTENT)

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


@pytest.mark.parametrize(
    "relative_cache_root",
    [
        "Library/Application Support/Chromium/Default/Code Cache",
        "AppData/Local/Chromium/User Data/Default/Service Worker/CacheStorage",
        "Library/Application Support/Cursor/Cache",
        "Library/Application Support/Code/Code Cache",
        "Library/Application Support/Windsurf/Service Worker/CacheStorage",
        "Library/Application Support/Claude/Cache",
        "AppData/Roaming/Cursor/Code Cache",
        "AppData/Roaming/Code/Service Worker/CacheStorage",
        "AppData/Roaming/Windsurf/Cache",
        "AppData/Roaming/Claude/Code Cache",
        ".config/Cursor/Service Worker/CacheStorage",
        ".config/Code/Cache",
        ".config/Windsurf/Code Cache",
        ".config/Claude/Service Worker/CacheStorage",
    ],
)
def test_probe_scans_explicit_chromium_and_electron_roots(
    tmp_path: Path, relative_cache_root: str
):
    cache_dir = tmp_path / relative_cache_root
    cache_dir.mkdir(parents=True)
    skill = cache_dir / "cached-skill.dat"
    skill.write_text(SKILL_CONTENT)

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(skill)]


@pytest.mark.parametrize(
    "relative_cache_root",
    [
        "Library/Application Support/Unknown Electron App/Cache",
        "AppData/Roaming/Unknown Electron App/Code Cache",
        ".config/Unknown Electron App/Service Worker/CacheStorage",
    ],
)
def test_probe_accepts_generic_cache_family_candidates(
    tmp_path: Path, relative_cache_root: str
):
    cache_dir = tmp_path / relative_cache_root
    cache_dir.mkdir(parents=True)
    skill = cache_dir / "cached-skill.dat"
    skill.write_text(SKILL_CONTENT)

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=[skill],
    )

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_heavy_explicit_cache_does_not_starve_hidden_candidates(
    monkeypatch,
    tmp_path: Path,
):
    heavy_root = tmp_path / ".cache" / "heavy"
    heavy_root.mkdir(parents=True)
    for index in range(3):
        (heavy_root / f"noise-{index}.dat").write_text("noise")
    hidden_skill = tmp_path / ".cache" / "hidden-skill.dat"
    hidden_skill.write_text(SKILL_CONTENT)
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/heavy",),
    )
    monkeypatch.setattr(disguised_skills_module, "MAX_PROBE_ENTRIES", 2)

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=[hidden_skill],
    )

    assert [artifact.path for artifact in artifacts] == [str(hidden_skill)]


def test_probe_follows_external_symlinked_profile_ancestor_for_user(tmp_path: Path):
    home = tmp_path / "home"
    profiles = home / "Library" / "Application Support" / "Google" / "Chrome"
    profiles.mkdir(parents=True)
    outside = tmp_path / "outside"
    cache_dir = outside / "Cache"
    cache_dir.mkdir(parents=True)
    escaped = cache_dir / "escaped.dat"
    escaped.write_text(SKILL_CONTENT)
    try:
        (profiles / "Default").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert [artifact.path for artifact in artifacts] == [str(escaped)]


def test_probe_skips_symlinked_profile_ancestor_for_system(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    profiles = home / "Library" / "Application Support" / "Google" / "Chrome"
    profiles.mkdir(parents=True)
    outside = tmp_path / "outside"
    cache_dir = outside / "Cache"
    cache_dir.mkdir(parents=True)
    (cache_dir / "escaped.dat").write_text(SKILL_CONTENT)
    try:
        (profiles / "Default").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "is_windows_system_context",
        lambda: True,
    )

    assert scan_disguised_skills(home=home, hidden_candidates=()) == []


def test_allowlisted_expansion_follows_external_file_target(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    links = home / ".cache" / "links"
    links.mkdir(parents=True)
    external = tmp_path / "external.dat"
    external.write_text(SKILL_CONTENT)
    try:
        (links / "candidate").symlink_to(external)
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/links/*",),
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert [artifact.path for artifact in artifacts] == [str(external)]


@pytest.mark.parametrize("alias_component", ["alias", "ali*"])
def test_allowlisted_expansion_traverses_covered_symlink_without_follow_budget(
    tmp_path: Path,
    monkeypatch,
    alias_component: str,
):
    home = tmp_path / "home"
    covered_root = home / ".cache" / "covered"
    deep_parts = tuple(
        f"level-{index}" for index in range(disguised_skills_module.MAX_PROBE_DEPTH + 1)
    )
    deep_root = covered_root.joinpath(*deep_parts)
    deep_root.mkdir(parents=True)
    skill = deep_root / "candidate.dat"
    skill.write_text(SKILL_CONTENT)
    links = home / ".cache" / "links"
    links.mkdir()
    try:
        (links / "alias").symlink_to(covered_root, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (
            ".cache/covered",
            str(Path(".cache", "links", alias_component, *deep_parts)),
        ),
    )
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_FOLLOWED_SYMLINK_TARGETS",
        0,
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert [artifact.path for artifact in artifacts] == [str(skill)]


def test_hidden_candidate_file_symlink_follows_external_target_for_user(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    home.mkdir()
    outside = tmp_path / "outside.dat"
    outside.write_text(SKILL_CONTENT)
    candidate = home / ".cache" / "candidate.dat"
    candidate.parent.mkdir()
    try:
        candidate.symlink_to(outside)
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())

    artifacts = scan_disguised_skills(
        home=home,
        hidden_candidates=[candidate],
    )

    assert [artifact.path for artifact in artifacts] == [str(outside)]


def test_hidden_candidate_under_linked_home_is_probed_at_resolved_target(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    home.mkdir()
    external_home = tmp_path / "external-home"
    skill = external_home / ".cache" / ".mozilla-profile-bak" / ".state" / "profile.dat"
    skill.parent.mkdir(parents=True)
    skill.write_text(SKILL_CONTENT)
    linked_home = tmp_path / "linked-home"
    try:
        linked_home.symlink_to(external_home, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())
    sweep = scan_hidden_spaces(
        home=home,
        system="Linux",
        extra_home_roots=(linked_home,),
        include_files=True,
        temp_roots=(),
    )

    artifacts = scan_disguised_skills(
        home=home,
        extra_home_roots=(linked_home,),
        hidden_candidates=sweep.files,
    )

    assert [artifact.path for artifact in artifacts] == [
        str(linked_home / ".cache" / ".mozilla-profile-bak" / ".state" / "profile.dat")
    ]


def test_hidden_candidate_file_symlink_is_skipped_for_system(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    home.mkdir()
    outside = tmp_path / "outside.dat"
    outside.write_text(SKILL_CONTENT)
    candidate = home / ".cache" / "candidate.dat"
    candidate.parent.mkdir()
    try:
        candidate.symlink_to(outside)
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())
    monkeypatch.setattr(
        disguised_skills_module,
        "is_windows_system_context",
        lambda: True,
    )

    assert (
        scan_disguised_skills(
            home=home,
            hidden_candidates=[candidate],
        )
        == []
    )


def test_candidate_bfs_follows_external_directory_and_file_targets(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    external_directory = tmp_path / "external-directory"
    directory_skill = external_directory / "nested" / "directory-skill.dat"
    directory_skill.parent.mkdir(parents=True)
    directory_skill.write_text(SKILL_CONTENT.replace("name: deploy", "name: directory"))
    file_skill = tmp_path / "file-skill.dat"
    file_skill.write_text(SKILL_CONTENT.replace("name: deploy", "name: file"))
    try:
        (probe_root / "directory-link").symlink_to(
            external_directory,
            target_is_directory=True,
        )
        (probe_root / "file-link.dat").symlink_to(file_skill)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert {artifact.path for artifact in artifacts} == {
        str(directory_skill),
        str(file_skill),
    }


def test_candidate_bfs_follows_relocated_and_beyond_depth_targets(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    relocated = home / "ordinary" / "relocated.dat"
    relocated.parent.mkdir()
    relocated.write_text(SKILL_CONTENT.replace("name: deploy", "name: relocated"))
    beyond_directory = home / "deep"
    for index in range(disguised_skills_module.MAX_PROBE_DEPTH):
        beyond_directory /= str(index)
    beyond_directory.mkdir(parents=True)
    beyond = beyond_directory / "beyond.dat"
    beyond.write_text(SKILL_CONTENT.replace("name: deploy", "name: beyond"))
    beyond_root = probe_root / "deep"
    for index in range(disguised_skills_module.MAX_PROBE_DEPTH + 1):
        beyond_root /= str(index)
    beyond_root.mkdir(parents=True)
    beyond_root_skill = beyond_root / "beyond-root.dat"
    beyond_root_skill.write_text(
        SKILL_CONTENT.replace("name: deploy", "name: beyond-root")
    )
    try:
        (probe_root / "relocated.dat").symlink_to(relocated)
        (probe_root / "beyond.dat").symlink_to(beyond)
        (probe_root / "beyond-directory").symlink_to(
            beyond_root,
            target_is_directory=True,
        )
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert {artifact.path for artifact in artifacts} == {
        str(relocated),
        str(beyond),
        str(beyond_root_skill),
    }


def test_candidate_bfs_follows_in_home_target_outside_allowlist(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    relocated = home / "ordinary" / "skill.dat"
    relocated.parent.mkdir()
    relocated.write_text(SKILL_CONTENT.replace("name: deploy", "name: relocated"))
    try:
        (probe_root / "relocated.dat").symlink_to(relocated)
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert {artifact.path for artifact in artifacts} == {str(relocated)}


def test_candidate_bfs_skips_broken_ancestor_and_loop_links(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    ordinary = home / "ordinary" / "not-allowlisted.dat"
    ordinary.parent.mkdir()
    ordinary.write_text(SKILL_CONTENT)
    try:
        (probe_root / "ancestor").symlink_to(home, target_is_directory=True)
        (probe_root / "broken").symlink_to(tmp_path / "missing")
        loop = probe_root / "loop"
        loop.symlink_to(loop)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )

    assert scan_disguised_skills(home=home, hidden_candidates=()) == []


def test_candidate_bfs_follow_cap_counts_unique_realpaths(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    targets = []
    for index in range(3):
        target = tmp_path / f"external-{index}.dat"
        target.write_text(
            SKILL_CONTENT.replace("name: deploy", f"name: external-{index}")
        )
        targets.append(target)
    try:
        (probe_root / "00-first.dat").symlink_to(targets[0])
        (probe_root / "01-duplicate.dat").symlink_to(targets[0])
        (probe_root / "02-second.dat").symlink_to(targets[1])
        (probe_root / "03-third.dat").symlink_to(targets[2])
    except OSError:
        pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_FOLLOWED_SYMLINK_TARGETS",
        2,
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert len(artifacts) == 2
    assert len({artifact.path for artifact in artifacts}) == 2
    assert {artifact.path for artifact in artifacts} <= {
        str(target) for target in targets
    }


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFO unavailable")
def test_non_file_root_link_does_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    cache = home / ".cache"
    cache.mkdir(parents=True)
    special_target = tmp_path / "special"
    os.mkfifo(special_target)
    special_link = cache / "a-special"
    special_link.symlink_to(special_target)
    valid_target = tmp_path / "valid.dat"
    valid_target.write_text(SKILL_CONTENT.replace("name: deploy", "name: valid"))
    valid_link = cache / "b-valid"
    valid_link.symlink_to(valid_target)
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/a-special", ".cache/b-valid"),
    )
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_FOLLOWED_SYMLINK_TARGETS",
        1,
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert {artifact.path for artifact in artifacts} == {str(valid_target)}


def test_unreadable_file_link_does_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    unreadable_target = tmp_path / "unreadable.dat"
    unreadable_target.write_text(SKILL_CONTENT)
    valid_target = tmp_path / "valid.dat"
    valid_target.write_text(SKILL_CONTENT.replace("name: deploy", "name: valid"))
    try:
        (probe_root / "a-unreadable.dat").symlink_to(unreadable_target)
        (probe_root / "z-valid.dat").symlink_to(valid_target)
    except OSError:
        pytest.skip("file symlinks unavailable")
    real_open = disguised_skills_module._open_candidate
    real_claim = disguised_skills_module.SymlinkFollowPolicy.claim
    claimed_targets: set[Path] = set()

    def track_claim(policy, target):
        claimed_targets.add(target.resolve())
        return real_claim(policy, target)

    def reject_first(candidate):
        if candidate == unreadable_target.resolve():
            assert candidate not in claimed_targets
            raise OSError("unreadable")
        return real_open(candidate)

    monkeypatch.setattr(
        disguised_skills_module.SymlinkFollowPolicy,
        "claim",
        track_claim,
    )
    monkeypatch.setattr(disguised_skills_module, "_open_candidate", reject_first)
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_FOLLOWED_SYMLINK_TARGETS",
        1,
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert [artifact.path for artifact in artifacts] == [str(valid_target)]


def test_followed_candidates_share_candidate_and_byte_budgets(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    targets = []
    for index in range(2):
        target = tmp_path / f"external-{index}.dat"
        target.write_text(
            SKILL_CONTENT.replace("name: deploy", f"name: external-{index}")
        )
        targets.append(target)
        try:
            (probe_root / f"{index}.dat").symlink_to(target)
        except OSError:
            pytest.skip("file symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )
    monkeypatch.setattr(disguised_skills_module, "MAX_CANDIDATES", 1)
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_TOTAL_CANDIDATE_BYTES",
        len(targets[0].read_bytes()),
    )

    artifacts = scan_disguised_skills(home=home, hidden_candidates=())

    assert len(artifacts) == 1
    assert artifacts[0].path in {str(target) for target in targets}


def test_followed_directory_keeps_probe_depth_cap(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    probe_root = home / ".cache" / "probe"
    probe_root.mkdir(parents=True)
    external = tmp_path / "external"
    too_deep = external
    for index in range(disguised_skills_module.MAX_PROBE_DEPTH + 1):
        too_deep /= str(index)
    too_deep.mkdir(parents=True)
    (too_deep / "skill.dat").write_text(SKILL_CONTENT)
    try:
        (probe_root / "external").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(
        disguised_skills_module,
        "_ALLOWLISTED_ROOT_PATTERNS",
        (".cache/probe",),
    )

    assert scan_disguised_skills(home=home, hidden_candidates=()) == []


def test_hidden_candidate_rejects_ancestor_replacement_between_stat_and_open(
    monkeypatch,
    tmp_path: Path,
):
    candidate_parent = tmp_path / ".cache" / "candidate"
    candidate_parent.mkdir(parents=True)
    candidate = candidate_parent / "skill.dat"
    candidate.write_text(SKILL_CONTENT)
    outside = tmp_path / "outside"
    outside.mkdir()
    outside_candidate = outside / candidate.name
    try:
        os.link(candidate, outside_candidate)
    except OSError:
        pytest.skip("hard links unavailable")
    original_open = disguised_skills_module.os.open
    replacement_happened = False

    def replace_ancestor_before_open(path, flags, *args, **kwargs):
        nonlocal replacement_happened
        if Path(path).name == candidate.name and not replacement_happened:
            replacement_happened = True
            candidate_parent.rename(tmp_path / "original-candidate-parent")
            candidate_parent.symlink_to(outside, target_is_directory=True)
        return original_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(
        disguised_skills_module.os,
        "open",
        replace_ancestor_before_open,
    )

    assert (
        scan_disguised_skills(
            home=tmp_path,
            hidden_candidates=[candidate],
        )
        == []
    )
    assert replacement_happened is True


def test_hidden_candidate_reads_only_from_open_descriptor(monkeypatch, tmp_path: Path):
    candidate = tmp_path / ".cache" / "candidate" / "skill.dat"
    candidate.parent.mkdir(parents=True)
    candidate.write_text(SKILL_CONTENT)

    def fail_pathname_read(*_args, **_kwargs):
        raise AssertionError("candidate pathname reopened")

    monkeypatch.setattr(
        disguised_skills_module,
        "read_bounded",
        fail_pathname_read,
        raising=False,
    )
    monkeypatch.setattr(disguised_skills_module, "_ALLOWLISTED_ROOT_PATTERNS", ())

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=[candidate],
    )

    assert [artifact.path for artifact in artifacts] == [str(candidate)]


def test_candidate_growth_never_requests_unbounded_tail(monkeypatch, tmp_path: Path):
    read_sizes: list[int] = []

    class GrowingHandle:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self, size: int) -> bytes:
            read_sizes.append(size)
            if size < 0:
                raise AssertionError("negative read size becomes unbounded")
            if len(read_sizes) == 1:
                return SKILL_CONTENT.encode()
            return b""

    monkeypatch.setattr(
        disguised_skills_module,
        "_open_candidate",
        lambda _candidate: (123, SimpleNamespace(st_size=1, st_mtime_ns=1)),
    )
    monkeypatch.setattr(
        disguised_skills_module.os,
        "fdopen",
        lambda _descriptor, _mode: GrowingHandle(),
    )

    artifact = disguised_skills_module._artifact_from_candidate(
        tmp_path / "growing.dat",
        budget=disguised_skills_module._ProbeBudget(),
    )

    assert artifact is None
    assert all(size >= 0 for size in read_sizes)


def test_standard_skill_root_candidate_is_scanned_when_normal_scan_cannot_find_it(
    tmp_path: Path,
):
    candidate = tmp_path / ".claude" / "skills" / "orphaned-copy.dat"
    candidate.parent.mkdir(parents=True)
    candidate.write_text(SKILL_CONTENT)

    artifacts = scan_disguised_skills(
        home=tmp_path,
        hidden_candidates=[candidate],
    )

    assert [artifact.path for artifact in artifacts] == [str(candidate)]


def test_probe_accepts_allowlisted_known_content_fingerprint(
    monkeypatch, tmp_path: Path
):
    cache_dir = tmp_path / "Library" / "Caches" / "Google" / "GoogleSoftwareUpdate"
    cache_dir.mkdir(parents=True)
    opaque_content = "trusted opaque skill copy"
    disguised_path = cache_dir / "known-copy.dat"
    disguised_path.write_text(opaque_content)
    (cache_dir / "0-too-large.dat").write_bytes(b"x" * 128)
    fingerprint = hashlib.sha256(opaque_content.encode()).hexdigest()
    monkeypatch.setattr(
        disguised_skills_module,
        "KNOWN_SKILL_CONTENT_SHA256",
        frozenset({fingerprint}),
    )
    monkeypatch.setattr(disguised_skills_module, "MAX_CANDIDATES", 1)
    monkeypatch.setattr(
        disguised_skills_module,
        "MAX_TOTAL_CANDIDATE_BYTES",
        len(opaque_content.encode()),
    )

    [artifact] = scan_disguised_skills(home=tmp_path)

    assert artifact.path == str(disguised_path)
    assert artifact.name == "known-copy"


def test_probe_skips_unreadable_root_and_continues(monkeypatch, tmp_path: Path):
    blocked_cache = (
        tmp_path
        / "AppData"
        / "Local"
        / "Google"
        / "Chrome"
        / "User Data"
        / "Default"
        / "Cache"
    )
    blocked_cache.mkdir(parents=True)
    (blocked_cache / "blocked.dat").write_text(SKILL_CONTENT)
    readable_cache = (
        tmp_path
        / "AppData"
        / "Local"
        / "Microsoft"
        / "Edge"
        / "User Data"
        / "Default"
        / "Cache"
    )
    readable_cache.mkdir(parents=True)
    readable_skill = readable_cache / "readable.dat"
    readable_skill.write_text(SKILL_CONTENT)
    original_scandir = disguised_skills_module.os.scandir

    def permission_denied_for_google(path):
        if Path(path) == blocked_cache:
            raise PermissionError(path)
        return original_scandir(path)

    monkeypatch.setattr(
        disguised_skills_module.os,
        "scandir",
        permission_denied_for_google,
    )

    artifacts = scan_disguised_skills(home=tmp_path)

    assert [artifact.path for artifact in artifacts] == [str(readable_skill)]


def test_probe_does_not_descend_beyond_depth_cap(tmp_path: Path):
    cache_dir = tmp_path / ".cache" / "google-chrome" / "Default" / "Cache"
    cache_dir.mkdir(parents=True)
    too_deep = cache_dir
    for index in range(disguised_skills_module.MAX_PROBE_DEPTH + 1):
        too_deep /= str(index)
    too_deep.mkdir(parents=True)
    (too_deep / "skill.dat").write_text(SKILL_CONTENT)

    assert scan_disguised_skills(home=tmp_path) == []
