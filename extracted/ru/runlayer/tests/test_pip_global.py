"""Behavior tests for bounded pip/pipx package-identity discovery."""

import os
from pathlib import Path

import pytest

from runlayer_cli.scan import pip_global as pip_global_module
from runlayer_cli.scan.clients import PipPackage
from runlayer_cli.scan.pip_global import PipGlobalPackage, scan_pip_global_packages
from runlayer_cli.scan.wsl_limits import MAX_WSL_HOMES


@pytest.mark.parametrize(
    "hidden_prefix",
    [".fontconfig-cache", ".gtk-icon-cache-bak"],
)
def test_detects_exact_metadata_identity_in_relocated_hidden_venv(
    tmp_path: Path,
    hidden_prefix: str,
):
    package = PipPackage("aider-chat")
    venv = tmp_path / ".cache" / hidden_prefix / "runtime"
    (venv / "pyvenv.cfg").parent.mkdir(parents=True)
    (venv / "pyvenv.cfg").write_text("home = /usr/bin")
    metadata = (
        venv
        / "lib"
        / "python3.13"
        / "site-packages"
        / "aider_chat-0.82.1.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Metadata-Version: 2.4\nName: aider-chat\nVersion: 0.82.1\n")

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings == {
        "aider-chat": PipGlobalPackage(
            package_name="aider-chat",
            version="0.82.1",
            metadata_path=metadata,
        )
    }


def test_detects_exact_metadata_identity_under_configured_pipx_home(
    tmp_path: Path,
):
    package = PipPackage("aider-chat")
    pipx_home = tmp_path / "tools"
    venv = pipx_home / "venvs" / "renamed-environment"
    metadata = (
        venv / "lib" / "python3.12" / "site-packages" / "renamed.dist-info" / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider_chat\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"PIPX_HOME": str(pipx_home)},
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata
    assert findings["aider-chat"].version == "1.2.3"


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_symlinked_pipx_environment(tmp_path: Path):
    package = PipPackage("aider-chat")
    real_env = tmp_path / "external-runtime"
    metadata = (
        real_env
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    pipx_home = tmp_path / "tools"
    venvs = pipx_home / "venvs"
    venvs.mkdir(parents=True)
    (venvs / "renamed-environment").symlink_to(
        real_env,
        target_is_directory=True,
    )

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"PIPX_HOME": str(pipx_home)},
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_broken_tool_environment_links_do_not_consume_env_cap(tmp_path: Path):
    package = PipPackage("aider-chat")
    pipx_home = tmp_path / "tools"
    venvs = pipx_home / "venvs"
    venvs.mkdir(parents=True)
    for index in range(pip_global_module.MAX_TOOL_ENVS_PER_ROOT):
        (venvs / f"a-broken-{index:02}").symlink_to(
            tmp_path / f"missing-{index}",
            target_is_directory=True,
        )
    valid_env = venvs / "z-valid"
    metadata = (
        valid_env
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"PIPX_HOME": str(pipx_home)},
        discover_hidden=False,
    )

    assert findings[package.name].metadata_path == metadata


