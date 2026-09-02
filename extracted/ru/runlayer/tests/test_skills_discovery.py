from runlayer_cli.skills.discovery import discover_skills


def _make_skill(tmp_path, rel_path, frontmatter=None, extra_files=None):
    skill_dir = tmp_path / rel_path
    skill_dir.mkdir(parents=True, exist_ok=True)
    content = ""
    if frontmatter:
        content = f"---\n{frontmatter}\n---\n"
    content += "# Skill docs\n"
    (skill_dir / "SKILL.md").write_text(content)
    if extra_files:
        for name, text in extra_files.items():
            p = skill_dir / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)


def test_discover_empty_dir(tmp_path):
    assert discover_skills(tmp_path) == []


def test_discover_single_skill(tmp_path):
    _make_skill(
        tmp_path,
        "skills/ticket-triage",
        "name: Ticket Triage\ndescription: Triage tickets",
    )
    result = discover_skills(tmp_path)
    assert len(result) == 1
    assert result[0].path == "skills/ticket-triage"
    assert result[0].name == "Ticket Triage"
    assert result[0].description == "Triage tickets"
    # SKILL.md should be in files
    titles = [f.title for f in result[0].files]
    assert "SKILL.md" in titles


def test_discover_case_variant_marker(tmp_path):
    skill_dir = tmp_path / "skills" / "sneaky"
    skill_dir.mkdir(parents=True)
    (skill_dir / "skill.md").write_text("---\nname: sneaky\n---\n# docs")
    result = discover_skills(tmp_path)
    assert len(result) == 1
    assert result[0].name == "sneaky"


def test_discover_multiple_skills(tmp_path):
    _make_skill(tmp_path, "skills/a", "name: Skill A")
    _make_skill(tmp_path, "skills/b", "name: Skill B")
    result = discover_skills(tmp_path)
    assert len(result) == 2
    paths = [s.path for s in result]
    assert "skills/a" in paths
    assert "skills/b" in paths


def test_discover_no_frontmatter_uses_folder_name(tmp_path):
    """SKILL.md without frontmatter falls back to folder name."""
    _make_skill(tmp_path, "skills/my-skill")
    result = discover_skills(tmp_path)
    assert len(result) == 1
    assert result[0].name == "my-skill"


def test_discover_missing_name_uses_folder_name(tmp_path):
    """SKILL.md with frontmatter but no name key falls back to folder name."""
    _make_skill(tmp_path, "skills/my-skill", "description: some desc")
    result = discover_skills(tmp_path)
    assert len(result) == 1
    assert result[0].name == "my-skill"


def test_discover_skips_hidden_dirs(tmp_path):
    _make_skill(tmp_path, ".git/hooks/skill", "name: hidden")
    _make_skill(tmp_path, "node_modules/pkg/skill", "name: hidden")
    _make_skill(tmp_path, "__pycache__/skill", "name: hidden")
    assert discover_skills(tmp_path) == []


def test_discover_collects_supported_files(tmp_path):
    _make_skill(
        tmp_path,
        "skills/demo",
        frontmatter="name: Demo",
        extra_files={
            "assets/config.yaml": "enabled: true",
            "assets/data.csv": "name,value",
            "assets/icon.xml": "<icon />",
            "assets/logo.SVG": "<svg />",
            "assets/schema.json": "{}",
            "assets/template.html": "<main />",
            "assets/theme.css": "body {}",
            "helper.py": "print('hi')",
            "notes.txt": "some notes",
            "sub/nested.md": "# Nested",
            "binary.bin": "not collected",
        },
    )
    result = discover_skills(tmp_path)
    titles = {f.title for f in result[0].files}
    assert "helper.py" in titles
    assert "notes.txt" in titles
    assert "sub/nested.md" in titles
    assert "binary.bin" not in titles  # unsupported extension


def test_discover_does_not_descend_into_skill_dir(tmp_path):
    """A SKILL.md inside a skill's subdir should not create a second skill."""
    skill_dir = tmp_path / "skills" / "parent"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: parent\n---\n")
    nested = skill_dir / "child"
    nested.mkdir()
    (nested / "SKILL.md").write_text("---\nname: child\n---\n")
    result = discover_skills(tmp_path)
    assert len(result) == 1
    assert result[0].name == "parent"


def test_discover_sorted_by_path(tmp_path):
    _make_skill(tmp_path, "z-skill", "name: Z")
    _make_skill(tmp_path, "a-skill", "name: A")
    _make_skill(tmp_path, "m-skill", "name: M")
    result = discover_skills(tmp_path)
    paths = [s.path for s in result]
    assert paths == sorted(paths)


def test_discover_non_string_frontmatter_values(tmp_path):
    """YAML-parsed int/bool name is coerced to string."""
    _make_skill(tmp_path, "skills/num", "name: 42\ndescription: 123")
    _make_skill(tmp_path, "skills/bool", "name: true\ndescription: false")
    result = discover_skills(tmp_path)
    by_path = {s.path: s for s in result}
    assert by_path["skills/num"].name == "42"
    assert by_path["skills/num"].description == "123"
    assert by_path["skills/bool"].name == "True"
    assert by_path["skills/bool"].description == "False"


def test_discover_truncates_long_name(tmp_path):
    long_name = "A" * 200
    _make_skill(tmp_path, "skills/long", f"name: {long_name}")
    result = discover_skills(tmp_path)
    assert len(result) == 1
    assert len(result[0].name) == 100
    assert result[0].name == "A" * 100


def test_discover_skill_at_root(tmp_path):
    """SKILL.md directly in root should use the root dir basename as path."""
    (tmp_path / "SKILL.md").write_text("---\nname: root-skill\n---\n")
    result = discover_skills(tmp_path)
    assert len(result) == 1
    assert result[0].path == tmp_path.name
    assert result[0].name == "root-skill"
