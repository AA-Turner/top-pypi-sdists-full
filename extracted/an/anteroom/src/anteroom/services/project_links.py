"""Project-link metadata profiles for public and internal distributions."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

PUBLIC_PROFILE = "public"
NEUTRAL_PROFILES = {"", "none", "neutral", "off", "disabled"}
PROFILE_ENV = "ANTEROOM_PROJECT_PROFILE"
LEGACY_PROFILE_ENV = "AI_CHAT_PROJECT_PROFILE"


@dataclass(frozen=True)
class ProjectIssueTrackingConfig:
    enabled: bool = False
    label_template: str = "#{number}"
    url_template: str = ""


@dataclass(frozen=True)
class ProjectConfig:
    profile: str = PUBLIC_PROFILE
    name: str = "Anteroom"
    repo_label: str = ""
    repo_url: str = ""
    docs_url: str = ""
    support_url: str = ""
    release_url_template: str = ""
    issue_tracking: ProjectIssueTrackingConfig = field(default_factory=ProjectIssueTrackingConfig)


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"false", "0", "no", "off", "disabled"}


def _profile_path(profile: str) -> Path | None:
    if profile in NEUTRAL_PROFILES:
        return None
    explicit = os.environ.get("ANTEROOM_PROJECT_PROFILE_PATH") or os.environ.get("AI_CHAT_PROJECT_PROFILE_PATH")
    if explicit:
        return Path(explicit).expanduser()
    package_path = Path(__file__).resolve().parent.parent / f"project-links.{profile}.yaml"
    if package_path.is_file():
        return package_path
    cwd_path = Path.cwd() / f"project-links.{profile}.yaml"
    if cwd_path.is_file():
        return cwd_path
    return None


def load_project_profile(profile: str | None) -> dict[str, Any]:
    """Load a named project-link profile without baking provider URLs into code."""
    selected = (profile or PUBLIC_PROFILE).strip().lower()
    path = _profile_path(selected)
    if path is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"project profile must be a mapping: {path}")
    return data


def project_mapping_from_env() -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    env_map = {
        "name": "ANTEROOM_PROJECT_NAME",
        "repo_label": "ANTEROOM_PROJECT_REPO_LABEL",
        "repo_url": "ANTEROOM_PROJECT_REPO_URL",
        "docs_url": "ANTEROOM_PROJECT_DOCS_URL",
        "support_url": "ANTEROOM_PROJECT_SUPPORT_URL",
        "release_url_template": "ANTEROOM_PROJECT_RELEASE_URL_TEMPLATE",
    }
    legacy_env_map = {
        "name": "AI_CHAT_PROJECT_NAME",
        "repo_label": "AI_CHAT_PROJECT_REPO_LABEL",
        "repo_url": "AI_CHAT_PROJECT_REPO_URL",
        "docs_url": "AI_CHAT_PROJECT_DOCS_URL",
        "support_url": "AI_CHAT_PROJECT_SUPPORT_URL",
        "release_url_template": "AI_CHAT_PROJECT_RELEASE_URL_TEMPLATE",
    }
    for key, env_name in env_map.items():
        value = os.environ.get(env_name, os.environ.get(legacy_env_map[key]))
        if value is not None:
            mapping[key] = value

    issue: dict[str, Any] = {}
    issue_enabled = os.environ.get(
        "ANTEROOM_PROJECT_ISSUE_TRACKING_ENABLED",
        os.environ.get("AI_CHAT_PROJECT_ISSUE_TRACKING_ENABLED"),
    )
    if issue_enabled is not None:
        issue["enabled"] = _as_bool(issue_enabled)
    issue_label = os.environ.get(
        "ANTEROOM_PROJECT_ISSUE_LABEL_TEMPLATE",
        os.environ.get("AI_CHAT_PROJECT_ISSUE_LABEL_TEMPLATE"),
    )
    if issue_label is not None:
        issue["label_template"] = issue_label
    issue_url = os.environ.get(
        "ANTEROOM_PROJECT_ISSUE_URL_TEMPLATE",
        os.environ.get("AI_CHAT_PROJECT_ISSUE_URL_TEMPLATE"),
    )
    if issue_url is not None:
        issue["url_template"] = issue_url
    if issue:
        mapping["issue_tracking"] = issue
    return mapping


def merge_project_mappings(*mappings: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for mapping in mappings:
        for key, value in mapping.items():
            if key == "issue_tracking" and isinstance(value, dict):
                current = merged.get("issue_tracking")
                if not isinstance(current, dict):
                    current = {}
                current.update(value)
                merged["issue_tracking"] = current
            else:
                merged[key] = value
    return merged


def build_project_config(raw: dict[str, Any] | None = None) -> ProjectConfig:
    raw = dict(raw or {})
    profile = str(
        raw.get("profile") or os.environ.get(PROFILE_ENV) or os.environ.get(LEGACY_PROFILE_ENV) or PUBLIC_PROFILE
    ).strip()
    profile_raw = load_project_profile(profile)
    merged = merge_project_mappings(profile_raw, raw, project_mapping_from_env())
    issue_raw = merged.get("issue_tracking", {})
    if not isinstance(issue_raw, dict):
        issue_raw = {}
    issue = ProjectIssueTrackingConfig(
        enabled=_as_bool(issue_raw.get("enabled"), default=False),
        label_template=str(issue_raw.get("label_template") or "#{number}"),
        url_template=str(issue_raw.get("url_template") or ""),
    )
    return ProjectConfig(
        profile=profile,
        name=str(merged.get("name") or "Anteroom"),
        repo_label=str(merged.get("repo_label") or ""),
        repo_url=str(merged.get("repo_url") or ""),
        docs_url=str(merged.get("docs_url") or ""),
        support_url=str(merged.get("support_url") or ""),
        release_url_template=str(merged.get("release_url_template") or ""),
        issue_tracking=issue,
    )


def project_display_label(project: ProjectConfig) -> str:
    return project.repo_label or project.name


def issue_label(project: ProjectConfig, number: str | int) -> str:
    return project.issue_tracking.label_template.format(number=number)


def issue_url(project: ProjectConfig, number: str | int) -> str:
    if not project.issue_tracking.enabled or not project.issue_tracking.url_template:
        return ""
    return project.issue_tracking.url_template.format(number=number)


def release_url(project: ProjectConfig, version: str) -> str:
    if not project.release_url_template:
        return ""
    return project.release_url_template.format(version=version)
