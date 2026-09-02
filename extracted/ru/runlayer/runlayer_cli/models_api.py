"""Pydantic response models for the Runlayer REST client.

Split out of ``api.py`` to keep that module focused on the HTTP client surface
(mirrors the ``catalog_client.py`` split). ``RunlayerClient`` and its callers
import these via ``runlayer_cli.api`` (re-exported there), so nothing outside
this package needs to know they moved.

Like ``models.py`` this stays free of any ``mcp`` dependency so the ``aiwatch``
PyInstaller bundle (which excludes ``mcp``) can import ``api.py`` cleanly.
"""

from __future__ import annotations

import datetime
from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ServerListItem(BaseModel):
    """Minimal server info for listing."""

    id: str
    name: str
    description: str | None = None
    status: str
    icon_url: str | None = None
    is_official: bool = False
    deployment_mode: str | None = None


class PluginListItem(BaseModel):
    """Minimal plugin info for listing."""

    id: str
    name: str
    install_name: str | None = None
    path: str | None = None
    description: str | None = None
    is_public: bool = False
    namespace: str | None = None
    is_owned_by_me: bool = False
    server_count: int = 0
    tool_count: int = 0
    skill_count: int = 0


class AutoSyncItem(BaseModel):
    """Minimal auto-sync item."""

    entity_type: str
    entity_id: str


class PluginServerRef(BaseModel):
    server_id: str
    tool_names: list[str] = []


class ServerToolItem(BaseModel):
    name: str
    description: str | None = None


class ResolvedServerTarget(BaseModel):
    server_id: str = Field(validation_alias=AliasChoices("server_id", "id"))


class PluginSkillRef(BaseModel):
    id: str
    name: str
    install_name: str | None = None
    description: str | None = None
    is_public: bool = False
    file_count: int = 0


class PluginDetail(PluginListItem):
    use_dynamic_tools: bool = False
    identifier: str | None = None
    can_edit: bool = False
    skills: list[PluginSkillRef] = []
    servers: list[dict[str, Any]] = []
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class DeploymentPublic(BaseModel):
    """Public deployment model matching backend schema."""

    id: str
    name: str
    configuration: dict[str, Any]
    deployment_outputs: dict[str, Any] | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    template_yaml: str | None = None  # Always present for new deployments
    deletion_status: str | None = None  # "deleted", "deleting", or None (active)
    connected_servers: list[dict[str, Any]] = []  # List of connected MCP servers
    server_url: str | None = None
    task_role_arn: str | None = None
    connector_id: str | None = None  # Stable connector identity; None on old backends


class ValidateYAMLResponse(BaseModel):
    """Response from YAML validation endpoint."""

    valid: bool
    error: str | None = None
    parsed_config: dict[str, Any] | None = None


class RegistryCredentials(BaseModel):
    """Registry credentials response."""

    username: str
    password: str
    registry_url: str
    repository_url: str
    expires_at: datetime.datetime | None
    deployment_mode: Literal["ECS", "K8S", "LOCAL"] = "ECS"


# Backward-compatible alias for older imports.
ECRCredentials = RegistryCredentials


class DeploymentTriggerResponse(BaseModel):
    """Deployment trigger response."""

    deployment_id: str
    request_id: str
    status: str
    history_id: str


class SkillFileMetadata(BaseModel):
    id: str
    skill_id: str
    title: str
    description: str | None = None
    updated_at: datetime.datetime


class SkillDetail(BaseModel):
    id: str
    name: str
    install_name: str | None = None
    path: str | None = None
    description: str | None = None
    is_public: bool = False
    namespace: str | None = None
    identifier: str | None = None
    file_count: int = 0
    files: list[SkillFileMetadata] = []
    updated_at: datetime.datetime | None = None


class SkillFileDetail(BaseModel):
    id: str
    skill_id: str
    title: str
    description: str | None = None
    content: str


class AssignedSkillManifestItem(BaseModel):
    """One entry in the device skill-sync manifest (GET /ai-watch/skills/assigned)."""

    skill_id: str
    name: str
    install_name: str
    identifier: str
    updated_at: datetime.datetime


class AssignedSkillsManifest(BaseModel):
    """Skill-sync manifest for one device user.

    ``user_resolved=False`` means identity could not be established — the
    device must keep its current state. Reconcile (including to empty) only
    on an affirmative ``user_resolved=True``.
    """

    user_resolved: bool
    skills: list[AssignedSkillManifestItem]


class AssignedSkillFile(BaseModel):
    title: str
    content: str


class AssignedSkillContent(BaseModel):
    """Full file contents for one assigned skill."""

    skill_id: str
    name: str
    install_name: str
    identifier: str
    files: list[AssignedSkillFile]


class SkillScanFileScore(BaseModel):
    name: str
    score: float
    risk_level: str
    reasons: list[str] = []


class SkillScanResponse(BaseModel):
    scan_id: str = ""
    skill_score: float
    skill_risk_level: str
    classification: str
    files: list[SkillScanFileScore]


class IdentityForwardBundle(BaseModel):
    """Identity-forward bundle off the server-details read.

    Mirrors the backend's ``IdentityForwardResponse``. ``expires_at`` is
    unix seconds, set only for signed tokens (unsigned headers don't
    expire).
    """

    model_config = ConfigDict(extra="ignore")

    headers: dict[str, str] = {}
    expires_at: int | None = None
    applied: bool = False

    @property
    def needs_refresh(self) -> bool:
        """True when the bundle carries an expiring credential (signed
        token) — the only case the refresh loop has work to do."""
        return self.applied and self.expires_at is not None
