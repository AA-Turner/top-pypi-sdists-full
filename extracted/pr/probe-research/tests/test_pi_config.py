"""The pi settings.json `packages` array edit engine.

`settings.json` is pi's own file, read by pi at startup and, independently,
by pi-mcp-adapter for MCP discovery -- so the tests that matter most here are
the ones about NOT writing: malformed JSON, a non-object root, and a
non-list `packages` must leave the file byte-for-byte untouched, exactly like
`test_codex_config.py` treats `config.toml`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import pi_config


def _env(tmp_path: Path) -> dict[str, str]:
    """Points `pi_agent_dir()` at an isolated scratch dir. Never the real ~/.pi."""
    return {"PI_CODING_AGENT_DIR": str(tmp_path / "agent-dir")}


def _agent_dir(tmp_path: Path) -> Path:
    return tmp_path / "agent-dir"


def _settings(tmp_path: Path) -> Path:
    return _agent_dir(tmp_path) / "settings.json"


def _pkg_root(tmp_path: Path, name: str = "pkg-root") -> Path:
    """A fake `probe-research-pi` package directory -- real enough for
    `resolve_package_root`'s own `package.json` check, but install/remove
    given an explicit `package_root=` never call that function at all.

    Returned already `.resolve()`d: install/remove always resolve
    `package_root` themselves before writing or comparing, so a test that
    embeds the unresolved tmp_path form in its expectations would drift on a
    platform where the temp root itself is a symlink (macOS `/tmp` ->
    `/private/tmp`).
    """
    root = tmp_path / name
    root.mkdir(parents=True, exist_ok=True)
    (root / "package.json").write_text('{"name": "probe-research-pi"}\n', encoding="utf-8")
    return root.resolve()


# --- install: missing / malformed / wrong-shape settings.json -------------


def test_missing_settings_json_is_created_with_our_entry_and_parent_dirs(
    tmp_path: Path,
) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    assert not _agent_dir(tmp_path).exists()

    result = pi_config.install_package_entry(package_root=root, env=env)

    assert result.ok
    path = _settings(tmp_path)
    assert path.is_file()
    assert (
        path.read_text(encoding="utf-8") == json.dumps({"packages": [str(root)]}, indent=2) + "\n"
    )


def test_malformed_json_is_refused_and_the_file_is_untouched(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    original = "{not valid json"
    path.write_text(original, encoding="utf-8")

    result = pi_config.install_package_entry(package_root=root, env=env)

    assert not result.ok
    assert str(path) in result.detail
    assert path.read_text(encoding="utf-8") == original


def test_json_array_root_is_refused(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    original = "[]"
    path.write_text(original, encoding="utf-8")

    result = pi_config.install_package_entry(package_root=root, env=env)

    assert not result.ok
    assert path.read_text(encoding="utf-8") == original


def test_packages_as_a_string_is_refused(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    original = json.dumps({"packages": "oops"})
    path.write_text(original, encoding="utf-8")

    result = pi_config.install_package_entry(package_root=root, env=env)

    assert not result.ok
    assert path.read_text(encoding="utf-8") == original


# --- install: sibling keys, ordering, idempotency --------------------------


def test_sibling_keys_and_their_order_survive_the_merge(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    before = {"theme": "dark", "other": {"x": 1}, "packages": ["npm:some-other-thing"]}
    path.write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")

    result = pi_config.install_package_entry(package_root=root, env=env)

    assert result.ok
    expected = {
        "theme": "dark",
        "other": {"x": 1},
        "packages": ["npm:some-other-thing", str(root)],
    }
    assert path.read_text(encoding="utf-8") == json.dumps(expected, indent=2) + "\n"


def test_second_install_is_a_noop_and_the_file_is_byte_identical(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)

    first = pi_config.install_package_entry(package_root=root, env=env)
    assert first.ok
    after_first = _settings(tmp_path).read_text(encoding="utf-8")

    second = pi_config.install_package_entry(package_root=root, env=env)
    assert second.ok
    after_second = _settings(tmp_path).read_text(encoding="utf-8")

    assert after_first == after_second
    parsed = json.loads(after_second)
    assert parsed["packages"] == [str(root)]  # never duplicated


def test_existing_object_form_source_is_recognized_as_ours(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    before = {"packages": [{"source": str(root)}]}
    path.write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")

    result = pi_config.install_package_entry(package_root=root, env=env)

    assert result.ok
    # No-op: nothing appended, the object-form entry alone still satisfies us.
    assert json.loads(path.read_text(encoding="utf-8"))["packages"] == [{"source": str(root)}]


def test_existing_npm_entry_is_recognized_and_never_duplicated(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    before = {"packages": ["npm:probe-research-pi"]}
    path.write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")

    result = pi_config.install_package_entry(package_root=root, env=env)

    assert result.ok
    assert json.loads(path.read_text(encoding="utf-8"))["packages"] == ["npm:probe-research-pi"]


def test_relative_path_entry_resolved_against_agent_dir_is_recognized_as_ours(
    tmp_path: Path,
) -> None:
    """pi resolves a relative `packages` source from the AGENT DIR, not cwd
    and not the package root -- identity comparison must match that or an
    entry pi considers ours looks foreign to us."""
    env = _env(tmp_path)
    root = _pkg_root(tmp_path, name="pkg-root")
    agent_dir = _agent_dir(tmp_path)
    agent_dir.mkdir(parents=True)
    relative = "../pkg-root"
    assert (agent_dir / relative).resolve() == root.resolve()
    (agent_dir / "settings.json").write_text(
        json.dumps({"packages": [relative]}, indent=2) + "\n", encoding="utf-8"
    )

    install_result = pi_config.install_package_entry(package_root=root, env=env)
    assert install_result.ok
    assert json.loads((agent_dir / "settings.json").read_text(encoding="utf-8"))["packages"] == [
        relative
    ]  # no-op: recognized, nothing appended

    remove_result = pi_config.remove_package_entry(package_root=root, env=env)
    assert remove_result.ok
    assert json.loads((agent_dir / "settings.json").read_text(encoding="utf-8"))["packages"] == []


def test_a_different_packages_entries_survive_install_and_removal(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    other_object = {"source": "/opt/some/other-package"}
    before = {"packages": ["npm:some-other-package", other_object]}
    path.write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")

    install_result = pi_config.install_package_entry(package_root=root, env=env)
    assert install_result.ok
    after_install = json.loads(path.read_text(encoding="utf-8"))["packages"]
    assert after_install == ["npm:some-other-package", other_object, str(root)]

    remove_result = pi_config.remove_package_entry(package_root=root, env=env)
    assert remove_result.ok
    after_removal = json.loads(path.read_text(encoding="utf-8"))["packages"]
    assert after_removal == ["npm:some-other-package", other_object]


# --- removal -----------------------------------------------------------


def test_removal_leaves_empty_packages_list_and_other_keys_intact(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    before = {"theme": "dark", "packages": [str(root)]}
    path.write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")

    result = pi_config.remove_package_entry(package_root=root, env=env)

    assert result.ok
    after = json.loads(path.read_text(encoding="utf-8"))
    assert after == {"theme": "dark", "packages": []}


def test_removal_with_no_settings_file_is_a_noop_success(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    assert not _settings(tmp_path).exists()

    result = pi_config.remove_package_entry(package_root=root, env=env)

    assert result.ok
    assert not _settings(tmp_path).exists()


def test_removal_with_no_matching_entry_is_a_noop_success(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    before = {"packages": ["npm:something-else"]}
    original = json.dumps(before, indent=2) + "\n"
    path.write_text(original, encoding="utf-8")

    result = pi_config.remove_package_entry(package_root=root, env=env)

    assert result.ok
    assert path.read_text(encoding="utf-8") == original


def test_removal_refuses_malformed_json_and_leaves_it_untouched(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    original = "{not valid json"
    path.write_text(original, encoding="utf-8")

    result = pi_config.remove_package_entry(package_root=root, env=env)

    assert not result.ok
    assert path.read_text(encoding="utf-8") == original


# --- package_entry_installed (D7 status read) ------------------------------
#
# Unlike install/remove, this has no `package_root=` override -- it is meant
# to be called the way capabilities.installed_plugins() calls it, resolving
# the root itself -- so every test here points PROBE_PI_PACKAGE_ROOT at the
# fixture root explicitly, the same env dict `resolve_package_root` would see
# in production.


def test_package_entry_installed_is_false_when_settings_json_is_absent(tmp_path: Path) -> None:
    root = _pkg_root(tmp_path)
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}
    assert not _settings(tmp_path).exists()

    assert pi_config.package_entry_installed(env) is False


def test_package_entry_installed_is_true_after_install(tmp_path: Path) -> None:
    root = _pkg_root(tmp_path)
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}

    assert pi_config.package_entry_installed(env) is False
    install_result = pi_config.install_package_entry(package_root=root, env=env)
    assert install_result.ok
    assert pi_config.package_entry_installed(env) is True


def test_package_entry_installed_is_false_again_after_removal(tmp_path: Path) -> None:
    root = _pkg_root(tmp_path)
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}
    pi_config.install_package_entry(package_root=root, env=env)
    assert pi_config.package_entry_installed(env) is True

    remove_result = pi_config.remove_package_entry(package_root=root, env=env)
    assert remove_result.ok
    assert pi_config.package_entry_installed(env) is False


def test_package_entry_installed_recognizes_object_form_and_npm_form_entries(
    tmp_path: Path,
) -> None:
    """Delegates to the SAME identity matching install/remove use -- not just
    "is the packages list non-empty" -- so an entry in either shape pi itself
    would recognize as ours must also read as installed here."""
    root = _pkg_root(tmp_path)
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps({"packages": [{"source": str(root)}]}, indent=2) + "\n", encoding="utf-8"
    )
    assert pi_config.package_entry_installed(env) is True

    path.write_text(
        json.dumps({"packages": ["npm:probe-research-pi"]}, indent=2) + "\n", encoding="utf-8"
    )
    assert pi_config.package_entry_installed(env) is True


def test_package_entry_installed_is_false_for_a_different_packages_entry(tmp_path: Path) -> None:
    """A non-empty `packages` list that simply does not name us must not read
    as installed -- this is an identity check, not a presence check."""
    root = _pkg_root(tmp_path)
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps({"packages": ["npm:some-other-package"]}, indent=2) + "\n", encoding="utf-8"
    )

    assert pi_config.package_entry_installed(env) is False


def test_package_entry_installed_is_false_never_raises_on_malformed_json(tmp_path: Path) -> None:
    root = _pkg_root(tmp_path)
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text("{not valid json", encoding="utf-8")

    assert pi_config.package_entry_installed(env) is False


def test_package_entry_installed_is_false_never_raises_on_non_list_packages(
    tmp_path: Path,
) -> None:
    root = _pkg_root(tmp_path)
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}
    path = _settings(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"packages": "oops"}), encoding="utf-8")

    assert pi_config.package_entry_installed(env) is False


def test_package_entry_installed_is_false_never_raises_when_no_package_root_resolves(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No PROBE_PI_PACKAGE_ROOT, and the checkout walk pointed nowhere real
    (e.g. this CLI installed as a standalone wheel) -- `resolve_package_root`
    raises `PackageRootError` for install/remove, but a status read has no
    repair to offer, so this must swallow it and say `False`, never raise."""
    env = _env(tmp_path)  # no PROBE_PI_PACKAGE_ROOT
    fake_file = tmp_path / "nowhere" / "pi_config.py"
    fake_file.parent.mkdir(parents=True)
    monkeypatch.setattr(pi_config, "__file__", str(fake_file))

    assert pi_config.package_entry_installed(env) is False


