"""Tests for the dependency-free AI Watch uninstaller."""

from __future__ import annotations

import ast
import json
import os
import plistlib
import shutil
import signal
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from runlayer_cli import aiwatch_uninstall


def test_runlayer_command_matcher_covers_current_and_legacy_forms() -> None:
    own_commands = (
        '"/usr/local/lib/runlayer/aiwatch/aiwatch" hook --client cursor',
        r'& "C:\Program Files\Runlayer\AIWatch\aiwatch.exe" hook --client codex',
        r'"C:\Program Files\Runlayer\AIWatch\AIWATCH.EXE" HOOK --client cursor',
        '"/usr/local/lib/runlayer/aiwatch/aiwatch-hook" hook --client cursor',
        "/tmp/runlayer-hook.sh cursor",
        f"{sys.executable} -m runlayer_cli.hook --client claude_code",
    )
    for command in own_commands:
        assert aiwatch_uninstall.is_runlayer_command(command), command

    assert not aiwatch_uninstall.is_runlayer_command("/opt/acme/run-hook")
    assert not aiwatch_uninstall.is_runlayer_command("echo aiwatch")


def test_runlayer_command_matcher_stays_aligned_with_hook_install() -> None:
    from runlayer_cli.hook_install import clients

    uninstall_names = set(aiwatch_uninstall._RUNLAYER_SCRIPT_NAMES)
    install_names = set(clients._RUNLAYER_SCRIPT_NAMES)
    assert install_names <= uninstall_names
    assert uninstall_names - install_names == {"runlayer-hook.exe"}

    own_commands = (
        *(f"/opt/runlayer/{name} hook" for name in sorted(uninstall_names)),
        '"/opt/runlayer/aiwatch" hook --client cursor',
        r'& "C:\Program Files\Runlayer\runlayer.exe" hook --client codex',
        f"{sys.executable} -m runlayer_cli.hook --client claude_code",
    )
    third_party_commands = (
        "/opt/acme/run-hook",
        "echo aiwatch",
        "/opt/runlayer/aiwatch scan",
        "/opt/runlayer/runlayer setup",
    )
    for command in own_commands:
        assert aiwatch_uninstall.is_runlayer_command(command), command
        assert clients._is_runlayer_command(command), command
    for command in third_party_commands:
        assert not aiwatch_uninstall.is_runlayer_command(command), command
        assert not clients._is_runlayer_command(command), command


def test_browser_policy_constants_stay_aligned_with_install_side() -> None:
    from runlayer_cli.hook_install import browser_extension, firefox_extension

    assert (
        aiwatch_uninstall._RUNLAYER_CHROME_EXTENSION_ID
        == browser_extension.RUNLAYER_CHROME_EXTENSION_ID
    )
    assert (
        aiwatch_uninstall._RUNLAYER_FIREFOX_EXTENSION_ID
        == firefox_extension.RUNLAYER_FIREFOX_EXTENSION_ID
    )


def test_managed_grok_config_constants_stay_aligned_with_install_side() -> None:
    from runlayer_cli import mdm_config

    assert aiwatch_uninstall._MACOS_MANAGED_CONFIG_PATHS == mdm_config.MACOS_PLIST_PATHS
    assert aiwatch_uninstall._GROK_HOME_KEY == mdm_config.GROK_HOME_KEY
    assert aiwatch_uninstall._HOST_KEY == mdm_config.HOST_KEY


@pytest.mark.parametrize(
    ("url", "managed_host"),
    [
        (
            "https://downloads.runlayer.com/extension/update_manifest.xml",
            None,
        ),
        (
            "https://tenant.runlayer.com/api/v1/binary-packages/"
            "browser-extension/chrome/token/update.xml",
            None,
        ),
        (
            "https://tenant.runlayer.com/api/v1/binary-packages/"
            "browser-extension/chrome/token/update.xml/",
            None,
        ),
        (
            "https://tenant.runlayer.com/api/v1/binary-packages/"
            "browser-extension/chrome/token/nested/update.xml",
            None,
        ),
        (
            "https://ai.customer.example/api/v1/binary-packages/"
            "browser-extension/chrome/token/update.xml",
            "https://ai.customer.example",
        ),
        (
            "https://extensions.runlayer.example/aiwatch/update.xml",
            None,
        ),
        (
            "https://downloads.runlayer.com/cli/manifest.json",
            None,
        ),
        (
            "https://extensions.example.com/extension/update_manifest.xml",
            None,
        ),
    ],
)
def test_runlayer_update_url_matcher_stays_aligned_with_install_side(
    url: str,
    managed_host: str | None,
) -> None:
    from runlayer_cli.hook_install import browser_extension

    assert aiwatch_uninstall._is_runlayer_update_url(
        url,
        managed_host=managed_host,
    ) == browser_extension._is_runlayer_update_url(
        url,
        managed_host=managed_host,
    )


def test_without_runlayer_hooks_preserves_third_party_nested_entries() -> None:
    hooks = {
        "PreToolUse": [
            {
                "matcher": "",
                "hooks": [
                    {
                        "type": "command",
                        "command": "/usr/local/bin/aiwatch hook --client claude_code",
                    },
                    {"type": "command", "command": "/opt/acme/hook"},
                ],
            }
        ],
        "Stop": [
            {
                "type": "command",
                "bash": "/opt/acme/stop",
                "powershell": r"C:\Acme\stop.exe",
            },
            {
                "type": "command",
                "bash": "/usr/local/bin/aiwatch-hook hook",
                "powershell": r"C:\Runlayer\aiwatch-hook.exe hook",
            },
        ],
    }

    assert aiwatch_uninstall.without_runlayer_hooks(hooks) == {
        "PreToolUse": [
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": "/opt/acme/hook"}],
            }
        ],
        "Stop": [
            {
                "type": "command",
                "bash": "/opt/acme/stop",
                "powershell": r"C:\Acme\stop.exe",
            }
        ],
    }


def test_without_runlayer_hooks_keeps_cleaned_nested_sibling_fields() -> None:
    hooks = {
        "Stop": [
            {
                "hooks": [
                    {
                        "command": "/usr/local/bin/aiwatch hook --client claude_code",
                        "bash": "/opt/acme/stop",
                    }
                ]
            }
        ]
    }

    assert aiwatch_uninstall.without_runlayer_hooks(hooks) == {
        "Stop": [{"hooks": [{"bash": "/opt/acme/stop"}]}]
    }


def test_without_runlayer_hooks_keeps_parent_when_nested_hooks_empty() -> None:
    hooks = {
        "PreToolUse": [
            {
                "command": "/opt/acme/parent-hook",
                "hooks": [
                    {
                        "command": "/usr/local/bin/aiwatch hook --client claude_code",
                    }
                ],
            }
        ]
    }

    assert aiwatch_uninstall.without_runlayer_hooks(hooks) == {
        "PreToolUse": [{"command": "/opt/acme/parent-hook"}]
    }


def test_clean_json_hooks_preserves_config_and_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text(
        json.dumps(
            {
                "theme": "dark",
                "hooks": {
                    "PreToolUse": [
                        {"command": "/opt/acme/hook"},
                        {"command": "/usr/local/bin/aiwatch hook --client cursor"},
                    ]
                },
            }
        )
    )

    assert aiwatch_uninstall.clean_json_hooks(path)
    assert json.loads(path.read_text()) == {
        "theme": "dark",
        "hooks": {"PreToolUse": [{"command": "/opt/acme/hook"}]},
    }
    first = path.read_bytes()
    assert not aiwatch_uninstall.clean_json_hooks(path)
    assert path.read_bytes() == first


