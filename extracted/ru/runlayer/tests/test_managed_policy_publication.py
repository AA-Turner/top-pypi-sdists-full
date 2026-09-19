"""Managed policy publication never runs native code in the installer process."""

from __future__ import annotations

import importlib
import io
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock

import pytest


ROOT = Path("/Library/Managed Preferences")
DOMAIN = "com.google.Chrome"
SENTINEL = "__publish_managed_policy__"


@pytest.fixture
def publisher(monkeypatch):
    module = importlib.import_module("runlayer_cli.managed_policy_publication")
    monkeypatch.setattr(module.sys, "platform", "darwin")
    monkeypatch.setattr(module.os, "geteuid", lambda: 0)
    return module


@pytest.mark.parametrize("frozen", [False, True])
def test_publication_uses_bounded_child_with_domain_only_payload(
    publisher, monkeypatch, frozen
):
    monkeypatch.setattr(sys, "frozen", frozen, raising=False)
    run = Mock(return_value=subprocess.CompletedProcess([], 0))
    monkeypatch.setattr(publisher.subprocess, "run", run)
    paths = [ROOT / f"{DOMAIN}.plist", ROOT / f"{DOMAIN}.plist"]

    publisher.publish_managed_policy(paths)

    args, kwargs = run.call_args
    expected = (
        [sys.executable, SENTINEL]
        if frozen
        else [sys.executable, "-m", "runlayer_cli.managed_policy_publication"]
    )
    assert args == (expected,)
    assert json.loads(kwargs["input"]) == [DOMAIN]
    assert kwargs["stdout"] is subprocess.DEVNULL
    assert kwargs["stderr"] is subprocess.DEVNULL
    assert kwargs["timeout"] == 5
    assert kwargs["check"] is True


@pytest.mark.parametrize(
    "failure",
    [
        OSError("sensitive detail"),
        subprocess.TimeoutExpired("secret argument", 5),
        subprocess.CalledProcessError(-11, "secret argument"),
    ],
)
def test_child_failure_is_sanitized_and_retryable(publisher, monkeypatch, failure):
    run = Mock(side_effect=[failure, subprocess.CompletedProcess([], 0)])
    monkeypatch.setattr(publisher.subprocess, "run", run)

    with pytest.raises(
        OSError, match="managed browser policy publication failed"
    ) as exc:
        publisher.publish_managed_policy([ROOT / f"{DOMAIN}.plist"])
    assert "secret" not in str(exc.value)
    assert "sensitive" not in str(exc.value)
    publisher.publish_managed_policy([ROOT / f"{DOMAIN}.plist"])
    assert run.call_count == 2


def test_temporary_policy_paths_never_publish_to_host(publisher, monkeypatch, tmp_path):
    run = Mock()
    monkeypatch.setattr(publisher.subprocess, "run", run)
    publisher.publish_managed_policy([tmp_path / f"{DOMAIN}.plist"])
    run.assert_not_called()


def test_non_macos_parent_does_not_spawn(publisher, monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    run = Mock()
    monkeypatch.setattr(publisher.subprocess, "run", run)
    publisher.publish_managed_policy([ROOT / f"{DOMAIN}.plist"])
    run.assert_not_called()


@pytest.mark.parametrize(
    "payload",
    [
        b"null",
        b"[]",
        b"{}",
        b'["../invalid"]',
        b'["a\\n.b"]',
        b'["com..example"]',
        b'[".com.example"]',
        b'["com.example."]',
        b'["single_label"]',
        b'["com.\\u212a"]',
        b'["com.ex\\u00e4mple"]',
        json.dumps(["a." + "b" * 254]).encode(),
        b"x" * 4097,
    ],
)
def test_child_rejects_invalid_payload_without_loading_native_api(
    publisher, monkeypatch, payload
):
    native = Mock()
    monkeypatch.setattr(publisher, "_publish_native", native)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(payload)))
    assert publisher.main() == 2
    native.assert_not_called()


@pytest.mark.parametrize("domain", ["com.Example_label-123", "a." + "b" * 253])
def test_child_accepts_valid_ascii_labels(publisher, monkeypatch, domain):
    native = Mock()
    monkeypatch.setattr(publisher, "_publish_native", native)
    monkeypatch.setattr(
        sys, "stdin", io.TextIOWrapper(io.BytesIO(json.dumps([domain]).encode()))
    )
    assert publisher.main() == 0
    native.assert_called_once_with([domain])


def test_child_rejects_non_root(publisher, monkeypatch):
    monkeypatch.setattr(publisher.os, "geteuid", lambda: 501)
    native = Mock()
    monkeypatch.setattr(publisher, "_publish_native", native)
    assert publisher.main() == 2
    native.assert_not_called()