# --- package root resolution --------------------------------------------


def test_probe_pi_package_root_env_is_honored(tmp_path: Path) -> None:
    root = _pkg_root(tmp_path, name="explicit-root")
    env = {"PROBE_PI_PACKAGE_ROOT": str(root)}

    assert pi_config.resolve_package_root(env) == root.resolve()


def test_probe_pi_package_root_pointing_at_a_dir_without_package_json_fails_loud(
    tmp_path: Path,
) -> None:
    empty = tmp_path / "empty-dir"
    empty.mkdir()
    env = {"PROBE_PI_PACKAGE_ROOT": str(empty)}

    with pytest.raises(pi_config.PackageRootError, match="PROBE_PI_PACKAGE_ROOT"):
        pi_config.resolve_package_root(env)


def test_checkout_walk_finds_the_real_package_from_repo_layout() -> None:
    """No PROBE_PI_PACKAGE_ROOT set: the walk must find THIS checkout's own
    agent/plugins/probe-research-pi, proving the walk logic against real
    layout rather than only a synthetic tmp_path stand-in."""
    root = pi_config.resolve_package_root({})

    assert root.name == "probe-research-pi"
    assert root.parent.name == "plugins"
    assert (root / "package.json").is_file()
    declared = json.loads((root / "package.json").read_text(encoding="utf-8"))
    assert declared["name"] == "probe-research-pi"