def test_clean_json_hooks_verifies_before_replace(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    original = '{ "hooks": [not valid] }\n'
    path.write_text(original)

    assert not aiwatch_uninstall.clean_json_hooks(path)
    assert path.read_text() == original


def test_clean_jsonc_hooks_tolerates_comments_and_trailing_commas(
    tmp_path: Path,
) -> None:
    path = tmp_path / "settings.json"
    path.write_text(
        """\
{
  // Existing user setting.
  "theme": "dark",
  "hooks": {
    "PreToolUse": [
      {"command": "/usr/local/bin/aiwatch hook --client cursor"},
    ],
  },
}
"""
    )

    assert aiwatch_uninstall.clean_json_hooks(path)
    assert json.loads(path.read_text()) == {"theme": "dark"}


def test_clean_json_hooks_refuses_symlink_target(tmp_path: Path) -> None:
    target = tmp_path / "outside.json"
    original = json.dumps(
        {"hooks": {"PreToolUse": [{"command": "/usr/local/bin/aiwatch hook"}]}}
    )
    target.write_text(original)
    link = tmp_path / "settings.json"
    link.symlink_to(target)

    assert not aiwatch_uninstall.clean_json_hooks(link)
    assert target.read_text() == original


def _swap_directory_for_symlink(directory: Path, outside: Path) -> None:
    parked = directory.with_name(f"{directory.name}.parked")
    directory.rename(parked)
    directory.symlink_to(outside, target_is_directory=True)


def test_anchored_read_rejects_intermediate_symlink_swap(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home"
    parent = home / ".claude"
    parent.mkdir(parents=True)
    target = parent / "settings.json"
    target.write_text('{"theme": "dark"}')
    outside = tmp_path / "outside"
    outside.mkdir()
    outside_target = outside / target.name
    outside_target.write_text('{"outside": true}')
    outside_before = outside_target.read_bytes()
    real_open = os.open
    swapped = False

    def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
        nonlocal swapped
        if not swapped and (Path(path) == target or path == parent.name):
            swapped = True
            _swap_directory_for_symlink(parent, outside)
        return real_open(path, flags, mode, dir_fd=dir_fd)

    monkeypatch.setattr(aiwatch_uninstall.os, "open", swapping_open)

    assert aiwatch_uninstall._read_regular_text(target, anchor=home) is None
    assert outside_target.read_bytes() == outside_before


def test_anchored_replace_does_not_follow_swapped_intermediate_directory(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home"
    swapped_parent = home / ".claude"
    parent = swapped_parent / "config"
    parent.mkdir(parents=True)
    target = parent / "settings.json"
    target.write_text('{"theme": "dark"}')
    snapshot = aiwatch_uninstall._read_regular_text(target, anchor=home)
    assert snapshot is not None
    outside = tmp_path / "outside"
    outside_parent = outside / "config"
    outside_parent.mkdir(parents=True)
    outside_target = outside_parent / target.name
    os.link(target, outside_target)
    outside_before = outside_target.read_bytes()
    real_open = os.open
    swapped = False

    def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
        nonlocal swapped
        if not swapped and (Path(path) == parent or path == swapped_parent.name):
            swapped = True
            _swap_directory_for_symlink(swapped_parent, outside)
        return real_open(path, flags, mode, dir_fd=dir_fd)

    monkeypatch.setattr(aiwatch_uninstall.os, "open", swapping_open)

    assert not aiwatch_uninstall._atomic_replace(
        target,
        b'{"theme": "light"}\n',
        snapshot,
        anchor=home,
    )
    assert outside_target.read_bytes() == outside_before


def test_anchored_unlink_does_not_follow_swapped_intermediate_directory(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home"
    parent = home / ".claude"
    parent.mkdir(parents=True)
    target = parent / "runlayer.json"
    target.write_text("{}")
    outside = tmp_path / "outside"
    outside.mkdir()
    outside_target = outside / target.name
    outside_target.write_text("outside")
    real_unlink = os.unlink
    swapped = False

    def swapping_unlink(path, *, dir_fd=None):
        nonlocal swapped
        if not swapped and (Path(path) == target or path == target.name):
            swapped = True
            _swap_directory_for_symlink(parent, outside)
        return real_unlink(path, dir_fd=dir_fd)

    monkeypatch.setattr(aiwatch_uninstall.os, "unlink", swapping_unlink)

    assert aiwatch_uninstall._unlink_regular(target, anchor=home)
    assert outside_target.read_text() == "outside"


def test_owned_tree_removal_rejects_intermediate_symlink_swap(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home"
    first_parent = home / ".agents"
    target = first_parent / "plugins" / "runlayer-hooks"
    target.mkdir(parents=True)
    (target / "plugin.json").write_text("{}")
    outside = tmp_path / "outside"
    outside_target = outside / "plugins" / "runlayer-hooks"
    outside_target.mkdir(parents=True)
    outside_file = outside_target / "third-party.json"
    outside_file.write_text("outside")
    real_open = os.open
    real_rmtree = shutil.rmtree
    swapped = False

    def swap_once() -> None:
        nonlocal swapped
        if not swapped:
            swapped = True
            _swap_directory_for_symlink(first_parent, outside)

    def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
        if Path(path) == target or path == first_parent.name:
            swap_once()
        return real_open(path, flags, mode, dir_fd=dir_fd)

    def swapping_rmtree(path, *args, **kwargs):
        if Path(path) == target:
            swap_once()
        return real_rmtree(path, *args, **kwargs)

    monkeypatch.setattr(aiwatch_uninstall.os, "open", swapping_open)
    monkeypatch.setattr(aiwatch_uninstall.shutil, "rmtree", swapping_rmtree)

    assert not aiwatch_uninstall._remove_owned_tree(target, anchor=home)
    assert outside_file.read_text() == "outside"


def test_clean_runlayer_named_json_deletes_only_when_empty(tmp_path: Path) -> None:
    empty_after_filter = tmp_path / "runlayer.json"
    empty_after_filter.write_text(
        json.dumps(
            {
                "version": 1,
                "hooks": {
                    "PreToolUse": [{"command": "/usr/local/bin/aiwatch-hook hook"}]
                },
            }
        )
    )
    with_third_party = tmp_path / "runlayer-with-third-party.json"
    with_third_party.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"command": "/usr/local/bin/aiwatch-hook hook"},
                        {"command": "/opt/acme/hook"},
                    ]
                }
            }
        )
    )

    assert aiwatch_uninstall.clean_json_hooks(
        empty_after_filter, delete_when_empty=True
    )
    assert not empty_after_filter.exists()
    assert aiwatch_uninstall.clean_json_hooks(with_third_party, delete_when_empty=True)
    assert json.loads(with_third_party.read_text()) == {
        "hooks": {"PreToolUse": [{"command": "/opt/acme/hook"}]}
    }


