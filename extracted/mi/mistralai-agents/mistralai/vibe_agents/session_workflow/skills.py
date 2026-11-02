"""Session workflow skill request types."""

from typing import Literal
from urllib.parse import urlsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from mistralai.vibe_agents.session_workflow.commands import JsonObject, MessagePartResourceLink

REGISTRY_SKILL_RESOURCE_KIND: Literal["registry_skill"] = "registry_skill"
SKILL_RESOURCE_LINK_URI_SCHEME = "mistral-skill"
SKILL_RESOURCE_LINK_MIME_TYPE = "application/vnd.mistral.skill"
SKILL_RESOURCE_KIND_ANNOTATION_KEY = "vibe_agents.resource_kind"
SKILL_ID_ANNOTATION_KEY = "vibe_agents.skill_id"


class RequestedSkillInput(BaseModel):
    """Input model that specifies a registry skill requested for session startup."""

    # Strict on purpose: a request model the control plane validates. Clients read
    # sessions through forward-compatible models (``_internal.wire_models``) instead.
    model_config = ConfigDict(extra="forbid")

    type: Literal["registry_skill"]
    id: UUID
    version: int | None = None


class RegistrySkillResourceLinkAnnotations(BaseModel):
    model_config = ConfigDict(extra="allow", validate_by_alias=True, validate_by_name=True)

    resource_kind: Literal["registry_skill"] = Field(alias=SKILL_RESOURCE_KIND_ANNOTATION_KEY)
    skill_id: UUID = Field(alias=SKILL_ID_ANNOTATION_KEY)


def registry_skill_resource_uri(skill_id: UUID) -> str:
    return f"{SKILL_RESOURCE_LINK_URI_SCHEME}://{skill_id}"


def requested_skill_from_resource_link(part: MessagePartResourceLink) -> RequestedSkillInput | None:
    if (
        not part.uri.startswith(f"{SKILL_RESOURCE_LINK_URI_SCHEME}:")
        and part.mime_type != SKILL_RESOURCE_LINK_MIME_TYPE
        and not _annotations_claim_registry_skill(part.annotations)
    ):
        return None

    uri_skill_id = _skill_id_from_registry_skill_uri(part.uri)
    if part.mime_type is not None and part.mime_type != SKILL_RESOURCE_LINK_MIME_TYPE:
        raise ValueError(
            f"registry skill resource links must use mimeType {SKILL_RESOURCE_LINK_MIME_TYPE!r} when provided"
        )
    if part.annotations is None:
        raise ValueError("registry skill resource links require annotations")

    annotations = RegistrySkillResourceLinkAnnotations.model_validate(part.annotations)
    if annotations.skill_id != uri_skill_id:
        raise ValueError("registry skill resource link URI and annotation skill id must match")
    return RequestedSkillInput(type=REGISTRY_SKILL_RESOURCE_KIND, id=uri_skill_id)


def _annotations_claim_registry_skill(annotations: JsonObject | None) -> bool:
    if annotations is None:
        return False
    return (
        annotations.get(SKILL_RESOURCE_KIND_ANNOTATION_KEY) == REGISTRY_SKILL_RESOURCE_KIND
        or SKILL_ID_ANNOTATION_KEY in annotations
    )


def _skill_id_from_registry_skill_uri(uri: str) -> UUID:
    parsed = urlsplit(uri)
    if parsed.scheme != SKILL_RESOURCE_LINK_URI_SCHEME:
        raise ValueError(f"registry skill resource links must use {SKILL_RESOURCE_LINK_URI_SCHEME!r} URI scheme")
    if not parsed.netloc or parsed.path or parsed.query or parsed.fragment:
        raise ValueError("registry skill resource link URI must have the form mistral-skill://<uuid>")
    return UUID(parsed.netloc)


__all__ = [
    "REGISTRY_SKILL_RESOURCE_KIND",
    "SKILL_ID_ANNOTATION_KEY",
    "SKILL_RESOURCE_KIND_ANNOTATION_KEY",
    "SKILL_RESOURCE_LINK_MIME_TYPE",
    "SKILL_RESOURCE_LINK_URI_SCHEME",
    "RegistrySkillResourceLinkAnnotations",
    "RequestedSkillInput",
    "registry_skill_resource_uri",
    "requested_skill_from_resource_link",
]
