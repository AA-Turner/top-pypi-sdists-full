import pytest

from runlayer_cli.skill_identifier import (
    SkillFileInput,
    SkillIdentifier,
    compute_skill_identifier,
)


class TestComputeSkillIdentifier:
    def test_single_file(self):
        result = compute_skill_identifier(
            [SkillFileInput(name="SKILL.md", content="hello")]
        )
        assert isinstance(result, SkillIdentifier)
        assert len(result.root) == 64
        assert "SKILL.md" in result.file_hashes

    def test_ordering_invariance(self):
        files_a = [
            SkillFileInput(name="a.md", content="aaa"),
            SkillFileInput(name="b.md", content="bbb"),
        ]
        files_b = [
            SkillFileInput(name="b.md", content="bbb"),
            SkillFileInput(name="a.md", content="aaa"),
        ]
        assert (
            compute_skill_identifier(files_a).root
            == compute_skill_identifier(files_b).root
        )

    def test_content_change_changes_id(self):
        base = [SkillFileInput(name="f.md", content="v1")]
        modified = [SkillFileInput(name="f.md", content="v2")]
        assert (
            compute_skill_identifier(base).root
            != compute_skill_identifier(modified).root
        )

    def test_name_change_changes_id(self):
        base = [SkillFileInput(name="a.md", content="same")]
        renamed = [SkillFileInput(name="b.md", content="same")]
        assert (
            compute_skill_identifier(base).root
            != compute_skill_identifier(renamed).root
        )

    def test_multiple_files(self):
        files = [
            SkillFileInput(name="SKILL.md", content="main"),
            SkillFileInput(name="helper.py", content="def x(): pass"),
            SkillFileInput(name="config.json", content="{}"),
        ]
        result = compute_skill_identifier(files)
        assert len(result.file_hashes) == 3
        assert all(len(h) == 64 for h in result.file_hashes.values())

    def test_empty_files_raises(self):
        with pytest.raises(ValueError, match="no files"):
            compute_skill_identifier([])

    def test_determinism(self):
        files = [SkillFileInput(name="x.md", content="y")]
        r1 = compute_skill_identifier(files)
        r2 = compute_skill_identifier(files)
        assert r1.root == r2.root
        assert r1.file_hashes == r2.file_hashes

    def test_whitespace_normalization(self):
        f1 = [SkillFileInput(name="  a.md  ", content="  hello  ")]
        f2 = [SkillFileInput(name="a.md", content="hello")]
        assert compute_skill_identifier(f1).root == compute_skill_identifier(f2).root