def test_clean_vscode_settings_removes_only_runlayer_values(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text(
        json.dumps(
            {
                "editor.tabSize": 2,
                "chat.hookFilesLocations": {
                    "~/.copilot/hooks": True,
                    ".claude/settings.json": False,
                    ".claude/settings.local.json": False,
                    "~/.claude/settings.json": False,
                    "~/acme/hooks": True,
                },
            }
        )
    )

    assert aiwatch_uninstall.clean_vscode_settings(path)
    assert json.loads(path.read_text()) == {
        "editor.tabSize": 2,
        "chat.hookFilesLocations": {"~/acme/hooks": True},
    }


def test_clean_hermes_yaml_preserves_non_runlayer_content(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(
        """\
mcp_servers:
  linear:
    url: https://linear.example/mcp
hooks:
  pre_tool_call:
  - command: /usr/local/bin/aiwatch hook --client hermes
  - command: /opt/acme/hook
  transform_tool_result:
  - command: /usr/local/bin/aiwatch-hook hook --client hermes
model: auto
"""
    )

    assert aiwatch_uninstall.clean_hermes_yaml(path)
    assert (
        path.read_text()
        == """\
mcp_servers:
  linear:
    url: https://linear.example/mcp
hooks:
  pre_tool_call:
  - command: /opt/acme/hook
model: auto
"""
    )
    first = path.read_bytes()
    assert not aiwatch_uninstall.clean_hermes_yaml(path)
    assert path.read_bytes() == first


def test_strip_managed_ignore_block_preserves_user_lines(tmp_path: Path) -> None:
    path = tmp_path / ".cursorignore"
    path.write_text(
        """\
dist/

# >>> Runlayer managed - do not edit >>>
.env
mcp.json
# <<< Runlayer managed <<<

vendor/
"""
    )

    assert aiwatch_uninstall.strip_managed_ignore_block(path)
    assert path.read_text() == "dist/\n\nvendor/\n"
    assert not aiwatch_uninstall.strip_managed_ignore_block(path)


def test_strip_only_managed_ignore_block_deletes_file(tmp_path: Path) -> None:
    path = tmp_path / ".claudeignore"
    path.write_text(
        """\
# >>> Runlayer managed - do not edit >>>
.env
# <<< Runlayer managed <<<
"""
    )

    assert aiwatch_uninstall.strip_managed_ignore_block(path)
    assert not path.exists()


def test_clean_cline_scripts_leaves_unowned_files(tmp_path: Path) -> None:
    hooks = tmp_path / ".cline" / "hooks"
    hooks.mkdir(parents=True)
    owned = hooks / "PreToolUse.sh"
    owned.write_text(
        "#!/bin/sh\n# runlayer-owned Cline hook — safe to delete\nexec aiwatch hook\n"
    )
    legacy = hooks / "SessionStart.zsh"
    legacy.write_text("#!/bin/zsh\n/usr/local/bin/aiwatch-hook hook\n")
    third_party = hooks / "PreToolUse.bash"
    third_party.write_text("#!/bin/bash\nexec /opt/acme/hook\n")

    assert aiwatch_uninstall.clean_cline_scripts(hooks) == 2
    assert not owned.exists()
    assert not legacy.exists()
    assert third_party.exists()
    assert aiwatch_uninstall.clean_cline_scripts(hooks) == 0


def test_clean_browser_owned_artifacts_strips_only_runlayer_forcelist_entry(
    tmp_path: Path,
) -> None:
    managed = tmp_path / "Managed Preferences"
    external = tmp_path / "External Extensions"
    managed.mkdir()
    external.mkdir()
    shared = managed / "com.google.Chrome.plist"
    shared.write_bytes(
        plistlib.dumps(
            {
                "ExtensionInstallForcelist": [
                    "jijfcalfdbnjfpfcalkodmgmfijpfddi;"
                    "https://downloads.runlayer.com/extension/update_manifest.xml",
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;https://acme.test/update.xml",
                ]
            }
        )
    )
    extension_id = "jijfcalfdbnjfpfcalkodmgmfijpfddi"
    extension_policy = managed / f"com.google.Chrome.extensions.{extension_id}.plist"
    extension_policy.write_bytes(
        plistlib.dumps({"Host": "https://tenant.runlayer.com"})
    )
    external_entry = external / f"{extension_id}.json"
    external_entry.write_text(
        json.dumps(
            {
                "external_update_url": (
                    "https://downloads.runlayer.com/extension/update_manifest.xml"
                )
            }
        )
    )

    extension_ids = aiwatch_uninstall.clean_chrome_force_install_policy(shared)

    assert extension_ids == {extension_id}
    assert (
        aiwatch_uninstall.clean_browser_owned_artifacts(
            managed,
            external,
            extension_ids=extension_ids,
        )
        == 2
    )
    assert not extension_policy.exists()
    assert not external_entry.exists()
    assert plistlib.loads(shared.read_bytes()) == {
        "ExtensionInstallForcelist": [
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;https://acme.test/update.xml"
        ]
    }


def test_chrome_force_policy_ids_drive_partial_install_artifact_cleanup(
    tmp_path: Path,
) -> None:
    managed = tmp_path / "Managed Preferences"
    external = tmp_path / "External Extensions"
    managed.mkdir()
    external.mkdir()
    extension_id = "b" * 32
    shared = managed / "com.google.Chrome.plist"
    shared.write_bytes(
        plistlib.dumps(
            {
                "ExtensionInstallForcelist": [
                    f"{extension_id};"
                    "https://ai.customer.example/api/v1/binary-packages/"
                    "browser-extension/chrome/token/update.xml"
                ]
            }
        )
    )
    extension_policy = managed / f"com.google.Chrome.extensions.{extension_id}.plist"
    extension_policy.write_bytes(
        plistlib.dumps(
            {
                "Host": "https://tenant.runlayer.com",
                "OrgApiKey": "rl_org_secret",
            }
        )
    )

    extension_ids = aiwatch_uninstall.clean_chrome_force_install_policy(
        shared,
        managed_host="https://ai.customer.example",
    )

    assert extension_ids == {extension_id}
    assert (
        aiwatch_uninstall.clean_browser_owned_artifacts(
            managed,
            external,
            extension_ids=extension_ids,
        )
        == 1
    )
    assert not shared.exists()
    assert not extension_policy.exists()


def test_firefox_install_uninstall_roundtrip_preserves_shared_policy(
    tmp_path: Path,
) -> None:
    from runlayer_cli.hook_install import firefox_extension

    path = tmp_path / "org.mozilla.firefox.plist"
    pre_install = {
        "EnterprisePoliciesEnabled": True,
        "DisableTelemetry": True,
        "ExtensionSettings": {
            "other@example.com": {"installation_mode": "allowed"},
        },
        "3rdparty": {
            "Extensions": {
                "other@example.com": {"Host": "https://other.example"},
            },
        },
    }
    installed = firefox_extension.expected_firefox_policy(
        pre_install,
        extension_id=firefox_extension.RUNLAYER_FIREFOX_EXTENSION_ID,
        install_url=firefox_extension.RUNLAYER_FIREFOX_INSTALL_URL,
        managed={
            "host": "https://tenant.runlayer.com",
            "org_api_key": "rl_org_secret",
        },
    )
    path.write_bytes(plistlib.dumps(installed, fmt=plistlib.FMT_BINARY))

    assert aiwatch_uninstall.clean_firefox_policy(path)
    assert plistlib.loads(path.read_bytes()) == pre_install
    assert b"OrgApiKey" not in path.read_bytes()
    assert b"rl_org_secret" not in path.read_bytes()


def test_firefox_uninstall_deletes_runlayer_only_policy(tmp_path: Path) -> None:
    from runlayer_cli.hook_install import firefox_extension

    path = tmp_path / "org.mozilla.firefox.plist"
    installed = firefox_extension.expected_firefox_policy(
        {},
        extension_id=firefox_extension.RUNLAYER_FIREFOX_EXTENSION_ID,
        install_url=firefox_extension.RUNLAYER_FIREFOX_INSTALL_URL,
        managed={
            "host": "https://tenant.runlayer.com",
            "org_api_key": "rl_org_secret",
        },
    )
    path.write_bytes(plistlib.dumps(installed))

    assert aiwatch_uninstall.clean_firefox_policy(path)
    assert not path.exists()


def test_firefox_uninstall_preserves_unowned_enterprise_enabled_policy(
    tmp_path: Path,
) -> None:
    path = tmp_path / "org.mozilla.firefox.plist"
    original = plistlib.dumps({"EnterprisePoliciesEnabled": True})
    path.write_bytes(original)

    assert not aiwatch_uninstall.clean_firefox_policy(path)
    assert path.read_bytes() == original


def test_chrome_install_uninstall_roundtrip_preserves_shared_policy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from runlayer_cli.hook_install import browser_extension

    monkeypatch.setattr(browser_extension.platform, "system", lambda: "Darwin")
    managed_dir = tmp_path / "Managed Preferences"
    external_dir = tmp_path / "External Extensions"
    managed_dir.mkdir()
    shared = managed_dir / "com.google.Chrome.plist"
    third_party_entry = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;https://acme.test/update.xml"
    shared.write_bytes(
        plistlib.dumps({"ExtensionInstallForcelist": [third_party_entry]})
    )
    browser_extension.install_browser_extension(
        {
            "host": "https://tenant.runlayer.com",
            "org_api_key": "rl_org_secret",
            "browser_extension_id": (browser_extension.RUNLAYER_CHROME_EXTENSION_ID),
            "browser_extension_update_url": (
                browser_extension.RUNLAYER_CHROME_UPDATE_URL
            ),
        },
        managed_prefs_dir=managed_dir,
        external_dir=external_dir,
    )

    extension_ids = aiwatch_uninstall.clean_chrome_force_install_policy(shared)
    aiwatch_uninstall.clean_browser_owned_artifacts(
        managed_dir,
        external_dir,
        extension_ids=extension_ids,
    )

    assert plistlib.loads(shared.read_bytes()) == {
        "ExtensionInstallForcelist": [third_party_entry]
    }
    extension_id = browser_extension.RUNLAYER_CHROME_EXTENSION_ID
    assert not (
        managed_dir / f"com.google.Chrome.extensions.{extension_id}.plist"
    ).exists()
    assert not (external_dir / f"{extension_id}.json").exists()


def test_browser_policy_cleanup_refuses_intermediate_symlinks(
    tmp_path: Path,
) -> None:
    system_root = tmp_path / "system"
    library = system_root / "Library"
    library.mkdir(parents=True)

    outside_firefox = tmp_path / "outside-firefox"
    outside_firefox.mkdir()
    firefox_policy = outside_firefox / "org.mozilla.firefox.plist"
    firefox_policy.write_bytes(
        plistlib.dumps(
            {
                "ExtensionSettings": {
                    "aiwatch@runlayer.com": {
                        "installation_mode": "force_installed",
                    }
                }
            }
        )
    )
    firefox_before = firefox_policy.read_bytes()
    (library / "Preferences").symlink_to(
        outside_firefox,
        target_is_directory=True,
    )

    outside_chrome = tmp_path / "outside-chrome"
    outside_chrome.mkdir()
    chrome_policy = outside_chrome / "com.google.Chrome.plist"
    chrome_policy.write_bytes(
        plistlib.dumps(
            {
                "ExtensionInstallForcelist": [
                    "jijfcalfdbnjfpfcalkodmgmfijpfddi;"
                    "https://downloads.runlayer.com/extension/update_manifest.xml"
                ]
            }
        )
    )
    chrome_before = chrome_policy.read_bytes()
    (library / "Managed Preferences").symlink_to(
        outside_chrome,
        target_is_directory=True,
    )

    assert not aiwatch_uninstall.clean_firefox_policy(
        library / "Preferences" / firefox_policy.name,
        _anchor=system_root,
    )
    assert (
        aiwatch_uninstall.clean_chrome_force_install_policy(
            library / "Managed Preferences" / chrome_policy.name,
            _anchor=system_root,
        )
        == set()
    )
    assert firefox_policy.read_bytes() == firefox_before
    assert chrome_policy.read_bytes() == chrome_before


def test_browser_policy_phase_cleans_current_and_legacy_firefox(
    tmp_path: Path,
) -> None:
    from runlayer_cli.hook_install import firefox_extension

    system_root = tmp_path / "system"
    preferences = system_root / "Library" / "Preferences"
    managed = system_root / "Library" / "Managed Preferences"
    external = (
        system_root
        / "Library"
        / "Application Support"
        / "Google"
        / "Chrome"
        / "External Extensions"
    )
    preferences.mkdir(parents=True)
    managed.mkdir(parents=True)
    external.mkdir(parents=True)
    managed_config = {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
    }
    current = preferences / "org.mozilla.firefox.plist"
    current.write_bytes(
        plistlib.dumps(
            firefox_extension.expected_firefox_policy(
                {},
                extension_id=firefox_extension.RUNLAYER_FIREFOX_EXTENSION_ID,
                install_url=firefox_extension.RUNLAYER_FIREFOX_INSTALL_URL,
                managed=managed_config,
            )
        )
    )
    legacy_pre_install = {
        "EnterprisePoliciesEnabled": True,
        "DisableTelemetry": True,
    }
    legacy = managed / "org.mozilla.firefox.plist"
    legacy.write_bytes(
        plistlib.dumps(
            firefox_extension.expected_firefox_policy(
                legacy_pre_install,
                extension_id=firefox_extension.RUNLAYER_FIREFOX_EXTENSION_ID,
                install_url=firefox_extension.RUNLAYER_FIREFOX_INSTALL_URL,
                managed=managed_config,
            )
        )
    )
    chrome = managed / "com.google.Chrome.plist"
    chrome.write_bytes(
        plistlib.dumps(
            {
                "ExtensionInstallForcelist": [
                    "jijfcalfdbnjfpfcalkodmgmfijpfddi;"
                    "https://downloads.runlayer.com/extension/update_manifest.xml"
                ]
            }
        )
    )

    result = aiwatch_uninstall._clean_browser_policies(system_root)

    assert result == {"ok": True, "preferences_changed": True}
    assert not current.exists()
    assert plistlib.loads(legacy.read_bytes()) == legacy_pre_install
    assert not chrome.exists()


def test_browser_policy_phase_does_not_mark_legacy_firefox_as_system_preference(
    tmp_path: Path,
) -> None:
    system_root = tmp_path / "system"
    legacy = (
        system_root / "Library" / "Managed Preferences" / "org.mozilla.firefox.plist"
    )
    legacy.parent.mkdir(parents=True)
    legacy.write_bytes(
        plistlib.dumps(
            {
                "ExtensionSettings": {
                    "aiwatch@runlayer.com": {
                        "installation_mode": "force_installed",
                    }
                }
            }
        )
    )

    result = aiwatch_uninstall._clean_browser_policies(system_root)

    assert result == {"ok": True, "preferences_changed": False}
    assert not legacy.exists()


def test_clean_user_home_covers_all_owned_surfaces(tmp_path: Path) -> None:
    home = tmp_path / "alice"
    json_paths = (
        home / ".cursor" / "hooks.json",
        home / ".copilot" / "hooks" / "runlayer.json",
        home / ".claude" / "settings.json",
        home / ".codex" / "hooks.json",
        home / ".copilot" / "settings.json",
        home / ".codeium" / "windsurf" / "hooks.json",
        home / ".qwen" / "settings.json",
        home / ".gemini" / "settings.json",
        home / ".grok" / "hooks" / "runlayer.json",
        home / ".config" / "devin" / "config.json",
    )
    for path in json_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {"command": "/usr/local/bin/aiwatch hook --client cursor"}
                        ]
                    }
                }
            )
        )
    goose = home / ".agents" / "plugins" / "runlayer-hooks"
    goose.mkdir(parents=True)
    (goose / "plugin.json").write_text('{"name":"runlayer-hooks"}')
    legacy_vscode_hook = home / ".copilot" / "hooks" / "hooks" / "runlayer-hook.sh"
    legacy_vscode_hook.parent.mkdir(parents=True)
    legacy_vscode_hook.write_text(
        (Path(__file__).parents[1] / "hooks" / "runlayer-hook.sh").read_text()
    )

    assert aiwatch_uninstall.clean_user_home(home) > 0
    assert not goose.exists()
    assert not legacy_vscode_hook.exists()
    preserved_shared_configs = {
        home / ".claude" / "settings.json",
        home / ".qwen" / "settings.json",
        home / ".config" / "devin" / "config.json",
    }
    for path in json_paths:
        if path in preserved_shared_configs:
            assert path.exists()
            assert json.loads(path.read_text()) == {}
        else:
            assert not path.exists()
    assert aiwatch_uninstall.clean_user_home(home) == 0


