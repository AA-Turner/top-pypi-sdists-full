"""Exercise editable-install diagnostics through the real setup-check output paths."""

import json
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.setup import commands, dependency_checker, doctor
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.fixloop import ErrorClass


@pytest.fixture
def setup_check_context(tmp_path, monkeypatch, flags, required_problem, metadata_kind):
    """Isolate unrelated checks while retaining the real editable check, doctor, and renderer."""
    root = tmp_path / "current worktree"
    root.mkdir()
    (root / "pyproject.toml").touch()
    child = root / "nested"
    child.mkdir()
    monkeypatch.chdir(child)
    monkeypatch.setattr(sys, "argv", ["agdt-setup-check", *flags])
    home = tmp_path / "home"
    bundle = home / ".agdt/certs/unified-ca-bundle.pem"
    bundle.parent.mkdir(parents=True)
    bundle.write_text("-----BEGIN CERTIFICATE-----\nfake\n-----END CERTIFICATE-----\n")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr("agentic_devtools.state._get_git_repo_root", lambda: root)

    source = root if metadata_kind == "healthy" else tmp_path / "deleted worktree"
    raw = json.dumps({"dir_info": {"editable": metadata_kind != "noneditable"}, "url": source.as_uri()})
    if metadata_kind == "absent":
        raw = None
    elif metadata_kind == "malformed":
        raw = "{"
    dist = Mock(spec=["read_text"])
    dist.read_text.return_value = raw
    monkeypatch.setattr(dependency_checker, "distribution", Mock(return_value=dist))

    def check_tool(name, **kwargs):
        return DependencyStatus(name=name, found=name != "git" or required_problem == "none", **kwargs)

    monkeypatch.setattr(dependency_checker, "_check_dependency", check_tool)
    for name in ("_check_path_profile", "_check_git_hooks_config"):
        monkeypatch.setattr(dependency_checker, name, lambda: DependencyStatus(name="configuration", found=True))
    provider = Mock(valid=True, found=True, path=root / "provider.yml")
    provider.report_details.return_value = {}
    monkeypatch.setattr(
        "agentic_devtools.cli.setup.provider_configuration.check_provider_configuration", lambda _: provider
    )
    monkeypatch.setattr(
        commands,
        "check_corrupted_artifacts_status",
        lambda: (DependencyStatus(name="corrupted-artifacts", found=True), []),
    )
    registry = doctor.RepairRegistry()
    repaired_names = []

    def repair(dep):
        repaired_names.append(dep.name)
        dep.found = required_problem == "repaired"
        return dep.found

    registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: repair)
    monkeypatch.setattr(doctor, "get_default_registry", lambda: registry)
    monkeypatch.setattr("agentic_devtools.cli.setup.repairs.registration.register_default_repairs", lambda: None)
    monkeypatch.setattr(commands, "register_stale_install_repair", lambda _: None)
    return root, repaired_names


@pytest.mark.parametrize("flags", [[], ["--json"], ["--fix"], ["--fix", "--json"]])
@pytest.mark.parametrize("required_problem", ["none", "unresolved", "repaired"])
@pytest.mark.parametrize("metadata_kind", ["stale", "healthy", "absent", "noneditable", "malformed"])
def test_editable_install_output_and_report_only(
    tmp_path, capsys, flags, required_problem, metadata_kind, setup_check_context
):
    """Warnings survive every report path without becoming repairs or affecting exit codes."""
    root, repaired_names = setup_check_context
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    with patch.dict(os.environ):
        environment = dict(os.environ)
        if flags or required_problem != "none":
            with pytest.raises(SystemExit) as exit_info:
                commands.setup_check_cmd()
            exit_code = exit_info.value.code
        else:
            commands.setup_check_cmd()
            exit_code = 0
        assert dict(os.environ) == environment
    expected_exit = 0 if required_problem == "none" or (required_problem == "repaired" and "--fix" in flags) else 2
    assert exit_code == expected_exit
    assert repaired_names == (["git"] if "--fix" in flags and required_problem != "none" else [])
    after = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert after == before
    assert not (tmp_path / "deleted worktree").exists()
    output = capsys.readouterr().out
    stale = metadata_kind in ("stale", "malformed")
    if "--json" in flags:
        report = json.loads(output)
        status = next(s for s in report["details"]["dependencies"] if s["name"] == "editable-install")
        assert status["found"] is not stale
        assert status["required"] is False
        assert status["category"] == "Warning"
        assert status["install_hint"].startswith("pip install -e ")
        assert str(root) in status["install_hint"]
        assert report["exit_code"] == expected_exit
        git_status = next(s for s in report["details"]["dependencies"] if s["name"] == "git")
        assert git_status["found"] is (required_problem == "none")
        assert not any(p["name"] == "repair:editable-install" for p in report["phases"])
    else:
        assert "editable-install" in output
        assert "(Warning)" in output
        if stale:
            assert "Install: pip install -e " in output
            assert str(root) in output