def test_missing_native_symbol_fails_silently(publisher, monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "stdin", io.TextIOWrapper(io.BytesIO(json.dumps([DOMAIN]).encode()))
    )
    monkeypatch.setattr(
        publisher, "_publish_native", Mock(side_effect=AttributeError("secret detail"))
    )
    assert publisher.main() == 2
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize("entrypoint", ["aiwatch", "main", "aiwatch_uninstall"])
def test_packaged_entrypoints_dispatch_publication_before_normal_work(
    publisher, monkeypatch, entrypoint
):
    module = importlib.import_module(f"runlayer_cli.{entrypoint}")
    child = Mock(return_value=2)
    monkeypatch.setattr(publisher, "main", child)
    monkeypatch.setattr(sys, "argv", ["frozen-executable", SENTINEL])
    if entrypoint == "aiwatch_uninstall":
        monkeypatch.setattr(
            module, "_discover_local_homes_and_uids", Mock(side_effect=AssertionError)
        )
        assert module.main() == 2
    else:
        with pytest.raises(SystemExit) as exc:
            (module.cli if entrypoint == "main" else module.main)()
        assert exc.value.code == 2
    child.assert_called_once_with()


@pytest.mark.parametrize("browser_name", ["browser_extension", "edge_extension"])
def test_reconciliation_publishes_unchanged_install_and_withdrawal(
    monkeypatch, tmp_path, browser_name
):
    browser = importlib.import_module(f"runlayer_cli.hook_install.{browser_name}")
    monkeypatch.setattr(browser.platform, "system", lambda: "Darwin")
    publish = Mock()
    monkeypatch.setattr(
        "runlayer_cli.managed_policy_publication.publish_managed_policy", publish
    )
    extension_id = "jijfcalfdbnjfpfcalkodmgmfijpfddi"
    managed = {
        "browser_extension_id": extension_id,
        "browser_extension_enabled": True,
        "browser_extension_update_url": browser.RUNLAYER_CHROME_UPDATE_URL,
        "host": "https://tenant.example",
        "org_api_key": "rl_org_test",
    }
    kwargs = {"managed_prefs_dir": tmp_path}
    if browser_name == "browser_extension":
        install = browser.install_browser_extension
        kwargs["external_dir"] = tmp_path / "external"
        domain = "com.google.Chrome"
    else:
        install = browser.install_edge_extension
        domain = "com.microsoft.Edge"
    for config in (managed, managed, {}, {}):
        install(config, **kwargs)
    assert publish.call_count == 4
    for call in publish.call_args_list:
        paths = set(call.args[0])
        assert tmp_path / f"{domain}.plist" in paths
        assert tmp_path / f"{domain}.extensions.{extension_id}.plist" in paths


def test_uninstaller_publishes_repeated_withdrawal(monkeypatch, tmp_path):
    from runlayer_cli import aiwatch_uninstall as uninstall

    publish = Mock()
    monkeypatch.setattr(uninstall, "publish_managed_policy", publish, raising=False)
    uninstall._clean_browser_policies(system_root=tmp_path)
    uninstall._clean_browser_policies(system_root=tmp_path)
    assert publish.call_count == 2
    for call in publish.call_args_list:
        paths = set(call.args[0])
        for domain in ("com.google.Chrome", "com.microsoft.Edge"):
            assert tmp_path / f"Library/Managed Preferences/{domain}.plist" in paths


@pytest.mark.parametrize("browser_name", ["browser_extension", "edge_extension"])
def test_partial_install_publishes_committed_policy_and_preserves_original_error(
    monkeypatch, tmp_path, browser_name
):
    browser = importlib.import_module(f"runlayer_cli.hook_install.{browser_name}")
    monkeypatch.setattr(browser.platform, "system", lambda: "Darwin")
    original_error = OSError("artifact write failed")
    publish = Mock(side_effect=OSError("publication failed"))
    monkeypatch.setattr(
        "runlayer_cli.managed_policy_publication.publish_managed_policy", publish
    )
    managed = {
        "browser_extension_id": "jijfcalfdbnjfpfcalkodmgmfijpfddi",
        "browser_extension_enabled": True,
        "browser_extension_update_url": browser.RUNLAYER_CHROME_UPDATE_URL,
        "host": "https://tenant.example",
        "org_api_key": "rl_org_test",
    }
    kwargs = {"managed_prefs_dir": tmp_path}
    if browser_name == "browser_extension":
        install = browser.install_browser_extension
        kwargs["external_dir"] = tmp_path / "external"
        writer_name = "write_if_changed"
        failing_name = managed["browser_extension_id"] + ".json"
    else:
        install = browser.install_edge_extension
        writer_name = "_write_policy"
        failing_name = browser.EDGE_POLICY_NAME
    writer = getattr(browser, writer_name)

    def partial_write(path, content):
        if path.name == failing_name:
            raise original_error
        return writer(path, content)

    monkeypatch.setattr(browser, writer_name, partial_write)
    for _ in range(2):
        with pytest.raises(OSError) as exc:
            install(managed, **kwargs)
        assert exc.value is original_error
    assert any(tmp_path.glob("*.extensions.*.plist"))
    assert publish.call_count == 2


