"""Tests for references config section."""

from __future__ import annotations

import tempfile
from pathlib import Path

import yaml

from anteroom.config import ReferencesConfig, _resolve_reference_paths, load_config


def _r(p: str | Path) -> Path:
    return Path(p).resolve()


class TestReferencesConfig:
    def test_defaults_empty(self) -> None:
        cfg = ReferencesConfig()
        assert cfg.instructions == []
        assert cfg.rules == []
        assert cfg.skills == []

    def test_loads_from_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            base = _r(tmpdir)
            cfg_path = base / "config.yaml"
            cfg_path.write_text(
                yaml.dump(
                    {
                        "ai": {"base_url": "http://localhost:8080", "api_key": "k"},
                        "references": {
                            "instructions": ["team/instructions.md", "team/setup.md"],
                            "rules": ["team/rules/no-eval.md"],
                            "skills": ["team/skills/deploy.md"],
                        },
                    }
                )
            )

            config, _ = load_config(cfg_path)
            # Paths are resolved to absolute during config loading
            assert len(config.references.instructions) == 2
            assert all(Path(p).is_absolute() for p in config.references.instructions)
            assert config.references.instructions[0] == str((base / "team" / "instructions.md").resolve())
            assert len(config.references.rules) == 1
            assert len(config.references.skills) == 1

    def test_missing_references_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            base = _r(tmpdir)
            cfg_path = base / "config.yaml"
            cfg_path.write_text(
                yaml.dump(
                    {
                        "ai": {"base_url": "http://localhost:8080", "api_key": "k"},
                    }
                )
            )

            config, _ = load_config(cfg_path)
            assert config.references.instructions == []
            assert config.references.rules == []
            assert config.references.skills == []

    def test_filters_non_string_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            base = _r(tmpdir)
            cfg_path = base / "config.yaml"
            cfg_path.write_text(
                yaml.dump(
                    {
                        "ai": {"base_url": "http://localhost:8080", "api_key": "k"},
                        "references": {
                            "instructions": ["valid.md", 123, None, "", "also-valid.md"],
                        },
                    }
                )
            )

            config, _ = load_config(cfg_path)
            assert len(config.references.instructions) == 2
            assert all(Path(p).is_absolute() for p in config.references.instructions)

    def test_invalid_references_section_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            base = _r(tmpdir)
            cfg_path = base / "config.yaml"
            cfg_path.write_text(
                yaml.dump(
                    {
                        "ai": {"base_url": "http://localhost:8080", "api_key": "k"},
                        "references": "not-a-dict",
                    }
                )
            )

            config, _ = load_config(cfg_path)
            assert config.references.instructions == []

    def test_partial_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            base = _r(tmpdir)
            cfg_path = base / "config.yaml"
            cfg_path.write_text(
                yaml.dump(
                    {
                        "ai": {"base_url": "http://localhost:8080", "api_key": "k"},
                        "references": {
                            "rules": ["rule1.md"],
                        },
                    }
                )
            )

            config, _ = load_config(cfg_path)
            assert config.references.instructions == []
            assert len(config.references.rules) == 1
            assert Path(config.references.rules[0]).is_absolute()
            assert config.references.skills == []

    def test_references_from_project_config(self) -> None:
        from anteroom.services.trust import compute_content_hash, save_trust_decision

        with tempfile.TemporaryDirectory() as tmpdir:
            base = _r(tmpdir)

            personal = base / "config.yaml"
            personal.write_text(
                yaml.dump(
                    {
                        "ai": {"base_url": "http://localhost:8080", "api_key": "k"},
                    }
                )
            )

            proj_dir = base / "project" / ".anteroom"
            proj_dir.mkdir(parents=True)
            proj_cfg = proj_dir / "config.yaml"
            proj_cfg.write_text(
                yaml.dump(
                    {
                        "references": {
                            "instructions": ["project-instructions.md"],
                            "skills": ["project-skill.md"],
                        },
                    }
                )
            )

            content = proj_cfg.read_text(encoding="utf-8")
            content_hash = compute_content_hash(content)
            save_trust_decision(str(proj_cfg.resolve()), content_hash, recursive=False, data_dir=base)

            config, _ = load_config(personal, project_config_path=proj_cfg)
            # Project config paths resolved relative to project config dir
            assert len(config.references.instructions) == 1
            assert Path(config.references.instructions[0]).is_absolute()
            assert config.references.instructions[0] == str((proj_dir / "project-instructions.md").resolve())
            assert len(config.references.skills) == 1
            assert Path(config.references.skills[0]).is_absolute()


class TestResolveReferencePaths:
    def test_resolves_relative_to_base_dir(self, tmp_path: Path) -> None:
        base_dir = tmp_path / "home" / ".anteroom"
        base_dir.mkdir(parents=True)
        raw: dict = {"references": {"skills": ["skills/deploy"]}}
        result = _resolve_reference_paths(raw, base_dir)
        paths = result["references"]["skills"]
        assert len(paths) == 1
        assert Path(paths[0]).is_absolute()
        assert paths[0] == str((base_dir / "skills" / "deploy").resolve())

    def test_preserves_absolute_paths(self, tmp_path: Path) -> None:
        abs_path = str(tmp_path / "skills" / "deploy")
        raw: dict = {"references": {"skills": [abs_path]}}
        result = _resolve_reference_paths(raw, tmp_path)
        assert result["references"]["skills"] == [abs_path]

    def test_no_references_is_noop(self, tmp_path: Path) -> None:
        raw: dict = {"ai": {"model": "gpt-4"}}
        result = _resolve_reference_paths(raw, tmp_path)
        assert result == raw

    def test_handles_all_reference_types(self, tmp_path: Path) -> None:
        raw: dict = {
            "references": {
                "instructions": ["docs/guide.md"],
                "rules": ["rules/no-eval.md"],
                "skills": ["skills/deploy"],
            }
        }
        result = _resolve_reference_paths(raw, tmp_path)
        for key in ("instructions", "rules", "skills"):
            paths = result["references"][key]
            assert len(paths) == 1
            assert Path(paths[0]).is_absolute()
