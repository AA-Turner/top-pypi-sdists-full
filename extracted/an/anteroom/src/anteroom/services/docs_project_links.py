"""Render documentation links through the configured project profile."""

from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from .project_links import (
    ProjectConfig,
    build_project_config,
    issue_label,
    issue_url,
    project_display_label,
    release_url,
)

PUBLIC_REPO_URL = "https://github.com/troylar/anteroom"
PUBLIC_REPO_LABEL = "github.com/troylar/anteroom"
PUBLIC_REPO_NAME = "troylar/anteroom"

_TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".toml", ".txt"}
_ISSUE_LINK_RE = re.compile(
    r"\[(?P<label>[^\]]*#(?P<num>\d+)[^\]]*)\]\("
    r"https://github\.com/troylar/anteroom/issues/(?P=num)\)"
)
_ISSUE_URL_RE = re.compile(r"https://github\.com/troylar/anteroom/issues/(?P<num>\d+)")
_REPO_LINK_RE = re.compile(r"\[(?P<label>[^\]]+)\]\(https://github\.com/troylar/anteroom(?:\.git)?\)")
_RELEASE_LINK_RE = re.compile(
    r"\[(?P<label>[^\]]+)\]\(https://github\.com/troylar/anteroom/releases/tag/(?P<version>[^)]+)\)"
)
_RELEASE_URL_RE = re.compile(r"https://github\.com/troylar/anteroom/releases/tag/(?P<version>[^\s)]+)")
_GITHUB_SOCIAL_RE = re.compile(
    r"(?m)^    - icon: fontawesome/brands/github\n      link: https://github\.com/troylar/anteroom\n"
)


def _markdown_issue_ref(project: ProjectConfig, number: str) -> str:
    label = issue_label(project, number)
    url = issue_url(project, number)
    if url:
        return f"[{label}]({url})"
    return label


def _markdown_release_ref(project: ProjectConfig, version: str, label: str) -> str:
    url = release_url(project, version)
    if url:
        rendered_label = "Release" if "GitHub" in label else label
        return f"[{rendered_label}]({url})"
    return "Release"


def _markdown_repo_ref(project: ProjectConfig) -> str:
    label = project_display_label(project)
    if project.repo_url:
        return f"[{label}]({project.repo_url})"
    return label


def render_project_links_text(text: str, project: ProjectConfig) -> str:
    """Rewrite Anteroom-owned public links for the selected project profile."""
    repo_url = project.repo_url or project_display_label(project)
    repo_git_url = f"{project.repo_url}.git" if project.repo_url.startswith(("http://", "https://")) else repo_url
    repo_label = project_display_label(project)

    text = _ISSUE_LINK_RE.sub(lambda m: _markdown_issue_ref(project, m.group("num")), text)
    text = _ISSUE_URL_RE.sub(lambda m: issue_url(project, m.group("num")) or issue_label(project, m.group("num")), text)
    text = _REPO_LINK_RE.sub(lambda m: _markdown_repo_ref(project), text)
    text = _RELEASE_LINK_RE.sub(
        lambda m: _markdown_release_ref(project, m.group("version"), m.group("label")),
        text,
    )
    text = _RELEASE_URL_RE.sub(lambda m: release_url(project, m.group("version")) or "Release", text)
    text = text.replace(f"{PUBLIC_REPO_URL}.git", repo_git_url)
    text = text.replace(PUBLIC_REPO_URL, repo_url)
    text = text.replace(PUBLIC_REPO_LABEL, repo_label)
    return text


def _repo_icon(project: ProjectConfig) -> str:
    hostname = (urlparse(project.repo_url).hostname or "").lower()
    if hostname == "github.com" or hostname.endswith(".github.com"):
        return "fontawesome/brands/github"
    if hostname == "gitlab.com" or hostname.endswith(".gitlab.com") or hostname.startswith("gitlab."):
        return "fontawesome/brands/gitlab"
    if hostname == "bitbucket.org" or hostname.endswith(".bitbucket.org") or hostname.startswith("bitbucket."):
        return "fontawesome/brands/bitbucket"
    return "material/source-repository"


def _render_mkdocs_social(text: str, project: ProjectConfig) -> str:
    if not project.repo_url:
        return _GITHUB_SOCIAL_RE.sub("", text)
    replacement = f"    - icon: {_repo_icon(project)}\n      link: {project.repo_url}\n"
    return _GITHUB_SOCIAL_RE.sub(replacement, text)


def _render_mkdocs_yml(path: Path, project: ProjectConfig) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^repo_url:.*$", f"repo_url: {project.repo_url or ''}", text, flags=re.MULTILINE)
    text = re.sub(r"^repo_name:.*$", f"repo_name: {project.repo_label or ''}", text, flags=re.MULTILINE)
    text = re.sub(
        r"^    repo: fontawesome/brands/github$",
        f"    repo: {_repo_icon(project)}",
        text,
        flags=re.MULTILINE,
    )
    text = _render_mkdocs_social(text, project)
    text = render_project_links_text(text, project)
    path.write_text(text, encoding="utf-8")


def render_project_links_in_place(root: Path, project: ProjectConfig | None = None) -> None:
    project = project or build_project_config()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in _TEXT_SUFFIXES:
            continue
        if path.name == "mkdocs.yml":
            _render_mkdocs_yml(path, project)
            continue
        text = path.read_text(encoding="utf-8")
        rendered = render_project_links_text(text, project)
        if rendered != text:
            path.write_text(rendered, encoding="utf-8")


def prepare_docs_site(mkdocs_yml: Path, project: ProjectConfig | None = None) -> Path:
    """Copy a docs tree to a temporary rendered tree and return its mkdocs.yml."""
    project = project or build_project_config()
    source_root = mkdocs_yml.resolve().parent
    rendered_root = Path(tempfile.mkdtemp(prefix="anteroom-docs-"))
    shutil.copy2(mkdocs_yml, rendered_root / "mkdocs.yml")
    for item in ("docs", "README.md"):
        src = source_root / item
        dst = rendered_root / item
        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.is_file():
            shutil.copy2(src, dst)
    render_project_links_in_place(rendered_root, project)
    return rendered_root / "mkdocs.yml"
