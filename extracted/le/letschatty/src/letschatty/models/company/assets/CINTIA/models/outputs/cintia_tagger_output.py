from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .cintia_decision_output import DecisionOutput, DecisionOutputType


class CintiaTaggerOutputData(BaseModel):
    tags: List[str] = Field(default=[], description="Tags to apply to the chat")
    products: List[str] = Field(default=[], description="Products to assign to the chat")
    flow: List[str] = Field(default=[], description="Flow steps")
    quality_score: Optional[float | str] = Field(
        default=None, description="Lead quality score"
    )
    target_funnel_id: Optional[str] = Field(default=None, description="Target funnel ID")
    data_collection: Optional[dict] = Field(
        default=None, description="Data collection status"
    )

    # Slug-shaped references — populated by tagger PGPs that use SlugCatalog
    # (e.g. pgp-implementator-tagger-with-intent). Resolved server-side to ids
    # in the callback before calling api-chatty's apply_tagger_output.
    tag_slugs: Optional[List[str]] = Field(
        default=None,
        description="Slugs the AI returned for tag selection — resolved server-side to ids.",
    )
    product_slugs: Optional[List[str]] = Field(
        default=None,
        description="Slugs the AI returned for product selection — resolved server-side to ids.",
    )
    funnel_slug: Optional[str] = Field(
        default=None,
        description="Slug for the funnel the chat belongs to — resolved server-side to id.",
    )
    stage_slug: Optional[str] = Field(
        default=None,
        description="Slug for the current stage of the funnel — resolved server-side to id. Only meaningful when funnel_slug is set.",
    )

    untag_tag_slugs: Optional[List[str]] = Field(
        default=None,
        description=(
            "Slugs the AI returned for tag REMOVAL. Resolved server-side to tag ids. "
            "Only populated by tagger-using-tag-references-and-untag; ignored by all "
            "other tagger PGPs."
        ),
    )

    # Canonical first-person rephrasing of the user's last message.
    # Written by the tagger, embedded by the callback, consumed by downstream
    # PGPs as a similarity query (cleaner than raw chat text).
    user_intention: Optional[str] = Field(
        default=None,
        description="Canonical first-person rephrasing of the user's last message — same language, preserve uncertainty/negation, no fabrication, 1 sentence.",
    )


class CintiaTaggerOutput(DecisionOutput):
    type: Literal[DecisionOutputType.TAGGER] = DecisionOutputType.TAGGER
    data: CintiaTaggerOutputData