def test_uninstaller_reports_publication_failure(monkeypatch, tmp_path):
    from runlayer_cli import aiwatch_uninstall as uninstall

    monkeypatch.setattr(
        uninstall, "publish_managed_policy", Mock(side_effect=OSError("failed"))
    )
    result = uninstall._clean_browser_policies(system_root=tmp_path)
    assert result["ok"] is False


@pytest.mark.parametrize("browser_name", ["browser_extension", "edge_extension"])
def test_partial_withdrawal_publishes_removed_force_policy(
    monkeypatch, tmp_path, browser_name
):
    browser = importlib.import_module(f"runlayer_cli.hook_install.{browser_name}")
    monkeypatch.setattr(browser.platform, "system", lambda: "Darwin")
    publish = Mock()
    monkeypatch.setattr(
        "runlayer_cli.managed_policy_publication.publish_managed_policy", publish
    )
    extension_id = "jijfcalfdbnjfpfcalkodmgmfijpfddi"
    managed = {
        "browser_extension_id": extension_id,
        "browser_extension_enabled": True,
        "browser_extension_update_url": browser.RUNLAYER_CHROME_UPDATE_URL,
        "host": "https://tenant.example",
        "org_api_key": "rl_org_test",
    }
    kwargs = {"managed_prefs_dir": tmp_path}
    if browser_name == "browser_extension":
        install = browser.install_browser_extension
        kwargs["external_dir"] = tmp_path / "external"
        failing_path = kwargs["external_dir"] / f"{extension_id}.json"
    else:
        install = browser.install_edge_extension
        failing_path = tmp_path / browser.EDGE_TENANT_POLICY_NAME
    install(managed, **kwargs)
    publish.reset_mock()
    unlink = Path.unlink
    original_error = OSError("artifact removal failed")

    def partial_unlink(path, *args, **kwargs):
        if path == failing_path:
            raise original_error
        return unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", partial_unlink)
    with pytest.raises(OSError) as exc:
        install({}, **kwargs)
    assert exc.value is original_error
    assert failing_path.exists()
    publish.assert_called_once()


@pytest.mark.parametrize("corrupt_shared_policy", [False, True])
def test_main_uninstall_publishes_after_orphan_artifact_removal(
    monkeypatch, tmp_path, corrupt_shared_policy
):
    from runlayer_cli import aiwatch_uninstall as uninstall

    directory = tmp_path / "Library/Managed Preferences"
    directory.mkdir(parents=True)
    tenant = directory / (
        "com.google.Chrome.extensions."
        + uninstall._RUNLAYER_CHROME_EXTENSION_ID
        + ".plist"
    )
    tenant.write_bytes(b"synthetic orphan")
    if corrupt_shared_policy:
        (directory / "com.google.Chrome.plist").write_bytes(b"invalid plist")
    artifacts = uninstall.clean_browser_owned_artifacts
    policies = uninstall._clean_browser_policies
    monkeypatch.setattr(
        uninstall,
        "clean_browser_owned_artifacts",
        lambda *_args, **kwargs: artifacts(directory, tmp_path / "external", **kwargs),
    )
    monkeypatch.setattr(
        uninstall,
        "_clean_browser_policies",
        lambda **kwargs: policies(tmp_path, **kwargs),
    )
    monkeypatch.setattr(
        uninstall,
        "_attempt_phase",
        lambda name, operation: (
            operation() if name in {"browser artifacts", "browser policy"} else None
        ),
    )
    monkeypatch.setattr(uninstall.signal, "alarm", lambda *_args: None)
    monkeypatch.setattr(uninstall.signal, "signal", lambda *_args: None)
    published = []

    def publish(paths):
        assert not tenant.exists()
        published.append(paths)

    monkeypatch.setattr(uninstall, "publish_managed_policy", publish)
    assert uninstall.main() == 0
    assert len(published) == 1
    assert tenant in published[0]