def _no_checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """The CUSTOMER shape: no `PROBE_PI_PACKAGE_ROOT`, and the ancestor walk
    pointed at a directory with no research-os checkout above it -- i.e. this
    CLI installed as a wheel from PyPI, which is every install that is not a
    plugin developer's own machine."""
    env = _env(tmp_path)
    fake_file = tmp_path / "nowhere" / "pi_config.py"
    fake_file.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(pi_config, "__file__", str(fake_file))
    return env


# --- the mirror install (no checkout anywhere) ---------------------------


def test_install_writes_the_mirror_source_when_no_checkout_resolves(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """This used to refuse loudly (`reachable=False`, "could not find the
    probe-research-pi package"), which is what every customer saw: the plugin
    had no distribution channel, so the only shape that could succeed was a
    developer's own checkout. It now installs the published mirror repo, which
    pi clones and loads from its root manifest."""
    env = _no_checkout(tmp_path, monkeypatch)

    result = pi_config.install_package_entry(env=env)

    assert result.ok
    assert pi_config.MIRROR_GIT_SOURCE in result.detail
    written = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert written["packages"] == [pi_config.MIRROR_GIT_SOURCE]


def test_the_mirror_source_is_a_form_pi_can_actually_parse() -> None:
    """The regression that shipped in 0.131.0. pi's `isLocalPath()` treats
    `github:` as non-local, which looks like support, but `parseGitUrl()`
    accepts only a `git:` prefix or a full protocol URL -- so
    `github:owner/repo` parses as NEITHER and pi looks for a directory of that
    literal name. Verified against pi 0.84.3: `git:github.com/...` and
    `https://github.com/...` install, `github:...` does not. 0.86.0's
    `isLocalPath()` and `parseGitUrl()` are byte-identical.

    Asserted on the constant itself because nothing else can catch it: the
    entry writes fine, the settings file looks right, and pi reports the
    package as configured -- it simply never installs, so the extension,
    skills and MCP tools are all silently absent.
    """
    assert not pi_config.MIRROR_GIT_SOURCE.startswith("github:")
    assert pi_config.MIRROR_GIT_SOURCE.startswith("git:") or pi_config.MIRROR_GIT_SOURCE.startswith(
        "https://"
    )
    # ...and it must still be recognised as ours, or install/remove stop
    # matching the very entry we write.
    assert pi_config._git_repo_identity(pi_config.MIRROR_GIT_SOURCE) == (
        "github.com",
        pi_config.MIRROR_REPO.lower(),
    )


def test_installing_the_mirror_twice_is_a_noop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env = _no_checkout(tmp_path, monkeypatch)
    assert pi_config.install_package_entry(env=env).ok
    before = _settings(tmp_path).read_bytes()

    again = pi_config.install_package_entry(env=env)

    assert again.ok
    assert "no-op" in again.detail
    assert _settings(tmp_path).read_bytes() == before


def test_mirror_entry_is_removable_without_any_checkout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Removal used to need a resolvable package root too, so a
    mirror-installed user could not uninstall without a research-os clone."""
    env = _no_checkout(tmp_path, monkeypatch)
    assert pi_config.install_package_entry(env=env).ok

    removed = pi_config.remove_package_entry(env=env)

    assert removed.ok
    written = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert written["packages"] == []


def test_package_entry_installed_sees_the_mirror_entry_without_a_checkout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`probe doctor`'s signal (D7). Reporting False here would tell every
    mirror-installed user the pi plugin is missing on a machine where it is
    installed and loading."""
    env = _no_checkout(tmp_path, monkeypatch)
    assert pi_config.package_entry_installed(env) is False

    assert pi_config.install_package_entry(env=env).ok

    assert pi_config.package_entry_installed(env) is True


@pytest.mark.parametrize(
    "source",
    [
        "github:prbe-ai/research-os-agent",
        "git:github.com/prbe-ai/research-os-agent",
        "https://github.com/prbe-ai/research-os-agent",
        "https://github.com/prbe-ai/research-os-agent.git",
        "git@github.com:prbe-ai/research-os-agent.git",
        "ssh://git@github.com/prbe-ai/research-os-agent",
        "github:prbe-ai/research-os-agent#v1.2.3",
        "github:PRBE-AI/Research-OS-Agent",
    ],
)
def test_every_spelling_of_the_mirror_is_recognised_as_ours(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source: str
) -> None:
    """A hand-written or pinned entry must be recognised, never duplicated --
    pi accepts all of these forms for one repo."""
    env = _no_checkout(tmp_path, monkeypatch)
    _agent_dir(tmp_path).mkdir(parents=True, exist_ok=True)
    _settings(tmp_path).write_text(json.dumps({"packages": [source]}), encoding="utf-8")

    assert pi_config.package_entry_installed(env) is True
    assert "no-op" in pi_config.install_package_entry(env=env).detail


@pytest.mark.parametrize(
    "source",
    [
        "github:someone-else/research-os-agent",
        "github:prbe-ai/research-os-agent-fork",
        "https://gitlab.com/prbe-ai/research-os-agent",
        "npm:some-other-package",
    ],
)
def test_a_foreign_git_or_npm_source_is_never_ours(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source: str
) -> None:
    """Removal must never touch somebody else's package, and a same-named repo
    under a different owner or host is somebody else's."""
    env = _no_checkout(tmp_path, monkeypatch)
    _agent_dir(tmp_path).mkdir(parents=True, exist_ok=True)
    _settings(tmp_path).write_text(json.dumps({"packages": [source]}), encoding="utf-8")

    assert pi_config.package_entry_installed(env) is False

    assert pi_config.remove_package_entry(env=env).ok
    survived = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert survived["packages"] == [source]


def test_a_dev_era_checkout_entry_is_removable_from_a_wheel_install(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The upgrade path. Someone who installed from a checkout has an absolute
    path in `packages`; their CLI is a wheel, so no local root resolves and the
    path comparison has nothing to compare against. Recognising the entry by
    its declared `name` is what lets uninstall remove it -- otherwise it stays,
    the next install appends the mirror beside it, and pi loads the extension
    twice."""
    env = _no_checkout(tmp_path, monkeypatch)
    old_install = _pkg_root(tmp_path, name="old-checkout")
    (old_install / "package.json").write_text(
        json.dumps({"name": "probe-research-pi"}), encoding="utf-8"
    )
    _agent_dir(tmp_path).mkdir(parents=True, exist_ok=True)
    _settings(tmp_path).write_text(json.dumps({"packages": [str(old_install)]}), encoding="utf-8")

    assert pi_config.package_entry_installed(env) is True
    # ...so a re-install is a no-op rather than a duplicate,
    assert "no-op" in pi_config.install_package_entry(env=env).detail
    # ...and uninstall actually removes it.
    assert pi_config.remove_package_entry(env=env).ok
    assert json.loads(_settings(tmp_path).read_text(encoding="utf-8"))["packages"] == []


def test_a_local_dir_that_is_not_our_package_is_left_alone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Name matching must not turn into "any local path is ours"."""
    env = _no_checkout(tmp_path, monkeypatch)
    foreign = _pkg_root(tmp_path, name="someone-elses")
    (foreign / "package.json").write_text(
        json.dumps({"name": "some-other-package"}), encoding="utf-8"
    )
    _agent_dir(tmp_path).mkdir(parents=True, exist_ok=True)
    _settings(tmp_path).write_text(json.dumps({"packages": [str(foreign)]}), encoding="utf-8")

    assert pi_config.package_entry_installed(env) is False
    assert pi_config.remove_package_entry(env=env).ok
    survived = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert survived["packages"] == [str(foreign)]


def test_a_local_checkout_still_wins_over_the_mirror(tmp_path: Path) -> None:
    """A plugin developer must keep getting their own tree: the mirror is the
    fallback, never an override."""
    root = _pkg_root(tmp_path, name="dev-checkout")
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(root)}

    assert pi_config.resolve_install_source(env) == str(root.resolve())

    assert pi_config.install_package_entry(env=env).ok
    written = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert written["packages"] == [str(root.resolve())]


def test_a_broken_package_root_env_refuses_without_raising(tmp_path: Path) -> None:
    """Loud, but a Result -- the wizard's step runner reads Results, so raising
    here would crash the whole run instead of failing one step."""
    empty = tmp_path / "empty-dir-2"
    empty.mkdir()
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(empty)}

    result = pi_config.install_package_entry(env=env)

    assert not result.ok
    assert not result.reachable
    assert "PROBE_PI_PACKAGE_ROOT" in result.detail
    assert not _settings(tmp_path).exists()

    removal = pi_config.remove_package_entry(env=env)
    assert not removal.ok
    assert not removal.reachable