def test_clean_user_home_sweeps_managed_grok_home(tmp_path: Path) -> None:
    home = tmp_path / "alice"
    hook_path = home / "managed-grok" / "hooks" / "runlayer.json"
    hook_path.parent.mkdir(parents=True)
    hook_path.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"command": ("/usr/local/bin/aiwatch hook --client grok_cli")}
                    ]
                }
            }
        )
    )

    assert (
        aiwatch_uninstall.clean_user_home(
            home,
            grok_home="~/managed-grok",
        )
        > 0
    )
    assert not hook_path.exists()


def test_clean_user_home_rejects_managed_grok_home_outside_home(
    tmp_path: Path,
) -> None:
    home = tmp_path / "alice"
    home.mkdir()
    hook_path = tmp_path / "outside" / "hooks" / "runlayer.json"
    hook_path.parent.mkdir(parents=True)
    hook_path.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"command": ("/usr/local/bin/aiwatch hook --client grok_cli")}
                    ]
                }
            }
        )
    )

    aiwatch_uninstall.clean_user_home(
        home,
        grok_home=str(hook_path.parents[1]),
    )

    assert hook_path.exists()


def test_read_managed_cleanup_config_uses_first_valid_config_path(
    tmp_path: Path,
) -> None:
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    managed.write_bytes(plistlib.dumps({"Host": "https://example.com"}))
    local.write_bytes(plistlib.dumps({"GrokHome": "~/local-grok"}))

    assert aiwatch_uninstall._read_managed_cleanup_config((managed, local)) == {
        "grok_home": "~/local-grok",
        "host": "https://example.com",
    }

    managed.write_bytes(plistlib.dumps({"GrokHome": "~/managed-grok"}))
    assert aiwatch_uninstall._read_managed_cleanup_config((managed, local)) == {
        "grok_home": "~/managed-grok",
        "host": None,
    }


