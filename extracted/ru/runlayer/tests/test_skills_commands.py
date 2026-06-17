"""Tests for skills command argument validation."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import typer
from typer.testing import CliRunner

from runlayer_cli.api import SkillDetail, SkillScanResponse
from runlayer_cli.main import app
from runlayer_cli.skills.installer import InstallResult, LockEntry
from runlayer_cli.skills.sync_engine import SyncResult

runner = CliRunner()


def _entry(name: str) -> LockEntry:
    return LockEntry(name=name, id=f"id-{name}", client="claude_code")


def _resolve_dirs(tmp_path: Path) -> tuple[Path, Path, Path]:
    return (
        tmp_path / "canonical",
        tmp_path / "editor",
        tmp_path / "lock.yml",
    )


def test_add_all_works_without_source(tmp_path: Path):
    install_mock = AsyncMock(return_value=InstallResult(installed=["a"]))
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient"),
        patch(
            "runlayer_cli.commands.skills.install_skills",
            new=install_mock,
        ),
    ):
        result = runner.invoke(
            app,
            ["skills", "add", "--all"],
        )

    assert result.exit_code == 0
    install_mock.assert_awaited_once()
    kwargs = install_mock.await_args_list[0].kwargs
    assert kwargs["install_all"] is True
    assert kwargs["source"] is None


@pytest.mark.parametrize("client_name", ["vscode", "goose"])
def test_add_accepts_supported_native_skill_client(tmp_path: Path, client_name: str):
    install_mock = AsyncMock(return_value=InstallResult(installed=["a"]))
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ) as resolve_dirs_mock,
        patch("runlayer_cli.commands.skills.RunlayerClient"),
        patch(
            "runlayer_cli.commands.skills.install_skills",
            new=install_mock,
        ),
    ):
        result = runner.invoke(
            app,
            ["skills", "add", "org/repo", "--client", client_name],
        )

    assert result.exit_code == 0
    assert resolve_dirs_mock.call_args is not None
    assert resolve_dirs_mock.call_args.args[0] == client_name
    kwargs = install_mock.await_args_list[0].kwargs
    assert kwargs["client_name"] == client_name


def test_skills_find_installs_selected_skills_for_multiple_clients(
    tmp_path: Path,
) -> None:
    install_mock = AsyncMock(return_value=InstallResult(installed=["review"]))
    selected_skill = SkillDetail(
        id="skill-1",
        name="review",
        namespace="Org/Repo",
        description="Review things",
    )
    selected_skill_two = SkillDetail(
        id="skill-2",
        name="deploy",
        namespace="Org/Repo",
        description="Deploy things",
    )

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ) as resolve_dirs_mock,
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
        patch(
            "runlayer_cli.commands.skills.install_skills",
            new=install_mock,
        ),
        patch(
            "runlayer_cli.commands.skills.prompt_items",
            return_value=[selected_skill, selected_skill_two],
        ),
        patch(
            "runlayer_cli.commands.skills.prompt_clients",
            return_value=["cursor", "vscode"],
        ),
        patch(
            "runlayer_cli.commands.skills.prompt_scope",
            return_value="global",
        ),
        patch("runlayer_cli.commands.skills.confirm_install"),
        patch("runlayer_cli.commands.skills.console.status") as status_mock,
    ):
        client_class.return_value.list_skills.return_value = [
            selected_skill,
            selected_skill_two,
        ]
        result = runner.invoke(app, ["skills", "find"])

    assert result.exit_code == 0
    status_mock.assert_called_once_with("Loading skills...")
    client_class.return_value.list_skills.assert_called_once_with(filter="all")
    assert resolve_dirs_mock.call_count == 2
    assert resolve_dirs_mock.call_args_list[0].args[0] == "cursor"
    assert resolve_dirs_mock.call_args_list[1].args[0] == "vscode"
    assert all(call.args[1] is True for call in resolve_dirs_mock.call_args_list)
    assert install_mock.await_count == 4
    calls = install_mock.await_args_list
    assert calls[0].kwargs["source"] == "skill-1"
    assert calls[1].kwargs["source"] == "skill-2"
    assert calls[2].kwargs["source"] == "skill-1"
    assert calls[3].kwargs["source"] == "skill-2"
    assert calls[0].kwargs["client_name"] == "cursor"
    assert calls[2].kwargs["client_name"] == "vscode"
    assert all(call.kwargs["install_scope"] == "global" for call in calls)


def test_skills_find_handles_empty_catalog(tmp_path: Path) -> None:
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        client_class.return_value.list_skills.return_value = []
        result = runner.invoke(app, ["skills", "find"])

    assert result.exit_code == 0
    assert "No skills available." in result.output


def test_skills_find_cancelled_before_install(tmp_path: Path) -> None:
    install_mock = AsyncMock(return_value=InstallResult(installed=["review"]))
    selected_skill = SkillDetail(
        id="skill-1",
        name="review",
        namespace="Org/Repo",
        description="Review things",
    )

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
        patch(
            "runlayer_cli.commands.skills.install_skills",
            new=install_mock,
        ),
        patch(
            "runlayer_cli.commands.skills.prompt_items",
            return_value=[selected_skill],
        ),
        patch(
            "runlayer_cli.commands.skills.prompt_clients",
            return_value=["claude_code"],
        ),
        patch(
            "runlayer_cli.commands.skills.prompt_scope",
            return_value="project",
        ),
        patch(
            "runlayer_cli.commands.skills.confirm_install",
            side_effect=typer.Exit(0),
        ),
    ):
        client_class.return_value.list_skills.return_value = [selected_skill]
        result = runner.invoke(app, ["skills", "find"])

    assert result.exit_code == 0
    install_mock.assert_not_awaited()


def test_skills_push_dry_run_requires_auth_up_front(tmp_path: Path) -> None:
    sync_mock = AsyncMock(return_value=SyncResult())
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.skills.resolve_credentials") as resolve_mock,
        patch("runlayer_cli.commands.skills.RunlayerClient"),
        patch("runlayer_cli.commands.skills.sync_skills", new=sync_mock),
    ):
        resolve_mock.return_value = {"host": "https://example.com", "secret": "rl_test"}
        result = runner.invoke(
            app,
            ["skills", "push", str(tmp_path), "--namespace", "myorg/repo", "--dry-run"],
        )

    assert result.exit_code == 0
    assert resolve_mock.call_args.kwargs["require_auth"] is True


def test_skills_push_public_passed_to_sync(tmp_path: Path) -> None:
    sync_mock = AsyncMock(return_value=SyncResult())
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient"),
        patch("runlayer_cli.commands.skills.sync_skills", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            [
                "skills",
                "push",
                str(tmp_path),
                "--namespace",
                "myorg/repo",
                "--public",
            ],
        )

    assert result.exit_code == 0
    assert sync_mock.await_args.kwargs["is_public"] is True


def test_skills_push_without_public_preserves_remote_visibility(tmp_path: Path) -> None:
    sync_mock = AsyncMock(return_value=SyncResult())
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient"),
        patch("runlayer_cli.commands.skills.sync_skills", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["skills", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    assert sync_mock.await_args.kwargs["is_public"] is None


def test_skills_scan_prints_json_and_allows_org_keys(tmp_path: Path) -> None:
    skill_dir = tmp_path / "review-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: review-skill\n---\n# skill\n")
    (skill_dir / "helper.py").write_text("print('ok')\n")

    response = SkillScanResponse.model_validate(
        {
            "skill_score": 0.12,
            "skill_risk_level": "Minimal",
            "classification": "UNKNOWN_SKILL",
            "files": [
                {
                    "name": "SKILL.md",
                    "score": 0.12,
                    "risk_level": "Minimal",
                    "reasons": ["Tool passed security scan"],
                }
            ],
        }
    )

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.skills.resolve_credentials") as resolve_mock,
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        resolve_mock.return_value = {
            "host": "https://example.com",
            "secret": "rl_org_x",
        }
        client_class.return_value.score_skill.return_value = response

        result = runner.invoke(app, ["skills", "scan", str(skill_dir)])

    assert result.exit_code == 0
    assert resolve_mock.call_args.kwargs["allow_org_key"] is True
    client_class.assert_called_once_with(
        hostname="https://example.com",
        secret="rl_org_x",
    )
    client_class.return_value.score_skill.assert_called_once()
    score_call = client_class.return_value.score_skill.call_args.kwargs
    assert score_call["skill_name"] == "review-skill"
    assert score_call["files"] == [
        {"name": "SKILL.md", "content": "---\nname: review-skill\n---\n# skill\n"},
        {"name": "helper.py", "content": "print('ok')\n"},
    ]
    assert json.loads(result.output)["skill_risk_level"] == "Minimal"


def test_skills_scan_supports_name_override(tmp_path: Path) -> None:
    skill_dir = tmp_path / "review-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: review-skill\n---\n# skill\n")

    response = SkillScanResponse.model_validate(
        {
            "skill_score": 0.2,
            "skill_risk_level": "Low",
            "classification": "UNKNOWN_SKILL",
            "files": [],
        }
    )

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_org_x"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        client_class.return_value.score_skill.return_value = response

        result = runner.invoke(
            app,
            [
                "skills",
                "scan",
                str(skill_dir),
                "--name",
                "override-name",
            ],
        )

    assert result.exit_code == 0
    assert client_class.return_value.score_skill.call_args.kwargs["skill_name"] == (
        "override-name"
    )


def test_skills_scan_fail_on_warn_returns_exit_code_2(tmp_path: Path) -> None:
    skill_dir = tmp_path / "review-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: review-skill\n---\n# skill\n")

    response = SkillScanResponse.model_validate(
        {
            "skill_score": 0.7,
            "skill_risk_level": "Medium",
            "classification": "UNKNOWN_SKILL",
            "files": [],
        }
    )

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_org_x"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        client_class.return_value.score_skill.return_value = response

        result = runner.invoke(
            app,
            ["skills", "scan", str(skill_dir), "--fail-on", "warn"],
        )

    assert result.exit_code == 2
    assert json.loads(result.output)["skill_risk_level"] == "Medium"


def test_skills_scan_unknown_risk_level_fails_closed(tmp_path: Path) -> None:
    skill_dir = tmp_path / "review-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: review-skill\n---\n# skill\n")

    response = SkillScanResponse.model_validate(
        {
            "skill_score": 0.95,
            "skill_risk_level": "Critical",
            "classification": "UNKNOWN_SKILL",
            "files": [],
        }
    )

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_org_x"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        client_class.return_value.score_skill.return_value = response

        result = runner.invoke(
            app,
            ["skills", "scan", str(skill_dir), "--fail-on", "block"],
        )

    assert result.exit_code == 3
    assert json.loads(result.output)["skill_risk_level"] == "Critical"


def test_skills_scan_rejects_name_override_for_multiple_skills(tmp_path: Path) -> None:
    skill_a = tmp_path / "a"
    skill_b = tmp_path / "b"
    skill_a.mkdir()
    skill_b.mkdir()
    (skill_a / "SKILL.md").write_text("---\nname: a\n---\n")
    (skill_b / "SKILL.md").write_text("---\nname: b\n---\n")

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_org_x"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        result = runner.invoke(
            app,
            ["skills", "scan", str(tmp_path), "--name", "override-name"],
        )

    assert result.exit_code == 1
    assert "--name requires a single skill path" in result.output
    client_class.return_value.score_skill.assert_not_called()


def test_skills_scan_scans_multiple_skills_under_grouped_plugin_folders(
    tmp_path: Path,
) -> None:
    review_skill = tmp_path / "plugin-a" / "skills" / "review"
    triage_skill = tmp_path / "plugin-b" / "skills" / "triage"
    review_skill.mkdir(parents=True)
    triage_skill.mkdir(parents=True)
    (review_skill / "SKILL.md").write_text("---\nname: review\n---\n# review\n")
    (triage_skill / "SKILL.md").write_text("---\nname: triage\n---\n# triage\n")

    review_response = SkillScanResponse.model_validate(
        {
            "skill_score": 0.12,
            "skill_risk_level": "Minimal",
            "classification": "UNKNOWN_SKILL",
            "files": [
                {
                    "name": "SKILL.md",
                    "score": 0.12,
                    "risk_level": "Minimal",
                    "reasons": ["Tool passed security scan"],
                }
            ],
        }
    )
    triage_response = SkillScanResponse.model_validate(
        {
            "skill_score": 0.77,
            "skill_risk_level": "High",
            "classification": "AUTOMATION",
            "files": [
                {
                    "name": "SKILL.md",
                    "score": 0.77,
                    "risk_level": "High",
                    "reasons": ["Needs review"],
                }
            ],
        }
    )

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_org_x"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        client_class.return_value.score_skill.side_effect = [
            review_response,
            triage_response,
        ]

        result = runner.invoke(app, ["skills", "scan", str(tmp_path)])

    assert result.exit_code == 0
    assert client_class.return_value.score_skill.call_count == 2
    assert [
        call.kwargs["skill_name"]
        for call in client_class.return_value.score_skill.call_args_list
    ] == ["review", "triage"]

    payload = json.loads(result.output)
    assert payload == {
        "skills": [
            {
                "path": "plugin-a/skills/review",
                "name": "review",
                "skill_score": 0.12,
                "skill_risk_level": "Minimal",
                "classification": "UNKNOWN_SKILL",
                "files": [
                    {
                        "name": "SKILL.md",
                        "score": 0.12,
                        "risk_level": "Minimal",
                        "reasons": ["Tool passed security scan"],
                    }
                ],
            },
            {
                "path": "plugin-b/skills/triage",
                "name": "triage",
                "skill_score": 0.77,
                "skill_risk_level": "High",
                "classification": "AUTOMATION",
                "files": [
                    {
                        "name": "SKILL.md",
                        "score": 0.77,
                        "risk_level": "High",
                        "reasons": ["Needs review"],
                    }
                ],
            },
        ]
    }


def test_skills_scan_multiple_skills_honors_fail_on_warn(tmp_path: Path) -> None:
    skill_a = tmp_path / "a"
    skill_b = tmp_path / "b"
    skill_a.mkdir()
    skill_b.mkdir()
    (skill_a / "SKILL.md").write_text("---\nname: a\n---\n")
    (skill_b / "SKILL.md").write_text("---\nname: b\n---\n")

    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_org_x"},
        ),
        patch("runlayer_cli.commands.skills.RunlayerClient") as client_class,
    ):
        client_class.return_value.score_skill.side_effect = [
            SkillScanResponse.model_validate(
                {
                    "skill_score": 0.12,
                    "skill_risk_level": "Minimal",
                    "classification": "UNKNOWN_SKILL",
                    "files": [],
                }
            ),
            SkillScanResponse.model_validate(
                {
                    "skill_score": 0.7,
                    "skill_risk_level": "Medium",
                    "classification": "UNKNOWN_SKILL",
                    "files": [],
                }
            ),
        ]

        result = runner.invoke(
            app,
            ["skills", "scan", str(tmp_path), "--fail-on", "warn"],
        )

    assert result.exit_code == 2
    payload = json.loads(result.output)
    assert [skill["skill_risk_level"] for skill in payload["skills"]] == [
        "Minimal",
        "Medium",
    ]


@pytest.mark.parametrize(
    ("args", "expected_message"),
    [
        (["skills", "add", "org/repo", "--all"], "either SOURCE or --all"),
        (["skills", "add"], "Use SOURCE or --all"),
    ],
)
def test_add_arg_validation(args: list[str], expected_message: str):
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert expected_message in result.output


def test_remove_all_prompts_and_aborts_on_no(tmp_path: Path):
    uninstall_mock = AsyncMock()
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.skills.read_lockfile",
            return_value=[_entry("a"), _entry("b")],
        ),
        patch("runlayer_cli.commands.skills.typer.confirm", return_value=False),
        patch(
            "runlayer_cli.commands.skills.uninstall_skill",
            new=uninstall_mock,
        ),
    ):
        result = runner.invoke(app, ["skills", "remove", "--all"])

    assert result.exit_code == 0
    assert "Aborted." in result.output
    uninstall_mock.assert_not_called()


def test_remove_all_yes_removes_without_prompt(tmp_path: Path):
    uninstall_mock = AsyncMock()
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.skills.read_lockfile",
            return_value=[_entry("a"), _entry("b")],
        ),
        patch("runlayer_cli.commands.skills.typer.confirm") as confirm_mock,
        patch(
            "runlayer_cli.commands.skills.uninstall_skill",
            new=uninstall_mock,
        ),
    ):
        result = runner.invoke(app, ["skills", "remove", "--all", "--yes"])

    assert result.exit_code == 0
    assert "Done: 2 removed" in result.output
    confirm_mock.assert_not_called()
    assert uninstall_mock.await_count == 2


@pytest.mark.parametrize(
    ("args", "expected_message"),
    [
        (["skills", "remove", "my-skill", "--all"], "either SKILL_NAME or --all"),
        (["skills", "remove"], "Use SKILL_NAME or --all"),
    ],
)
def test_remove_arg_validation(args: list[str], expected_message: str):
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert expected_message in result.output


def test_remove_all_global_uses_global_scope(tmp_path: Path):
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ) as resolve_dirs_mock,
        patch(
            "runlayer_cli.commands.skills.read_lockfile",
            return_value=[_entry("a")],
        ),
        patch(
            "runlayer_cli.commands.skills.uninstall_skill",
            new=AsyncMock(),
        ),
    ):
        result = runner.invoke(app, ["skills", "remove", "--all", "--yes", "--global"])

    assert result.exit_code == 0
    assert resolve_dirs_mock.call_args is not None
    assert resolve_dirs_mock.call_args.args[1] is True


def test_remove_all_filters_entries_by_selected_client(tmp_path: Path):
    entries = [
        LockEntry(name="a", id="id-a", client="claude_code"),
        LockEntry(name="b", id="id-b", client="cursor"),
    ]
    uninstall_mock = AsyncMock()
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.skills.read_lockfile",
            return_value=entries,
        ),
        patch(
            "runlayer_cli.commands.skills.uninstall_skill",
            new=uninstall_mock,
        ),
    ):
        result = runner.invoke(
            app,
            [
                "skills",
                "remove",
                "--all",
                "--yes",
                "--client",
                "cursor",
            ],
        )

    assert result.exit_code == 0
    assert "Done: 1 removed" in result.output
    uninstall_mock.assert_awaited_once()
    args = uninstall_mock.await_args_list[0].args
    assert args[0] == "b"
    assert args[-1] == "cursor"


@pytest.mark.parametrize(
    "command",
    [
        ["skills", "list"],
        ["skills", "remove", "--all", "--yes"],
    ],
)
def test_shows_friendly_error_when_lockfile_invalid(tmp_path: Path, command: list[str]):
    with (
        patch(
            "runlayer_cli.commands.skills.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.skills.resolve_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.skills.read_lockfile",
            side_effect=ValueError("invalid lockfile YAML"),
        ),
    ):
        result = runner.invoke(app, command)

    assert result.exit_code == 1
    assert "Error: invalid lockfile YAML" in result.output
    assert "See logs for details:" in result.output
