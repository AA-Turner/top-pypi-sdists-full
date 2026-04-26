from __future__ import annotations

from pathlib import Path

from anteroom.services.docs_project_links import prepare_docs_site, render_project_links_text
from anteroom.services.project_links import build_project_config


def _internal_project():
    return build_project_config(
        {
            "profile": "neutral",
            "name": "Internal Gateway",
            "repo_label": "gitlab.internal/platform/gateway",
            "repo_url": "https://gitlab.internal/platform/gateway",
            "release_url_template": "https://gitlab.internal/platform/gateway/-/releases/{version}",
            "issue_tracking": {"enabled": False},
        }
    )


def test_render_project_links_text_removes_public_issue_urls() -> None:
    text = (
        "See [#1580](https://github.com/troylar/anteroom/issues/1580), "
        "[GitHub Release](https://github.com/troylar/anteroom/releases/tag/v1.2.3), "
        "and https://github.com/troylar/anteroom."
    )

    rendered = render_project_links_text(text, _internal_project())

    assert "github.com/troylar/anteroom" not in rendered
    assert "#1580" in rendered
    assert "https://gitlab.internal/platform/gateway/-/releases/v1.2.3" in rendered
    assert "https://gitlab.internal/platform/gateway" in rendered


def test_render_project_links_text_suppresses_repo_markdown_link_without_url() -> None:
    project = build_project_config({"profile": "neutral"})

    rendered = render_project_links_text(
        "See [GitHub](https://github.com/troylar/anteroom) and clone https://github.com/troylar/anteroom.git.",
        project,
    )

    assert "github.com/troylar/anteroom" not in rendered
    assert "[GitHub](Anteroom)" not in rendered
    assert "See Anteroom" in rendered


def test_prepare_docs_site_renders_internal_docs_without_public_repo(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text(
        "Tracked by [#1580](https://github.com/troylar/anteroom/issues/1580).\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("git clone https://github.com/troylar/anteroom.git\n", encoding="utf-8")
    mkdocs_yml = tmp_path / "mkdocs.yml"
    mkdocs_yml.write_text(
        """
site_name: test
repo_url: https://github.com/troylar/anteroom
repo_name: troylar/anteroom
docs_dir: docs
nav:
  - Home: index.md
""".lstrip(),
        encoding="utf-8",
    )

    rendered_mkdocs = prepare_docs_site(mkdocs_yml, _internal_project())
    rendered_root = rendered_mkdocs.parent
    rendered_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in rendered_root.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yml", ".yaml"}
    )

    assert "github.com/troylar/anteroom" not in rendered_text
    assert "gitlab.internal/platform/gateway" in rendered_text


def test_prepare_docs_site_suppresses_github_social_when_repo_url_blank(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("# Home\n", encoding="utf-8")
    mkdocs_yml = tmp_path / "mkdocs.yml"
    mkdocs_yml.write_text(
        """
site_name: test
repo_url: https://github.com/troylar/anteroom
repo_name: troylar/anteroom
theme:
  icon:
    repo: fontawesome/brands/github
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/troylar/anteroom
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/anteroom/
nav:
  - Home: index.md
""".lstrip(),
        encoding="utf-8",
    )

    rendered_mkdocs = prepare_docs_site(mkdocs_yml, build_project_config({"profile": "neutral"}))
    rendered_text = rendered_mkdocs.read_text(encoding="utf-8")

    assert "github.com/troylar/anteroom" not in rendered_text
    assert "fontawesome/brands/github" not in rendered_text
    assert "link: Anteroom" not in rendered_text
    assert "material/source-repository" in rendered_text
    assert "fontawesome/brands/python" in rendered_text


def test_prepare_docs_site_uses_internal_forge_social_icon(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("# Home\n", encoding="utf-8")
    mkdocs_yml = tmp_path / "mkdocs.yml"
    mkdocs_yml.write_text(
        """
site_name: test
repo_url: https://github.com/troylar/anteroom
repo_name: troylar/anteroom
theme:
  icon:
    repo: fontawesome/brands/github
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/troylar/anteroom
nav:
  - Home: index.md
""".lstrip(),
        encoding="utf-8",
    )

    rendered_mkdocs = prepare_docs_site(mkdocs_yml, _internal_project())
    rendered_text = rendered_mkdocs.read_text(encoding="utf-8")

    assert "github.com/troylar/anteroom" not in rendered_text
    assert "fontawesome/brands/github" not in rendered_text
    assert "fontawesome/brands/gitlab" in rendered_text
    assert "link: https://gitlab.internal/platform/gateway" in rendered_text


def test_prepare_docs_site_uses_generic_icon_for_deceptive_repo_url(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("# Home\n", encoding="utf-8")
    mkdocs_yml = tmp_path / "mkdocs.yml"
    mkdocs_yml.write_text(
        """
site_name: test
repo_url: https://github.com/troylar/anteroom
repo_name: troylar/anteroom
theme:
  icon:
    repo: fontawesome/brands/github
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/troylar/anteroom
nav:
  - Home: index.md
""".lstrip(),
        encoding="utf-8",
    )
    project = build_project_config(
        {
            "profile": "neutral",
            "repo_label": "internal.example/repo",
            "repo_url": "https://internal.example/repo?mirror=github.com",
        }
    )

    rendered_mkdocs = prepare_docs_site(mkdocs_yml, project)
    rendered_text = rendered_mkdocs.read_text(encoding="utf-8")

    assert "fontawesome/brands/github" not in rendered_text
    assert "material/source-repository" in rendered_text
    assert "link: https://internal.example/repo?mirror=github.com" in rendered_text