def test_enterprise_legacy_cleanup_covers_all_historical_roots() -> None:
    expected = {
        Path("/Library/Application Support/Cursor"),
        Path("/Library/Application Support/ClaudeCode"),
        Path("/Library/Application Support/Windsurf"),
        Path("/Library/Application Support/GeminiCli"),
        Path("/private/etc/codex"),
        Path("/private/etc/github-copilot/policy.d"),
    }

    assert expected <= {
        root for root, _old_name in aiwatch_uninstall._ENTERPRISE_LEGACY_ROOTS
    }


def test_enterprise_cleanup_anchors_json_and_legacy_paths(
    tmp_path: Path, monkeypatch
) -> None:
    system_root = tmp_path / "system"
    enterprise_root = system_root / "Library/Application Support/Cursor"
    config = enterprise_root / "hooks.json"
    config.parent.mkdir(parents=True)
    config.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"command": "/usr/local/bin/aiwatch hook"},
                        {"command": "/opt/acme/hook"},
                    ]
                }
            }
        )
    )
    legacy = enterprise_root / "hooks" / "runlayer-hook.sh"
    legacy.parent.mkdir()
    legacy.write_text("#!/bin/sh\n")
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_JSON_HOOK_PATHS",
        ((Path("/Library/Application Support/Cursor/hooks.json"), True),),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_ROUTING_PATHS",
        (),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_LEGACY_ROOTS",
        ((Path("/Library/Application Support/Cursor"), None),),
    )

    aiwatch_uninstall._clean_enterprise_hooks(system_root=system_root)

    assert json.loads(config.read_text()) == {
        "hooks": {"PreToolUse": [{"command": "/opt/acme/hook"}]}
    }
    assert not legacy.exists()


def test_enterprise_cleanup_refuses_intermediate_symlink(
    tmp_path: Path, monkeypatch
) -> None:
    system_root = tmp_path / "system"
    application_support = system_root / "Library/Application Support"
    application_support.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside_hooks = outside / "hooks"
    outside_hooks.mkdir(parents=True)
    config = outside / "hooks.json"
    config.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"command": "/usr/local/bin/aiwatch hook"},
                    ]
                }
            }
        )
    )
    legacy = outside_hooks / "runlayer-hook.sh"
    legacy.write_text("#!/bin/sh\n")
    (application_support / "Cursor").symlink_to(
        outside,
        target_is_directory=True,
    )
    original_config = config.read_bytes()
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_JSON_HOOK_PATHS",
        ((Path("/Library/Application Support/Cursor/hooks.json"), True),),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_ROUTING_PATHS",
        (),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_LEGACY_ROOTS",
        ((Path("/Library/Application Support/Cursor"), None),),
    )

    aiwatch_uninstall._clean_enterprise_hooks(system_root=system_root)

    assert config.read_bytes() == original_config
    assert legacy.exists()


# --- LLM routing cleanup (mirrors hook_install.llm_routing.unroute for MDM) ---


