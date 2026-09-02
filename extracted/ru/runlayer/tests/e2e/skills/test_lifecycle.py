import shutil
import json
from pathlib import Path

from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier
from runlayer_cli.skills.installer import read_lockfile


def _create_skill_dir(root: Path, name: str) -> None:
    """Create a minimal skill directory with SKILL.md."""
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: E2E test skill\n---\n\n# {name}\n\nTest skill.\n"
    )


def _create_customer_shape_skill_dir(
    root: Path,
    name: str,
    *,
    extra_files: dict[str, str],
) -> Path:
    """Create a standalone skill dir shaped like the customer fixture."""
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Customer-shape e2e skill\n---\n\n# {name}\n\nUse this skill.\n"
    )
    for rel_path, content in extra_files.items():
        file_path = skill_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    return skill_dir


def test_skills_push_lifecycle(runner, cli_args, tmp_path, unique_id):
    """runlayer skills push → push (idempotent) → push --prune"""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"test-skill-{unique_id}"
    _create_skill_dir(skills_root, skill_name)

    namespace = f"e2e-test/{unique_id}"

    result = runner.invoke(
        app,
        [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"push failed: {output}"
    assert "1 created" in output

    result = runner.invoke(
        app,
        [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"push 2 failed: {output}"
    assert "1 unchanged" in output or "0 created" in output

    shutil.rmtree(skills_root / skill_name)
    result = runner.invoke(
        app,
        [
            *cli_args,
            "skills",
            "push",
            str(skills_root),
            "--namespace",
            namespace,
            "--prune",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"prune failed: {output}"
    assert "1 deleted" in output


def test_skills_scan_returns_json(
    runner, base_url, security_scan_api_key, tmp_path, unique_id
):
    """skills scan returns JSON from security scan API."""
    skill_dir = tmp_path / "scan-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: scan-skill-{unique_id}\ndescription: E2E test skill\n---\n\n# scan\n"
    )
    (skill_dir / "helper.py").write_text("print('scan')\n")

    result = runner.invoke(
        app,
        [
            "--secret",
            security_scan_api_key,
            "--host",
            base_url,
            "skills",
            "scan",
            str(skill_dir),
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output

    payload = json.loads(output)
    assert "skill_score" in payload
    assert "skill_risk_level" in payload
    assert "classification" in payload
    assert {file["name"] for file in payload["files"]} == {"SKILL.md", "helper.py"}


def test_skills_push_preserves_public_visibility(
    runner, cli_args, api_client, tmp_path, unique_id
):
    """skills push --public → skills push preserves public visibility"""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"test-skill-{unique_id}"
    _create_skill_dir(skills_root, skill_name)

    namespace = f"e2e-test/{unique_id}"

    try:
        result = runner.invoke(
            app,
            [
                *cli_args,
                "skills",
                "push",
                str(skills_root),
                "--namespace",
                namespace,
                "--public",
            ],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"public push failed: {output}"

        pushed_skill = next(
            skill
            for skill in api_client.list_skills(namespace)
            if skill.path == skill_name
        )
        assert pushed_skill.is_public is True

        result = runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"plain push failed: {output}"

        pushed_skill = next(
            skill
            for skill in api_client.list_skills(namespace)
            if skill.path == skill_name
        )
        assert pushed_skill.is_public is True
    finally:
        for skill in api_client.list_skills(namespace):
            api_client.delete_skill(skill.id)


def test_skills_add_list_remove(runner, cli_args, tmp_path, unique_id, monkeypatch):
    """runlayer skills add → list → remove"""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"test-skill-{unique_id}"
    _create_skill_dir(skills_root, skill_name)

    namespace = f"e2e-test/{unique_id}"

    result = runner.invoke(
        app,
        [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
    )
    assert result.exit_code == 0, f"push failed: {strip_ansi(result.output)}"

    project_dir = tmp_path / "project"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    result = runner.invoke(
        app,
        [*cli_args, "skills", "add", namespace, "--client", "claude_code"],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"add failed: {output}"
    assert "1 installed" in output

    result = runner.invoke(app, ["skills", "list", "--client", "claude_code"])
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"list failed: {output}"
    assert skill_name in output

    result = runner.invoke(
        app, ["skills", "remove", skill_name, "--client", "claude_code"]
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"remove failed: {output}"
    assert "Removed" in output

    shutil.rmtree(skills_root / skill_name)
    runner.invoke(
        app,
        [
            *cli_args,
            "skills",
            "push",
            str(skills_root),
            "--namespace",
            namespace,
            "--prune",
        ],
    )


def test_skills_push_separate_root_skill_dirs_do_not_clobber(
    runner, cli_args, api_client, tmp_path, unique_id
):
    """Separate standalone skill dirs in one namespace should create distinct skills."""
    root = tmp_path / "customer-shape"
    org_skills = root / "Organization Skills"
    org_skills.mkdir(parents=True)

    first_skill_dir = _create_customer_shape_skill_dir(
        org_skills,
        f"brand-voice-{unique_id}",
        extra_files={"helper.py": "print('tone')\n"},
    )
    second_skill_dir = _create_customer_shape_skill_dir(
        org_skills,
        f"image-workflow-{unique_id}",
        extra_files={
            "README.md": "# Notes\n",
            "EXAMPLES.md": "Example content\n",
            "references/REFERENCE.md": "Reference content\n",
        },
    )

    namespace = f"e2e-root-skill/{unique_id}"

    try:
        first = runner.invoke(
            app,
            [
                *cli_args,
                "skills",
                "push",
                str(first_skill_dir),
                "--namespace",
                namespace,
            ],
        )
        first_output = strip_ansi(first.output)
        assert first.exit_code == 0, f"first push failed: {first_output}"
        assert "1 created" in first_output

        second = runner.invoke(
            app,
            [
                *cli_args,
                "skills",
                "push",
                str(second_skill_dir),
                "--namespace",
                namespace,
            ],
        )
        second_output = strip_ansi(second.output)
        assert second.exit_code == 0, f"second push failed: {second_output}"
        assert "1 created" in second_output

        skills = sorted(
            api_client.list_skills(namespace), key=lambda skill: skill.path or ""
        )
        assert len(skills) == 2
        assert len({skill.id for skill in skills}) == 2
        assert {skill.path for skill in skills} == {
            first_skill_dir.name,
            second_skill_dir.name,
        }
        assert {skill.name for skill in skills} == {
            first_skill_dir.name,
            second_skill_dir.name,
        }
    finally:
        for skill in api_client.list_skills(namespace):
            api_client.delete_skill(skill.id)


def test_skills_add_list_remove_vscode(
    runner, cli_args, tmp_path, unique_id, monkeypatch
):
    """runlayer skills add/list/remove works for VS Code native skills."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"test-skill-{unique_id}"
    _create_skill_dir(skills_root, skill_name)

    namespace = f"e2e-test/{unique_id}"

    result = runner.invoke(
        app,
        [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
    )
    assert result.exit_code == 0, f"push failed: {strip_ansi(result.output)}"

    project_dir = tmp_path / "project"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    result = runner.invoke(
        app,
        [*cli_args, "skills", "add", namespace, "--client", "vscode"],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"add failed: {output}"
    assert "1 installed" in output

    installed_skill = project_dir / ".agents" / "skills" / skill_name
    assert installed_skill.exists()
    assert not installed_skill.is_symlink()
    assert (installed_skill / "SKILL.md").exists()
    assert not (project_dir / ".vscode" / "skills" / skill_name).exists()

    lockfile = project_dir / ".runlayer" / "skill-lock.yml"
    assert lockfile.exists()
    lockfile_text = lockfile.read_text(encoding="utf-8")
    assert "client: vscode" in lockfile_text
    assert f"name: {skill_name}" in lockfile_text

    result = runner.invoke(app, ["skills", "list", "--client", "vscode"])
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"list failed: {output}"
    assert skill_name in output

    result = runner.invoke(app, ["skills", "remove", skill_name, "--client", "vscode"])
    output = strip_ansi(result.output)
    assert result.exit_code == 0, f"remove failed: {output}"
    assert "Removed" in output
    assert not installed_skill.exists()

    shutil.rmtree(skills_root / skill_name)
    runner.invoke(
        app,
        [
            *cli_args,
            "skills",
            "push",
            str(skills_root),
            "--namespace",
            namespace,
            "--prune",
        ],
    )


# ---------------------------------------------------------------------------
# Skill identifier (Merkle) e2e tests
# ---------------------------------------------------------------------------


def _skill_md_content(name: str, description: str = "E2E test skill") -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\nTest skill.\n"


def _prune_namespace(runner, cli_args, skills_root, namespace):
    """Push empty root with --prune to delete all remote skills in namespace."""
    runner.invoke(
        app,
        [
            *cli_args,
            "skills",
            "push",
            str(skills_root),
            "--namespace",
            namespace,
            "--prune",
        ],
    )


def _lockfile_identifiers(lockfile_path: Path) -> dict[str, str | None]:
    """Return {skill_name: identifier} from a skill-lock.yml."""
    entries = read_lockfile(lockfile_path)
    return {e.name: e.identifier for e in entries}


def test_push_identifier_returned_by_backend(
    runner, cli_args, api_client, tmp_path, unique_id
):
    """Backend returns an identifier matching the local Merkle computation."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"id-check-{unique_id}"
    skill_content = _skill_md_content(skill_name)
    skill_dir = skills_root / skill_name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(skill_content)

    namespace = f"e2e-id/{unique_id}"

    try:
        result = runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        assert result.exit_code == 0, f"push failed: {strip_ansi(result.output)}"

        skills = api_client.list_skills(namespace)
        assert len(skills) == 1
        remote = skills[0]
        assert remote.identifier is not None, "backend did not return an identifier"

        local_id = compute_skill_identifier(
            [SkillFileInput(name="SKILL.md", content=skill_content)]
        )
        assert remote.identifier == local_id.root
    finally:
        _prune_namespace(runner, cli_args, skills_root, namespace)


def test_push_idempotent_identifier_stable(
    runner, cli_args, api_client, tmp_path, unique_id
):
    """Second push of unchanged skill yields 'unchanged'; identifier stays the same."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"idem-{unique_id}"
    _create_skill_dir(skills_root, skill_name)

    namespace = f"e2e-idem/{unique_id}"

    try:
        runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        id_after_first = api_client.list_skills(namespace)[0].identifier

        result = runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"push 2 failed: {output}"
        assert "1 unchanged" in output

        id_after_second = api_client.list_skills(namespace)[0].identifier
        assert id_after_first is not None
        assert id_after_first == id_after_second
    finally:
        _prune_namespace(runner, cli_args, skills_root, namespace)


def test_push_file_change_triggers_new_identifier(
    runner, cli_args, api_client, tmp_path, unique_id
):
    """Modifying file content produces a new identifier and 'updated' on push."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"fchg-{unique_id}"
    skill_dir = skills_root / skill_name
    skill_dir.mkdir(parents=True)
    original_content = _skill_md_content(skill_name)
    (skill_dir / "SKILL.md").write_text(original_content)

    namespace = f"e2e-fchg/{unique_id}"

    try:
        runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        id_before = api_client.list_skills(namespace)[0].identifier
        assert id_before is not None

        modified_content = _skill_md_content(
            skill_name, description="Updated description"
        )
        (skill_dir / "SKILL.md").write_text(modified_content)

        result = runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"push 2 failed: {output}"
        assert "1 updated" in output

        id_after = api_client.list_skills(namespace)[0].identifier
        assert id_after is not None
        assert id_after != id_before

        expected = compute_skill_identifier(
            [SkillFileInput(name="SKILL.md", content=modified_content)]
        )
        assert id_after == expected.root
    finally:
        _prune_namespace(runner, cli_args, skills_root, namespace)


def test_push_metadata_change_updates_identifier(
    runner, cli_args, api_client, tmp_path, unique_id
):
    """Changing frontmatter (name/description) alters SKILL.md content, changing the identifier."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"meta-{unique_id}"
    skill_dir = skills_root / skill_name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(_skill_md_content(skill_name))

    namespace = f"e2e-meta/{unique_id}"

    try:
        runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        id_before = api_client.list_skills(namespace)[0].identifier

        new_content = _skill_md_content(skill_name, description="Changed metadata only")
        (skill_dir / "SKILL.md").write_text(new_content)

        result = runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"push 2 failed: {output}"
        assert "1 updated" in output

        id_after = api_client.list_skills(namespace)[0].identifier
        assert id_after != id_before
    finally:
        _prune_namespace(runner, cli_args, skills_root, namespace)


def test_update_short_circuits_on_matching_identifier(
    runner, cli_args, tmp_path, unique_id, monkeypatch
):
    """skills update reports 'up to date' when lockfile identifier matches remote."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"upsc-{unique_id}"
    _create_skill_dir(skills_root, skill_name)

    namespace = f"e2e-upsc/{unique_id}"

    result = runner.invoke(
        app,
        [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
    )
    assert result.exit_code == 0, f"push failed: {strip_ansi(result.output)}"

    project_dir = tmp_path / "project"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    try:
        result = runner.invoke(
            app,
            [*cli_args, "skills", "add", namespace, "--client", "claude_code"],
        )
        assert result.exit_code == 0, f"add failed: {strip_ansi(result.output)}"

        lockfile_path = project_dir / ".runlayer" / "skill-lock.yml"
        ids = _lockfile_identifiers(lockfile_path)
        assert skill_name in ids
        assert ids[skill_name] is not None, "identifier not persisted in lockfile"

        skill_md = project_dir / ".agents" / "skills" / skill_name / "SKILL.md"
        content_before = skill_md.read_text(encoding="utf-8")

        result = runner.invoke(
            app,
            [*cli_args, "skills", "update", "--client", "claude_code"],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"update failed: {output}"
        assert "up to date" in output.lower()

        assert skill_md.read_text(encoding="utf-8") == content_before
    finally:
        runner.invoke(app, ["skills", "remove", skill_name, "--client", "claude_code"])
        _prune_namespace(runner, cli_args, skills_root, namespace)


def test_update_detects_remote_change(
    runner, cli_args, tmp_path, unique_id, monkeypatch
):
    """skills update fetches new files when remote identifier differs from lockfile."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"updt-{unique_id}"
    skill_dir = skills_root / skill_name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(_skill_md_content(skill_name))

    namespace = f"e2e-updt/{unique_id}"

    result = runner.invoke(
        app,
        [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
    )
    assert result.exit_code == 0, f"push failed: {strip_ansi(result.output)}"

    project_dir = tmp_path / "project"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    try:
        result = runner.invoke(
            app,
            [*cli_args, "skills", "add", namespace, "--client", "claude_code"],
        )
        assert result.exit_code == 0, f"add failed: {strip_ansi(result.output)}"

        lockfile_path = project_dir / ".runlayer" / "skill-lock.yml"
        id_before = _lockfile_identifiers(lockfile_path)[skill_name]

        updated_content = _skill_md_content(skill_name, description="Remotely updated")
        (skill_dir / "SKILL.md").write_text(updated_content)
        push_result = runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        assert push_result.exit_code == 0, (
            f"re-push failed: {strip_ansi(push_result.output)}"
        )

        result = runner.invoke(
            app,
            [*cli_args, "skills", "update", "--client", "claude_code"],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"update failed: {output}"
        assert "1 updated" in output

        id_after = _lockfile_identifiers(lockfile_path)[skill_name]
        assert id_after is not None
        assert id_after != id_before

        installed_content = (
            project_dir / ".agents" / "skills" / skill_name / "SKILL.md"
        ).read_text(encoding="utf-8")
        assert "Remotely updated" in installed_content
    finally:
        runner.invoke(app, ["skills", "remove", skill_name, "--client", "claude_code"])
        _prune_namespace(runner, cli_args, skills_root, namespace)


def test_multi_file_update_round_trip(
    runner, cli_args, tmp_path, unique_id, monkeypatch
):
    """Push multi-file skill, add, change one file remotely, update -> content on disk matches."""
    skills_root = tmp_path / "skills-source"
    skills_root.mkdir()
    skill_name = f"mfrt-{unique_id}"
    helper_v1 = "def greet():\n    return 'hello'\n"
    helper_v2 = "def greet():\n    return 'hello world'\n"

    _create_customer_shape_skill_dir(
        skills_root, skill_name, extra_files={"helper.py": helper_v1}
    )

    namespace = f"e2e-mfrt/{unique_id}"

    result = runner.invoke(
        app,
        [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
    )
    assert result.exit_code == 0, f"push failed: {strip_ansi(result.output)}"

    project_dir = tmp_path / "project"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    try:
        result = runner.invoke(
            app,
            [*cli_args, "skills", "add", namespace, "--client", "claude_code"],
        )
        assert result.exit_code == 0, f"add failed: {strip_ansi(result.output)}"

        installed_helper = project_dir / ".agents" / "skills" / skill_name / "helper.py"
        assert installed_helper.read_text(encoding="utf-8") == helper_v1

        (skills_root / skill_name / "helper.py").write_text(helper_v2)
        push_result = runner.invoke(
            app,
            [*cli_args, "skills", "push", str(skills_root), "--namespace", namespace],
        )
        assert push_result.exit_code == 0

        result = runner.invoke(
            app,
            [*cli_args, "skills", "update", "--client", "claude_code"],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, f"update failed: {output}"
        assert "1 updated" in output

        assert installed_helper.read_text(encoding="utf-8") == helper_v2
    finally:
        runner.invoke(app, ["skills", "remove", skill_name, "--client", "claude_code"])
        _prune_namespace(runner, cli_args, skills_root, namespace)