def test_a_broken_package_root_env_still_fails_loud(tmp_path: Path) -> None:
    """The mirror fallback must NOT swallow an explicit override that points
    nowhere -- a researcher who set the var made a specific claim."""
    empty = tmp_path / "empty-dir"
    empty.mkdir()
    env = {**_env(tmp_path), "PROBE_PI_PACKAGE_ROOT": str(empty)}

    with pytest.raises(pi_config.PackageRootError, match="PROBE_PI_PACKAGE_ROOT"):
        pi_config.resolve_install_source(env)


# --- legacy symlink migration (D4) ---------------------------------------


def test_migrate_removes_a_symlink_that_resolves_inside_the_package_root(
    tmp_path: Path,
) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    agent_dir = _agent_dir(tmp_path)
    extensions = agent_dir / "extensions"
    extensions.mkdir(parents=True)
    link = extensions / "probe-research-pi"
    link.symlink_to(root, target_is_directory=True)

    result = pi_config.migrate_legacy_symlink(root, env=env)

    assert result.ok
    assert "removed" in result.detail
    assert not link.is_symlink()
    assert not link.exists()


def test_migrate_leaves_a_symlink_pointing_elsewhere_and_says_why(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    elsewhere = tmp_path / "some-other-checkout"
    elsewhere.mkdir()
    agent_dir = _agent_dir(tmp_path)
    extensions = agent_dir / "extensions"
    extensions.mkdir(parents=True)
    link = extensions / "probe-research-pi"
    link.symlink_to(elsewhere, target_is_directory=True)

    result = pi_config.migrate_legacy_symlink(root, env=env)

    assert result.ok
    assert "left" in result.detail
    assert str(elsewhere.resolve()) in result.detail
    assert link.is_symlink()


def test_migrate_leaves_a_real_directory_alone(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)
    agent_dir = _agent_dir(tmp_path)
    extensions = agent_dir / "extensions"
    real_dir = extensions / "probe-research-pi"
    real_dir.mkdir(parents=True)
    (real_dir / "marker.txt").write_text("still here\n", encoding="utf-8")

    result = pi_config.migrate_legacy_symlink(root, env=env)

    assert result.ok
    assert "real directory" in result.detail
    assert not real_dir.is_symlink()
    assert (real_dir / "marker.txt").exists()


def test_migrate_with_nothing_there_is_a_noop(tmp_path: Path) -> None:
    env = _env(tmp_path)
    root = _pkg_root(tmp_path)

    result = pi_config.migrate_legacy_symlink(root, env=env)

    assert result.ok
    assert "nothing to migrate" in result.detail


# --- pi_agent_dir / settings_path -----------------------------------------


def test_pi_agent_dir_env_override(tmp_path: Path) -> None:
    env = {"PI_CODING_AGENT_DIR": str(tmp_path / "custom")}
    assert pi_config.pi_agent_dir(env) == tmp_path / "custom"


def test_pi_agent_dir_defaults_to_dot_pi_agent(tmp_path: Path) -> None:
    assert pi_config.pi_agent_dir({}) == Path.home() / ".pi" / "agent"


def test_settings_path_is_agent_dir_slash_settings_json(tmp_path: Path) -> None:
    env = {"PI_CODING_AGENT_DIR": str(tmp_path / "custom")}
    assert pi_config.settings_path(env) == tmp_path / "custom" / "settings.json"