_CLAUDE_ENV_KEYS = (
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_API_KEY_HELPER_TTL_MS",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)


def _claude_routing_config() -> dict:
    return {
        "permissions": {"allow": ["Read"]},
        "env": {
            "ANTHROPIC_BASE_URL": "https://gateway.example.com/anthropic",
            "CLAUDE_CODE_API_KEY_HELPER_TTL_MS": 240000,
            "ANTHROPIC_AUTH_TOKEN": "",
            "ANTHROPIC_API_KEY": "",
            "CLAUDE_CODE_OAUTH_TOKEN": "",
            "CLAUDE_CODE_USE_BEDROCK": "",
            "CLAUDE_CODE_USE_VERTEX": "",
            "CLAUDE_CODE_USE_FOUNDRY": "",
            "FOREIGN_ENV": "kept",
        },
        "apiKeyHelper": "/usr/local/bin/aiwatch credential claude",
    }


_CODEX_ROUTING_TOML = (
    'model_provider = "runlayer"\n\n'
    'approval_policy = "on-request"\n[features]\nhooks = true\nmodel = "gpt-5"\n\n'
    '[model_providers.runlayer]\nname = "Runlayer"\n'
    'base_url = "https://gateway.example.com/openai/v1"\nwire_api = "responses"\n\n'
    '[model_providers.runlayer.auth]\ncommand = "/usr/local/bin/aiwatch"\n'
    'args = ["credential", "codex"]\ntimeout_ms = 5000\nrefresh_interval_ms = 240000\n'
)


@pytest.mark.parametrize(
    "helper, expected",
    [
        ("/usr/local/bin/aiwatch credential claude", True),
        ('"C:\\Program Files\\Runlayer\\AIWatch\\aiwatch.exe" credential claude', True),
        ('"C:\\Program Files\\Runlayer\\AIWATCH.EXE" credential claude', True),
        ("python -m runlayer_cli.aiwatch credential claude", True),
        ("/opt/foreign/helper", False),
        ("/opt/acme/credential claude", False),
        ("", False),
        ("/usr/local/bin/aiwatch credential codex", False),
        ("/usr/local/bin/aiwatch hook --client claude_code", False),
    ],
)
def test_is_runlayer_helper_matches_credential_helper_forms(
    helper: str, expected: bool
) -> None:
    assert aiwatch_uninstall._is_runlayer_helper(helper) is expected


@pytest.mark.parametrize("non_string", [None, 123, [], {}])
def test_is_runlayer_helper_rejects_non_strings(non_string: object) -> None:
    assert aiwatch_uninstall._is_runlayer_helper(non_string) is False


def test_is_runlayer_helper_stays_aligned_with_hook_install() -> None:
    from runlayer_cli.hook_install import llm_routing

    samples = (
        "/usr/local/bin/aiwatch credential claude",
        '"C:\\Program Files\\Runlayer\\AIWatch\\AIWATCH.EXE" credential claude',
        "python -m runlayer_cli.aiwatch credential claude",
        "/opt/foreign/helper",
        "/opt/acme/credential claude",
        "",
        "/usr/local/bin/aiwatch credential codex",
    )
    for sample in samples:
        assert aiwatch_uninstall._is_runlayer_helper(
            sample
        ) == llm_routing._is_runlayer_helper(sample), sample


def test_clean_claude_routing_strips_helper_and_env_keys(tmp_path: Path) -> None:
    path = tmp_path / "managed-settings.json"
    path.write_text(json.dumps(_claude_routing_config(), indent=2) + "\n")

    assert aiwatch_uninstall.clean_claude_routing(path)
    after = json.loads(path.read_text())
    assert "apiKeyHelper" not in after
    for key in _CLAUDE_ENV_KEYS:
        assert key not in after["env"], key
    assert after["env"]["FOREIGN_ENV"] == "kept"
    assert after["permissions"] == {"allow": ["Read"]}


def test_clean_claude_routing_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "managed-settings.json"
    path.write_text(json.dumps(_claude_routing_config(), indent=2) + "\n")

    assert aiwatch_uninstall.clean_claude_routing(path)
    first = path.read_bytes()
    assert not aiwatch_uninstall.clean_claude_routing(path)
    assert path.read_bytes() == first


def test_clean_claude_routing_noop_when_no_routing(tmp_path: Path) -> None:
    path = tmp_path / "managed-settings.json"
    original = (
        json.dumps(
            {"permissions": {"allow": ["Read"]}, "env": {"FOREIGN_ENV": "kept"}},
            indent=2,
        )
        + "\n"
    )
    path.write_text(original)

    assert not aiwatch_uninstall.clean_claude_routing(path)
    assert path.read_text() == original


def test_clean_claude_routing_noop_when_file_missing(tmp_path: Path) -> None:
    assert not aiwatch_uninstall.clean_claude_routing(tmp_path / "missing.json")


def test_clean_claude_routing_noop_when_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "managed-settings.json"
    original = "{not valid json"
    path.write_text(original)

    assert not aiwatch_uninstall.clean_claude_routing(path)
    assert path.read_text() == original


def test_clean_claude_routing_strips_routing_without_hooks_key(tmp_path: Path) -> None:
    """MDM managed-settings.json under ENG-3204 has no ``hooks`` key — only routing."""
    config = {
        "env": {key: "" for key in _CLAUDE_ENV_KEYS},
        "apiKeyHelper": "/usr/local/bin/aiwatch credential claude",
    }
    path = tmp_path / "managed-settings.json"
    path.write_text(json.dumps(config, indent=2) + "\n")

    assert aiwatch_uninstall.clean_claude_routing(path)
    after = json.loads(path.read_text())
    assert "apiKeyHelper" not in after
    assert all(key not in after.get("env", {}) for key in _CLAUDE_ENV_KEYS)


@pytest.mark.parametrize(
    "foreign_helper", ["/opt/foreign/helper", "/opt/acme/credential claude"]
)
def test_clean_claude_routing_keeps_foreign_api_key_helper(
    tmp_path: Path, foreign_helper: str
) -> None:
    content = (
        json.dumps(
            {"apiKeyHelper": foreign_helper, "env": {"FOREIGN_ENV": "kept"}},
            indent=2,
        )
        + "\n"
    )
    path = tmp_path / "managed-settings.json"
    path.write_text(content)

    assert not aiwatch_uninstall.clean_claude_routing(path)
    assert path.read_text() == content


def test_clean_claude_routing_leaves_non_dict_env_untouched(tmp_path: Path) -> None:
    """A malformed ``env`` that is not an object is left alone (no crash, no strip)."""
    content = (
        json.dumps(
            {
                "apiKeyHelper": "/usr/local/bin/aiwatch credential claude",
                "env": "not-a-dict",
            },
            indent=2,
        )
        + "\n"
    )
    path = tmp_path / "managed-settings.json"
    path.write_text(content)

    # The Runlayer helper is still stripped, but the non-dict env is untouched.
    assert aiwatch_uninstall.clean_claude_routing(path)
    after = json.loads(path.read_text())
    assert "apiKeyHelper" not in after
    assert after["env"] == "not-a-dict"


def test_clean_codex_routing_strips_model_provider_and_tables(tmp_path: Path) -> None:
    path = tmp_path / "managed_config.toml"
    path.write_text(_CODEX_ROUTING_TOML)

    assert aiwatch_uninstall.clean_codex_routing(path)
    toml = path.read_text()
    assert 'model_provider = "runlayer"' not in toml
    assert "[model_providers.runlayer]" not in toml
    assert "[model_providers.runlayer.auth]" not in toml
    assert "[model_providers.runlayer" not in toml
    assert 'approval_policy = "on-request"' in toml
    assert "[features]\nhooks = true" in toml
    assert 'model = "gpt-5"' in toml


def test_clean_codex_routing_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "managed_config.toml"
    path.write_text(_CODEX_ROUTING_TOML)

    assert aiwatch_uninstall.clean_codex_routing(path)
    first = path.read_bytes()
    assert not aiwatch_uninstall.clean_codex_routing(path)
    assert path.read_bytes() == first


def test_clean_codex_routing_noop_when_no_routing(tmp_path: Path) -> None:
    content = 'model_provider = "openai"\nmodel = "gpt-5"\n'
    path = tmp_path / "managed_config.toml"
    path.write_text(content)

    assert not aiwatch_uninstall.clean_codex_routing(path)
    assert path.read_text() == content


def test_clean_codex_routing_noop_when_file_missing(tmp_path: Path) -> None:
    assert not aiwatch_uninstall.clean_codex_routing(tmp_path / "missing.toml")


def test_clean_codex_routing_preserves_foreign_provider_tables(
    tmp_path: Path,
) -> None:
    content = (
        'model_provider = "openai"\nmodel = "gpt-5"\n\n'
        '[model_providers.openai]\nname = "OpenAI"\n'
    )
    path = tmp_path / "managed_config.toml"
    path.write_text(content)

    assert not aiwatch_uninstall.clean_codex_routing(path)
    assert path.read_text() == content


def test_clean_codex_routing_preserves_trailing_newline(tmp_path: Path) -> None:
    path = tmp_path / "managed_config.toml"
    path.write_text(_CODEX_ROUTING_TOML)

    aiwatch_uninstall.clean_codex_routing(path)
    assert path.read_text().endswith("\n")


def test_without_runlayer_codex_config_stays_aligned_with_hook_install() -> None:
    from runlayer_cli.hook_install import llm_routing

    samples = (
        _CODEX_ROUTING_TOML,
        'model_provider = "openai"\nmodel = "gpt-5"\n',
        'approval_policy = "on-request"\n',
        "",
        'model_provider = "runlayer"\n',
        '[model_providers.runlayer]\nname = "Runlayer"\n[model_providers.runlayer.auth]\ncommand = "x"\n',
    )
    for sample in samples:
        assert aiwatch_uninstall._without_runlayer_codex_config(
            sample
        ) == llm_routing._without_runlayer_codex_config(sample), repr(sample)


def test_enterprise_routing_paths_cover_mdm_routing_targets() -> None:
    paths = {path for path, _ in aiwatch_uninstall._ENTERPRISE_ROUTING_PATHS}
    assert (
        Path("/Library/Application Support/ClaudeCode/managed-settings.json") in paths
    )
    assert Path("/private/etc/codex/managed_config.toml") in paths


def test_llm_routing_credential_path_stays_aligned_with_install_side() -> None:
    from runlayer_cli.aiwatch_credential import CREDENTIAL_RELATIVE_PATH

    assert (
        aiwatch_uninstall._LLM_ROUTING_CREDENTIAL_RELATIVE_PATH
        == CREDENTIAL_RELATIVE_PATH
    )


def test_enterprise_cleanup_strips_hooks_and_routing_from_managed_settings(
    tmp_path: Path, monkeypatch
) -> None:
    system_root = tmp_path / "system"
    managed = (
        system_root / "Library/Application Support/ClaudeCode/managed-settings.json"
    )
    managed.parent.mkdir(parents=True)
    managed.write_text(
        json.dumps(
            {
                "permissions": {"allow": ["Read"]},
                "env": {
                    "ANTHROPIC_BASE_URL": "https://gateway.example.com/anthropic",
                    "FOREIGN_ENV": "kept",
                },
                "hooks": {
                    "PreToolUse": [
                        {"command": "/usr/local/bin/aiwatch hook --client claude_code"}
                    ]
                },
                "apiKeyHelper": "/usr/local/bin/aiwatch credential claude",
            },
            indent=2,
        )
        + "\n"
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_JSON_HOOK_PATHS",
        (
            (
                Path("/Library/Application Support/ClaudeCode/managed-settings.json"),
                False,
            ),
        ),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_LEGACY_ROOTS",
        (),
    )

    aiwatch_uninstall._clean_enterprise_hooks(system_root=system_root)

    after = json.loads(managed.read_text())
    assert "apiKeyHelper" not in after
    assert "ANTHROPIC_BASE_URL" not in after["env"]
    assert after["env"]["FOREIGN_ENV"] == "kept"
    assert "hooks" not in after
    assert after["permissions"] == {"allow": ["Read"]}


def test_enterprise_cleanup_strips_codex_hooks_and_routing(
    tmp_path: Path, monkeypatch
) -> None:
    system_root = tmp_path / "system"
    codex_dir = system_root / "private/etc/codex"
    codex_dir.mkdir(parents=True)
    hooks_json = codex_dir / "hooks.json"
    managed_toml = codex_dir / "managed_config.toml"
    hooks_json.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"command": "/usr/local/bin/aiwatch hook --client codex"}
                    ]
                }
            }
        )
    )
    managed_toml.write_text(_CODEX_ROUTING_TOML)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_JSON_HOOK_PATHS",
        ((Path("/private/etc/codex/hooks.json"), True),),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_LEGACY_ROOTS",
        (),
    )

    aiwatch_uninstall._clean_enterprise_hooks(system_root=system_root)

    assert not hooks_json.exists()
    toml = managed_toml.read_text()
    assert 'model_provider = "runlayer"' not in toml
    assert "[model_providers.runlayer]" not in toml
    assert 'approval_policy = "on-request"' in toml
    assert 'model = "gpt-5"' in toml
    assert managed_toml.exists()


def test_enterprise_routing_cleanup_refuses_intermediate_symlink(
    tmp_path: Path, monkeypatch
) -> None:
    system_root = tmp_path / "system"
    application_support = system_root / "Library/Application Support"
    application_support.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    outside_config = outside / "managed-settings.json"
    original = json.dumps(_claude_routing_config(), indent=2) + "\n"
    outside_config.write_text(original)
    (application_support / "ClaudeCode").symlink_to(outside, target_is_directory=True)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_JSON_HOOK_PATHS",
        (),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_LEGACY_ROOTS",
        (),
    )

    aiwatch_uninstall._clean_enterprise_hooks(system_root=system_root)

    assert outside_config.read_text() == original