def test_detects_pipx_package_in_wsl_home_from_windows(tmp_path: Path):
    wsl_home = tmp_path / "wsl" / "home" / "alice"
    metadata = (
        wsl_home
        / ".local"
        / "share"
        / "pipx"
        / "venvs"
        / "aider-chat"
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path / "windows-home",
        system="Windows",
        environment={},
        wsl_homes=[wsl_home],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


def test_detects_pipx_package_after_first_distro_home_cap(tmp_path: Path):
    first_distro_homes = [
        tmp_path / "Distro-0" / "home" / f"user-{index}"
        for index in range(MAX_WSL_HOMES)
    ]
    later_distro_home = tmp_path / "Distro-1" / "home" / "alice"
    metadata = (
        later_distro_home
        / ".local"
        / "share"
        / "pipx"
        / "venvs"
        / "aider-chat"
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path / "windows-home",
        system="Windows",
        environment={},
        wsl_homes=[*first_distro_homes, later_distro_home],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


def test_detects_identity_in_active_environment_dist_packages(tmp_path: Path):
    venv = tmp_path / "active-runtime"
    metadata = (
        venv
        / "lib"
        / "python3.12"
        / "dist-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={"VIRTUAL_ENV": str(venv)},
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


def test_detects_identity_in_system_dist_packages(
    tmp_path: Path,
    monkeypatch,
):
    lib_root = tmp_path / "system-lib"
    metadata = (
        lib_root
        / "python3.12"
        / "dist-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    monkeypatch.setattr(
        pip_global_module,
        "_POSIX_SYSTEM_PYTHON_LIB_ROOTS",
        (lib_root,),
    )
    hidden_env = tmp_path / ".hidden-runtime"
    (hidden_env / "lib" / "python3.12" / "site-packages").mkdir(parents=True)
    monkeypatch.setattr(pip_global_module, "MAX_SITE_PACKAGES", 1)

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path / "home",
        system="Linux",
        environment={},
        python_env_roots=[hidden_env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


def test_detects_identity_in_windows_user_python_install(tmp_path: Path):
    metadata = (
        tmp_path
        / "AppData"
        / "Local"
        / "Programs"
        / "Python"
        / "Python313"
        / "Lib"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Windows",
        environment={},
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


@pytest.mark.parametrize(
    ("system", "metadata_relative", "renamed_script"),
    [
        (
            "Linux",
            "lib/python3.12/site-packages/aider_chat-1.2.3.dist-info/METADATA",
            "bin/netcheck",
        ),
        (
            "Windows",
            "Lib/site-packages/aider_chat-1.2.3.dist-info/METADATA",
            "Scripts/colorprofile.exe",
        ),
    ],
)
def test_renamed_console_script_does_not_hide_distribution_identity(
    tmp_path: Path,
    system: str,
    metadata_relative: str,
    renamed_script: str,
):
    package = PipPackage("aider-chat")
    venv = tmp_path / "relocated-runtime"
    metadata = venv / metadata_relative
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    script = venv / renamed_script
    script.parent.mkdir(parents=True)
    script.write_text("renamed launcher")

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system=system,
        environment={},
        python_env_roots=[venv],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


def test_wrong_metadata_name_is_rejected(tmp_path: Path):
    package = PipPackage("aider-chat")
    venv = tmp_path / "relocated-runtime"
    metadata = (
        venv
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: innocent-tool\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[venv],
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_external_symlinked_environment(tmp_path: Path):
    package = PipPackage("aider-chat")
    real_env = tmp_path / "real-runtime"
    metadata = (
        real_env
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    linked_env = tmp_path / "linked-runtime"
    linked_env.symlink_to(real_env, target_is_directory=True)

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[linked_env],
        discover_hidden=False,
    )

    assert findings[package.name] == PipGlobalPackage(
        package_name=package.name,
        version="1.2.3",
        metadata_path=metadata,
    )


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_broken_discovered_env_links_do_not_consume_env_cap(tmp_path: Path):
    package = PipPackage("aider-chat")
    broken_envs = []
    for index in range(pip_global_module.MAX_ENV_ROOTS):
        broken_env = tmp_path / f"a-broken-{index:02}"
        broken_env.symlink_to(
            tmp_path / f"missing-{index}",
            target_is_directory=True,
        )
        broken_envs.append(broken_env)
    valid_env = tmp_path / "z-valid"
    metadata = (
        valid_env
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")

    findings = scan_pip_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[*broken_envs, valid_env],
        discover_hidden=False,
    )

    assert findings[package.name].metadata_path == metadata


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_symlinked_environment_is_resolved_once_for_all_package_roots(
    tmp_path: Path,
):
    real_env = tmp_path / "real-runtime"
    metadata_by_package = {
        "aider-chat": (
            real_env
            / "lib"
            / "python3.12"
            / "site-packages"
            / "aider_chat-1.2.3.dist-info"
            / "METADATA"
        ),
        "mcp-server-git": (
            real_env
            / "lib"
            / "python3.12"
            / "dist-packages"
            / "mcp_server_git-2.3.4.dist-info"
            / "METADATA"
        ),
    }
    for package_name, metadata in metadata_by_package.items():
        metadata.parent.mkdir(parents=True)
        version = "1.2.3" if package_name == "aider-chat" else "2.3.4"
        metadata.write_text(f"Name: {package_name}\nVersion: {version}\n")
    linked_env = tmp_path / "linked-runtime"
    linked_env.symlink_to(real_env, target_is_directory=True)

    findings = scan_pip_global_packages(
        [PipPackage(name) for name in metadata_by_package],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[linked_env],
        discover_hidden=False,
    )

    assert {
        package_name: finding.metadata_path
        for package_name, finding in findings.items()
    } == metadata_by_package


def test_windows_system_scan_skips_symlinked_environment(
    tmp_path: Path,
    monkeypatch,
):
    real_env = tmp_path / "real-runtime"
    metadata = (
        real_env
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    linked_env = tmp_path / "linked-runtime"
    try:
        linked_env.symlink_to(real_env, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    original_scandir = os.scandir
    original_stat = Path.stat
    original_read = pip_global_module.read_bounded

    def guarded_scandir(path):
        candidate = Path(path)
        if (
            candidate == linked_env
            or candidate == real_env
            or real_env in candidate.parents
        ):
            raise AssertionError("SYSTEM followed linked environment")
        return original_scandir(path)

    def guarded_stat(path, *args, **kwargs):
        if path == real_env or real_env in path.parents:
            raise AssertionError("SYSTEM statted linked environment target")
        return original_stat(path, *args, **kwargs)

    def guarded_read(path, *, max_bytes):
        if path == real_env or real_env in path.parents:
            raise AssertionError("SYSTEM read linked environment target")
        return original_read(path, max_bytes=max_bytes)

    monkeypatch.setattr(
        pip_global_module,
        "is_windows_system_context",
        lambda: True,
    )
    monkeypatch.setattr(pip_global_module.os, "scandir", guarded_scandir)
    monkeypatch.setattr(Path, "stat", guarded_stat)
    monkeypatch.setattr(pip_global_module, "read_bounded", guarded_read)

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[linked_env],
        discover_hidden=False,
    )

    assert findings == {}


def test_windows_system_scan_keeps_real_environment_roots(
    tmp_path: Path,
    monkeypatch,
):
    env = tmp_path / "runtime"
    metadata = (
        env
        / "lib"
        / "python3.12"
        / "site-packages"
        / "aider_chat-1.2.3.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    monkeypatch.setattr(
        pip_global_module,
        "is_windows_system_context",
        lambda: True,
    )

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_external_site_packages_root(tmp_path: Path):
    env = tmp_path / "runtime"
    python_lib = env / "lib" / "python3.12"
    python_lib.mkdir(parents=True)
    external_site = tmp_path / "external-site-packages"
    metadata = external_site / "aider_chat-1.2.3.dist-info" / "METADATA"
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    (python_lib / "site-packages").symlink_to(
        external_site,
        target_is_directory=True,
    )

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


def test_windows_system_scan_never_traverses_linked_site_packages(
    tmp_path: Path,
    monkeypatch,
):
    env = tmp_path / "runtime"
    python_lib = env / "lib" / "python3.12"
    python_lib.mkdir(parents=True)
    external_site = tmp_path / "external-site-packages"
    metadata = external_site / "aider_chat-1.2.3.dist-info" / "METADATA"
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    linked_site = python_lib / "site-packages"
    linked_site.symlink_to(external_site, target_is_directory=True)
    original_scandir = os.scandir
    original_stat = Path.stat
    original_read = pip_global_module.read_bounded

    def guarded_scandir(path):
        candidate = Path(path)
        if candidate == linked_site or candidate == external_site:
            raise AssertionError("SYSTEM followed linked site-packages")
        return original_scandir(path)

    def guarded_stat(path, *args, **kwargs):
        if path == external_site or external_site in path.parents:
            raise AssertionError("SYSTEM statted linked site-packages target")
        return original_stat(path, *args, **kwargs)

    def guarded_read(path, *, max_bytes):
        if path == external_site or external_site in path.parents:
            raise AssertionError("SYSTEM read linked site-packages target")
        return original_read(path, max_bytes=max_bytes)

    monkeypatch.setattr(
        pip_global_module,
        "is_windows_system_context",
        lambda: True,
    )
    monkeypatch.setattr(pip_global_module.os, "scandir", guarded_scandir)
    monkeypatch.setattr(Path, "stat", guarded_stat)
    monkeypatch.setattr(pip_global_module, "read_bounded", guarded_read)

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_external_dist_info_directory(tmp_path: Path):
    env = tmp_path / "runtime"
    site_packages = env / "lib" / "python3.12" / "site-packages"
    site_packages.mkdir(parents=True)
    external_dist_info = tmp_path / "external-dist-info"
    metadata = external_dist_info / "METADATA"
    external_dist_info.mkdir()
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    (site_packages / "aider_chat-1.2.3.dist-info").symlink_to(
        external_dist_info,
        target_is_directory=True,
    )

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_rejects_symlinked_metadata(tmp_path: Path):
    env = tmp_path / "runtime"
    dist_info = (
        env / "lib" / "python3.12" / "site-packages" / "aider_chat-1.2.3.dist-info"
    )
    dist_info.mkdir(parents=True)
    external_metadata = tmp_path / "external-metadata"
    external_metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    (dist_info / "METADATA").symlink_to(external_metadata)

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_unvisited_dist_info_target_inside_site_packages(
    tmp_path: Path,
):
    env = tmp_path / "runtime"
    site_packages = env / "lib" / "python3.12" / "site-packages"
    staged = site_packages / "staged"
    staged.mkdir(parents=True)
    (staged / "METADATA").write_text("Name: aider-chat\nVersion: 1.2.3\n")
    (site_packages / "aider_chat-1.2.3.dist-info").symlink_to(
        staged,
        target_is_directory=True,
    )

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == staged / "METADATA"


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_skips_broken_and_looped_dist_info_links(tmp_path: Path):
    env = tmp_path / "runtime"
    site_packages = env / "lib" / "python3.12" / "site-packages"
    site_packages.mkdir(parents=True)
    broken = site_packages / "broken.dist-info"
    broken.symlink_to(tmp_path / "missing", target_is_directory=True)
    looped = site_packages / "looped.dist-info"
    loop_peer = tmp_path / "loop-peer"
    looped.symlink_to(loop_peer, target_is_directory=True)
    loop_peer.symlink_to(looped, target_is_directory=True)

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_caps_followed_dist_info_targets(tmp_path: Path):
    env = tmp_path / "runtime"
    site_packages = env / "lib" / "python3.12" / "site-packages"
    site_packages.mkdir(parents=True)
    packages = [
        PipPackage(f"external-package-{index:02}")
        for index in range(pip_global_module.MAX_FOLLOWED_SYMLINK_TARGETS + 1)
    ]
    for package in packages:
        external_dist_info = tmp_path / "outside" / package.name
        external_dist_info.mkdir(parents=True)
        (external_dist_info / "METADATA").write_text(
            f"Name: {package.name}\nVersion: 1.2.3\n"
        )
        (site_packages / f"{package.name}.dist-info").symlink_to(
            external_dist_info,
            target_is_directory=True,
        )

    findings = scan_pip_global_packages(
        packages,
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert tuple(findings) == tuple(
        package.name
        for package in packages[: pip_global_module.MAX_FOLLOWED_SYMLINK_TARGETS]
    )


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_invalid_dist_info_links_do_not_consume_follow_cap(tmp_path: Path):
    env = tmp_path / "runtime"
    site_packages = env / "lib" / "python3.12" / "site-packages"
    site_packages.mkdir(parents=True)
    for index in range(pip_global_module.MAX_FOLLOWED_SYMLINK_TARGETS):
        external_dist_info = tmp_path / "outside" / f"invalid-{index:02}"
        external_dist_info.mkdir(parents=True)
        (external_dist_info / "METADATA").write_text(
            "Name: wrong-package\nVersion: 1.2.3\n"
        )
        (site_packages / f"a-invalid-{index:02}.dist-info").symlink_to(
            external_dist_info,
            target_is_directory=True,
        )
    valid_dist_info = tmp_path / "outside" / "valid"
    valid_dist_info.mkdir()
    valid_metadata = valid_dist_info / "METADATA"
    valid_metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    (site_packages / "z-valid.dist-info").symlink_to(
        valid_dist_info,
        target_is_directory=True,
    )

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == valid_metadata


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_empty_site_packages_links_do_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.setattr(pip_global_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)
    empty_env = tmp_path / "a-empty-env"
    empty_parent = empty_env / "lib" / "python3.12"
    empty_parent.mkdir(parents=True)
    empty_site = tmp_path / "empty-site"
    empty_site.mkdir()
    (empty_parent / "site-packages").symlink_to(
        empty_site,
        target_is_directory=True,
    )

    valid_env = tmp_path / "z-valid-env"
    valid_parent = valid_env / "lib" / "python3.12"
    valid_parent.mkdir(parents=True)
    valid_site = tmp_path / "valid-site"
    valid_metadata = valid_site / "aider_chat-1.2.3.dist-info" / "METADATA"
    valid_metadata.parent.mkdir(parents=True)
    valid_metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    (valid_parent / "site-packages").symlink_to(
        valid_site,
        target_is_directory=True,
    )

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[empty_env, valid_env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == valid_metadata


def test_metadata_walk_checkpoints_resource_governor(tmp_path: Path):
    venv = tmp_path / "relocated-runtime"
    site_packages = venv / "lib" / "python3.12" / "site-packages"
    site_packages.mkdir(parents=True)
    for index in range(3):
        (site_packages / f"unrelated-{index}.dist-info").mkdir()
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[venv],
        discover_hidden=False,
        checkpoint=checkpoint,
    )

    assert checkpoints >= 4


def test_child_directory_discovery_caps_dirents_and_checkpoints(
    tmp_path: Path,
    monkeypatch,
):
    for index in range(5):
        (tmp_path / f"environment-{index}").mkdir()
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    monkeypatch.setattr(pip_global_module, "MAX_CHILD_ENTRIES", 3)

    children = pip_global_module._bounded_child_directories(  # noqa: SLF001
        tmp_path,
        checkpoint=checkpoint,
    )

    assert len(children) == 3
    assert set(children) <= {tmp_path / f"environment-{index}" for index in range(5)}
    assert checkpoints == 3


def test_site_packages_overflow_scans_bounded_prefix(
    tmp_path: Path,
    monkeypatch,
):
    env = tmp_path / "runtime"
    site_packages = env / "lib" / "python3.12" / "site-packages"
    metadata = site_packages / "aider_chat-1.2.3.dist-info" / "METADATA"
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 1.2.3\n")
    overflow_entry = site_packages / "overflow.dist-info"
    overflow_entry.mkdir()
    real_scandir = os.scandir

    class _OrderedScandir:
        def __enter__(self):
            return iter(
                [
                    type("_Entry", (), {"name": metadata.parent.name})(),
                    type("_Entry", (), {"name": overflow_entry.name})(),
                ]
            )

        def __exit__(self, *_args):
            return False

    def ordered_scandir(path):
        if Path(path) == site_packages:
            return _OrderedScandir()
        return real_scandir(path)

    monkeypatch.setattr(pip_global_module, "MAX_SITE_ENTRIES", 1)
    monkeypatch.setattr(pip_global_module.os, "scandir", ordered_scandir)

    findings = scan_pip_global_packages(
        [PipPackage("aider-chat")],
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=[env],
        discover_hidden=False,
    )

    assert findings["aider-chat"].metadata_path == metadata


def test_python_directory_filter_does_not_spend_match_cap_on_noise(
    tmp_path: Path,
):
    for index in range(pip_global_module.MAX_TOOL_ENVS_PER_ROOT):
        (tmp_path / f"noise-{index}").mkdir()
    python_dir = tmp_path / "python3.13"
    python_dir.mkdir()

    assert pip_global_module._bounded_child_directories(  # noqa: SLF001
        tmp_path,
        name_prefix="python",
    ) == [python_dir]


def test_standard_env_root_cap_round_robins_tool_managers(
    monkeypatch,
    tmp_path: Path,
):
    pipx_root = tmp_path / "pipx" / "venvs"
    uv_root = tmp_path / "uv"
    pipx_envs = [
        pipx_root / f"environment-{index}"
        for index in range(pip_global_module.MAX_ENV_ROOTS)
    ]
    uv_env = uv_root / "agent"

    def fake_children(
        root: Path,
        *,
        name_prefix: str | None = None,
        checkpoint=None,
        windows_system_context: bool = False,
    ) -> list[Path]:
        del name_prefix, checkpoint, windows_system_context
        if root == pipx_root:
            return pipx_envs
        if root == uv_root:
            return [uv_env]
        return []

    monkeypatch.setattr(
        pip_global_module,
        "_bounded_child_directories",
        fake_children,
    )

    roots = pip_global_module._standard_env_roots(  # noqa: SLF001
        home=tmp_path,
        system="Linux",
        environment={
            "PIPX_HOME": str(tmp_path / "pipx"),
            "UV_TOOL_DIR": str(uv_root),
        },
        checkpoint=None,
        windows_system_context=False,
    )

    assert len(roots) == pip_global_module.MAX_ENV_ROOTS
    assert uv_env in roots


def test_site_package_cap_does_not_eagerly_walk_one_source(
    monkeypatch,
    tmp_path: Path,
):
    standard_envs = [tmp_path / "standard-1", tmp_path / "standard-2"]
    system_site = tmp_path / "system-site"
    visited_envs: list[Path] = []

    monkeypatch.setattr(pip_global_module, "MAX_SITE_PACKAGES", 2)
    monkeypatch.setattr(
        pip_global_module,
        "_standard_env_roots",
        lambda **_kwargs: standard_envs,
    )
    monkeypatch.setattr(
        pip_global_module,
        "_user_site_packages",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        pip_global_module,
        "_system_site_packages",
        lambda *_args, **_kwargs: [system_site],
    )

    def fake_site_packages(
        env_root: Path,
        *,
        checkpoint=None,
        windows_system_context: bool = False,
    ) -> list[Path]:
        del checkpoint, windows_system_context
        visited_envs.append(env_root)
        return [env_root / "site-packages"]

    monkeypatch.setattr(
        pip_global_module,
        "_site_packages_for_env",
        fake_site_packages,
    )

    roots = pip_global_module._site_packages_roots(  # noqa: SLF001
        home=tmp_path,
        system="Linux",
        environment={},
        python_env_roots=(),
        checkpoint=None,
        windows_system_context=False,
    )

    assert roots == [standard_envs[0] / "site-packages", system_site]
    assert visited_envs == [standard_envs[0]]