def test_clean_user_home_deletes_llm_routing_credential(tmp_path: Path) -> None:
    home = tmp_path / "alice"
    credential = home / ".runlayer" / "aiwatch" / "llm-routing-credential"
    credential.parent.mkdir(parents=True)
    credential.write_text("rlk_secret_device_key\n")

    assert aiwatch_uninstall.clean_user_home(home) > 0
    assert not credential.exists()
    assert aiwatch_uninstall.clean_user_home(home) == 0


def test_clean_user_home_credential_unlink_refuses_symlink(tmp_path: Path) -> None:
    home = tmp_path / "alice"
    target = tmp_path / "stolen-credential"
    target.write_text("attacker-token\n")
    cred_parent = home / ".runlayer" / "aiwatch"
    cred_parent.mkdir(parents=True)
    (cred_parent / "llm-routing-credential").symlink_to(target)

    aiwatch_uninstall.clean_user_home(home)

    assert target.read_text() == "attacker-token\n"


def test_main_runs_enterprise_routing_cleanup(monkeypatch) -> None:
    routing_cleaned: list[Path] = []

    def fake_clean_claude_routing(path: Path, *, _anchor: Path | None = None) -> bool:
        routing_cleaned.append(path)
        return False

    monkeypatch.setattr(
        aiwatch_uninstall,
        "_discover_local_homes_and_uids",
        lambda: {"homes": [], "uids": set()},
    )
    monkeypatch.setattr(aiwatch_uninstall, "_bootout_jobs", lambda _uids: None)
    monkeypatch.setattr(aiwatch_uninstall, "_kill_daemon_processes", lambda: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_ENTERPRISE_ROUTING_PATHS",
        (
            (
                Path("/Library/Application Support/ClaudeCode/managed-settings.json"),
                fake_clean_claude_routing,
            ),
        ),
    )
    monkeypatch.setattr(aiwatch_uninstall, "_ENTERPRISE_JSON_HOOK_PATHS", ())
    monkeypatch.setattr(aiwatch_uninstall, "_ENTERPRISE_LEGACY_ROOTS", ())
    monkeypatch.setattr(
        aiwatch_uninstall,
        "clean_browser_owned_artifacts",
        lambda _managed, _external, **_kwargs: 0,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_clean_browser_policies",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(aiwatch_uninstall, "_PACKAGE_PATHS", ())
    monkeypatch.setattr(aiwatch_uninstall, "_RECEIPT_IDS", ())
    monkeypatch.setattr(aiwatch_uninstall, "_run", lambda _command: None)

    assert aiwatch_uninstall.main() == 0
    assert routing_cleaned == [
        Path("/Library/Application Support/ClaudeCode/managed-settings.json")
    ]


def test_module_import_closure_is_stdlib_only() -> None:
    probe = textwrap.dedent(
        """
        import sys

        blocked = ("yaml", "re2", "runlayer_cli.hook_install")

        class Blocker:
            def find_spec(self, fullname, path=None, target=None):
                if any(
                    fullname == name or fullname.startswith(name + ".")
                    for name in blocked
                ):
                    raise ModuleNotFoundError(fullname)
                return None

        sys.meta_path.insert(0, Blocker())
        import runlayer_cli.aiwatch_uninstall
        leaked = [
            name
            for name in sys.modules
            if any(name == item or name.startswith(item + ".") for item in blocked)
        ]
        if leaked:
            raise SystemExit(",".join(sorted(leaked)))
        """
    )

    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=Path(__file__).parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_user_discovery_does_not_stat_home_entries_in_parent(monkeypatch) -> None:
    class NetworkHomeEntry:
        name = "network-user"
        path = "/Users/network-user"

        def stat(self, *, follow_symlinks: bool):
            raise AssertionError("parent must not stat a network home")

    monkeypatch.setattr(
        aiwatch_uninstall.os,
        "scandir",
        lambda _root: (NetworkHomeEntry(),),
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_run_capture",
        lambda _command, **_kwargs: "",
        raising=False,
    )

    discovered = aiwatch_uninstall._discover_local_homes_and_uids()

    assert Path("/Users/network-user") in discovered["homes"]
    assert Path("/private/var/root") in discovered["homes"]


def test_daemon_kill_matches_only_installed_binary_paths(monkeypatch) -> None:
    commands: list[tuple[str, ...]] = []
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_run",
        lambda command, **_kwargs: commands.append(command),
    )
    monkeypatch.setattr(aiwatch_uninstall.time, "sleep", lambda _seconds: None)

    aiwatch_uninstall._kill_daemon_processes()

    pattern = (
        r"^(/usr/local/bin/aiwatch|"
        r"/usr/local/lib/runlayer/aiwatch/aiwatch) daemon( |$)"
    )
    assert commands == [
        ("/usr/bin/pkill", "-TERM", "-f", pattern),
        ("/usr/bin/pkill", "-KILL", "-f", pattern),
    ]


def test_remove_package_artifacts_tracks_preference_change_without_failing_noop(
    tmp_path: Path,
    monkeypatch,
) -> None:
    preferences_dir = tmp_path / "Library" / "Preferences"
    preference = preferences_dir / "com.runlayer.aiwatch.plist"
    package_binary = tmp_path / "usr" / "local" / "bin" / "aiwatch"
    preference.parent.mkdir(parents=True)
    package_binary.parent.mkdir(parents=True)
    preference.write_text("preference")
    package_binary.write_text("binary")
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_SYSTEM_PREFERENCES_DIR",
        preferences_dir,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_PACKAGE_PATHS",
        (preference, package_binary),
    )

    assert aiwatch_uninstall._remove_package_artifacts() == {
        "ok": True,
        "preferences_changed": True,
    }
    assert aiwatch_uninstall._remove_package_artifacts() == {
        "ok": True,
        "preferences_changed": False,
    }


@pytest.mark.parametrize(
    ("result", "expected_ok"),
    [
        ({"ok": False, "preferences_changed": True}, False),
        ({"ok": False, "changed": False}, False),
        (None, True),
    ],
)
def test_attempt_phase_logs_structured_cleanup_result(
    monkeypatch,
    result: object,
    expected_ok: bool,
) -> None:
    phases: list[tuple[str, bool]] = []
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_log_phase",
        lambda name, ok: phases.append((name, ok)),
    )

    assert (
        aiwatch_uninstall._attempt_phase("package artifacts", lambda: result) == result
    )
    assert phases == [("package artifacts", expected_ok)]


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="macOS uninstaller log uses POSIX directory descriptors",
)
def test_log_phase_writes_stderr_and_protected_log(
    tmp_path: Path, monkeypatch, capfd
) -> None:
    log_root = tmp_path / "Logs"
    log_root.mkdir()
    log_path = log_root / "Runlayer" / "aiwatch-uninstall.log"
    monkeypatch.setattr(aiwatch_uninstall, "_UNINSTALL_LOG_ROOT", log_root)
    monkeypatch.setattr(aiwatch_uninstall, "_UNINSTALL_LOG_PATH", log_path)

    aiwatch_uninstall._log_phase("launchd jobs", False)

    expected = "[aiwatch-uninstall] launchd jobs: failed\n"
    assert capfd.readouterr().err == expected
    assert log_path.read_text() == expected


@pytest.mark.skipif(
    not hasattr(signal, "SIGALRM"),
    reason="home cleanup watchdog uses SIGALRM",
)
def test_home_child_timeout_exits_as_failure(monkeypatch) -> None:
    class ExitCalled(BaseException):
        def __init__(self, code: int) -> None:
            self.code = code

    handlers = []

    def fake_exit(code: int) -> None:
        raise ExitCalled(code)

    monkeypatch.setattr(aiwatch_uninstall.os, "fork", lambda: 0, raising=False)
    monkeypatch.setattr(aiwatch_uninstall.os, "_exit", fake_exit)
    monkeypatch.setattr(
        aiwatch_uninstall.signal,
        "signal",
        lambda signum, handler: handlers.append((signum, handler)),
    )
    monkeypatch.setattr(aiwatch_uninstall.signal, "alarm", lambda _seconds: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "clean_user_home",
        lambda _home, **_kwargs: 0,
    )

    with pytest.raises(ExitCalled) as normal_exit:
        aiwatch_uninstall._clean_home_in_child(Path("/Users/test"))

    assert normal_exit.value.code == 0
    assert len(handlers) == 1
    signum, handler = handlers[0]
    assert signum == signal.SIGALRM
    with pytest.raises(ExitCalled) as timeout_exit:
        handler(signal.SIGALRM, None)
    assert timeout_exit.value.code == 1


def test_home_child_receives_managed_grok_home(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[Path, str | None]] = []

    monkeypatch.setattr(aiwatch_uninstall.os, "fork", None, raising=False)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "clean_user_home",
        lambda home, *, grok_home=None: calls.append((home, grok_home)),
    )

    assert aiwatch_uninstall._clean_home_in_child(
        Path("/Users/alice"),
        "~/managed-grok",
    )
    assert calls == [(Path("/Users/alice"), "~/managed-grok")]


def test_main_logs_failed_phase_and_continues(monkeypatch) -> None:
    phases: list[tuple[str, bool]] = []
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_discover_local_homes_and_uids",
        lambda: {"homes": [], "uids": set()},
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_bootout_jobs",
        lambda _uids: (_ for _ in ()).throw(RuntimeError("launchctl failed")),
    )
    monkeypatch.setattr(aiwatch_uninstall, "_kill_daemon_processes", lambda: None)
    monkeypatch.setattr(aiwatch_uninstall, "_clean_enterprise_hooks", lambda: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "clean_browser_owned_artifacts",
        lambda _managed, _external, **_kwargs: 0,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_clean_browser_policies",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(aiwatch_uninstall, "_PACKAGE_PATHS", ())
    monkeypatch.setattr(aiwatch_uninstall, "_RECEIPT_IDS", ())
    monkeypatch.setattr(aiwatch_uninstall, "_run", lambda _command: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_log_phase",
        lambda name, ok: phases.append((name, ok)),
        raising=False,
    )

    assert aiwatch_uninstall.main() == 0
    assert ("launchd jobs", False) in phases
    assert ("daemon processes", True) in phases


def test_main_finishes_fixed_cost_teardown_before_home_cleanup(monkeypatch) -> None:
    phases: list[str] = []

    def attempt_phase(name: str, _operation) -> object:
        phases.append(name)
        if name == "user discovery":
            return {"homes": [Path("/Users/network-user")], "uids": set()}
        return None

    monkeypatch.setattr(aiwatch_uninstall, "_attempt_phase", attempt_phase)
    monkeypatch.setattr(aiwatch_uninstall.signal, "alarm", lambda _seconds: None)

    assert aiwatch_uninstall.main() == 0

    home_index = phases.index("user home /Users/network-user")
    fixed_cost_phases = {
        "managed config",
        "package artifacts",
        "TCC reset",
        "enterprise hooks",
        "browser artifacts",
        "browser policy",
        *(f"receipt {receipt_id}" for receipt_id in aiwatch_uninstall._RECEIPT_IDS),
    }
    assert all(phases.index(name) < home_index for name in fixed_cost_phases)
    assert phases.index("managed config") < phases.index("package artifacts")


def test_main_dispatches_root_home_to_bounded_child(monkeypatch) -> None:
    cleaned_homes: list[Path] = []
    monkeypatch.setattr(aiwatch_uninstall.os, "scandir", lambda _root: ())
    monkeypatch.setattr(aiwatch_uninstall, "_run_capture", lambda _command: "")
    monkeypatch.setattr(aiwatch_uninstall, "_bootout_jobs", lambda _uids: None)
    monkeypatch.setattr(aiwatch_uninstall, "_kill_daemon_processes", lambda: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_clean_home_in_child",
        lambda home, _grok_home=None: cleaned_homes.append(home),
    )
    monkeypatch.setattr(aiwatch_uninstall, "_clean_enterprise_hooks", lambda: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "clean_browser_owned_artifacts",
        lambda _managed, _external, **_kwargs: 0,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_clean_browser_policies",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_remove_package_path",
        lambda _path: {"ok": True, "changed": False},
    )
    monkeypatch.setattr(aiwatch_uninstall, "_run", lambda _command: None)

    assert aiwatch_uninstall.main() == 0
    assert cleaned_homes == [Path("/private/var/root")]


def test_main_removes_legacy_package_artifacts_and_receipt(monkeypatch) -> None:
    expected_paths = {
        Path("/usr/local/bin/aiwatch-hook"),
        Path("/usr/local/bin/aiwatch-enforce"),
        Path("/usr/local/lib/runlayer/aiwatch-enforce"),
    }
    assert expected_paths <= set(aiwatch_uninstall._PACKAGE_PATHS)

    commands: list[tuple[str, ...]] = []
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_discover_local_homes_and_uids",
        lambda: {"homes": [], "uids": set()},
    )
    monkeypatch.setattr(aiwatch_uninstall, "_bootout_jobs", lambda _uids: None)
    monkeypatch.setattr(aiwatch_uninstall, "_kill_daemon_processes", lambda: None)
    monkeypatch.setattr(aiwatch_uninstall, "_clean_enterprise_hooks", lambda: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "clean_browser_owned_artifacts",
        lambda _managed, _external, **_kwargs: 0,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_clean_browser_policies",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_remove_package_path",
        lambda _path: {"ok": True, "changed": False},
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_run",
        lambda command, **_kwargs: commands.append(command),
    )

    assert aiwatch_uninstall.main() == 0
    assert (
        "/usr/sbin/pkgutil",
        "--forget",
        "com.runlayer.aiwatch-enforce",
    ) in commands


@pytest.mark.parametrize(
    ("package_preferences_changed", "firefox_policy_changed", "should_refresh"),
    [
        (True, False, True),
        (False, True, True),
        (True, True, True),
        (False, False, False),
    ],
)
def test_main_refreshes_cfprefsd_only_after_system_preferences_change(
    monkeypatch,
    package_preferences_changed: bool,
    firefox_policy_changed: bool,
    should_refresh: bool,
) -> None:
    commands: list[tuple[str, ...]] = []
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_discover_local_homes_and_uids",
        lambda: {"homes": [], "uids": set()},
    )
    monkeypatch.setattr(aiwatch_uninstall, "_bootout_jobs", lambda _uids: None)
    monkeypatch.setattr(aiwatch_uninstall, "_kill_daemon_processes", lambda: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_remove_package_artifacts",
        lambda: {
            "ok": True,
            "preferences_changed": package_preferences_changed,
        },
    )
    monkeypatch.setattr(aiwatch_uninstall, "_clean_enterprise_hooks", lambda: None)
    monkeypatch.setattr(
        aiwatch_uninstall,
        "clean_browser_owned_artifacts",
        lambda _managed, _external, **_kwargs: 0,
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_clean_browser_policies",
        lambda **_kwargs: {
            "ok": True,
            "preferences_changed": firefox_policy_changed,
        },
    )
    monkeypatch.setattr(
        aiwatch_uninstall,
        "_run",
        lambda command, **_kwargs: commands.append(command) or True,
    )

    assert aiwatch_uninstall.main() == 0
    assert commands.count(("/usr/bin/killall", "cfprefsd")) == int(should_refresh)


def test_privileged_uninstaller_bans_unbounded_or_user_session_commands() -> None:
    module_path = Path(__file__).parents[1] / "runlayer_cli" / "aiwatch_uninstall.py"
    source = module_path.read_text()
    lowered = source.lower()
    assert "osascript" not in lowered
    assert "plutil" not in lowered
    assert "/usr/bin/defaults" not in lowered
    assert "pwd.getpwall" not in source

    tree = ast.parse(source)
    subprocess_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "subprocess"
        and node.func.attr in {"run", "check_call", "check_output", "Popen"}
    ]
    assert subprocess_calls
    for call in subprocess_calls:
        assert any(keyword.arg == "timeout" for keyword in call.keywords), (
            f"unbounded subprocess call at line {call.lineno}"
        )

    blocking_child_waits = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "os"
        and node.func.attr == "waitpid"
        and len(node.args) >= 2
        and isinstance(node.args[1], ast.Constant)
        and node.args[1].value == 0
    ]
    assert not blocking_child_waits, (
        "a killed network-home probe must never use blocking waitpid"
    )
